#  +--------------------------------------------------------------------------------------------+  # noqa: E501
#  | pet-table DynamoDB table map/schema/call it what you want                                  |  # noqa: E501
#  +========================+=============================+=====================================+  # noqa: E501
#  | Key                    | Data type                   | Record types used in                |  # noqa: E501
#  +------------------------+-----------------------------+-------------------------------------+  # noqa: E501
#  | name (partition key)   | str                         | All                                 |  # noqa: E501
#  | sort_key (sort key)    | str                         | All                                 |  # noqa: E501
#  | breed                  | str                         | Details                             |  # noqa: E501
#  | dob                    | Decimal as posix timestamp  | Details                             |  # noqa: E501
#  | gender                 | str                         | Details                             |  # noqa: E501
#  | colour                 | str                         | Details                             |  # noqa: E501
#  | microchip_number       | Decimal as int              | Details                             |  # noqa: E501
#  | date_time              | Decimal as posix timestamp  | All                                 |  # noqa: E501
#  | medicine_name          | str                         | Medication                          |  # noqa: E501
#  | medicine_type          | str                         | Medication                          |  # noqa: E501
#  | ailment                | str                         | Illness                             |  # noqa: E501
#  | description            | str                         | Illness, Observation, Appointment   |  # noqa: E501
#  | next_due               | Decimal as posix timestamp  | Medication                          |  # noqa: E501
#  | record_type            | str                         | All                                 |  # noqa: E501
#  +------------------------+-----------------------------+-------------------------------------+  # noqa: E501
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