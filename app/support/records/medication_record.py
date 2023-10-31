from typing import Dict, Optional, Union
from app.support.records.abstract_record import AbstractRecordFactory
from app.support.records.pet_table_models import (
    MedicationRecordModel,
    RecordType
)
from app.support.misc import utc_timestamp_now
from datetime import datetime, timezone
from decimal import Decimal


class MedicationRecordFactory(AbstractRecordFactory):
    model: MedicationRecordModel

    def __init__(self):
        self.model = MedicationRecordModel

    def produce_record(
            self,
            pet_name: str,
            time_of_administration: datetime,
            name_of_medicine: str,
            type_of_medicine: str,
            next_due: Optional[datetime]
    ) -> Dict[str, Union[str, Decimal, bool]]:
        sort_key = f"{RecordType.MEDICATION.value}#{type_of_medicine}#{utc_timestamp_now()}"  # noqa: E501
        medicine_record = {
            "name": pet_name,
            "sort_key": sort_key,
            "date_time": Decimal(time_of_administration.astimezone(tz=timezone.utc).timestamp()),  # noqa: E501
            "medicine_name": name_of_medicine,
            "medicine_type": type_of_medicine,
            "repeat": True if next_due is not None else False
        }
        if next_due is not None:
            medicine_record['next_due'] = Decimal(next_due.timestamp())
        return medicine_record

    def _extra_record_validation(self, record: Dict) -> bool:
        valid = True
        if (repeat := record.get('repeat')) is None:
            valid = False
        if repeat and record.get('next_due') is None:
            # Record must have next_due attribute if repeat is True
            valid = False
        return valid
