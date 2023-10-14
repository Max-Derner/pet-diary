from app.supporting_cast.record_skeletons.pet_table_models import AppointmentRecordModel  # noqa: E501
from app.supporting_cast.record_skeletons.abstract_record import AbstractRecordFactory  # noqa: E501
from datetime import datetime
from typing import Dict, Optional, Union
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
            ) -> Dict[str, Union[str, float]]:
        if sort_key_timestamp is None:
            sort_key = f"appointment#{utc_timestamp_now()}"
        else:
            sort_key = f"appointment#{sort_key_timestamp}"
        illness_record = {
            "name": name,
            "sort_key": sort_key,
            "date_time": date_time.timestamp(),
            "description": description
        }
        return illness_record

    def _convert_model_to_record(self, model: AppointmentRecordModel) -> Dict:
        return self.produce_record(
            name=model.name,
            sort_key_timestamp=float(model.sort_key.split('#')[-1]),
            date_time=datetime.fromtimestamp(model.date_time),
            description=model.description
        )
