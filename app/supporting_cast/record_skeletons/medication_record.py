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
            next_due: Optional[datetime]
    ) -> Dict[str, Union[str, float]]:
        sort_key = f"medication#{type_of_medicine}#{utc_timestamp_now()}"
        medicine_record = {
            "name": name,
            "sort_key": sort_key,
            "date_time": date_prescribed.timestamp(),
            "medicine_name": name_of_medicine,
            "medicine_type": type_of_medicine,
            "next_due": next_due.timestamp() if next_due is not None else None
        }
        return medicine_record
