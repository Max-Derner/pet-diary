from logging import Logger
from typing import Any

from pytest import mark

from app.support.record_formatting import (
    RecordFormatter,
    RecordStyle,
)


def test_initialisation():
    rf = RecordFormatter()

    assert isinstance(rf.log, Logger)
    assert isinstance(rf.justification, int)
    assert rf._records == []
    assert isinstance(rf.card_width, int)
    assert isinstance(rf._divider, str)
    assert isinstance(rf._style, RecordStyle)
    assert isinstance(rf.column_width, int)


@mark.parametrize('input_val, expected_to_work',
                  [
                      (12, True),
                      (1.5, False),
                      ("a good space", False),
                  ])
def test_justification_setter(input_val: Any, expected_to_work: bool):
    rf = RecordFormatter()
    old_justification = rf.justification

    rf.justification = input_val

    if expected_to_work:
        assert rf.justification == input_val
    else:
        assert rf.justification == old_justification


@mark.parametrize('input_val, expected_to_work',
                  [
                      (12, True),
                      (1.5, False),
                      ("a good space", False),
                  ])
def test_column_width_setter(input_val: Any, expected_to_work: bool):
    rf = RecordFormatter()
    old_column_width = rf.column_width

    rf.column_width = input_val

    if expected_to_work:
        assert rf.column_width == input_val
    else:
        assert rf.column_width == old_column_width


@mark.parametrize('input_val, expected_to_work',
                  [
                      (12, False),
                      (1.5, False),
                      ("a good space", False),
                      (RecordStyle.SMS, True),
                      (RecordStyle.CARD, True),
                  ])
def test_style_setter(input_val: Any, expected_to_work: bool):
    rf = RecordFormatter()
    old_style = rf.style

    rf.style = input_val

    if expected_to_work:
        assert rf.style == input_val
    else:
        assert rf.style == old_style


def test_add_records():
    bad_records = [
        1,
        'hi',
        True,
        ('c', 3),
    ]
    good_records = [
        {'a': 1},
        {'b': 2},
    ]
    more_good_records = [
        {'d': 4},
        {'e': 5}
    ]
    single_record = {'f': 6}
    input_records = []
    input_records.extend(bad_records)
    input_records.extend(good_records)
    expected_records = []
    expected_records.extend(good_records)
    expected_records.extend(more_good_records)
    expected_records.append(single_record)
    rf = RecordFormatter()

    rf.add_records(records=input_records)
    rf.add_records(records=more_good_records)
    rf.add_records(records='all those ones')
    rf.add_records(records=single_record)

    assert rf._records == expected_records


def test_format_record_line():
    rf = RecordFormatter()
    record = {'key': 'all the details and whatnot'}

    line = rf.format_record_line(
        display_name='DISPLAY NAME',
        record=record,
        key='key'
    )

    assert line == "DISPLAY NAME:       All The Details And Whatnot\n"


@mark.parametrize('style',
                  [
                      RecordStyle.CARD,
                      RecordStyle.SMS
                  ])
def tests_str_to_column(style: RecordStyle):
    long_text = 'I am a sample of text that is supposed to be big enough that it can get wrapped plus a made up word: supercaladoodadimaginariouso'
    with open("tests/formatted_column.txt", mode='r') as fileio:
        expected_text = fileio.readlines()
    if style == RecordStyle.SMS:
        expected_text = [
            line.lstrip(' ')
            for line in expected_text
        ]
    expected_text = ''.join(expected_text)
    rf = RecordFormatter()

    rf.justification = 10
    rf.column_width = 10
    rf.style = style
    column = rf.str_to_column(string=long_text)

    assert column == expected_text

