from support.common.aws_resources import (
    get_weekly_reminder_topic,
    get_daily_reminder_topic
)


def subscribe_to_weekly_reminder_topic(email_address: str):
    weekly_reminder_topic = get_weekly_reminder_topic()
    weekly_reminder_topic.subscribe(
        Protocol='email',
        Endpoint=email_address
    )


def subscribe_to_daily_reminder_topic(phone_number: str):
    weekly_reminder_topic = get_daily_reminder_topic()
    response = weekly_reminder_topic.subscribe(
        Protocol='sms',
        Endpoint=phone_number
    )
    return response


def _user_input_subscribe_to_weekly_reminder():
    print("So you want to subscribe an email address to the weekly reminder topic.")
    email_address = input("Enter email address now and press enter, or enter nothing to skip. ")
    if email_address == '':
        print("Very well, you have chosen to skip this for now")
    else:
        subscribe_to_weekly_reminder_topic(email_address=email_address)
        print("Good, you have submitted a subscription.")
        print("You will need to confirm that subscription before you start getting notifications.")


def _user_input_subscribe_to_daily_reminder():
    print("So you want to subscribe an phone number to the daily reminder topic.")
    phone_number = input("Enter phone number now and press enter, or enter nothing to skip. ")
    if phone_number == '':
        print("Very well, you have chosen to skip this for now")
    else:
        subscribe_to_daily_reminder_topic(phone_number=phone_number)
        print("Good, you have submitted a subscription.")


if __name__ == "__main__":
    user_input = input("What are we subscribing to?\n\t1: Weekly reminder\n\t2: Daily reminder\n Enter '1' or '2': ")
    print(f"user inpur is {user_input}")
    if user_input == '1':
        _user_input_subscribe_to_weekly_reminder()
    elif user_input == '2':
        _user_input_subscribe_to_daily_reminder()
    else:
        print("You've stuffed that right up.\nYou only needed to enter a number.")
