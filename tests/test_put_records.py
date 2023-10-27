from unittest.mock import patch, Mock
from datetime import datetime
from decimal import Decimal
from app.supporting_cast.data_access_layer.put_records import (
    put_appointment_record,
    put_details_record,
    put_illness_record,
    put_medication_record,
    put_observation_record
)


PUT_RECORDS_PACKAGE = 'app.supporting_cast.data_access_layer.put_records'
RECORDS_PACKAGE = 'app.supporting_cast.records'


@patch(f'{RECORDS_PACKAGE}.appointment_record.utc_timestamp_now')
@patch(f'{PUT_RECORDS_PACKAGE}.get_pet_table_resource')
def tests_put_appointment_record(get_pet_table_resource: Mock,
                                 utc_timestamp_now: Mock):
    pet_table = Mock()
    put_item = Mock()
    pet_table.put_item = put_item
    get_pet_table_resource.return_value = pet_table
    utc_timestamp_now.return_value = 123456.789
    expected_item = {
        'name': 'me',
        'sort_key': 'appointment#123456.789',
        'date_time': Decimal(32494863600),
        'description': 'Got to get vaccinated against millennium bug'
        }

    put_appointment_record(
        pet_name='me',
        appointment_time=datetime(year=2999,
                                  month=9,
                                  day=21),
        description='Got to get vaccinated against millennium bug'
    )

    put_item.assert_called_once_with(Item=expected_item)


@patch(f'{PUT_RECORDS_PACKAGE}.get_pet_table_resource')
def tests_put_details_record(get_pet_table_resource: Mock):
    pet_table = Mock()
    put_item = Mock()
    pet_table.put_item = put_item
    get_pet_table_resource.return_value = pet_table
    expected_item = {
        'name': 'me',
        'sort_key': 'details',
        'dob': Decimal(-4955212725),
        'colour': 'bit peaky',
        'gender': 'yes',
        'breed': 'not yet',
        'microchip_number': 741852963
        }

    put_details_record(pet_name='me',
                       date_of_birth=datetime(year=1812,
                                              month=12,
                                              day=23),
                       colour='bit peaky',
                       gender='yes',
                       breed='not yet',
                       microchip_number=741852963)

    put_item.assert_called_once_with(Item=expected_item)


@patch(f'{RECORDS_PACKAGE}.illness_record.utc_timestamp_now')
@patch(f'{PUT_RECORDS_PACKAGE}.get_pet_table_resource')
def tests_put_illness_record(get_pet_table_resource: Mock,
                             utc_timestamp_now: Mock):
    pet_table = Mock()
    put_item = Mock()
    pet_table.put_item = put_item
    get_pet_table_resource.return_value = pet_table
    utc_timestamp_now.return_value = 123456.789
    expected_item = {
        'name': 'me',
        'sort_key': 'illness#stinky butt#123456.789',
        'ailment': 'stinky butt',
        'date_time': Decimal(-24077951925),
        'description': 'butt is so stinky, neighbours have complained'}

    put_illness_record(
        pet_name='me',
        ailment='stinky butt',
        observed_time=datetime(year=1207,
                               month=1,
                               day=1),
        description='butt is so stinky, neighbours have complained'
    )

    put_item.assert_called_once_with(Item=expected_item)


@patch(f'{RECORDS_PACKAGE}.medication_record.utc_timestamp_now')
@patch(f'{PUT_RECORDS_PACKAGE}.get_pet_table_resource')
def tests_put_medication_record(get_pet_table_resource: Mock,
                                utc_timestamp_now: Mock):
    pet_table = Mock()
    put_item = Mock()
    pet_table.put_item = put_item
    get_pet_table_resource.return_value = pet_table
    utc_timestamp_now.return_value = 123456.789
    expected_item = {
        'name': 'me',
        'sort_key': 'medication#good kind#123456.789',
        'date_time': Decimal('1698102000'),
        'medicine_name': 'feel-better-aloxin',
        'medicine_type': 'good kind',
        'repeat': False
        }

    put_medication_record(pet_name='me',
                          time_of_administration=datetime(year=2023,
                                                          month=10,
                                                          day=24),
                          name_of_medicine='feel-better-aloxin',
                          type_of_medication='good kind')

    put_item.assert_called_once_with(Item=expected_item)


@patch(f'{RECORDS_PACKAGE}.medication_record.utc_timestamp_now')
@patch(f'{PUT_RECORDS_PACKAGE}.get_pet_table_resource')
def tests_put_medication_record_alt(get_pet_table_resource: Mock,
                                    utc_timestamp_now: Mock):
    pet_table = Mock()
    put_item = Mock()
    pet_table.put_item = put_item
    get_pet_table_resource.return_value = pet_table
    utc_timestamp_now.return_value = 123456.789
    expected_item = {
        'name': 'me',
        'sort_key': 'medication#good kind#123456.789',
        'date_time': Decimal(1698102000),
        'medicine_name': 'feel-better-aloxin',
        'medicine_type': 'good kind',
        'repeat': True,
        'next_due': Decimal(1706054400)}

    put_medication_record(pet_name='me',
                          time_of_administration=datetime(year=2023,
                                                          month=10,
                                                          day=24),
                          name_of_medicine='feel-better-aloxin',
                          type_of_medication='good kind',
                          next_due=datetime(year=2024,
                                            month=1,
                                            day=24))

    put_item.assert_called_once_with(Item=expected_item)


@patch(f'{RECORDS_PACKAGE}.observation_record.utc_timestamp_now')
@patch(f'{PUT_RECORDS_PACKAGE}.get_pet_table_resource')
def tests_put_observation_record(get_pet_table_resource: Mock,
                                 utc_timestamp_now: Mock):
    pet_table = Mock()
    put_item = Mock()
    pet_table.put_item = put_item
    get_pet_table_resource.return_value = pet_table
    utc_timestamp_now.return_value = 123456.789
    expected_item = {
        'name': 'me',
        'sort_key': 'observation#123456.789',
        'date_time': Decimal(1698015600),
        'description': 'Broke venv, get very upset wth self'
        }

    put_observation_record(pet_name='me',
                           observed=datetime(year=2023,
                                             month=10,
                                             day=23),
                           description='Broke venv, get very upset wth self')

    put_item.assert_called_once_with(Item=expected_item)
