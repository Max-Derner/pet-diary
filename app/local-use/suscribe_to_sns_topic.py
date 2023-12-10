from support.common.aws_resources import get_weekly_reminder_topic


def subscribe_to_weekly_reminder_topic(email_address: str):
    weekly_reminder_topic = get_weekly_reminder_topic()
    weekly_reminder_topic.subscribe(
        Protocol='email',
        Endpoint=email_address
    )


if __name__ == "__main__":
    print("So you want to subscribe an email address to the weekly reminder topic.")
    email_address = input("Enter email address now and press enter, or enter nothing to skip. ")
    if email_address == '':
        print("Very well, you have chosen to skip this for now")
    else:
        subscribe_to_weekly_reminder_topic(email_address=email_address)
        print("Good, you have submitted a subscription request.")
        print("You will need to confirm that subscription before you start getting notifications.")
