from typing import Any, List, Dict
from logging import Logger
from enum import Enum

from .common.logger import get_full_logger
from .common.misc import british_format_time
from .data_access_layer.records.pet_table_models import RecordType

RECORD_CARD_WIDTH = 60
DIVIDER = f"\n{'='.ljust(RECORD_CARD_WIDTH, '=')}\n"


def format_record(record: Dict):
    """formats record into a style resembling a card"""
    justification = 20
    fr = ''  # formatted record
    # record_type is in every record
    record_type: str = record['record_type']
    record_title = ' ~~- -~- ' + record_type.title() + ' Record -~- -~~ '
    fr += record_title.center(RECORD_CARD_WIDTH, ' ') + '\n'
    # name is in every record
    pet_name: str = record["name"]
    fr += 'Pet:'.ljust(justification) + f'{pet_name.title()}\n'
    if (breed := record.get('breed')) is not None:
        fr += 'Breed:'.ljust(justification) + f'{breed.title()}\n'
    if (dob := record.get('dob')) is not None:
        fr += 'Date of Birth:'.ljust(justification) + f'{british_format_time(float(dob))}\n'
    if (gender := record.get('gender')) is not None:
        fr += 'Gender:'.ljust(justification) + f'{gender.title()}\n'
    if (colour := record.get('colour')) is not None:
        fr += 'Colour:'.ljust(justification) + f'{colour.title()}\n'
    if (chip_num := record.get('microchip_number')) is not None:
        fr += 'Microchip number:'.ljust(justification) + f'{chip_num}\n'
    if (medicine_name := record.get('medicine_name')) is not None:
        fr += 'Name of medicine:'.ljust(justification) + f'{medicine_name.title()}\n'
    if (medicine_type := record.get('medicine_type')) is not None:
        fr += 'Type of medicine:'.ljust(justification) + f'{medicine_type.title()}\n'
    if record_type is not RecordType.DETAILS.value:  # no one needs to know when you added a details record
        # but date_time is in every record
        fr += 'Date and time:'.ljust(justification) + f'{british_format_time(float(record["date_time"]))}\n'
    if (next_due := record.get('next_due')) is not None:
        fr += 'Next due:'.ljust(justification) + f'{british_format_time(float(next_due))}\n'
    if (ailment := record.get('ailment')) is not None:
        fr += 'Ailment:'.ljust(justification) + f'{ailment.title()}\n'
    if (description := record.get('description')) is not None:
        column_width = RECORD_CARD_WIDTH - justification
        description_column: str = str_to_column(
            string=description,
            column_width=column_width
        )
        # Justify column to the right
        description_column: List[str] = description_column.split('\n')
        description_column = [
            ' '.ljust(justification) + line
            for line in description_column
        ]
        # Add section title in
        section_title = 'Description:'
        description_column[0] = section_title + description_column[0][len(section_title):]
        description_section = '\n'.join(description_column) + '\n'
        fr += description_section
    return fr


def str_to_column(string: str, column_width: int) -> str:
    """Forces text into a column, newspaper style"""
    string_lines = []
    while len(string) > 0:
        next_line: str = string[:column_width]
        # Figure out if line is short enough to fit in column
        if len(next_line) < column_width:
            string = string[len(next_line):].lstrip(' ')
        # Otherwise, try to split of space or hyphen
        elif (last_space_idx := next_line.rfind(' ')) != -1:  # -1 is failure
            next_line = next_line[:last_space_idx]
            string = string[len(next_line):].lstrip(' ')
        elif (last_hyphen_idx := next_line.rfind('-')) != -1:  # -1 is failure
            next_line = next_line[:last_hyphen_idx + 1]
            string = string[len(next_line):]
        # Last ditch hope is to manually put in hyphen
        else:
            next_line = next_line[:-1] + '-'
            string = string[len(next_line) - 1:]
        string_lines.append(next_line)
    return '\n'.join(string_lines)


def record_formatter(records: List[Dict]) -> str:
    """formats records into a style resembling a card"""
    record_cards = []
    for record in records:
        record_cards.append(format_record(record=record))
    return DIVIDER + f'{DIVIDER}'.join(record_cards)


class RecordStyle(str, Enum):
    CARD = 'card styling'
    SMS = 'test message styling'


class RecordFormatter:
    _records: List[Dict]
    _: int
    _log: Logger
    _card_width: int
    _divider: str
    _style: RecordStyle
    _column_width: int

    def __init__(self):
        self._log = get_full_logger()
        self._justification = 20
        self._records = []
        self._column_width = 40
        self._divider = f"\n{'='.ljust(self.card_width, '=')}\n"
        self._style = RecordStyle.CARD

    @property
    def card_width(self) -> int:
        return self._column_width + self.justification

    @property
    def column_width(self) -> int:
        return self._column_width

    @column_width.setter
    def column_width(self, value):
        if isinstance(value, int):
            self._column_width = value
            self.log.debug(f"column_width set to: {value}")
        else:
            self.log.debug(
                f"column_width not set. Expected type int, got type {type(value)}"
            )

    @property
    def log(self) -> Logger:
        return self._log

    @property
    def justification(self) -> int:
        return self._justification

    @justification.setter
    def justification(self, value: int):
        if isinstance(value, int):
            self._justification = value
            self.log.debug(f"justification set to: {value}")
        else:
            self.log.debug(
                f"justification not set. Expected type int, got type {type(value)}"
            )

    @property
    def style(self) -> int:
        return self._style

    @style.setter
    def style(self, value):
        if isinstance(value, RecordStyle):
            self._style = value
            self.log.debug(f"style set to: {value}")
        else:
            self.log.debug(
                f"style not set. Expected type RecordStyle, got type {type(value)}"
            )

    def add_records(self, records: List[Dict]):
        if not isinstance(records, list):
            records = [records]
        good_records = [record for record in records if isinstance(record, dict)]
        if len(good_records) != len(records):
            self.log.debug(
                f"{len(records) - len(good_records)} records were not the correct type and will not be formatted"
            )
        self._records.extend(good_records)

    def str_to_column(self, string: str) -> str:
        """Forces text into a column, newspaper style"""
        string_lines = []
        while len(string) > 0:
            next_line: str = string[:self.column_width]
            # Figure out if line is short enough to fit in column
            if len(next_line) < self.column_width:
                string = string[len(next_line):].lstrip(' ')
            # Otherwise, try to split on space or hyphen
            elif (last_space_idx := next_line.rfind(' ')) != -1:  # -1 is failure
                next_line = next_line[:last_space_idx]
                string = string[len(next_line):].lstrip(' ')
            elif (last_hyphen_idx := next_line.rfind('-')) != -1:  # -1 is failure
                next_line = next_line[:last_hyphen_idx + 1]
                string = string[len(next_line):]
            # Last ditch hope is to forcefully put in hyphen
            else:
                next_line = next_line[:-1] + '-'
                string = string[len(next_line) - 1:]
            string_lines.append(next_line)
        # justify column
        if self._style == RecordStyle.CARD:
            string_lines = [
                ''.ljust(self.justification) + line
                for line in string_lines
            ]
        return '\n'.join(string_lines)
