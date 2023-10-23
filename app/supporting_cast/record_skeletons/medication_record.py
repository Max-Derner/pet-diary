from typing import Dict, Optional, Union
from app.supporting_cast.record_skeletons.abstract_record import AbstractRecordFactory  # noqa: E501
from app.supporting_cast.record_skeletons.pet_table_models import MedicationRecordModel  # noqa: E501
from app.supporting_cast.misc import utc_timestamp_now
from datetime import datetime
from decimal import Decimal


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
    ) -> Dict[str, Union[str, Decimal, bool]]:
        sort_key = f"medication#{type_of_medicine}#{utc_timestamp_now()}"
        medicine_record = {
            "name": name,
            "sort_key": sort_key,
            "date_time": Decimal(date_prescribed.timestamp()),
            "medicine_name": name_of_medicine,
            "medicine_type": type_of_medicine,
            "repeat": True if next_due is not None else False
        }
        if next_due is not None:
            medicine_record['next_due'] = Decimal(next_due.timestamp())
        return medicine_record