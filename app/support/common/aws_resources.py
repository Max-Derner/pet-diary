from boto3 import resource

from support.common.logger import get_full_logger


logger = get_full_logger()


def get_pet_table_resource():
    """
    returns DynamoDB table resource pointed at the table 'pet_table'
    available methods can be found at:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html
    You can get the client through <resource>.meta.client
    which then allows use of the following:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
    """

    dynamo = resource('dynamodb')
    pet_table = dynamo.Table('pet_table')
    return pet_table


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
