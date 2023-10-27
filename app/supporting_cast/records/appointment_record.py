from app.supporting_cast.records.pet_table_models import (
    AppointmentRecordModel
)
from app.supporting_cast.records.abstract_record import (
    AbstractRecordFactory
)
from datetime import datetime
from typing import Dict, Optional, Union
from decimal import Decimal
from supporting_cast.misc import utc_timestamp_now


class AppointmentRecordFactory(AbstractRecordFactory):
    model: AppointmentRecordModel

    def __init__(self):
        self.model = AppointmentRecordModel

    def produce_record(
            self,
            name: str,
            date_time: datetime,
            description: str
            ) -> Dict[str, Union[str, Decimal]]:
        sort_key = f"appointment#{utc_timestamp_now()}"
        illness_record = {
            "name": name,
            "sort_key": sort_key,
            "date_time": Decimal(date_time.timestamp()),
            "description": description
        }
        return illness_record
