#  +--------------------------------------------------------------------------------------------+
#  | pet-table DynamoDB table map/schema/call it what you want                                  |
#  +========================+=============================+=====================================+
#  | Key                    | Data type                   | Record types used in                |
#  +------------------------+-----------------------------+-------------------------------------+
#  | name (partition key)   | str                         | All                                 |
#  | sort_key (sort key)    | str                         | All                                 |
#  | breed                  | str                         | Details                             |
#  | dob                    | Decimal as posix timestamp  | Details                             |
#  | gender                 | str                         | Details                             |
#  | colour                 | str                         | Details                             |
#  | microchip_number       | Decimal as int              | Details                             |
#  | date_time              | Decimal as posix timestamp  | All                                 |
#  | medicine_name          | str                         | Medication                          |
#  | medicine_type          | str                         | Medication                          |
#  | ailment                | str                         | Illness                             |
#  | description            | str                         | Illness, Observation, Appointment   |
#  | next_due               | Decimal as posix timestamp  | Medication                          |
#  | record_type            | str                         | All                                 |
#  +------------------------+-----------------------------+-------------------------------------+
#
#  Record Types = Details, Medication, Illness, Observation, Appointment
#

from typing import Any, Optional
from decimal import Decimal
from enum import Enum
from typing_extensions import Annotated
from numbers import Number

from pydantic import (
    BaseModel,
    model_validator
)
from pydantic.functional_validators import AfterValidator


class RecordType(str, Enum):
    APPOINTMENT = 'appointment'
    DETAILS = 'details'
    ILLNESS = 'illness'
    MEDICATION = 'medication'
    OBSERVATION = 'observation'


def _check_microchip_number(v: Any) -> Decimal:
    # Dynamo needs type: Decimal, microchip has to be positive integer
    if isinstance(v, Number) and v >= 0 and v % 1 == 0:
        return v
    else:
        raise ValueError("Microchip number needs to be a positive whole number")


MICROCHIP_NUM = Annotated[Decimal, AfterValidator(_check_microchip_number)]


class DetailsRecordModel(BaseModel):
    name: str
    sort_key: str
    breed: str
    dob: Decimal
    date_time: Decimal
    gender: str
    colour: str
    microchip_number: MICROCHIP_NUM
    record_type: str


class MedicationRecordModel(BaseModel):
    name: str
    sort_key: str
    date_time: Decimal
    medicine_name: str
    medicine_type: str
    repeat: bool
    next_due: Optional[Decimal] = None
    record_type: str

    @model_validator(mode='after')
    def check_repeat_and_next_due(self) -> 'MedicationRecordModel':
        if self.repeat is True and self.next_due is None:
            # Record must have next_due attribute if repeat is True
            raise ValueError('Medication is a repeat item but next_due has nt been set')
        return self


class IllnessRecordModel(BaseModel):
    name: str
    sort_key: str
    date_time: Decimal
    ailment: str
    description: str
    record_type: str


class ObservationRecordModel(BaseModel):
    name: str
    sort_key: str
    date_time: Decimal
    description: str
    record_type: str


class AppointmentRecordModel(BaseModel):
    name: str
    sort_key: str
    date_time: Decimal
    description: str
    record_type: str
