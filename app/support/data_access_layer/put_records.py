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
    logger.info("Getting Dynamo resource")
    pet_table = get_pet_table_resource()
    logger.info("Getting Record Factory")
    factory = AppointmentRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        name=pet_name,
        date_time=appointment_time,
        description=description
    )
    _arbitrary_validation_and_record_put(
        factory=factory,
        record=record,
        table=pet_table
    )


def put_details_record(pet_name: str,
                       date_of_birth: datetime,
                       colour: str,
                       gender: str,
                       breed: str,
                       microchip_number: int):
    logger.info("Getting Dynamo resource")
    pet_table = get_pet_table_resource()
    logger.info("Getting Record Factory")
    factory: DetailsRecordFactory = DetailsRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        name=pet_name,
        date_of_birth=date_of_birth,
        colour=colour,
        gender=gender,
        breed=breed,
        microchip_number=microchip_number
    )
    _arbitrary_validation_and_record_put(
        factory=factory,
        record=record,
        table=pet_table
    )


def put_illness_record(pet_name: str,
                       ailment: str,
                       observed_time: datetime,
                       description: str):
    logger.info("Getting Dynamo resource")
    pet_table = get_pet_table_resource()
    logger.info("Getting Record Factory")
    factory = IllnessRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        name=pet_name,
        ailment=ailment,
        date_time=observed_time,
        description=description
    )
    _arbitrary_validation_and_record_put(
        factory=factory,
        record=record,
        table=pet_table
    )


def put_medication_record(pet_name: str,
                          time_of_administration: datetime,
                          name_of_medicine: str,
                          type_of_medication: str,
                          next_due: Optional[datetime] = None):
    logger.info("Getting Dynamo resource")
    pet_table = get_pet_table_resource()
    logger.info("Getting Record Factory")
    factory = MedicationRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        name=pet_name,
        administered=time_of_administration,
        name_of_medicine=name_of_medicine,
        type_of_medicine=type_of_medication,
        next_due=next_due
    )
    _arbitrary_validation_and_record_put(
        factory=factory,
        record=record,
        table=pet_table
    )


def put_observation_record(pet_name: str,
                           observed: datetime,
                           description: str):
    logger.info("Getting Dynamo resource")
    pet_table = get_pet_table_resource()
    logger.info("Getting Record Factory")
    factory = ObservationRecordFactory()
    logger.info("Producing record")
    record = factory.produce_record(
        name=pet_name,
        date_time=observed,
        description=description
    )
    _arbitrary_validation_and_record_put(
        factory=factory,
        record=record,
        table=pet_table
    )


def _arbitrary_validation_and_record_put(factory: AbstractRecordFactory,
                                         record: Dict,
                                         table):
    logger.info("Validating record")
    if not factory.validate_record(record=record):
        record = factory.coerce_record_to_valid_state(record=record)
        if record is None:
            logger.warning("Record invalid, not attempting to publish record")
    logger.info("Putting record in Dynamo")
    _ = table.put_item(
        Item=record,
    )
    logger.info("Successful")
