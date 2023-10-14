#  +--------------------------------------------------------------------------------------------------------+ # noqa: E501
#  | pet-table DynamoDB table map/schema/call it what you want                                              | # noqa: E501
#  +========================+=============================+=================================================+ # noqa: E501
#  | Key                    | Data type                   | Record types used in                            | # noqa: E501
#  +------------------------+-----------------------------+-------------------------------------------------+ # noqa: E501
#  | name (partition key)   | str                         | All                                             | # noqa: E501
#  | sort_key (sort key)    | str                         | All                                             | # noqa: E501
#  | breed                  | str                         | Details                                         | # noqa: E501
#  | dob                    | float as posix timestamp    | Details                                         | # noqa: E501
#  | gender                 | str                         | Details                                         | # noqa: E501
#  | colour                 | str                         | Details                                         | # noqa: E501
#  | microchip_number       | int                         | Details                                         | # noqa: E501
#  | date_time              | float as posix timestamp    | Medication, Illness, Observation, Appointment   | # noqa: E501
#  | medicine_name          | str                         | Medication                                      | # noqa: E501
#  | medicine_type          | str                         | Medication                                      | # noqa: E501
#  | ailment                | str                         | Illness                                         | # noqa: E501
#  | description            | str                         | Illness, Observation, Appointment               | # noqa: E501
#  | next_due               | float as posix timestamp    | Medication                                      | # noqa: E501
#  +------------------------+-----------------------------+-------------------------------------------------+ # noqa: E501

from pydantic import BaseModel


class DetailsRecordModel(BaseModel):
    name: str
    sort_key: str
    breed: str
    dob: float
    gender: str
    colour: str
    microchip_number: int


class MedicationRecordModel(BaseModel):
    name: str
    sort_key: str
    date_time: float
    medicine_name: str
    medicine_type: str
    next_due: float


class IllnessRecordModel(BaseModel):
    name: str
    sort_key: str
    date_time: float
    ailment: str
    description: str


class ObservationRecordModel(BaseModel):
    name: str
    sort_key: str
    date_time: float
    description: str


class AppointmentRecordModel(BaseModel):
    name: str
    sort_key: str
    date_time: float
    description: str
