from typing import Dict, Union
from pydantic import ValidationError, BaseModel


class AbstractRecordFactory():
    model: BaseModel

    def __init__(self):
        # You should assign self.model here
        # Models can be found in the pet_table_models.py file
        raise NotImplementedError()

    def produce_record(self) -> Dict:
        raise NotImplementedError()

    def _convert_model_to_record(self) -> Dict:
        raise NotImplementedError()

    def validate_record(self, record: Dict) -> bool:
        try:
            self.model.model_validate(
                obj=record,
                strict=True
                )
        except ValidationError:
            return False
        return True

    def coerce_record_to_valid_state(self, record: Dict) -> Union[None, Dict]:
        """Returns None if record cannot be coerced into valid state,
        else returns newly valid record"""
        try:
            coerced = self.model.model_validate(
                obj=record,
                strict=False
                )
        except ValidationError:
            return None
        return self._convert_model_to_record(model=coerced)
