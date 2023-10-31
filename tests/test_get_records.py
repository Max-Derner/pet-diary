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
    get_illness_test_records,
    get_medication_test_records,
    get_appointment_test_records,
    get_observation_test_records,
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

    details_test_records = details_test_record_creator()
    appointment_test_records = get_appointment_test_records()
    observation_test_records = get_observation_test_records()
    illness_test_records = get_illness_test_records()
    medication_test_records = get_medication_test_records()

    def tests_get_all_records_for_pet(self):
        setup_test_dynamo_with_data()
        missing_records = []
        all_expected_records = []
        all_expected_records.extend(self.details_test_records)
        all_expected_records.extend(self.appointment_test_records)
        all_expected_records.extend(self.observation_test_records)
        all_expected_records.extend(self.illness_test_records)
        all_expected_records.extend(self.medication_test_records)

        result = get_all_records(pet_name='me')

        for record in all_expected_records:
            if record not in result:
                missing_records.append(record)
        assert missing_records == [], \
            f"""
            Some expected records were not received:
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

        assert result == self.details_test_records
