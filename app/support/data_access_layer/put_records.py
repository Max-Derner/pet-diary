from datetime import datetime
from typing import Dict, Optional
from app.support.logger import get_full_logger
from app.support.data_access_layer.helpers import get_pet_table_resource
from app.support.records.abstract_record import AbstractRecordFactory
from app.support.records.details_record import DetailsRecordFactory
from app.support.records.appointment_record import AppointmentRecordFactory
from app.support.records.illness_record import IllnessRecordFactory
from app.support.records.medication_record import MedicationRecordFactory
from app.support.records.observation_record import ObservationRecordFactory


logger = get_full_logger()


def put_appointment_record(pet_name: str,
                           appointment_time: datetime,
                           description: str):
    logger.info("Getting Record Factory")
    factory = AppointmentRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        pet_name=pet_name,
        appointment_time=appointment_time,
        description=description
    )
    _validate_record_then_put_in_pet_table(
        factory=factory,
        record=record
    )


def put_details_record(pet_name: str,
                       date_of_birth: datetime,
                       colour: str,
                       gender: str,
                       breed: str,
                       microchip_number: int):
    logger.info("Getting Record Factory")
    factory: DetailsRecordFactory = DetailsRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        pet_name=pet_name,
        date_of_birth=date_of_birth,
        colour=colour,
        gender=gender,
        breed=breed,
        microchip_number=microchip_number
    )
    _validate_record_then_put_in_pet_table(
        factory=factory,
        record=record
    )


def put_illness_record(pet_name: str,
                       ailment: str,
                       observed_time: datetime,
                       description: str):
    logger.info("Getting Record Factory")
    factory = IllnessRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        pet_name=pet_name,
        ailment=ailment,
        observed_time=observed_time,
        description=description
    )
    _validate_record_then_put_in_pet_table(
        factory=factory,
        record=record
    )


def put_medication_record(pet_name: str,
                          time_of_administration: datetime,
                          name_of_medicine: str,
                          type_of_medicine: str,
                          next_due: Optional[datetime] = None):
    logger.info("Getting Record Factory")
    factory = MedicationRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        pet_name=pet_name,
        time_of_administration=time_of_administration,
        name_of_medicine=name_of_medicine,
        type_of_medicine=type_of_medicine,
        next_due=next_due
    )
    _validate_record_then_put_in_pet_table(
        factory=factory,
        record=record
    )


def put_observation_record(pet_name: str,
                           observed_time: datetime,
                           description: str):
    logger.info("Getting Record Factory")
    factory = ObservationRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        pet_name=pet_name,
        observed_time=observed_time,
        description=description
    )
    _validate_record_then_put_in_pet_table(
        factory=factory,
        record=record
    )


def _validate_record_then_put_in_pet_table(factory: AbstractRecordFactory,
                                           record: Dict):
    logger.info("Validating record")
    if not factory.validate_record(record=record):
        record = factory.coerce_record_to_valid_state(record=record)
        if record is None:
            logger.warning("Record invalid, not attempting to publish record")
    logger.info("Getting Dynamo resource")
    table = get_pet_table_resource()
    logger.info("Putting record in Dynamo")
    response = table.put_item(
        Item=record,
    )
    logger.debug(f"RESPONSE: {response}")
    logger.info("Successful")
