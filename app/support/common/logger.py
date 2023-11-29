import logging
import os
from typing import List, Union
from .misc import ensure_directories_present


# If you've come here for answers on how all this works,
# let me point you to these docs:
# https://docs.python.org/3/library/logging.html
# https://docs.python.org/3/howto/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook
# https://docs.python.org/3/library/logging.html#logrecord-attributes


"""
              -~- -~- -~- Logging levels explained: -~- -~- -~-
+-----------+-----------------------------------------------------------------+
¦ DEBUG     ¦    Detailed information, typically of interest only when        ¦
¦           ¦    diagnosing problems.                                         ¦
+-----------+-----------------------------------------------------------------+
¦ INFO      ¦    Confirmation that things are working as expected.            ¦
+-----------+-----------------------------------------------------------------+
¦ WARNING   ¦    An indication that something unexpected happened, or         ¦
¦           ¦    indicative of some problem in the near future                ¦
¦           ¦    (e.g. 'disk space low').                                     ¦
¦           ¦    The software is still working as expected.                   ¦
+-----------+-----------------------------------------------------------------+
¦ ERROR     ¦    Due to a more serious problem, the software has not been     ¦
¦           ¦    able to perform some function.                               ¦
+-----------+-----------------------------------------------------------------+
¦ CRITICAL  ¦    A serious error, indicating that the program itself may be   ¦
¦           ¦    unable to continue running.                                  ¦
+-----------+-----------------------------------------------------------------+
"""

_ROOT_FILE_NAME = 'pet-diary'
_ROOT_DIR_PATH = os.path.dirname(os.path.abspath(_ROOT_FILE_NAME))
_ARTEFACTS_DIR = "logging_output"

_FILE_NAME_FOR_CONSOLE_OUTPUT = 'console_output.log'
_RELATIVE_CONSOLE_OUTPUT_FILE_PATH = f'{_ARTEFACTS_DIR}/{_FILE_NAME_FOR_CONSOLE_OUTPUT}'
_FULL_CONSOLE_OUTPUT_FILE_PATH = f'{_ROOT_DIR_PATH}/{_RELATIVE_CONSOLE_OUTPUT_FILE_PATH}'

_FILE_NAME_FOR_DEBUG_OUTPUT = 'debug_output.log'
_RELATIVE_DEBUG_OUTPUT_FILE_PATH = f'{_ARTEFACTS_DIR}/{_FILE_NAME_FOR_DEBUG_OUTPUT}'
_FULL_DEBUG_OUTPUT_FILE_PATH = f'{_ROOT_DIR_PATH}/{_RELATIVE_DEBUG_OUTPUT_FILE_PATH}'

_CONSOLE_LOG_LEVEL = logging.INFO
_DEBUG_FILE_LOG_LEVEL = logging.DEBUG

handlers: List[logging.Handler]

config_message = 'logger configured:\n'
config_message += 'logging will go to 2 output files\n'
config_message += 'console output - '.ljust(18) + f'{_FULL_CONSOLE_OUTPUT_FILE_PATH}\n'
config_message += 'debug output - '.ljust(18) + f'{_FULL_DEBUG_OUTPUT_FILE_PATH}\n'


def _get_debug_output_formatter() -> logging.Formatter:
    debug_file_format = '%(levelname)s '
    debug_file_format += 'from '
    debug_file_format += 'function "%(funcName)s" '
    debug_file_format += 'in "%(pathname)s", '
    debug_file_format += 'line %(lineno)s '
    debug_file_format += 'at %(asctime)s '
    debug_file_format += '\n%(message)s\n'
    return logging.Formatter(fmt=debug_file_format)


def _get_console_output_formatter() -> logging.Formatter:
    console_format = '%(message)s'
    return logging.Formatter(fmt=console_format)


def _get_stream_handler(
        level: int,
        formatter: logging.Formatter
        ) -> logging.StreamHandler:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level=level)
    stream_handler.setFormatter(fmt=formatter)
    return stream_handler


def _get_file_handler(
        level: int,
        filename: str,
        mode: str,
        formatter: logging.Formatter
        ) -> logging.FileHandler:
    file_handler = logging.FileHandler(filename=filename, mode=mode)
    file_handler.setLevel(level=level)
    file_handler.setFormatter(fmt=formatter)
    return file_handler


def _get_handlers(create_console_stream_handler: bool = True,
                  create_console_file_handler: bool = True,
                  create_debug_file_handler: bool = True
                  ) -> List[Union[None, logging.Handler]]:
    console_stream_handler, console_file_handler, debug_file_handler = None, None, None
    if create_console_stream_handler or create_console_file_handler:
        console_output_formatter = _get_console_output_formatter()
        if create_console_stream_handler:
            console_stream_handler = _get_stream_handler(
                level=_CONSOLE_LOG_LEVEL,
                formatter=console_output_formatter
                )
        if create_console_file_handler:
            console_file_handler = _get_file_handler(
                level=_CONSOLE_LOG_LEVEL,
                filename=_FULL_CONSOLE_OUTPUT_FILE_PATH,
                mode='w',
                formatter=console_output_formatter
                )
    if create_debug_file_handler:
        debug_output_formatter = _get_debug_output_formatter()
        debug_file_handler = _get_file_handler(
            level=_DEBUG_FILE_LOG_LEVEL,
            filename=_FULL_DEBUG_OUTPUT_FILE_PATH,
            mode='w',
            formatter=debug_output_formatter
            )

    return [console_stream_handler, console_file_handler, debug_file_handler]


def _add_handlers(
        handlers: Union[
            None,
            List[logging.FileHandler],
            List[logging.StreamHandler]
            ],
        logger: logging.Logger
        ):
    for handler in handlers:
        if handler is not None:
            logger.addHandler(handler)


def _set_up_logger(logger: logging.Logger,
                   create_console_stream_handler: bool = True,
                   create_console_file_handler: bool = True,
                   create_debug_file_handler: bool = True,
                   give_init_message: bool = True
                   ):
    output_directories = get_output_directories()
    ensure_directories_present(directories=output_directories)
    handlers = _get_handlers(
        create_console_stream_handler=create_console_stream_handler,
        create_console_file_handler=create_console_file_handler,
        create_debug_file_handler=create_debug_file_handler
        )
    _add_handlers(logger=logger, handlers=handlers)
    if give_init_message:
        logger.info(config_message)


def get_output_directories() -> List[str]:
    return_list = []
    output_files = [
        _RELATIVE_CONSOLE_OUTPUT_FILE_PATH,
        _RELATIVE_DEBUG_OUTPUT_FILE_PATH
        ]
    for output_file in output_files:
        directory = os.path.dirname(output_file)
        return_list.append(directory)
    return return_list


def get_full_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger('full_logger')
    logger.setLevel(level=logging.DEBUG)
    if not logger.hasHandlers():
        _set_up_logger(
            logger=logger,
            create_console_stream_handler=True,
            create_console_file_handler=True,
            create_debug_file_handler=True,
            give_init_message=True
        )
    return logger


def get_partial_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger('partial_logger')
    logger.setLevel(level=logging.DEBUG)
    if not logger.hasHandlers():
        _set_up_logger(
            logger=logger,
            create_console_stream_handler=True,
            create_console_file_handler=False,
            create_debug_file_handler=False,
            give_init_message=False
        )
    return logger
