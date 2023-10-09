.PHONY: cloud_report app destroy

cloud_report:
	sam validate --region eu-west-2 --lint
	checkov --compact -f ./template.yaml

app:
	sam deploy --template template.yaml --stack-name pet-diary-stack --region eu-west-2 --profile Admin

destroy:
	sam delete --stack-name pet-diary-stack --region eu-west-2 --profile Admin