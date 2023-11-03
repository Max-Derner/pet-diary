from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, List, Optional
import moto
from pytest import mark

from tests.helpers import (
    setup_test_dynamo_with_data
)
from app.support.records.pet_table_models import RecordType
from app.support.data_access_layer.helpers import get_pet_table_resource
from app.support.data_access_layer.get_records import (
    get_all_of_pets_records,
    get_all_of_pets_record_type,
    get_all_of_pets_record_type_after_point_in_time,
    get_all_records_of_medicine_type,
    get_all_records_of_medicine_type_in_next_due_timeframe,
)


@moto.mock_dynamodb
class TestsDynamoDBCalls:

    all_test_records: List[Dict]
    details_test_records: List[Dict]
    appointment_test_records: List[Dict]
    observation_test_records: List[Dict]
    illness_test_records: List[Dict]
    medication_test_records: List[Dict]

    def build_mock_table_and_refresh_known_test_records(self):
        setup_test_dynamo_with_data()
        test_table = get_pet_table_resource()
        scan_result = test_table.scan()
        self.all_test_records = scan_result['Items']
        self.details_test_records = [record for record
                                     in self.all_test_records
                                     if str(record['sort_key']).split('#')[0] == RecordType.DETAILS.value]  # noqa: E501
        self.appointment_test_records = [record for record
                                         in self.all_test_records
                                         if str(record['sort_key']).split('#')[0] == RecordType.APPOINTMENT.value]  # noqa: E501
        self.observation_test_records = [record for record
                                         in self.all_test_records
                                         if str(record['sort_key']).split('#')[0] == RecordType.OBSERVATION.value]  # noqa: E501
        self.illness_test_records = [record for record
                                     in self.all_test_records
                                     if str(record['sort_key']).split('#')[0] == RecordType.ILLNESS.value]  # noqa: E501
        self.medication_test_records = [record for record
                                        in self.all_test_records
                                        if str(record['sort_key']).split('#')[0] == RecordType.MEDICATION.value]  # noqa: E501

    def tests_get_all_records_for_pet(self):
        self.build_mock_table_and_refresh_known_test_records()
        pet_we_want = 'Avocato'
        missing_records = []
        all_expected_records = [record for record
                                in self.all_test_records
                                if record['name'] == pet_we_want]

        result = get_all_of_pets_records(pet_name=pet_we_want)

        for record in all_expected_records:
            if record not in result:
                missing_records.append(record)
        assert missing_records == [], \
            f"""
            Some expected records were not received:
                Missing: {missing_records}
                Received: {result}
                Expected: {all_expected_records}
            """

    def tests_get_all_records_wrong_name(self):
        self.build_mock_table_and_refresh_known_test_records()

        result = get_all_of_pets_records(pet_name='Quinn')

        assert result == []

    @mark.parametrize(
        argnames='record_type',
        argvalues=[
            RecordType.DETAILS,
            RecordType.APPOINTMENT,
            RecordType.ILLNESS,
            RecordType.MEDICATION,
            RecordType.OBSERVATION
        ]
    )
    def test_get_all_of_record_type_for_pet(self, record_type):
        self.build_mock_table_and_refresh_known_test_records()
        expected_pet = 'Avocato'
        expected_results = [
            record for record
            in self.all_test_records
            if record['name'] == expected_pet
            and str(record['sort_key']).split('#')[0] == record_type.value
            ]

        results = get_all_of_pets_record_type(
            pet_name=expected_pet,
            record_type=record_type
        )

        missed_results = []
        for expected_result in expected_results:
            if expected_result not in results:
                missed_results.append(expected_result)
        extra_results = []
        for result in results:
            if result not in expected_results:
                extra_results.append(result)
        assert missed_results == [] and extra_results == [], \
            f"""
            Results returned incorrectly:
            {len(missed_results)} missed results: {missed_results}
            {len(extra_results)} extra results: {extra_results}
            """

    @mark.parametrize(
        argnames='record_type, point_in_time',
        argvalues=[
            (RecordType.APPOINTMENT, datetime(year=1808, month=3, day=23)),
            (RecordType.ILLNESS, datetime(year=1808, month=4, day=4)),
            (RecordType.MEDICATION, datetime(year=1808, month=4, day=5)),
            (RecordType.OBSERVATION, datetime(year=1810, month=1, day=1))
        ]
    )
    def test_get_all_of_record_type_after_point_in_time(
            self,
            record_type,
            point_in_time: datetime
            ):
        self.build_mock_table_and_refresh_known_test_records()
        expected_pet = 'Avocato'
        expected_results = [
            record for record
            in self.all_test_records
            if record['name'] == expected_pet
            and str(record['sort_key']).split('#')[0] == record_type.value
            and record['date_time'] > point_in_time.astimezone(tz=timezone.utc).timestamp()  # noqa: E501
            ]

        result = get_all_of_pets_record_type_after_point_in_time(
            pet_name=expected_pet,
            point_in_time=point_in_time,
            record_type=record_type
        )

        assert result == expected_results

    @mark.parametrize(
        argnames='medicine_type',
        argvalues=['deworm', 'deflea', 'antiemetic', 'vaccine']
    )
    def test_get_all_records_of_medicine_type(self, medicine_type):
        self.build_mock_table_and_refresh_known_test_records()
        expected_results = [
            record for record
            in self.medication_test_records
            if record['medicine_type'] == medicine_type
            ]

        result = get_all_records_of_medicine_type(
            medicine_type=medicine_type
        )

        assert result == expected_results

    @mark.parametrize(
        argnames='medicine_type, lower_limit, upper_limit',
        argvalues=[
            ('deworm', datetime(year=1808, month=4, day=5), datetime(year=1808, month=7, day=13)),  # noqa: E501
            ('deworm', None, datetime(year=1808, month=7, day=13)),
            ('deworm', datetime(year=1808, month=4, day=5), None),
            ('deworm', None, None),
            ('deflea', datetime(year=1808, month=4, day=5), datetime(year=1808, month=7, day=13)),  # noqa: E501
            ('deflea', None, datetime(year=1808, month=7, day=13)),
            ('deflea', datetime(year=1808, month=4, day=5), None),
            ('deflea', None, None),
            ('antiemetic', datetime(year=1808, month=4, day=5), datetime(year=1808, month=7, day=13)),  # noqa: E501
            ('antiemetic', None, datetime(year=1808, month=7, day=13)),
            ('antiemetic', datetime(year=1808, month=4, day=5), None),
            ('antiemetic', None, None),
            ('vaccine', datetime(year=1808, month=4, day=5), datetime(year=1808, month=7, day=13)),  # noqa: E501
            ('vaccine', None, datetime(year=1808, month=7, day=13)),
            ('vaccine', datetime(year=1808, month=4, day=5), None),
            ('vaccine', None, None),
        ]
    )
    def test_get_all_records_of_medicine_type_in_next_due_timeframe(
            self,
            medicine_type,
            lower_limit: Optional[datetime],
            upper_limit: Optional[datetime]
            ):
        self.build_mock_table_and_refresh_known_test_records()
        lower_limit_decimal_timestamp: Optional[Decimal] = Decimal(lower_limit.astimezone(tz=timezone.utc).timestamp())if lower_limit is not None else None  # noqa: E501
        upper_limit_decimal_timestamp: Optional[Decimal] = Decimal(upper_limit.astimezone(tz=timezone.utc).timestamp())if upper_limit is not None else None  # noqa: E501
        expected_results = [
            record for record
            in self.medication_test_records
            if record['medicine_type'] == medicine_type
            ]
        if lower_limit_decimal_timestamp is not None:

            expected_results = [record for record
                                in expected_results
                                if record['next_due'] >= lower_limit_decimal_timestamp  # noqa: E501
                                ]
        if upper_limit_decimal_timestamp is not None:

            expected_results = [record for record
                                in expected_results
                                if record['next_due'] <= upper_limit_decimal_timestamp  # noqa: E501
                                ]
        result = get_all_records_of_medicine_type_in_next_due_timeframe(
            medicine_type=medicine_type,
            lower_date_limit=lower_limit,
            upper_date_limit=upper_limit
        )

        assert result == expected_results
