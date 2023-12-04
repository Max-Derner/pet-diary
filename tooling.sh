#! /bin/bash

# This is the tooling used by pdt

_aws_exports() {
    AVAILABLE_PROFILES=$(grep -F '[profile' <~/.aws/config | sed -e 's/\[profile //g' -e 's/\]//g')
    PS3='Profile selection: '
    select AWS_PROFILE in $AVAILABLE_PROFILES; do
        if [ -n "$AWS_PROFILE" ]; then break; fi
    done
    CONFIG_SNIPPET=$(grep -A 20 -F "[profile ${AWS_PROFILE}]" <~/.aws/config)
    AWS_ACCOUNT_ID=$(echo "$CONFIG_SNIPPET" | grep -m 1 -F 'sso_account_id = ' | sed -e 's/sso_account_id = //g' -e 's/ *$//g')
    AWS_REGION=$(echo "$CONFIG_SNIPPET" | grep -m 1 -F 'sso_region = ' | sed -e 's/sso_region = //g' -e 's/ *$//g')
    echo "Exporting AWS_PROFILE as: $AWS_PROFILE"
    export AWS_PROFILE
    echo "Exporting AWS_ACCOUNT_ID as: $AWS_ACCOUNT_ID"
    export AWS_REGION
    echo "Exporting AWS_REGION as: $AWS_REGION"
    export AWS_REGION
}

_verify_venv_active() {
    if [ -z "${VIRTUAL_ENV}" ];
        then echo "Activate the venv than try again";
        return 1;
    fi
}

aws-login() {
    _aws_exports
    echo "Logging into AWS CLI"
    aws sso login
}

aws-add-test-profile() {
    _verify_venv_active
    echo "Checking aws config for test profile"
    TEST_PROFILE_HEADER='profile only-unit-tests!'
    if [ ! -e ~/.aws/config ]; then
        echo "There was no aws config file found at ~/.aws/config"
        echo "If you have specified a different location for the config, then I trust you to fix this yourself"
        return 1
    elif [ -z "$(grep -o -F "$TEST_PROFILE_HEADER" <~/.aws/config)" ]; then
        echo "Test profile not found, adding now"
        cat "${VIRTUAL_ENV}/../aws-test-profile" >> ~/.aws/config
    else
        echo "Testing profile found already"
    fi
}

_aws-force-config-and-test-profile() {
    echo "Creating parent directory '~/.aws'"
    mkdir ~/.aws
    echo "Creating config file with test profile."
    cat "${VIRTUAL_ENV}/../aws-test-profile" >> ~/.aws/config
}

_delimit() {
    echo "================================================================================"
    echo
}

full-security-check() {
    EXIT_STATUS=0
    _verify_venv_active
    echo -e "\tGenerating Security Report"
    echo -e "\t\t$(date)"
    _delimit
    python-security-check || EXIT_STATUS="$?"
    _delimit
    _sam-security-check || EXIT_STATUS="$?"
    _delimit
    third-party-security-check || EXIT_STATUS="$?"
    return "$EXIT_STATUS"
}

sam-check() {
    _verify_venv_active
    _sam-validate-template
    _sam-security-check
    return "$?"  # ensures function returns same code _sam-security-check exits with
}

_sam-validate-template() {
    AWS_REGION='eu-west-2'
    echo "Validating SAM template as if region is ${AWS_REGION}"
	sam validate \
    --region "$AWS_REGION" \
    --lint
}

_sam-security-check() {
    echo "Checking SAM template for security faults with Checkov"
    checkov \
    --compact \
    -f "${VIRTUAL_ENV}/../template.yaml"
    return "$?"  # ensures function returns same code checkov exits with
}

