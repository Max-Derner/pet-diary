from boto3 import resource
# TODO move this file out of DAL


def get_pet_table_resource():
    """
    returns DynamoDB table resource pointed at the table 'pet_table'
    available methods can be found at:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html
    You can get the client through <resource>.meta.client
    which then allows use of the following:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
    """

    dynamo = resource('dynamodb')
    pet_table = dynamo.Table('pet_table')
    return pet_table
