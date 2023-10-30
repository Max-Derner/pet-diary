from typing import List, Dict
from boto3.dynamodb.conditions import Key
from app.support.data_access_layer.helpers import get_pet_table_resource


def get_all_records_for_pet(name: str) -> List[Dict]:
    pet_table = get_pet_table_resource()
    response = pet_table.query(
        KeyConditionExpression=Key('name').eq(name)
    )
    return response['Items']
