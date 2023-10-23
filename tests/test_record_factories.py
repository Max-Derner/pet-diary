from unittest.mock import Mock, patch
from unittest import TestCase
from app.supporting_cast.record_skeletons.illness_record import IllnessRecordFactory  # noqa: E501
from app.supporting_cast.record_skeletons.details_record import DetailsRecordFactory  # noqa: E501
from app.supporting_cast.record_skeletons.medication_record import MedicationRecordFactory  # noqa: E501
from app.supporting_cast.record_skeletons.observation_record import ObservationRecordFactory  # noqa: E501
from app.supporting_cast.record_skeletons.appointment_record import AppointmentRecordFactory  # noqa: E501
from datetime import datetime
from decimal import Decimal

RECORD_SKELETON_MODULE = 'app.supporting_cast.record_skeletons'


class TestsIllnessRecordFactory(TestCase):

    correct_illness_record = {
        'name': 'me',
        'sort_key': 'illness#stinky-butt#123456.789',
        'date_time': Decimal(1697238000.0),
        'ailment': 'stinky-butt',
        'description': 'Butt so stinky, it makes everyone in the room cry',
        }

    nearly_correct_illness_record = {
        'name': 'me',
        'sort_key': 'illness#stinky-butt#123456.789',
        'date_time': '1697238000.0',
        'ailment': 'stinky-butt',
        'description': 'Butt so stinky, it makes everyone in the room cry',
        }

    invalid_illness_record = {
        'name': 'me',
        'sort_key': 'illness#stinky-butt#123456.789',
        'date_time': 'today',
        'ailment': 'stinky-butt',
        'description': 'Butt so stinky, it makes everyone in the room cry',
        }

    @patch(f'{RECORD_SKELETON_MODULE}.illness_record.utc_timestamp_now')
    def tests_produces_record_of_correct_form(self, utc_timestamp_now: Mock):
        utc_timestamp_now.return_value = 123456.789
        illness_factory = IllnessRecordFactory()
        actual_record = illness_factory.produce_record(
            name='me',
            ailment='stinky-butt',
            date_time=datetime(year=2023,
                               month=10,
                               day=14),
            description="Butt so stinky, it makes everyone in the room cry"
        )
        assert actual_record == self.correct_illness_record

    def tests_can_coerce_record_into_correct_form(self):
        illness_factory = IllnessRecordFactory()
        returned_record = illness_factory.coerce_record_to_valid_state(
            record=self.nearly_correct_illness_record
        )
        assert returned_record == self.correct_illness_record

    def tests_returns_none_when_record_is_screwed(self):
        illness_factory = IllnessRecordFactory()
        actual_record = illness_factory.coerce_record_to_valid_state(
            record=self.invalid_illness_record
        )
        assert actual_record is None


