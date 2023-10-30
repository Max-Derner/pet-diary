from app.support.records.pet_table_models import AppointmentRecordModel
from app.support.records.abstract_record import AbstractRecordFactory
from datetime import datetime
from typing import Dict, Union
from decimal import Decimal
from support.misc import utc_timestamp_now


class AppointmentRecordFactory(AbstractRecordFactory):
    model: AppointmentRecordModel

    def __init__(self):
        self.model = AppointmentRecordModel

    def produce_record(
            self,
            pet_name: str,
            appointment_time: datetime,
            description: str
            ) -> Dict[str, Union[str, Decimal]]:
        sort_key = f"appointment#{utc_timestamp_now()}"
        illness_record = {
            "name": pet_name,
            "sort_key": sort_key,
            "date_time": Decimal(appointment_time.timestamp()),
            "description": description
        }
        return illness_record
