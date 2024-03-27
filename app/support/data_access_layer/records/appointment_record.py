from datetime import datetime, timezone
from decimal import Decimal

from app.support.data_access_layer.records.abstract_record import AbstractRecordFactory
from app.support.data_access_layer.records.pet_table_models import (
    AppointmentRecordModel,
    RecordType
)
from app.support.common.misc import utc_timestamp_now


class AppointmentRecordFactory(AbstractRecordFactory):
    model: AppointmentRecordModel

    def __init__(self):
        self.model = AppointmentRecordModel

    def produce_record(
            self,
            pet_name: str,
            appointment_time: datetime,
            description: str
            ) -> dict[str, str | Decimal]:
        sort_key = f"{RecordType.APPOINTMENT.value}#{utc_timestamp_now()}"
        illness_record = {
            "name": pet_name,
            "sort_key": sort_key,
            "date_time": Decimal(appointment_time.astimezone(tz=timezone.utc).timestamp()),
            "description": description,
            'record_type': RecordType.APPOINTMENT.value
        }
        return illness_record
