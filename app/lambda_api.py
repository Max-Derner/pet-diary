import json
from datetime import datetime
from pprint import pformat

from support.record_formatting import RecordFormatter
from support.data_access_layer.records.pet_table_models import RecordType
from support.common.logger import get_full_logger
from support.common.misc import DynamoItemJSONEncoder
from support.data_access_layer.get_records import (
    get_all_of_pets_record_type,
    get_all_of_pets_record_type_after_point_in_time,
    get_all_of_pets_records
)


logger = get_full_logger()


def lambda_api(event, context):
    logger.info(f"event:\n{pformat(event)}")
    match event.get('queryStringParameters'):
        case {"name": name, "record_type": record_type, "date": date}:
            logger.info("case path 1")
            point_in_time = datetime.strptime(date, "%Y-%m-%d")
            records = get_all_of_pets_record_type_after_point_in_time(
                pet_name=name,
                record_type=record_type,
                point_in_time=point_in_time,
            )
        case {"name": name, "record_type": record_type}:
            logger.info("case path 2")
            records = get_all_of_pets_record_type(
                pet_name=name,
                record_type=record_type,
            )
        case {"name": name}:
            logger.info("case path 3")
            records = get_all_of_pets_records(
                pet_name=name,
            )
        case _:
            logger.info("case path default")
            record_type_options = " | ".join([record_type for record_type in iter(RecordType)])
            return {
                'statusCode': 400,
                'body': json.dumps(
                    obj={
                        'message': 'invalid request',
                        'query parameters': 'name, record_type, date',
                        'name format': 'str',
                        "record_type format": f'string literal: {record_type_options}',
                        "date": "YYYY-MM-DD"
                    },
                    cls=DynamoItemJSONEncoder
                )
            }
    rf = RecordFormatter()
    formatted_records = rf.format_records(records=records)
    spreadable_records = {f"line#{idx + 1}": line for idx, line in enumerate(formatted_records.split("\n"))}
    return_obj = {
        'query': str(event.get("queryStringParameters")),
        **spreadable_records,
    }

    logger.info(f"return object:\n{pformat(return_obj)}")

    return {
        'statusCode': 200,
        'body': json.dumps(
            obj=return_obj,
            cls=DynamoItemJSONEncoder,
        )
    }


# Sample lambda event
"""
{'headers': {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
             'accept-encoding': 'gzip, deflate, br',
             'accept-language': 'en-GB,en;q=0.5',
             'dnt': '1',
             'host': 'iyhgxg525fqmj2kg3ibjcunbje0etnfw.lambda-url.eu-west-2.on.aws',
             'sec-fetch-dest': 'document',
             'sec-fetch-mode': 'navigate',
             'sec-fetch-site': 'none',
             'sec-fetch-user': '?1',
             'upgrade-insecure-requests': '1',
             'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) '
                           'Gecko/20100101 Firefox/124.0',
             'x-amzn-tls-cipher-suite': 'TLS_AES_128_GCM_SHA256',
             'x-amzn-tls-version': 'TLSv1.3',
             'x-amzn-trace-id': 'Root=1-65ffe778-3c8755da5d1fe93276d67e9c',
             'x-forwarded-for': '31.205.76.4',
             'x-forwarded-port': '443',
             'x-forwarded-proto': 'https'},
 'isBase64Encoded': False,
 'queryStringParameters': {'name': 'Abbi', 'type': 'magic'},
 'rawPath': '/',
 'rawQueryString': 'name=Abbi&type=magic',
 'requestContext': {'accountId': 'anonymous',
                    'apiId': 'iyhgxg525fqmj2kg3ibjcunbje0etnfw',
                    'domainName': 'iyhgxg525fqmj2kg3ibjcunbje0etnfw.lambda-url.eu-west-2.on.aws',
                    'domainPrefix': 'iyhgxg525fqmj2kg3ibjcunbje0etnfw',
                    'http': {'method': 'GET',
                             'path': '/',
                             'protocol': 'HTTP/1.1',
                             'sourceIp': '31.205.76.4',
                             'userAgent': 'Mozilla/5.0 (X11; Ubuntu; Linux '
                                          'x86_64; rv:124.0) Gecko/20100101 '
                                          'Firefox/124.0'},
                    'requestId': 'c6193c79-dfb2-4b96-a3b4-92b64482b8e7',
                    'routeKey': '$default',
                    'stage': '$default',
                    'time': '24/Mar/2024:08:42:32 +0000',
                    'timeEpoch': 1711269752508},
 'routeKey': '$default',
 'version': '2.0'}
"""
# When making the lambda GET request with: https://iyhgxg525fqmj2kg3ibjcunbje0etnfw.lambda-url.eu-west-2.on.aws/?name=Abbi&type=magic
# We get the above response
# Sections of note are:
#  'rawQueryString': 'name=Abbi&type=magic',
#  'queryStringParameters': {'name': 'Abbi', 'type': 'magic'},
