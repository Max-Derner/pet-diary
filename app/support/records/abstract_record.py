from typing import Dict, Union
from pydantic import ValidationError, BaseModel
from app.support.logger import get_full_logger


logger = get_full_logger()


class AbstractRecordFactory():
    model: BaseModel

    def __init__(self):
        # You should assign self.model here
        # Models can be found in the pet_table_models.py file
        raise NotImplementedError()

    def produce_record(self) -> Dict:
        raise NotImplementedError()

    def _extra_record_validation(self, record: Dict) -> bool:
        """
        Use this function to perform additional validation on your model.
        It is always called by validate_record, and as default, does nothing.
        """
        return True

    def validate_record(self, record: Dict) -> bool:
        logger.info(f"Received request to validate the record: {record}")
        logger.info("Validating record, stage 1/2")
        try:
            self.model.model_validate(
                obj=record,
                strict=True
                )
        except ValidationError as e:
            logger.warning("Record failed validation")
            logger.warning(str(e))
            return False
        logger.info("Validating record, stage 2/2")
        if self._extra_record_validation(record=record):
            logger.info("Record successfully validated")
            return True
        else:
            logger.warning("Record failed validation")
            return False

    def coerce_record_to_valid_state(self, record: Dict) -> Union[None, Dict]:
        """Returns None if record cannot be coerced into valid state,
        else returns newly valid record"""
        logger.info(f"Received request to coerce record: {record}")
        logger.info("Attempting coercion")
        try:
            coerced = self.model.model_validate(
                obj=record,
                strict=False
                )
        except ValidationError as e:
            logger.warning("Record coercion failed")
            logger.warning(str(e))
            return None
        logger.info("Coercion successful")
        return coerced.model_dump()
