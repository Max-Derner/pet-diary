from app.supporting_cast.record_skeletons.pet_table_models import ObservationRecordModel  # noqa: E501
from app.supporting_cast.record_skeletons.abstract_record import AbstractRecordFactory  # noqa: E501
from datetime import datetime
from typing import Dict, Union
from supporting_cast.misc import utc_timestamp_now


class ObservationRecordFactory(AbstractRecordFactory):
    model: ObservationRecordModel

    def __init__(self):
        self.model = ObservationRecordModel

    def produce_record(
            self,
            name: str,
            date_time: datetime,
            description: str
            ) -> Dict[str, Union[str, float]]:
        sort_key = f"observation#{utc_timestamp_now()}"
        illness_record = {
            "name": name,
            "sort_key": sort_key,
            "date_time": date_time.timestamp(),
            "description": description
        }
        return illness_record
