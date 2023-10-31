import moto
from unittest.mock import patch
from tests.helpers import (
    setup_test_dynamo_with_data
)
from app.support.data_access_layer.get_records import (
    get_all_records,
    get_all_of_record_type
)
from app.support.records.pet_table_models import RecordType
from tests.helpers import (
    RECORDS_MODULE,
    details_test_record_creator,
    illness_test_record_creator,
    medication_test_record_creator,
    appointment_test_record_creator,
    observation_test_record_creator,
    fake_utc_timestamp_now
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

        result = get_all_records(pet_name='me')

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

    def tests_get_all_records_wrong_name(self):
        setup_test_dynamo_with_data()

        result = get_all_records(pet_name='you')

        assert result == []

    def test_get_all_of_record_type_for_pet_details(self):
        setup_test_dynamo_with_data()

        result = get_all_of_record_type(
            pet_name='me',
            record_type=RecordType.DETAILS
        )

        assert result == [self.details_test_record]
