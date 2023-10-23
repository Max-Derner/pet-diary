from app.supporting_cast.record_skeletons.pet_table_models import AppointmentRecordModel  # noqa: E501
from app.supporting_cast.record_skeletons.abstract_record import AbstractRecordFactory  # noqa: E501
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
            description: str,
            sort_key_timestamp: Optional[float] = None
            ) -> Dict[str, Union[str, Decimal]]:
        if sort_key_timestamp is None:
            sort_key = f"appointment#{utc_timestamp_now()}"
        else:
            sort_key = f"appointment#{sort_key_timestamp}"
        illness_record = {
            "name": name,
            "sort_key": sort_key,
            "date_time": Decimal(date_time.timestamp()),
            "description": description
        }
        return illness_record
