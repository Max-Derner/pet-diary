#! /bin/bash

# This is the tooling used by pdt

get-aws-profile() {
    grep -E 'PROFILE:' <.pdt-config | sed -e 's/PROFILE://g'
}
get-aws-region() {
    grep -E 'REGION:' <.pdt-config| sed -e 's/REGION://g'
}

_aws_exports() {
    AVAILABLE_PROFILES=$(grep -F '[profile' <~/.aws/config | sed -e 's/\[profile //g' -e 's/\]//g')
    PS3='Profile selection: '
    select AWS_PROFILE in $AVAILABLE_PROFILES; do
        if [ -n "$AWS_PROFILE" ]; then break; fi
    done
    CONFIG_SNIPPET=$(grep -A 20 -F "[profile ${AWS_PROFILE}]" <~/.aws/config)
    AWS_ACCOUNT_ID=$(echo "$CONFIG_SNIPPET" | grep -F 'sso_account_id = ' | sed -e 's/sso_account_id = //g' -e 's/ *$//g')
    echo "Exporting AWS_PROFILE as: $AWS_PROFILE"
    echo "Exporting AWS_ACCOUNT_ID as: $AWS_ACCOUNT_ID"
    export AWS_PROFILE
    export AWS_ACCOUNT_ID
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

_delimit() {
    echo "================================================================================"
    echo
}

full-security-check() {
    EXIT_STATUS=0
    _verify_venv_active
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
    AWS_REGION=$(get-aws-region)
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
    AWS_REGION=$(get-aws-region)
    AWS_PROFILE=$(get-aws-profile)
    echo "Deploying application into the $AWS_REGION region, using the $AWS_PROFILE profile"
    sam deploy \
    --template "{VIRTUAL_ENV}/../template.yaml" \
    --stack-name pet-diary-stack \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE"
}

sam-destroy() {
    AWS_REGION=$(get-aws-region)
    AWS_PROFILE=$(get-aws-profile)
    echo "Tearing down application from the $AWS_REGION region, using the $AWS_PROFILE profile"
    sam delete \
    --stack-name pet-diary-stack \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE"
}

python-lint() {
    _verify_venv_active
    echo "linting Python"
    flake8 \
    --exclude 'pet-diary-venv/**' \
    "${VIRTUAL_ENV}/.."
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

configure-vars() {
    # Check AWS CLI is in place and configured
    if [ -z "$(which aws)" ]; then 
        echo "Looks like you haven't installed AWS CLI yet."
        echo "Do that, and configure it first, then come back."
        return 1
    fi
    if [ ! -e ~/.aws/config ]; then
        echo "Looks like you haven't configured your AWS CLI."
        echo "Configure that and then come back."
        return 1
    fi
    # Start config
    AWS_CONFIG=$(cat ~/.aws/config)
    # Establish chosen AWS profile
    AVAILABLE_AWS_PROFILES=$(echo "$AWS_CONFIG" | grep -E '\[profile .*\]' | sed -e 's/.*\[profile //g' -e 's/\].*//g')
    echo "Please choose an AWS profile"
    PS3='Choose profile: '
    select AWS_PROFILE in $AVAILABLE_AWS_PROFILES; do
        echo "You chose $AWS_PROFILE"
        break
    done
    # Establish chosen AWS region
    AVAILABLE_AWS_REGIONS=$(echo "$AWS_CONFIG" | grep -E 'region = ' | sed -e 's/region = //g')
    echo "Please choose an AWS region"
    PS3='Choose region: '
    select AWS_REGION in $AVAILABLE_AWS_REGIONS; do
        echo "You chose $AWS_REGION"
        break
    done
    # Drop profile and region into config file
    CONFIG=$(echo "PROFILE:${AWS_PROFILE}"; echo "REGION:${AWS_REGION}")
    echo "$CONFIG" > .pdt-config
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
    if [ -n "$(grep -o -F "$(cat .env)" <./pet-diary-venv/bin/activate)" ]; then
        echo "Looks like you're all set up"
    else
        echo "Amending pet-diary-venv/bin/activate"
        sudo tee -a ./pet-diary-venv/bin/activate <.env 1>/dev/null
    fi
    # restart venv
    echo "Restarting virtual environment"
    deactivate
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
    echo "Installing Grype"
    cat "${VIRTUAL_ENV}/../installation-files/grype-install.sh" | sudo sh -s -- -b /usr/local/bin
}