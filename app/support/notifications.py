from typing import List, Dict, Tuple
from datetime import timedelta

from boto3 import resource

from support.common.logger import get_full_logger
from support.record_formatting import record_formatter, DIVIDER
from support.common.misc import current_date


logger = get_full_logger()


def get_weekly_reminder_topic():
    """
    return sns Topic PD_Weekly_Reminder
    available methods can be found at:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/topic/index.html
    """
    # Client ----> https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html
    # Resource --> https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/service-resource/index.html
    # Topic  ----> https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/topic/index.html

    desired_topic_display_name = 'PD_Weekly_Reminder'
    logger.info(f"Acquiring {desired_topic_display_name} topic")
    sns = resource('sns')
    topic_collection = sns.topics.all()
    logger.info(f"Found {len(list(topic_collection))} topics, narrowing down")

    for topic in topic_collection:
        if topic.attributes['DisplayName'] == desired_topic_display_name:
            logger.info(f"Found {desired_topic_display_name} topic")
            return topic
    raise ValueError(f"The topic {desired_topic_display_name} could not be found")


def publish_to_weekly_reminder_topic(subject: str, message: str):
    topic = get_weekly_reminder_topic()
    logger.info(f"Publishing message to sns topic: {topic.attributes['DisplayName']}")
    response = topic.publish(
        Subject=subject,
        Message=message,
    )
    logger.debug(f"RESPONSE: {response}")
    logger.info("Success")


def format_reminder_email(records: List[Dict], timespan: timedelta) -> Tuple[str, str]:
    """
    returns -> (subject, message)
    """
    subject = f"Your Pet Health Diary weekly reminder for {timespan.days} days, from {current_date()}"

    if len(records) == 0:
        reminders = 'There are no reminders for this period.'
    else:
        reminders = record_formatter(records)
        reminders += DIVIDER

    message = """
Hello,
    These are your reminders for this period:

"""
    message += reminders

    message += """

We wish you and your pets all the best,
Pet Health Diary (part of Derner Industries)
"""

    return subject, message
