from boto3 import client
from botocore.exceptions import ClientError
from boto3_type_annotations.dynamodb import client as ddb_client


dynamo_client: ddb_client = client("dynamodb")

def get_dynamodb_client() -> ddb_client:
    dynamo_client = client('dynamodb', region='eu-west-2')