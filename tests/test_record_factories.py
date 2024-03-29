from datetime import datetime, timedelta
from decimal import Decimal

from unittest.mock import patch
import pytest

from app.support.data_access_layer.records.illness_record import IllnessRecordFactory
from app.support.data_access_layer.records.details_record import DetailsRecordFactory
from app.support.data_access_layer.records.medication_record import MedicationRecordFactory
from app.support.data_access_layer.records.observation_record import ObservationRecordFactory
from app.support.data_access_layer.records.appointment_record import AppointmentRecordFactory
from app.support.data_access_layer.records.pet_table_models import RecordType
from .helpers import mock_utc_timestamp_now

RECORDS_MODULE = 'app.support.data_access_layer.records'


class TestsIllnessRecordFactory:

    date_time = datetime(year=2023, month=10, day=14)

    correct_illness_record = {
        'name': 'me',
        'sort_key': f'illness#stinky-butt#{mock_utc_timestamp_now()}',
        'date_time': Decimal(date_time.timestamp()),
        'ailment': 'stinky-butt',
        'description': 'Butt so stinky, it makes everyone in the room cry',
        'record_type': RecordType.ILLNESS.value
        }

    nearly_correct_illness_record = {
        'name': 'me',
        'sort_key': f'illness#stinky-butt#{mock_utc_timestamp_now()}',
        'date_time': f'{Decimal(date_time.timestamp())}',  # it's a string!
        'ailment': 'stinky-butt',
        'description': 'Butt so stinky, it makes everyone in the room cry',
        'record_type': RecordType.ILLNESS.value
        }

    invalid_illness_record = {
        'name': 'me',
        'sort_key': f'illness#stinky-butt#{mock_utc_timestamp_now()}',
        'date_time': 'today',
        'ailment': 'stinky-butt',
        'description': 'Butt so stinky, it makes everyone in the room cry',
        'record_type': RecordType.ILLNESS.value
        }

    @patch(
            f'{RECORDS_MODULE}.illness_record.utc_timestamp_now',
            mock_utc_timestamp_now
            )
    def tests_produces_record_of_correct_form(self):
        illness_factory = IllnessRecordFactory()

        actual_record = illness_factory.produce_record(
            pet_name='me',
            ailment='stinky-butt',
            observed_time=self.date_time,
            description="Butt so stinky, it makes everyone in the room cry"
        )

        assert actual_record == self.correct_illness_record

    def tests_can_coerce_record_into_correct_form(self):
        illness_factory = IllnessRecordFactory()

        returned_record = illness_factory.coerce_record_to_valid_state(
            record=self.nearly_correct_illness_record
        )

        assert returned_record == self.correct_illness_record

    def tests_returns_none_from_validation_when_record_is_screwed(self):
        illness_factory = IllnessRecordFactory()

        actual_record = illness_factory.coerce_record_to_valid_state(
            record=self.invalid_illness_record
        )

        assert actual_record is None

    def tests_produces_valid_record(self):
        illness_factory = IllnessRecordFactory()
        record = illness_factory.produce_record(
            pet_name='me',
            ailment='stinky-butt',
            observed_time=self.date_time,
            description="Butt so stinky, it makes everyone in the room cry"
        )

        validation_result = illness_factory.validate_record(record=record)

        assert validation_result is True


