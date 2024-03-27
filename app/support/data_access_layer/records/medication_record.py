from typing import Optional
from datetime import datetime, timezone
from decimal import Decimal

from app.support.data_access_layer.records.abstract_record import AbstractRecordFactory
from app.support.data_access_layer.records.pet_table_models import (
    MedicationRecordModel,
    RecordType
)
from app.support.common.misc import utc_timestamp_now


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
    ) -> dict[str, str | Decimal | bool]:
        sort_key = f"{RecordType.MEDICATION.value}#{type_of_medicine}#{utc_timestamp_now()}"
        if next_due is None:
            next_due_section = {
                'repeat': False
            }
        else:
            next_due_section = {
                'repeat': True,
                'next_due': Decimal(next_due.timestamp())
            }
        medicine_record = {
            "name": pet_name,
            "sort_key": sort_key,
            "date_time": Decimal(time_of_administration.astimezone(tz=timezone.utc).timestamp()),
            "medicine_name": name_of_medicine,
            "medicine_type": type_of_medicine,
            'record_type': RecordType.MEDICATION.value,
            **next_due_section
        }
        return medicine_record
