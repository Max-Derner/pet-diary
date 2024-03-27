
from datetime import timedelta

from support.common.misc import utc_datetime_now
from support.data_access_layer.get_records import (
    get_all_records_of_medicine_in_next_due_timeframe,
    get_all_records_of_appointment_in_timeframe
)
from support.common.logger import get_full_logger


logger = get_full_logger()


def find_reminders(timespan: timedelta):
    today = utc_datetime_now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    reminder_limit = today + timespan
    logger.info(f"Finding appointments and medicine due in the next two weeks: {today} to {reminder_limit}")

    appointments_to_remind = get_all_records_of_appointment_in_timeframe(
        lower_date_limit=today,
        upper_date_limit=reminder_limit
    )
    logger.info(f"Found {len(appointments_to_remind)} appointments")

    medicines_to_remind = get_all_records_of_medicine_in_next_due_timeframe(
        lower_date_limit=today,
        upper_date_limit=reminder_limit
    )
    logger.info(f"Found {len(medicines_to_remind)} medicines")

    records_to_remind: list[dict] = []
    records_to_remind.extend(appointments_to_remind)
    records_to_remind.extend(medicines_to_remind)

    return records_to_remind