class TestsDetailsRecordFactory:

    date_of_birth = datetime(year=1805, month=12, day=12)

    correct_details_record = {
        'name': 'me',
        'sort_key': 'details',
        'breed': 'person',
        'colour': 'regular',
        'dob': Decimal(date_of_birth.timestamp()),
        'date_time': Decimal(mock_utc_timestamp_now()),
        'gender': 'yes',
        'microchip_number': 1,
        'record_type': RecordType.DETAILS.value
        }

    nearly_correct_details_record = {
        'name': 'me',
        'sort_key': 'details',
        'breed': 'person',
        'colour': 'regular',
        'dob': f'{Decimal(date_of_birth.timestamp())}',  # it's a string!
        'date_time': f'{Decimal(mock_utc_timestamp_now())}',  # it's a string!
        'gender': 'yes',
        'microchip_number': '1',
        'record_type': RecordType.DETAILS.value
        }

    invalid_details_record = {
        'name': 'me',
        'sort_key': 'details',
        'breed': 'person',
        'colour': 'regular',
        'dob': 'yesterday',
        'date_time': 'the time I created my pet details record',
        'gender': 'yes',
        'microchip_number': '1',
        'record_type': RecordType.DETAILS.value
        }

    @patch(
            f'{RECORDS_MODULE}.details_record.utc_timestamp_now',
            mock_utc_timestamp_now
            )
    def tests_produces_record_of_correct_form(self):
        details_factory = DetailsRecordFactory()

        actual_record = details_factory.produce_record(
            pet_name='me',
            date_of_birth=self.date_of_birth,
            colour='regular',
            gender='yes',
            breed='person',
            microchip_number=1
        )

        assert actual_record == self.correct_details_record

    def tests_can_coerce_record_into_correct_form(self):
        details_factory = DetailsRecordFactory()

        returned_record = details_factory.coerce_record_to_valid_state(
            record=self.nearly_correct_details_record
        )

        assert returned_record == self.correct_details_record

    def tests_returns_none_from_validation_when_record_is_screwed(self):
        details_factory = DetailsRecordFactory()

        actual_record = details_factory.coerce_record_to_valid_state(
            record=self.invalid_details_record
        )

        assert actual_record is None

    def tests_produces_valid_record(self):
        details_factory = DetailsRecordFactory()
        record = details_factory.produce_record(
            pet_name='me',
            date_of_birth=self.date_of_birth,
            colour='good',
            gender='yes',
            breed='people',
            microchip_number=123456789
        )

        validation_result = details_factory.validate_record(record=record)

        assert validation_result is True

    @pytest.mark.parametrize('microchip_number, validity',
                             [
                                 (1, True),
                                 (1.1, False),
                                 (-1, False),
                             ])
    def tests_microchip_number_must_be_int(self, microchip_number, validity):
        details_factory = DetailsRecordFactory()
        record = details_factory.produce_record(
            pet_name='me',
            date_of_birth=self.date_of_birth,
            colour='good',
            gender='yes',
            breed='people',
            microchip_number=microchip_number
        )

        validation_result = details_factory.validate_record(record=record)

        assert validation_result is validity, f"A microchip number of type: {type(microchip_number)} and value '{microchip_number}' is {'' if validity else 'not '}supposed to be valid"