sam-deploy() {
    _verify_venv_active
    echo "Creating Lambda packages"
    make lambda_packages/weekly_reminder.zip
    echo "Building application"
    sam build
    echo "Deploying application into the '$AWS_REGION' region, using the '$AWS_PROFILE' profile"
    sam deploy \
    --stack-name pet-diary-stack \
    --template "{VIRTUAL_ENV}/../template.yaml" \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --capabilities CAPABILITY_NAMED_IAM \
    --resolve-s3

    if [ "$?" != 0 ]; then
        echo "Did you get an issue with reserved concurrency for the account going below 10?"
        echo "Follow the instructions: https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html"
    fi
}

sam-destroy() {
    echo "Tearing down application from the '$AWS_REGION' region, using the '$AWS_PROFILE' profile"
    sam delete \
    --stack-name pet-diary-stack \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --s3-bucket pet-dairy-app
}

python-lint() {
    _verify_venv_active
    echo "linting Python"
    flake8 \
    --config tox.ini \
    && echo "No issues detected"
    return "$?"  # ensures function returns same code flake8 exits with
}

python-security-check() {
    echo "Checking app/ for Python security issues with Bandit"
    bandit \
    -x __pycache__ \
    -r "${VIRTUAL_ENV}/../app/"
    return "$?"  # ensures function returns same code bandit exits with
}

python-test() {
    _verify_venv_active
    pytest "${VIRTUAL_ENV}/../tests" -vv
}

configure-venv() {
    # Figure out if we're in the correct directory
    echo "Checking current working directory."
    CWD=$(pwd)
    MATCH=$(echo "$CWD" | grep -E '.*pet-diary')
    if [ -z "$MATCH" ]; then
        echo "Wrong directory, please change to the root directory of the project."
        return 1
    fi
    echo "Current working directory is: $CWD"
    # Check for venv
    echo "Checking for virtual environment."
    if [ -d 'pet-diary-venv/' ]; then
        echo "Virtual environment present."
    else
        echo "Creating virtual environment."
        python3 -m venv pet-diary-venv
    fi
    echo "Activating virtual environment."
    source ./pet-diary-venv/bin/activate
    # Install requirements
    echo "Updating pip, and installing dependancies."
    python3 -m pip install --upgrade pip
    pip install -r ./requirements.txt
    # Check venv configuration
    echo "Checking venv configuration"
    if grep -q -F "$(tail -n 1 .env)" <./pet-diary-venv/bin/activate; then
        echo "Looks like you're all set up"
    else
        echo "Amending pet-diary-venv/bin/activate"
        sudo tee -a ./pet-diary-venv/bin/activate <.env 1>/dev/null
    fi
    # restart venv
    ls ./
    ls ./pet-diary-venv
    ls ./pet-diary-venv/bin
    ls ./pet-diary-venv/bin/activate
    echo "Restarting virtual environment"
    source ./pet-diary-venv/bin/activate 1>/dev/null
    echo "Complete, enjoy your new venv"
}


third-party-security-check () {
    _verify_venv_active
    echo "Scanning project for 3rd party dependency issues using Grype"
    grype dir:"${VIRTUAL_ENV}/.." -q
    return "$?"  # ensures function returns same code grype exits with
}

install-anchore-security-tools () {
    _verify_venv_active
    echo "Checking for Grype"
    if [ -n "$(which grype)" ]; then
        echo "Grype install detected in $(which grype)"
        echo "Looks like you're already set up"
    else
        echo "Installing Grype"
        cat "${VIRTUAL_ENV}/../grype-install.sh" | sudo sh -s -- -b /usr/local/bin
    fi
}

coverage-python () {
    _verify_venv_active
    # For more information on test coverage see https://pytest-cov.readthedocs.io/en/latest/config.html
    OPTION="$1"
    case $OPTION in
        "term")
            pytest \
            --cov-report term-missing \
            --cov=app tests/
            ;;
        "html")
            pytest \
            --cov-report html:coverage/ \
            --cov=app tests/
            xdg-open coverage/index.html &
            ;;
        *)
            echo "Invalid option."
            echo "Options are html or term."
            return 1
            ;;
    esac
}