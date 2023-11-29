import json
from datetime import timedelta

from support.record_formatting import record_formatter
from support.common.logger import get_full_logger
from support.common.misc import utc_datetime_now
from support.data_access_layer.get_records import (
    get_all_records_of_medicine_in_next_due_timeframe,
    get_all_records_of_appointment_in_timeframe
)
from support.common.misc import DynamoItemJSONEncoder


logger = get_full_logger()


def lambda_weekly_reminder(*args, **kwargs):
    today = utc_datetime_now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    reminder_limit = today + timedelta(weeks=2)
    logger.info(f"Finding appointments and medicine due in the next two weeks: {today} to {reminder_limit}")  # noqa: E501

    appointments_to_remind = get_all_records_of_appointment_in_timeframe(
        lower_date_limit=today,
        upper_date_limit=reminder_limit
    )
    appointment_string = record_formatter(appointments_to_remind)  # noqa: F841
    logger.info(f"Found {len(appointments_to_remind)} appointments")  # noqa: E501

    medicines_to_remind = get_all_records_of_medicine_in_next_due_timeframe(
        lower_date_limit=today,
        upper_date_limit=reminder_limit
    )
    medicines_string = record_formatter(medicines_to_remind)  # noqa: F841
    logger.info(f"Found {len(medicines_to_remind)} medicines")  # noqa: E501

    return {
        'statusCode': 200,
        'body': json.dumps(
            obj={
                'appointments': appointments_to_remind,
                'medicines': medicines_to_remind
            },
            cls=DynamoItemJSONEncoder
        )
    }
