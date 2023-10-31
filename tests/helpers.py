import yaml
from typing import Dict
from os import environ
from datetime import datetime
from unittest.mock import patch
from app.support.data_access_layer.put_records import (
    put_details_record,
    put_appointment_record,
    put_illness_record,
    put_medication_record,
    put_observation_record
)
from support.data_access_layer.helpers import get_pet_table_resource
from app.support.records.appointment_record import AppointmentRecordFactory
from app.support.records.details_record import DetailsRecordFactory
from app.support.records.illness_record import IllnessRecordFactory
from app.support.records.medication_record import MedicationRecordFactory
from app.support.records.observation_record import ObservationRecordFactory


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
        'observed_time': datetime(year=1808, month=3, day=29),
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
        'type_of_medicine': 'antiemetic',
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
    put_details_record(**test_data['details'])
    put_appointment_record(**test_data['appointment'])
    put_observation_record(**test_data['observation'])
    put_illness_record(**test_data['illness'])
    put_medication_record(**test_data['medication'])


RECORDS_MODULE = 'app.support.records'


def fake_utc_timestamp_now():
    return datetime(year=1908, month=12, day=1)


def details_test_record_creator():
    return DetailsRecordFactory().produce_record(**test_data['details'])


@patch(
    f'{RECORDS_MODULE}.appointment_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
def appointment_test_record_creator():
    return AppointmentRecordFactory().produce_record(
        **test_data['appointment']
    )


@patch(
    f'{RECORDS_MODULE}.observation_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
def observation_test_record_creator():
    return ObservationRecordFactory().produce_record(
        **test_data['observation']
    )


@patch(
    f'{RECORDS_MODULE}.illness_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
def illness_test_record_creator():
    return IllnessRecordFactory().produce_record(
        **test_data['illness']
    )


@patch(
    f'{RECORDS_MODULE}.medication_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
def medication_test_record_creator():
    return MedicationRecordFactory().produce_record(
        **test_data['medication']
    )
