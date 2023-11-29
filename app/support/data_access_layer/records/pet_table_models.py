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

from typing import Optional
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class RecordType(str, Enum):
    APPOINTMENT = 'appointment'
    DETAILS = 'details'
    ILLNESS = 'illness'
    MEDICATION = 'medication'
    OBSERVATION = 'observation'


class DetailsRecordModel(BaseModel):
    name: str
    sort_key: str
    breed: str
    dob: Decimal
    date_time: Decimal
    gender: str
    colour: str
    microchip_number: Decimal
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
