from typing import Dict, Optional, Union
from app.supporting_cast.record_skeletons.abstract_record import AbstractRecordFactory  # noqa: E501
from app.supporting_cast.record_skeletons.pet_table_models import MedicationRecordModel  # noqa: E501
from app.supporting_cast.misc import utc_timestamp_now
from datetime import datetime


class MedicationRecordFactory(AbstractRecordFactory):
    model: MedicationRecordModel

    def __init__(self):
        self.model = MedicationRecordModel

    def produce_record(
            self,
            name: str,
            date_prescribed: datetime,
            name_of_medicine: str,
            type_of_medicine: str,
            next_due: Optional[datetime],
            sort_key_timestamp: Optional[int] = None
    ) -> Dict[str, Union[str, float]]:
        if sort_key_timestamp is None:
            sort_key = f"medication#{type_of_medicine}#{utc_timestamp_now()}"
        else:
            sort_key = f"medication#{type_of_medicine}#{sort_key_timestamp}"
        medicine_record = {
            "name": name,
            "sort_key": sort_key,
            "date_time": date_prescribed.timestamp(),
            "medicine_name": name_of_medicine,
            "medicine_type": type_of_medicine,
            "next_due": next_due.timestamp() if next_due is not None else None
        }
        return medicine_record

    def _convert_model_to_record(self, model: MedicationRecordModel):
        return self.produce_record(
            name=model.name,
            sort_key_timestamp=float(model.sort_key.split('#')[-1]),
            date_prescribed=datetime.fromtimestamp(model.date_time),
            type_of_medicine=model.medicine_type,
            name_of_medicine=model.medicine_name,
            next_due=datetime.fromtimestamp(model.next_due) if model.next_due is not None else None  # noqa: E501
        )
