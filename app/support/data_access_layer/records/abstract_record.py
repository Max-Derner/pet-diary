from pydantic import ValidationError, BaseModel

from app.support.common.logger import get_full_logger


logger = get_full_logger()


class AbstractRecordFactory():
    model: BaseModel

    def __init__(self):
        # You should assign self.model here
        # Models can be found in the pet_table_models.py file
        raise NotImplementedError()

    def produce_record(self) -> dict:
        raise NotImplementedError()

    def validate_record(self, record: dict) -> bool:
        logger.info(f"Received request to validate the record: {record}")
        try:
            self.model.model_validate(
                obj=record,
                strict=True
                )
            logger.info("Record valid")
            return True
        except ValidationError as e:
            logger.warning("Record failed validation")
            logger.warning(str(e))
            return False

    def coerce_record_to_valid_state(self, record: dict) -> None | dict:
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
