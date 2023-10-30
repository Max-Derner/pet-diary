import moto
from support.data_access_layer.put_records import put_observation_record
from tests.helpers import setup_test_dynamo_with_data
from datetime import datetime


@moto.mock_dynamodb
class TestsDynamoDBCalls:

    def tests_table_is_there(self):
        setup_test_dynamo_with_data()
        put_observation_record(
            pet_name='me',
            observed=datetime.now(),
            description='Broke venv, get very upset wth self'
        )
