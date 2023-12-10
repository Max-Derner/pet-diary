lambda_packages/weekly_reminder.zip: app/lambda_weekly_reminder.py \
									 app/support/record_formatting.py \
									 app/support/notifications.py \
									 app/support/common/ \
									 app/support/data_access_layer/get_records.py \
									 app/support/common/aws_resources.py \
									 app/support/data_access_layer/records/pet_table_models.py
	echo "Building weekly-reminder Lambda zip package"
	echo "Removing old directory and zip file"
	if [ -d lambda_packages/weekly_reminder ]; then rm -rf lambda_packages/weekly_reminder; fi
	if [ -e lambda_packages/weekly_reminder.zip ]; then rm lambda_packages/weekly_reminder.zip; fi
	echo "Creating directory structure"
	mkdir -p lambda_packages/weekly_reminder/support/data_access_layer/records
	mkdir -p lambda_packages/weekly_reminder/support/common

	echo "Copying files"

	cp app/__init__.py                  lambda_packages/weekly_reminder/__init__.py
	cp app/lambda_weekly_reminder.py    lambda_packages/weekly_reminder/lambda_weekly_reminder.py

	cp app/support/__init__.py 	         lambda_packages/weekly_reminder/support/__init__.py
	cp app/support/record_formatting.py  lambda_packages/weekly_reminder/support/record_formatting.py
	cp app/support/notifications.py  lambda_packages/weekly_reminder/support/notifications.py

	cp -r app/support/common    lambda_packages/weekly_reminder/support/

	cp app/support/data_access_layer/__init__.py       lambda_packages/weekly_reminder/support/data_access_layer/__init__.py
	cp app/support/data_access_layer/get_records.py    lambda_packages/weekly_reminder/support/data_access_layer/get_records.py

	cp app/support/data_access_layer/records/__init__.py            lambda_packages/weekly_reminder/support/data_access_layer/records/__init__.py
	cp app/support/data_access_layer/records/pet_table_models.py    lambda_packages/weekly_reminder/support/data_access_layer/records/pet_table_models.py

	echo "Tidying up __pycache__ directories"
	find ./lambda_packages/ -type d -name __pycache__ | xargs rm -rf

	echo "Zipping up package"
	cd lambda_packages/weekly_reminder; zip -r weekly_reminder.zip .; cd ..; mv weekly_reminder/weekly_reminder.zip ./

lambda_packages/lambda_libraries_layer.zip: app/lambda_requirements.txt

	echo "Building lambda-libraries-layer Lambda Layer zip package"
	echo "Removing old directory and zip file"
	if [ -d lambda_packages/lambda_libraries_layer ]; then rm -rf lambda_packages/lambda_libraries_layer; fi
	if [ -e lambda_packages/lambda_libraries_layer.zip ]; then rm lambda_packages/lambda_libraries_layer.zip; fi

	echo "Creating directory structure"
	mkdir -p lambda_packages/lambda_libraries_layer/python

	echo "Installing pip packages"
	pip install --target ./lambda_packages/lambda_libraries_layer/python -r ./app/lambda_requirements.txt

	echo "Zipping up package"
	cd lambda_packages/lambda_libraries_layer; zip -r lambda_libraries_layer.zip .; cd ..; mv lambda_libraries_layer/lambda_libraries_layer.zip ./

clean:
	rm -rf lambda_packages