class TestsDetailsRecordFactory(TestCase):

    correct_details_record = {
        'name': 'me',
        'sort_key': 'details',
        'breed': 'person',
        'colour': 'regular',
        'dob': Decimal(-5177087925.0),
        'gender': 'yes',
        'microchip_number': 1,
        }

    nearly_correct_details_record = {
        'name': 'me',
        'sort_key': 'details',
        'breed': 'person',
        'colour': 'regular',
        'dob': '-5177087925.0',
        'gender': 'yes',
        'microchip_number': '1',
        }

    invalid_details_record = {
        'name': 'me',
        'sort_key': 'details',
        'breed': 'person',
        'colour': 'regular',
        'dob': 'yesterday',
        'gender': 'yes',
        'microchip_number': '1',
        }

    def tests_produces_record_of_correct_form(self):
        details_factory = DetailsRecordFactory()
        actual_record = details_factory.produce_record(
            name='me',
            date_of_birth=datetime(year=1805,
                                   month=12,
                                   day=12),
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

    def tests_returns_none_when_record_is_screwed(self):
        details_factory = DetailsRecordFactory()
        actual_record = details_factory.coerce_record_to_valid_state(
            record=self.invalid_details_record
        )
        assert actual_record is None


class TestsMedicationRecordFactory(TestCase):

    correct_medication_record = {
        'name': 'me',
        'sort_key': 'medication#non-poisonous#123456.789',
        'date_time': Decimal(1701475200.0),
        'medicine_name': 'Flux-a-make-you-feel-better-a-tonne',
        'medicine_type': 'non-poisonous',
        'repeat': True,
        'next_due': Decimal(1704153600.0),
        }

    also_correct_medication_record = {
        'name': 'me',
        'sort_key': 'medication#non-poisonous#123456.789',
        'date_time': Decimal(1701475200.0),
        'medicine_name': 'Flux-a-make-you-feel-better-a-tonne',
        'repeat': False,
        'medicine_type': 'non-poisonous',
        }

    nearly_correct_medication_record = {
        'name': 'me',
        'sort_key': 'medication#non-poisonous#123456.789',
        'date_time': '1701475200.0',
        'medicine_name': 'Flux-a-make-you-feel-better-a-tonne',
        'medicine_type': 'non-poisonous',
        'repeat': 'True',
        'next_due': '1704153600.0',
        }

    invalid_medication_record = {
        'name': 'me',
        'sort_key': 'medication#non-poisonous#123456.789',
        'date_time': Decimal(1701475200.0),
        'medicine_name': 'Flux-a-make-you-feel-better-a-tonne',
        'medicine_type': 'non-poisonous',
        'repeat': 'yes',
        'next_due': 'never!',
        }

    @patch(f'{RECORD_SKELETON_MODULE}.medication_record.utc_timestamp_now')
    def tests_produces_record_of_correct_form(self, utc_timestamp_now: Mock):
        utc_timestamp_now.return_value = 123456.789
        medication_factory = MedicationRecordFactory()
        actual_record = medication_factory.produce_record(
            name='me',
            date_prescribed=datetime(year=2023,
                                     month=12,
                                     day=2),
            name_of_medicine="Flux-a-make-you-feel-better-a-tonne",
            type_of_medicine="non-poisonous",
            next_due=datetime(year=2024,
                              month=1,
                              day=2),
            )
        assert actual_record == self.correct_medication_record

    @patch(f'{RECORD_SKELETON_MODULE}.medication_record.utc_timestamp_now')
    def tests_produces_record_of_correct_form_when_medicine_not_due(self, utc_timestamp_now: Mock):  # noqa: E501
        utc_timestamp_now.return_value = 123456.789
        medication_factory = MedicationRecordFactory()
        actual_record = medication_factory.produce_record(
            name='me',
            date_prescribed=datetime(year=2023,
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

    def tests_returns_none_when_record_is_screwed(self):
        medication_factory = MedicationRecordFactory()
        actual_record = medication_factory.coerce_record_to_valid_state(
            record=self.invalid_medication_record
        )
        assert actual_record is None


class TestsObservationRecordFactory(TestCase):

    correct_observation_record = {
        'name': 'me',
        'sort_key': 'observation#123456.789',
        'date_time': Decimal(1697238000.0),
        'description': 'I have observed that you are not the nicest person, and I have concerns for your future health regarding me bloody well lamping you one sunshine',  # noqa: E501
        }

    nearly_correct_observation_record = {
        'name': 'me',
        'sort_key': 'observation#123456.789',
        'date_time': '1697238000.0',
        'description': 'I have observed that you are not the nicest person, and I have concerns for your future health regarding me bloody well lamping you one sunshine',  # noqa: E501
        }

    invalid_observation_record = {
        'name': 'me',
        'sort_key': 'observation#123456.789',
        'date_time': 'Tuesday mate',
        'description': 'I have observed that you are not the nicest person, and I have concerns for your future health regarding me bloody well lamping you one sunshine',  # noqa: E501
        }

    @patch(f'{RECORD_SKELETON_MODULE}.observation_record.utc_timestamp_now')
    def tests_produces_record_of_correct_form(self, utc_timestamp_now: Mock):
        utc_timestamp_now.return_value = 123456.789
        observation_factory = ObservationRecordFactory()
        actual_record = observation_factory.produce_record(
            name='me',
            date_time=datetime(year=2023,
                               month=10,
                               day=14),
            description="I have observed that you are not the nicest person, and I have concerns for your future health regarding me bloody well lamping you one sunshine"  # noqa: E501
        )
        assert actual_record == self.correct_observation_record

    def tests_can_coerce_record_into_correct_form(self):
        observation_factory = ObservationRecordFactory()
        returned_record = observation_factory.coerce_record_to_valid_state(
            record=self.nearly_correct_observation_record
        )
        assert returned_record == self.correct_observation_record

    def tests_returns_none_when_record_is_screwed(self):
        observation_factory = ObservationRecordFactory()
        actual_record = observation_factory.coerce_record_to_valid_state(
            record=self.invalid_observation_record
        )
        assert actual_record is None


class TestsAppointmentRecordFactory(TestCase):

    correct_appointment_record = {
        'name': 'me',
        'sort_key': 'appointment#123456.789',
        'date_time': Decimal(1697238000.0),
        'description': 'Appointment with Dr Nick to perform a butthole-dectomy so you can be less of a butthole',  # noqa: E501
        }

    nearly_correct_appointment_record = {
        'name': 'me',
        'sort_key': 'appointment#123456.789',
        'date_time': '1697238000.0',
        'description': 'Appointment with Dr Nick to perform a butthole-dectomy so you can be less of a butthole',  # noqa: E501
        }

    invalid_appointment_record = {
        'name': 'me',
        'sort_key': 'appointment#123456.789',
        'date_time': 'Tuesday mate',
        'description': 'Appointment with Dr Nick to perform a butthole-dectomy so you can be less of a butthole',  # noqa: E501
        }

    @patch(f'{RECORD_SKELETON_MODULE}.appointment_record.utc_timestamp_now')
    def tests_produces_record_of_correct_form(self, utc_timestamp_now: Mock):
        utc_timestamp_now.return_value = 123456.789
        appointment = AppointmentRecordFactory()
        actual_record = appointment.produce_record(
            name='me',
            date_time=datetime(year=2023,
                               month=10,
                               day=14),
            description="Appointment with Dr Nick to perform a butthole-dectomy so you can be less of a butthole"  # noqa: E501
        )
        assert actual_record == self.correct_appointment_record

    def tests_can_coerce_record_into_correct_form(self):
        appointment = AppointmentRecordFactory()
        returned_record = appointment.coerce_record_to_valid_state(
            record=self.nearly_correct_appointment_record
        )
        assert returned_record == self.correct_appointment_record

    def tests_returns_none_when_record_is_screwed(self):
        appointment = AppointmentRecordFactory()
        actual_record = appointment.coerce_record_to_valid_state(
            record=self.invalid_appointment_record
        )
        assert actual_record is None
