from support.logger import get_full_logger


logger = get_full_logger()


def weekly_reminder(*args, **kwargs):
    logger.info("Hello!")


if __name__ =="__main__":
    print("fuck...")