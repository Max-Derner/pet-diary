from typing import List, Dict
from boto3.dynamodb.conditions import Key
from app.support.data_access_layer.helpers import get_pet_table_resource
from app.support.records.pet_table_models import RecordType


def get_all_records(pet_name: str) -> List[Dict]:
    pet_table = get_pet_table_resource()
    response = pet_table.query(
        KeyConditionExpression=Key('name').eq(pet_name)
    )
    return response['Items']


def get_all_of_record_type(pet_name: str, record_type: RecordType):
    pet_table = get_pet_table_resource()
    response = pet_table.query(
        KeyConditionExpression=Key('name').eq(pet_name) & Key('sort_key').begins_with(record_type.value)  # noqa: E501
    )
    return response['Items']
