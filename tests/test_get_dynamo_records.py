from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
from unittest.mock import patch, Mock

import moto
from pytest import mark

from tests.helpers import (
    setup_test_dynamo_with_data
)
from app.support.data_access_layer.records.pet_table_models import RecordType
from support.common.aws_resources import get_pet_table_resource
from app.support.data_access_layer.get_records import (
    get_all_of_pets_records,
    get_all_of_pets_record_type,
    get_all_of_pets_record_type_after_point_in_time,
    get_all_records_of_medicine_type,
    get_all_records_of_medicine_type_in_next_due_timeframe,
    get_all_records_of_appointment_in_timeframe,
    get_all_of_record_type,
    get_all_records_of_medicine_in_next_due_timeframe
)
from app.support.find_reminders import find_reminders


@moto.mock_aws
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
                                     if str(record['sort_key']).split('#')[0] == RecordType.DETAILS.value]
        self.appointment_test_records = [record for record
                                         in self.all_test_records
                                         if str(record['sort_key']).split('#')[0] == RecordType.APPOINTMENT.value]
        self.observation_test_records = [record for record
                                         in self.all_test_records
                                         if str(record['sort_key']).split('#')[0] == RecordType.OBSERVATION.value]
        self.illness_test_records = [record for record
                                     in self.all_test_records
                                     if str(record['sort_key']).split('#')[0] == RecordType.ILLNESS.value]
        self.medication_test_records = [record for record
                                        in self.all_test_records
                                        if str(record['sort_key']).split('#')[0] == RecordType.MEDICATION.value]

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
            and record['date_time'] > point_in_time.astimezone(tz=timezone.utc).timestamp()
            ]

        results = get_all_of_pets_record_type_after_point_in_time(
            pet_name=expected_pet,
            point_in_time=point_in_time,
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

        results = get_all_records_of_medicine_type(
            medicine_type=medicine_type
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
        argnames='medicine_type, lower_limit, upper_limit',
        argvalues=[
            ('deworm', datetime(year=1808, month=4, day=5), datetime(year=1808, month=7, day=13)),
            ('deworm', None, datetime(year=1808, month=7, day=13)),
            ('deworm', datetime(year=1808, month=4, day=5), None),
            ('deworm', None, None),
            ('deflea', datetime(year=1808, month=4, day=5), datetime(year=1808, month=7, day=13)),
            ('deflea', None, datetime(year=1808, month=7, day=13)),
            ('deflea', datetime(year=1808, month=4, day=5), None),
            ('deflea', None, None),
            ('antiemetic', datetime(year=1808, month=4, day=5), datetime(year=1808, month=7, day=13)),
            ('antiemetic', None, datetime(year=1808, month=7, day=13)),
            ('antiemetic', datetime(year=1808, month=4, day=5), None),
            ('antiemetic', None, None),
            ('vaccine', datetime(year=1808, month=4, day=5), datetime(year=1808, month=7, day=13)),
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
        lower_limit_decimal_timestamp: Optional[Decimal] = Decimal(lower_limit.astimezone(tz=timezone.utc).timestamp())if lower_limit is not None else None
        upper_limit_decimal_timestamp: Optional[Decimal] = Decimal(upper_limit.astimezone(tz=timezone.utc).timestamp())if upper_limit is not None else None
        expected_results = [
            record for record
            in self.medication_test_records
            if record['medicine_type'] == medicine_type
            ]
        if lower_limit_decimal_timestamp is not None:

            expected_results = [record for record
                                in expected_results
                                if record['next_due'] >= lower_limit_decimal_timestamp
                                ]
        if upper_limit_decimal_timestamp is not None:

            expected_results = [record for record
                                in expected_results
                                if record['next_due'] <= upper_limit_decimal_timestamp
                                ]
        results = get_all_records_of_medicine_type_in_next_due_timeframe(
            medicine_type=medicine_type,
            lower_date_limit=lower_limit,
            upper_date_limit=upper_limit
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
        argnames='lower_limit, upper_limit',
        argvalues=[
            (datetime(year=1808, month=3, day=23), datetime(year=1809, month=3, day=23)),
            (None, datetime(year=1809, month=3, day=23)),
            (datetime(year=1808, month=3, day=23), None),
            (datetime(year=1812, month=1, day=29), datetime(year=1812, month=2, day=2)),
            (None, datetime(year=1812, month=2, day=2)),
            (datetime(year=1812, month=1, day=29), None),
            (None, None),
        ]
    )
    def test_get_all_records_of_appointment_in_timeframe(
            self,
            lower_limit: Optional[datetime],
            upper_limit: Optional[datetime]
            ):
        self.build_mock_table_and_refresh_known_test_records()
        lower_limit_decimal_timestamp: Optional[Decimal] = Decimal(lower_limit.astimezone(tz=timezone.utc).timestamp())if lower_limit is not None else None
        upper_limit_decimal_timestamp: Optional[Decimal] = Decimal(upper_limit.astimezone(tz=timezone.utc).timestamp())if upper_limit is not None else None
        expected_results = self.appointment_test_records
        if lower_limit_decimal_timestamp is not None:

            expected_results = [record for record
                                in expected_results
                                if record['date_time'] >= lower_limit_decimal_timestamp
                                ]
        if upper_limit_decimal_timestamp is not None:

            expected_results = [record for record
                                in expected_results
                                if record['date_time'] <= upper_limit_decimal_timestamp
                                ]

        results = get_all_records_of_appointment_in_timeframe(
            lower_date_limit=lower_limit,
            upper_date_limit=upper_limit
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
        argnames='lower_limit, upper_limit',
        argvalues=[
            (datetime(year=1808, month=3, day=23), datetime(year=1809, month=3, day=23)),
            (None, datetime(year=1809, month=3, day=23)),
            (datetime(year=1808, month=3, day=23), None),
            (datetime(year=1812, month=1, day=29), datetime(year=1812, month=2, day=2)),
            (None, datetime(year=1812, month=2, day=2)),
            (datetime(year=1812, month=1, day=29), None),
            (None, None),
        ]
    )
    def tests_get_all_records_of_medicine_in_next_due_timeframe(
            self,
            lower_limit: Optional[datetime],
            upper_limit: Optional[datetime]
            ):
        self.build_mock_table_and_refresh_known_test_records()
        lower_limit_decimal_timestamp: Optional[Decimal] = Decimal(lower_limit.astimezone(tz=timezone.utc).timestamp())if lower_limit is not None else None
        upper_limit_decimal_timestamp: Optional[Decimal] = Decimal(upper_limit.astimezone(tz=timezone.utc).timestamp())if upper_limit is not None else None
        expected_results = self.medication_test_records
        if lower_limit_decimal_timestamp is not None:

            expected_results = [record for record
                                in expected_results
                                if record['next_due'] >= lower_limit_decimal_timestamp
                                ]
        if upper_limit_decimal_timestamp is not None:

            expected_results = [record for record
                                in expected_results
                                if record['next_due'] <= upper_limit_decimal_timestamp
                                ]

        results = get_all_records_of_medicine_in_next_due_timeframe(
            lower_date_limit=lower_limit,
            upper_date_limit=upper_limit
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
        argnames='record_type',
        argvalues=[
            RecordType.APPOINTMENT,
            RecordType.DETAILS,
            RecordType.ILLNESS,
            RecordType.MEDICATION,
            RecordType.OBSERVATION,
        ]
    )
    def test_get_all_of_record_type(self, record_type):
        self.build_mock_table_and_refresh_known_test_records()
        expected_results = [
            record for record
            in self.all_test_records
            if str(record['record_type']) == record_type.value
            ]

        results = get_all_of_record_type(
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
        argnames='start_date, timespan',
        argvalues=[
            (datetime(year=1812, month=1, day=1), timedelta(weeks=26)),
            (datetime(year=1808, month=1, day=1), timedelta(weeks=104)),
            (datetime(year=1808, month=4, day=6), timedelta(days=1)),
        ]
    )
    @patch('app.support.find_reminders.utc_datetime_now')
    def tests_find_reminders(self,
                             utc_datetime_now: Mock,
                             start_date: datetime,
                             timespan: timedelta):
        end_date = start_date + timespan
        utc_datetime_now.return_value = start_date
        self.build_mock_table_and_refresh_known_test_records()
        records = find_reminders(timespan=timespan)

    # We want to group the returned records into correctly returned or not
        correct_records = []
        incorrect_records = []
        start_date = Decimal(start_date.timestamp())
        end_date = Decimal(end_date.timestamp())
        for record in records:
            # we should only get records back of the following types
            # but each gets it due date from a different field
            if record['record_type'] == RecordType.APPOINTMENT:
                record_date = record['date_time']
            elif record['record_type'] == RecordType.MEDICATION:
                record_date = record['next_due']
            else:
                incorrect_records.append(record)
                continue
            # we can now categorise the remaining records
            # by whether they are in the appropriate timeframe
            if start_date <= record_date <= end_date:
                correct_records.append(record)
            else:
                incorrect_records.append(record)

        # and now we can make assertions based on the grouping
        assert len(records) == len(correct_records), \
            f"Got {len(incorrect_records)} incorrect records returned: {str(incorrect_records)}"
