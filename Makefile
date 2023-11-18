weekly_reminder.zip: app/lambdas/weekly_reminder/weekly_reminder.py app/support/logger.py
	echo "Building weekly-reminder Lmabda zip package"
	echo "Removing old directory and zip file"
	if [ -d lambda_packages/weekly_reminder ]; then rm -rf lambda_packages/weekly_reminder; fi
	if [ -e lambda_packages/weekly_reminder.zip ]; then rm lambda_packages/weekly_reminder.zip; fi
	echo "Creating directory structure"
	mkdir -p lambda_packages/weekly_reminder/app/lambdas/weekly_reminder
	mkdir -p lambda_packages/weekly_reminder/app/support
	echo "Copying files"
	cp app/__init__.py lambda_packages/weekly_reminder/app/__init__.py
	cp app/support/__init__.py lambda_packages/weekly_reminder/app/support/__init__.py
	cp app/lambdas/__init__.py lambda_packages/weekly_reminder/app/lambdas/__init__.py
	cp app/lambdas/weekly_reminder/__init__.py lambda_packages/weekly_reminder/app/lambdas/weekly_reminder/__init__.py
	cp app/lambdas/weekly_reminder/weekly_reminder.py lambda_packages/weekly_reminder/app/lambdas/weekly_reminder/weekly_reminder.py
	cp app/support/logger.py lambda_packages/weekly_reminder/app/support/logger.py
	echo "Zipping up package"
	cd lambda_packages/weekly_reminder; zip -r weekly_reminder.zip .; cd ..; mv weekly_reminder/weekly_reminder.zip ./