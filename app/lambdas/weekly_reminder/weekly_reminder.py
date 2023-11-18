from app.support.logger import get_full_logger
import json


logger = get_full_logger()


def weekly_reminder(*args, **kwargs):
    logger.info("Hello!")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


if __name__ == "__main__":
    weekly_reminder()
