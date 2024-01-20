from logging import Logger
from typing import Any
from datetime import datetime

from pytest import mark

from app.support.record_formatting import (
    RecordFormatter,
    RecordStyle,
)
from app.support.data_access_layer.records.pet_table_models import RecordType


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


@mark.parametrize('style, pre_formatter',
                  [
                      (RecordStyle.CARD, None),
                      (RecordStyle.SMS, None),
                      (RecordStyle.SMS, lambda x: x.upper()),
                  ])
def test_format_record_section(style, pre_formatter):
    rf = RecordFormatter()
    rf.justification = 20
    rf.column_width = 20
    rf.style = style
    record = {'key': 'All the details and whatnot'}
    additional_kwargs = {'pre_formatter': pre_formatter} if pre_formatter is not None else {}

    line = rf.format_record_section(
        section_title='DISPLAY NAME',
        record=record,
        key='key',
        **additional_kwargs
    )

    if style == RecordStyle.CARD:
        assert line == "DISPLAY NAME:       All the details and\n                    whatnot\n"
    elif style == RecordStyle.SMS:
        if pre_formatter is None:
            assert line == "DISPLAY NAME:\nAll the details and\nwhatnot\n"
        else:
            assert line == "DISPLAY NAME:\nALL THE DETAILS AND\nWHATNOT\n"


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


def tests_format_record():
    monster_record = {
        'name': 'pet name',
        'breed': 'pets breed',
        'dob': datetime(year=2023, month=12, day=4).timestamp(),
        'gender': 'pets gender',
        'colour': 'colour of pet',
        'microchip_number': "1",
        'date_time': datetime(year=2023, month=1, day=1).timestamp(),
        'medicine_name': 'precise name of medication',
        'medicine_type': 'deflea, deworm, etc',
        'ailment': 'vomiting, lethargy, etc',
        'description': 'description of ailment, vet appointment, observation, etc',
        'next_due': datetime(year=2023, month=2, day=2).timestamp(),
        'record_type': RecordType.APPOINTMENT.value
    }
    with open('tests/formatted_record_example.txt', mode='r') as fileio:
        expected_formatting = fileio.read()

    fr = RecordFormatter()
    formatted_record = fr.format_record(record=monster_record)

    assert formatted_record == expected_formatting
