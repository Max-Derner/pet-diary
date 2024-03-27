import json
from datetime import timedelta

from support.common.logger import get_full_logger
from support.common.misc import DynamoItemJSONEncoder
from support.notifications import (
    publish_to_weekly_reminder_topic,
    format_reminder_email
)
from support.find_reminders import find_reminders


logger = get_full_logger()


def lambda_weekly_reminder(*args, **kwargs):
    timespan = timedelta(weeks=2)
    records_to_remind = find_reminders(timespan=timespan)
    logger.info("Forming weekly reminder email")
    subject, message = format_reminder_email(
        records=records_to_remind,
        timespan=timespan
    )

    logger.info("Sending email")
    publish_to_weekly_reminder_topic(
        subject=subject,
        message=message
    )

    message_lines = message.split('\n')
    spreadable_message = {f"line#{idx + 1}": line for idx, line in enumerate(message_lines)}

    return {
        'statusCode': 200,
        'body': json.dumps(
            obj={
                'subject': subject,
                **spreadable_message
            },
            cls=DynamoItemJSONEncoder
        )
    }
