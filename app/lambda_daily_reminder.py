import json
from datetime import timedelta

from support.common.logger import get_full_logger
from support.common.misc import DynamoItemJSONEncoder
from support.notifications import (
    publish_to_daily_reminder_topic,
    format_reminder_sms
)
from support.find_reminders import find_reminders


logger = get_full_logger()


def lambda_daily_reminder(*args, **kwargs):
    timespan = timedelta(days=1)
    records_to_remind = find_reminders(timespan=timespan)
    if len(records_to_remind) > 0:
        logger.info("Forming daily reminder sms")
        message = format_reminder_sms(
            records=records_to_remind,
            timespan=timespan
        )

        logger.info("Sending sms")
        publish_to_daily_reminder_topic(
            message=message
        )

    return {
        'statusCode': 200,
        'body': json.dumps(
            obj={
                'records': records_to_remind
            },
            cls=DynamoItemJSONEncoder
        )
    }
