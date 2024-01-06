from support.common.aws_resources import (
    get_weekly_reminder_topic,
    get_daily_reminder_topic,
    get_sns_client
)
from app.support.common.logger import get_full_logger

logger = get_full_logger()


def subscribe_to_weekly_reminder_topic(email_address: str):
    weekly_reminder_topic = get_weekly_reminder_topic()
    response = weekly_reminder_topic.subscribe(
        Protocol='email',
        Endpoint=email_address
    )
    return response


def subscribe_phone_number_to_daily_reminder(phone_number: str):
    """
    phone_number must include country code e.g. +4407852468055"""
    sns_client = get_sns_client()

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/create_sms_sandbox_phone_number.html
    sns_client.create_sms_sandbox_phone_number(
        PhoneNumber=phone_number,
        LanguageCode='en-GB'
    )

    otp = input("Enter OTP: ")

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/verify_sms_sandbox_phone_number.html
    sns_client.verify_sms_sandbox_phone_number(
        PhoneNumber=phone_number,
        OneTimePassword=otp
    )

    daily_reminder_topic = get_daily_reminder_topic()

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/subscribe.html
    sns_client.subscribe(
        TopicArn=daily_reminder_topic.arn,
        Protocol='sms',
        Endpoint=phone_number  # phone number
    )

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/list_sms_sandbox_phone_numbers.html
    logger.debug(sns_client.list_sms_sandbox_phone_numbers())


def _user_input_subscribe_to_weekly_reminder():
    logger.info("So you want to subscribe an email address to the weekly reminder topic.")
    email_address = input("Enter email address now and press enter, or enter nothing to skip. ")
    if email_address == '':
        logger.info("Very well, you have chosen to skip this for now")
    else:
        subscribe_to_weekly_reminder_topic(email_address=email_address)


def _user_input_subscribe_to_daily_reminder():
    logger.info("So you want to subscribe a phone number to the daily reminder topic.")
    logger.info("N.B. Be sure to enter the national code as well! e.g. +4407")
    phone_number = input("Enter phone number now and press enter, or enter nothing to skip. ")
    if phone_number == '':
        logger.info("Very well, you have chosen to skip this for now")
    else:
        subscribe_phone_number_to_daily_reminder(phone_number=phone_number)
        logger.info("Good, that should have done it")


if __name__ == "__main__":
    user_input = input("What are we subscribing to?\n\t1: Weekly reminder\n\t2: Daily reminder\n Enter '1' or '2': ")
    logger.info(f"user inpur is {user_input}")
    if user_input == '1':
        _user_input_subscribe_to_weekly_reminder()
    elif user_input == '2':
        _user_input_subscribe_to_daily_reminder()
    else:
        logger.info("You've stuffed that right up.\nYou only needed to enter a number.")
