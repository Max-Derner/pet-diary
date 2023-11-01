from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Dict, Optional
from boto3.dynamodb.conditions import Key, Attr
from app.support.data_access_layer.helpers import get_pet_table_resource
from app.support.records.pet_table_models import RecordType


def get_all_records(pet_name: str) -> List[Dict]:
    pet_table = get_pet_table_resource()
    fetching = True
    excl_key_kwarg = {}
    items = []
    while fetching:
        response = pet_table.query(
            ConsistentRead=True,
            KeyConditionExpression=Key('name').eq(pet_name),
            **excl_key_kwarg
        )
        if (last_key := response.get('LastEvaluatedKey')) is None:
            fetching = False
        else:
            excl_key_kwarg = {'ExclusiveStartKey': last_key}
        items.extend(response['Items'])
    return items


def get_all_of_record_type(
        pet_name: str,
        record_type: RecordType
        ) -> List[Dict]:
    pet_table = get_pet_table_resource()
    response = pet_table.query(
        KeyConditionExpression=Key('name').eq(pet_name) & Key('sort_key').begins_with(record_type.value)  # noqa: E501
    )
    return response['Items']


def get_all_of_record_type_after_point_in_time(
        pet_name: str,
        point_in_time: datetime,
        record_type: RecordType
        ) -> List[Dict]:
    pet_table = get_pet_table_resource()
    response = pet_table.query(
        KeyConditionExpression=Key('name').eq(pet_name) & Key('sort_key').begins_with(record_type.value),  # noqa: E501
        FilterExpression=Attr('date_time').gt(Decimal(point_in_time.astimezone(tz=timezone.utc).timestamp()))  # noqa: E501
    )
    return response['Items']


def get_all_records_of_medicine_type(medicine_type: str):
    pet_table = get_pet_table_resource()
    response = pet_table.query(
        IndexName='medicine_type',
        KeyConditionExpression=Key('medicine_type').eq(medicine_type)
    )
    return response['Items']


def get_all_records_of_medicine_type_in_timeframe(
        medicine_type: str,
        lower_date_limit: Optional[datetime],
        upper_date_limit: Optional[datetime]
        ):
    lower_limit_decimal_timestamp: Optional[Decimal] = Decimal(lower_date_limit.astimezone(tz=timezone.utc).timestamp())if lower_date_limit is not None else None  # noqa: E501
    upper_limit_decimal_timestamp: Optional[Decimal] = Decimal(upper_date_limit.astimezone(tz=timezone.utc).timestamp())if upper_date_limit is not None else None  # noqa: E501
    filter_expression = {}
    if lower_limit_decimal_timestamp is not None and upper_limit_decimal_timestamp is not None:  # noqa: E501
        filter_expression = {
            'FilterExpression': Attr('date_time').between(
                lower_limit_decimal_timestamp, upper_limit_decimal_timestamp
            )
        }
    elif lower_limit_decimal_timestamp is None and upper_limit_decimal_timestamp is not None:  # noqa: E501
        filter_expression = {
            'FilterExpression': Attr('date_time').lte(
                upper_limit_decimal_timestamp
            )
        }
    elif lower_limit_decimal_timestamp is not None and upper_limit_decimal_timestamp is None:  # noqa: E501
        filter_expression = {
            'FilterExpression': Attr('date_time').gte(
                lower_limit_decimal_timestamp
            )
        }
    else:
        return get_all_records_of_medicine_type(medicine_type=medicine_type)

    pet_table = get_pet_table_resource()
    response = pet_table.query(
        IndexName='medicine_type',
        KeyConditionExpression=Key('medicine_type').eq(medicine_type),
        **filter_expression
    )
    return response['Items']
