import logging
import pytest
from os.path import abspath
from app.supporting_cast.logger import (
    _get_debug_output_formatter,
    _get_console_output_formatter,
    _get_stream_handler,
    _get_file_handler
)


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
    filename = 'some_file_name.smth'
    file_handler = _get_file_handler(level=level,
                                     filename=filename,
                                     mode=mode,
                                     formatter=formatter)
    assert isinstance(file_handler, logging.FileHandler), \
        '_get_file_handler did not return a file handler as expected'
    assert file_handler.level == level, 'level was not set correctly'
    assert file_handler.formatter == formatter
    assert file_handler.mode == mode
    assert file_handler.baseFilename == abspath(filename)
