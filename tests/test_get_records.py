import moto
from unittest.mock import patch
from datetime import datetime
from tests.helpers import (
    setup_test_dynamo_with_data,
    test_data
)
from app.support.records.appointment_record import AppointmentRecordFactory
from app.support.records.details_record import DetailsRecordFactory
from app.support.records.illness_record import IllnessRecordFactory
from app.support.records.medication_record import MedicationRecordFactory
from app.support.records.observation_record import ObservationRecordFactory
from app.support.data_access_layer.get_records import (
    get_all_records_for_pet
)


RECORDS_MODULE = 'app.support.records'


def fake_utc_timestamp_now():
    return datetime(year=1908, month=12, day=1)


def details_test_record_creator():
    return DetailsRecordFactory().produce_record(
        pet_name=test_data['details']['pet_name'],
        date_of_birth=test_data['details']['date_of_birth'],
        colour=test_data['details']['colour'],
        gender=test_data['details']['gender'],
        breed=test_data['details']['breed'],
        microchip_number=test_data['details']['microchip_number']
    )


@patch(
    f'{RECORDS_MODULE}.appointment_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
def appointment_test_record_creator():
    return AppointmentRecordFactory().produce_record(
        pet_name=test_data['appointment']['pet_name'],
        appointment_time=test_data['appointment']['appointment_time'],
        description=test_data['appointment']['description']
    )


@patch(
    f'{RECORDS_MODULE}.observation_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
def observation_test_record_creator():
    return ObservationRecordFactory().produce_record(
        pet_name=test_data['observation']['pet_name'],
        observed_time=test_data['observation']['observed_time'],
        description=test_data['observation']['description']
    )


@patch(
    f'{RECORDS_MODULE}.illness_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
def illness_test_record_creator():
    return IllnessRecordFactory().produce_record(
        pet_name=test_data['illness']['pet_name'],
        ailment=test_data['illness']['ailment'],
        observed_time=test_data['illness']['observed_time'],
        description=test_data['illness']['description']
    )


@patch(
    f'{RECORDS_MODULE}.medication_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
def medication_test_record_creator():
    return MedicationRecordFactory().produce_record(
        pet_name=test_data['medication']['pet_name'],
        time_of_administration=test_data['medication']['time_of_administration'],  # noqa: E501
        name_of_medicine=test_data['medication']['name_of_medicine'],
        type_of_medicine=test_data['medication']['type_of_medicine'],
        next_due=test_data['medication']['next_due']
    )


@moto.mock_dynamodb
@patch(
    f'{RECORDS_MODULE}.appointment_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
@patch(
    f'{RECORDS_MODULE}.illness_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
@patch(
    f'{RECORDS_MODULE}.medication_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
@patch(
    f'{RECORDS_MODULE}.observation_record.utc_timestamp_now',
    fake_utc_timestamp_now
)
class TestsDynamoDBCalls:

    details_test_record = details_test_record_creator()
    appointment_test_record = appointment_test_record_creator()
    observation_test_record = observation_test_record_creator()
    illness_test_record = illness_test_record_creator()
    medication_test_record = medication_test_record_creator()

    def tests_get_all_records_for_pet(self):
        setup_test_dynamo_with_data()
        absences = []
        missing_records = []

        result = get_all_records_for_pet(name='me')

        if self.details_test_record not in result:
            absences.append("details")
            missing_records.append(self.details_test_record)
        if self.appointment_test_record not in result:
            absences.append("appointment")
            missing_records.append(self.appointment_test_record)
        if self.illness_test_record not in result:
            absences.append("illness")
            missing_records.append(self.illness_test_record)
        if self.medication_test_record not in result:
            absences.append("medication")
            missing_records.append(self.medication_test_record)
        if self.observation_test_record not in result:
            absences.append("observation")
            missing_records.append(self.observation_test_record)
        assert absences == [], \
            f"""
            Records are absent: {', '.join(absences)}
            Missing: {missing_records}
            Received: {result}
            """
