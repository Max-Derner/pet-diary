import json

from support.common.logger import get_full_logger
from support.common.misc import DynamoItemJSONEncoder


logger = get_full_logger()


def lambda_api(*args, **kwargs):
    logger.info("I am logger!")
    logger.info(f"args: {args}")
    logger.info(f"kwargs: {kwargs}")

    return {
        'statusCode': 200,
        'body': json.dumps(
            obj={
                'records': 'hi',
                'args': args,
                'kwargs': kwargs,
            },
            cls=DynamoItemJSONEncoder
        )
    }