class TestsMedicationRecordFactory:

    administered = datetime(year=2023, month=12, day=2)

    next_due = datetime(year=2024, month=1, day=2)

    correct_medication_record = {
        'name': 'me',
        'sort_key': f'medication#non-poisonous#{mock_utc_timestamp_now()}',
        'date_time': Decimal(administered.timestamp()),
        'medicine_name': 'Flux-a-make-you-feel-better-a-tonne',
        'medicine_type': 'non-poisonous',
        'repeat': True,
        'next_due': Decimal(next_due.timestamp()),
        'record_type': RecordType.MEDICATION.value
        }

    also_correct_medication_record = {
        'name': 'me',
        'sort_key': f'medication#non-poisonous#{mock_utc_timestamp_now()}',
        'date_time': Decimal(administered.timestamp()),
        'medicine_name': 'Flux-a-make-you-feel-better-a-tonne',
        'repeat': False,
        'medicine_type': 'non-poisonous',
        'record_type': RecordType.MEDICATION.value
        }

    nearly_correct_medication_record = {
        'name': 'me',
        'sort_key': f'medication#non-poisonous#{mock_utc_timestamp_now()}',
        'date_time': f'{Decimal(administered.timestamp())}',  # it's a string!
        'medicine_name': 'Flux-a-make-you-feel-better-a-tonne',
        'medicine_type': 'non-poisonous',
        'repeat': 'True',
        'next_due': '1704153600.0',
        'record_type': RecordType.MEDICATION.value
        }

    invalid_medication_record = {
        'name': 'me',
        'sort_key': f'medication#non-poisonous#{mock_utc_timestamp_now()}',
        'date_time': Decimal(administered.timestamp()),
        'medicine_name': 'Flux-a-make-you-feel-better-a-tonne',
        'medicine_type': 'non-poisonous',
        'repeat': 'yes',
        'next_due': 'never!',
        'record_type': RecordType.MEDICATION.value
        }

    @patch(
            f'{RECORDS_MODULE}.medication_record.utc_timestamp_now',
            mock_utc_timestamp_now
            )
    def tests_produces_record_of_correct_form(self):
        medication_factory = MedicationRecordFactory()

        actual_record = medication_factory.produce_record(
            pet_name='me',
            time_of_administration=datetime(year=2023,
                                            month=12,
                                            day=2),
            name_of_medicine="Flux-a-make-you-feel-better-a-tonne",
            type_of_medicine="non-poisonous",
            next_due=datetime(year=2024,
                              month=1,
                              day=2),
            )

        assert actual_record == self.correct_medication_record

    @patch(
            f'{RECORDS_MODULE}.medication_record.utc_timestamp_now',
            mock_utc_timestamp_now
            )
    def tests_produces_record_of_correct_form_when_medicine_not_due(self):
        medication_factory = MedicationRecordFactory()

        actual_record = medication_factory.produce_record(
            pet_name='me',
            time_of_administration=datetime(year=2023,
                                            month=12,
                                            day=2),
            name_of_medicine="Flux-a-make-you-feel-better-a-tonne",
            type_of_medicine="non-poisonous",
            next_due=None,
            )

        assert actual_record == self.also_correct_medication_record

    def tests_can_coerce_record_into_correct_form(self):
        medication_factory = MedicationRecordFactory()

        returned_record = medication_factory.coerce_record_to_valid_state(
            record=self.nearly_correct_medication_record
        )

        assert returned_record == self.correct_medication_record

    def tests_returns_none_from_validation_when_record_is_screwed(self):
        medication_factory = MedicationRecordFactory()

        actual_record = medication_factory.coerce_record_to_valid_state(
            record=self.invalid_medication_record
        )

        assert actual_record is None

    def tests_produces_valid_record(self):
        medication_factory = MedicationRecordFactory()
        record = medication_factory.produce_record(
            pet_name='me',
            time_of_administration=datetime.now(),
            name_of_medicine='poo better laxative tm',
            type_of_medicine='laxative',
            next_due=datetime.now() + timedelta(days=90)
        )

        result = medication_factory.validate_record(record=record)

        assert result is True

    def tests_produces_valid_record_alt(self):
        medication_factory = MedicationRecordFactory()
        record = medication_factory.produce_record(
            pet_name='me',
            time_of_administration=datetime.now(),
            name_of_medicine='poo better laxative tm',
            type_of_medicine='laxative',
            next_due=None
        )

        result = medication_factory.validate_record(record=record)

        assert result is True

    def tests_validation_failure_for_repeat_items_with_no_next_due_set(self):
        medication_factory = MedicationRecordFactory()
        record = medication_factory.produce_record(
            pet_name='me',
            time_of_administration=datetime.now(),
            name_of_medicine='poo better laxative tm',
            type_of_medicine='laxative',
            next_due=datetime.now()
        )
        del record['next_due']

        result = medication_factory.validate_record(record=record)

        assert result is False


