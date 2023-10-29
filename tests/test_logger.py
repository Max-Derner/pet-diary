import logging
import pytest
from os.path import abspath
from app.support.logger import (
    _ARTEFACTS_DIR,
    _ROOT_DIR_PATH,
    _get_debug_output_formatter,
    _get_console_output_formatter,
    _get_stream_handler,
    _get_file_handler,
    get_output_directories,
    get_partial_logger,
    get_full_logger
)
from support.file_interactors import ensure_directories_present


def tests_get_debug_output_formatter():
    formatter = _get_debug_output_formatter()
    assert isinstance(formatter, logging.Formatter), \
        'debug output formatter is not a formatter as expected'


def tests_get_console_output_formatter():
    formatter = _get_console_output_formatter()
    assert isinstance(formatter, logging.Formatter), \
        'console output formatter is not a formatter as expected'


@pytest.mark.parametrize('level', [logging.DEBUG,
                                   logging.INFO,
                                   logging.WARNING,
                                   logging.ERROR,
                                   logging.CRITICAL])
def tests_get_stream_handler(level):
    formatter = logging.Formatter()
    stream_handler = _get_stream_handler(level=level, formatter=formatter)
    assert isinstance(stream_handler, logging.StreamHandler), \
        '_get_stream_handler did not return a stream handler as expected'
    assert stream_handler.level == level, 'level was not set correctly'
    assert stream_handler.formatter == formatter


@pytest.mark.parametrize('level, mode', [(logging.DEBUG, 'w'),
                                         (logging.INFO, 'a'),
                                         (logging.WARNING, 'a'),
                                         (logging.ERROR, 'w'),
                                         (logging.CRITICAL, 'w')])
def tests_get_file_handler(level, mode):
    formatter = logging.Formatter()
    _FILE_NAME_FOR_TESTING = 'some_test_file.smth'
    _RELATIVE_CONSOLE_OUTPUT_FILE_PATH = f'{_ARTEFACTS_DIR}/{_FILE_NAME_FOR_TESTING}'  # noqa: E501
    _FULL_CONSOLE_OUTPUT_FILE_PATH = f'{_ROOT_DIR_PATH}/{_RELATIVE_CONSOLE_OUTPUT_FILE_PATH}'  # noqa: E501
    output_directories = get_output_directories()
    ensure_directories_present(directories=output_directories)
    file_handler = _get_file_handler(level=level,
                                     filename=_FULL_CONSOLE_OUTPUT_FILE_PATH,
                                     mode=mode,
                                     formatter=formatter)
    assert isinstance(file_handler, logging.FileHandler), \
        '_get_file_handler did not return a file handler as expected'
    assert file_handler.level == level, 'level was not set correctly'
    assert file_handler.formatter == formatter
    assert file_handler.mode == mode
    assert file_handler.baseFilename == abspath(_FULL_CONSOLE_OUTPUT_FILE_PATH)


def tests_get_partial_logger():
    logger = get_partial_logger()
    assert isinstance(logger, logging.Logger)


def tests_get_full_logger():
    logger = get_full_logger()
    assert isinstance(logger, logging.Logger)
