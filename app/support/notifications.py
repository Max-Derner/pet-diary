from typing import Any, Optional
from datetime import timedelta

from support.common.aws_resources import (
    get_weekly_reminder_topic,
    get_daily_reminder_topic
)
from support.common.logger import get_full_logger
from support.record_formatting import RecordFormatter, RecordStyle
from support.common.misc import current_date


logger = get_full_logger()


def publish_to_weekly_reminder_topic(subject: str, message: str):
    topic = get_weekly_reminder_topic()
    _publish_to_topic(
        topic=topic,
        subject=subject,
        message=message
    )


def publish_to_daily_reminder_topic(message: str):
    topic = get_daily_reminder_topic()
    _publish_to_topic(
        topic=topic,
        message=message
    )


def _publish_to_topic(topic: Any, message: str, subject: Optional[str] = None):
    logger.info(f"Publishing message to sns topic: {topic.attributes['DisplayName']}")
    publish_kwargs = {'Message': message}
    if subject is not None:
        publish_kwargs['Subject'] = subject
    response = topic.publish(**publish_kwargs)
    logger.debug(f"RESPONSE: {response}")
    logger.info("Success")


message_sign_off = """

We wish you and your pets all the best,
Pet Health Diary (part of Derner Industries)
"""


def format_reminder_email(records: list[dict], timespan: timedelta) -> tuple[str, str]:
    """
    returns -> (subject, message)
    """
    subject = f"Your Pet Health Diary weekly reminder for {timespan.days} days, from {current_date()}"

    message = """
Hello,
    These are your reminders for this period:

"""
    if len(records) == 0:
        reminders = 'There are no reminders for this period.'
    else:
        rf = RecordFormatter()
        reminders = rf.format_records(records=records)
    message += reminders
    message += message_sign_off
    return subject, message


def format_reminder_sms(records: list[dict], timespan: timedelta) -> str:
    message = f"""
Hello,
    These are your reminders for {timespan.days} days, from {current_date()}:

"""
    if len(records) == 0:
        reminders = 'There are no reminders for this period.'
    else:
        rf = RecordFormatter()
        rf.style = RecordStyle.SMS
        rf.column_width = 35
        reminders = rf.format_records(records=records)
    message += reminders
    message += message_sign_off
    return message
