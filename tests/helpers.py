import yaml
from typing import Dict
from os import environ

from app.support.data_access_layer.put_records import (
    put_details_record,
    put_appointment_record,
    put_illness_record,
    put_medication_record,
    put_observation_record
)
from support.common.aws_resources import get_pet_table_resource
from tests.mock_pet_table_data import test_data
from support.common.logger import get_full_logger

logger = get_full_logger()


def mock_utc_timestamp_now():
    return 123456.789


def _get_sam_template() -> Dict:
    loader = yaml.Loader
    # The following line is some ropey business, just don't access any values
    # that are populated by the '!GetAtt' function and you'll be fine.
    loader.add_constructor(tag='!GetAtt', constructor=lambda x, y: str(y))
    # This whole thing is only supposed to be used to make Dynamo mocking
    # easier anyway, using it for anything else is stupid.
    with open('template.yaml', mode='r') as file_io:
        full_template = yaml.load(stream=file_io, Loader=loader)
    return full_template


def get_pet_table_properties() -> Dict:
    full_template = _get_sam_template()
    # No get functions here, we want this to blow up if it can't find the table
    pet_table_properties = full_template['Resources']['PetTable']['Properties']
    return pet_table_properties


def setup_test_dynamo_with_data():
    """
    This function doesn't allow creation of tables.
    It should only be used for testing and called from within a test that has
    moto mocking enabled.
    If you follow the README for logging into AWS SSO,
    then this function should invalidate that.
    The moto library should then intercept your call to boto
    """

    # invalidate credentials
    logger.debug("Invalidating credentials")
    environ['AWS_PROFILE'] = 'only-unit-tests!'
    environ['AWS_ACCOUNT_ID'] = 'absolutely-not-sunshine!'
    # set up table using pet-table template file
    logger.debug("Creating table")
    test_table = get_pet_table_resource()
    ptp = get_pet_table_properties()
    test_table.meta.client.create_table(
        TableName=ptp['TableName'],
        AttributeDefinitions=ptp['AttributeDefinitions'],
        KeySchema=ptp['KeySchema'],
        GlobalSecondaryIndexes=ptp['GlobalSecondaryIndexes'],
        BillingMode=ptp['BillingMode'],
        ProvisionedThroughput=ptp['ProvisionedThroughput']
    )
    test_table.wait_until_exists()
    logger.debug("Populating test table")
    # fill table with test data
    for record in test_data['details']:
        put_details_record(**record)
    for record in test_data['appointment']:
        put_appointment_record(**record)
    for record in test_data['observation']:
        put_observation_record(**record)
    for record in test_data['illness']:
        put_illness_record(**record)
    for record in test_data['medication']:
        put_medication_record(**record)

    logger.debug("Checking table")
    result = test_table.scan()
    logger.debug(f"RESPONSE: {result}")
