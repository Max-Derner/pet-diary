from typing import Dict, List
from datetime import datetime

from app.support.common.logger import get_full_logger
from app.support.data_access_layer.get_records import (
    get_all_of_pets_records,
    get_all_of_pets_record_type,
    get_all_records_of_appointment_in_timeframe,
    get_all_records_of_medicine_in_next_due_timeframe
)
from app.support.data_access_layer.records.pet_table_models import RecordType
from app.support.record_formatting import record_formatter

logger = get_full_logger()


def user_driven_get_all_of_pets_records() -> List[Dict]:
    logger.info("Please enter the name of the pet whose records you wish to see:")
    pet_name = input()
    logger.info(f"You entered '{pet_name}'")
    records = get_all_of_pets_records(pet_name=pet_name)
    return records


def user_driven_get_all_of_pets_record_type() -> List[Dict]:
    logger.info("Please enter the name of the pet whose records you wish to see:")
    pet_name = input()
    logger.info(f"You entered '{pet_name}'")
    logger.info("Please choose the record type you wish to see:")
    choices = []
    for idx, rec_type in enumerate(RecordType):
        logger.info(f"{idx} -> {rec_type.value}")
        choices.append(rec_type)
    chosen_idx = int(input("Selection: "))
    logger.info(f"You chose '{choices[chosen_idx]}'")
    records = get_all_of_pets_record_type(
        pet_name=pet_name,
        record_type=choices[chosen_idx]
    )
    return records


def upcoming_records_after_point_in_time(point_in_time: datetime) -> List[Dict]:
    records = []
    records.extend(
        get_all_records_of_appointment_in_timeframe(
            lower_date_limit=point_in_time,
            upper_date_limit=None
        )
    )
    records.extend(
        get_all_records_of_medicine_in_next_due_timeframe(
            lower_date_limit=point_in_time,
            upper_date_limit=None
        )
    )
    return records


def upcoming_records() -> List[Dict]:
    return upcoming_records_after_point_in_time(
        point_in_time=datetime.now()
    )


def user_driven_upcoming_records_after_point_in_time() -> List[Dict]:
    logger.info("Please enter a year: ")
    year = int(input())
    logger.info("Please enter a month: ")
    month = int(input())
    logger.info("Please enter a day: ")
    day = int(input())
    point_in_time = datetime(
        year=year,
        month=month,
        day=day
    )
    logger.info(f"You have given the date: {datetime.date(point_in_time)}")
    return upcoming_records_after_point_in_time(
        point_in_time=point_in_time
    )


def main():
    logger.info("Make selection:")
    logger.info("1 -> All of a pets records")
    logger.info("2 -> Records of certain type, for particular pet, after point in time.")
    logger.info("3 -> Anything upcoming")
    logger.info("4 -> Anything in time frame")
    choice = input("Selection: ")
    logger.info(f"You chose '{choice}'")
    if choice == '1':
        records = user_driven_get_all_of_pets_records()
    elif choice == '2':
        records = user_driven_get_all_of_pets_record_type()
    elif choice == '3':
        records = upcoming_records()
    elif choice == '4':
        records = user_driven_upcoming_records_after_point_in_time()
    else:
        logger.info("Invalid choice!")
        exit(1)
    logger.info(record_formatter(records=records))


if __name__ == "__main__":
    main()