class TestsObservationRecordFactory:

    observed_date_time = datetime(year=2023, month=10, day=14)

    correct_observation_record = {
        'name': 'me',
        'sort_key': f'observation#{mock_utc_timestamp_now()}',
        'date_time': Decimal(observed_date_time.timestamp()),
        'description': 'I have observed that you are not the nicest person, and I have concerns for your future health regarding me bloody well lamping you one sunshine',
        'record_type': RecordType.OBSERVATION.value
        }

    nearly_correct_observation_record = {
        'name': 'me',
        'sort_key': f'observation#{mock_utc_timestamp_now()}',
        'date_time': f'{Decimal(observed_date_time.timestamp())}',  # it's a string!
        'description': 'I have observed that you are not the nicest person, and I have concerns for your future health regarding me bloody well lamping you one sunshine',
        'record_type': RecordType.OBSERVATION.value
        }

    invalid_observation_record = {
        'name': 'me',
        'sort_key': f'observation#{mock_utc_timestamp_now()}',
        'date_time': 'Tuesday mate',
        'description': 'I have observed that you are not the nicest person, and I have concerns for your future health regarding me bloody well lamping you one sunshine',
        'record_type': RecordType.OBSERVATION.value
        }

    @patch(
            f'{RECORDS_MODULE}.observation_record.utc_timestamp_now',
            mock_utc_timestamp_now
            )
    def tests_produces_record_of_correct_form(self):
        observation_factory = ObservationRecordFactory()

        actual_record = observation_factory.produce_record(
            pet_name='me',
            observed_time=self.observed_date_time,
            description="I have observed that you are not the nicest person, and I have concerns for your future health regarding me bloody well lamping you one sunshine"
        )

        assert actual_record == self.correct_observation_record

    def tests_can_coerce_record_into_correct_form(self):
        observation_factory = ObservationRecordFactory()

        returned_record = observation_factory.coerce_record_to_valid_state(
            record=self.nearly_correct_observation_record
        )

        assert returned_record == self.correct_observation_record

    def tests_returns_none_from_validation_when_record_is_screwed(self):
        observation_factory = ObservationRecordFactory()

        actual_record = observation_factory.coerce_record_to_valid_state(
            record=self.invalid_observation_record
        )

        assert actual_record is None

    def tests_produces_valid_record(self):
        observation_factory = ObservationRecordFactory()
        record = observation_factory.produce_record(
            pet_name='me',
            observed_time=self.observed_date_time,
            description="Observed burping in the vicinity of his wife. Wife disappointed"
        )

        validation_result = observation_factory.validate_record(record=record)

        assert validation_result is True


class TestsAppointmentRecordFactory:

    date_time = datetime(year=2023, month=10, day=14)

    correct_appointment_record = {
        'name': 'me',
        'sort_key': f'appointment#{mock_utc_timestamp_now()}',
        'date_time': Decimal(date_time.timestamp()),
        'description': 'Appointment with Dr Nick to perform a butthole-dectomy so you can be less of a butthole',
        'record_type': RecordType.APPOINTMENT.value
        }

    nearly_correct_appointment_record = {
        'name': 'me',
        'sort_key': f'appointment#{mock_utc_timestamp_now()}',
        'date_time': f'{Decimal(date_time.timestamp())}',  # it's a string!
        'description': 'Appointment with Dr Nick to perform a butthole-dectomy so you can be less of a butthole',
        'record_type': RecordType.APPOINTMENT.value
        }

    invalid_appointment_record = {
        'name': 'me',
        'sort_key': f'appointment#{mock_utc_timestamp_now}',
        'date_time': 'Tuesday mate',
        'description': 'Appointment with Dr Nick to perform a butthole-dectomy so you can be less of a butthole',
        'record_type': RecordType.APPOINTMENT.value
        }

    @patch(
            f'{RECORDS_MODULE}.appointment_record.utc_timestamp_now',
            mock_utc_timestamp_now
            )
    def tests_produces_record_of_correct_form(self):
        appointment = AppointmentRecordFactory()
        actual_record = appointment.produce_record(
            pet_name='me',
            appointment_time=self.date_time,
            description="Appointment with Dr Nick to perform a butthole-dectomy so you can be less of a butthole"
        )
        assert actual_record == self.correct_appointment_record

    def tests_can_coerce_record_into_correct_form(self):
        appointment = AppointmentRecordFactory()
        returned_record = appointment.coerce_record_to_valid_state(
            record=self.nearly_correct_appointment_record
        )
        assert returned_record == self.correct_appointment_record

    def tests_returns_none_from_validation_when_record_is_screwed(self):
        appointment = AppointmentRecordFactory()
        actual_record = appointment.coerce_record_to_valid_state(
            record=self.invalid_appointment_record
        )
        assert actual_record is None

    def tests_produces_valid_record(self):
        appointment = AppointmentRecordFactory()
        record = appointment.produce_record(
            pet_name='me',
            appointment_time=datetime.now(),
            description='Got appointment to do some coding'
        )

        validation_result = appointment.validate_record(record=record)

        assert validation_result is True
