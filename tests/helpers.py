import yaml
from typing import Dict
from os import environ
from datetime import datetime
from app.support.data_access_layer.put_records import (
    put_details_record,
    put_appointment_record,
    put_illness_record,
    put_medication_record,
    put_observation_record
)
from support.data_access_layer.helpers import get_pet_table_resource


def _get_sam_template() -> Dict:
    loader = yaml.Loader
    # The following line is some ropey business, just don't access anything
    # that uses the '!GetAtt' and you'll be fine.
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


test_data = {
    'details':
    {
        'pet_name': 'me',
        'date_of_birth': datetime(year=1807, month=12, day=23),
        'colour': 'some',
        'gender': 'yes',
        'breed': 'people',
        'microchip_number': 2
    },
    'appointment':
    {
        'pet_name': 'me',
        'appointment_time': datetime(year=1808, month=3, day=23),
        'description': 'Got to get first vaccination'
    },
    'observation':
    {
        'pet_name': 'me',
        'observed': datetime(year=1808, month=3, day=29),
        'description': 'seems vary lethargic since vaccine'
    },
    'illness':
    {
        'pet_name': 'me',
        'ailment': 'vomiting',
        'observed_time': datetime(year=1808, month=4, day=3),
        'description': 'seems to not be reacting well to the vaccine, has vomited twice today'  # noqa: E501
    },
    'medication':
    {
        'pet_name': 'me',
        'time_of_administration': datetime(year=1808, month=4, day=4),
        'name_of_medicine': 'feel-better-a-loxin',
        'type_of_medication': 'antiemetic',
        'next_due': datetime(year=1808, month=4, day=5)
    }
}


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
    environ['AWS_PROFILE'] = 'only-unit-tests!'
    environ['AWS_ACCOUNT_ID'] = 'absolutely-not-sunshine!'
    # set up table using pet-table template file
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
    # fill table with test data
    details = test_data['details']
    put_details_record(
        pet_name=details['pet_name'],
        date_of_birth=details['date_of_birth'],
        colour=details['colour'],
        gender=details['gender'],
        breed=details['breed'],
        microchip_number=details['microchip_number']
    )
    appointment = test_data['appointment']
    put_appointment_record(
        pet_name=appointment['pet_name'],
        appointment_time=appointment['appointment_time'],
        description=appointment['description']
    )
    observation = test_data['observation']
    put_observation_record(
        pet_name=observation['pet_name'],
        observed=observation['observed'],
        description=observation['description']
    )
    illness = test_data['illness']
    put_illness_record(
        pet_name=illness['pet_name'],
        ailment=illness['ailment'],
        observed_time=illness['observed_time'],
        description=illness['description']
    )
    medication = test_data['medication']
    put_medication_record(
        pet_name=medication['pet_name'],
        time_of_administration=medication['time_of_administration'],
        name_of_medicine=medication['name_of_medicine'],
        type_of_medication=medication['type_of_medication'],
        next_due=medication['next_due']
    )
