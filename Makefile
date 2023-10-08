.PHONY: cloud_report
cloud_report:
	sam validate --region eu-west-2 --lint
	checkov -f ./template.json