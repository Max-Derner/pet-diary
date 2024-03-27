from typing import Any, Callable, List, Dict
from logging import Logger
from enum import Enum

from .common.logger import get_full_logger
from .common.misc import british_format_time
from .data_access_layer.records.pet_table_models import RecordType


class RecordStyle(str, Enum):
    CARD = 'card styling'
    SMS = 'test message styling'


class RecordFormatter:
    """Defaults:
    justification: 20
    column width: 40
    style: card"""
    _: int
    _log: Logger
    _card_width: int
    divider: str
    _style: RecordStyle
    _column_width: int

    def __init__(self):
        self._style = RecordStyle.CARD
        self._justification = 20
        self._log = get_full_logger()
        self._column_width = 40

    @property
    def divider(self):
        return f"\n{'='.ljust(self.card_width, '=')}\n"

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
        if self.style == RecordStyle.SMS:
            return 0
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
        if self.style == RecordStyle.CARD:
            string_lines = [
                ''.ljust(self.justification) + line
                for line in string_lines
            ]
        return '\n'.join(string_lines)

    def format_record_section(self,
                              section_title: str,
                              record: Dict,
                              key: Any,
                              pre_formatter: Callable[[Any], str] = lambda x: x) -> str:
        section_title += ':'
        section = ''
        if (record_value := record.get(key)) is not None:
            # pre-format
            record_value = pre_formatter(record_value)
            # create column format
            column = self.str_to_column(string=record_value)
            if self.style == RecordStyle.CARD:
                # Force title in line with first line of column
                split_col = column.split('\n')
                split_col[0] = section_title + split_col[0][len(section_title):]
                section = '\n'.join(split_col)
            elif self.style == RecordStyle.SMS:
                section = f"{section_title}\n{column}"
            section += '\n'
        return section

    def format_record(self, record: Dict) -> str:
        """formats record into a style resembling a card"""
        fr = ''  # formatted record
        record_type: str = record['record_type']  # record_type is in every record
        record_title = ' ~~- -~- ' + record_type.title() + ' Record -~- -~~ '
        fr += record_title.center(self.card_width, ' ') + '\n'
        fr += self.format_record_section(
            section_title='Pet',
            key='name',
            record=record
        )
        fr += self.format_record_section(
            section_title='Breed',
            key='breed',
            record=record
        )
        fr += self.format_record_section(
            section_title='Date of Birth',
            key='dob',
            record=record,
            pre_formatter=british_format_time
        )
        fr += self.format_record_section(
            section_title='Gender',
            key='gender',
            record=record
        )
        fr += self.format_record_section(
            section_title='Colour',
            key='colour',
            record=record
        )
        fr += self.format_record_section(
            section_title='Microchip number',
            key='microchip_number',
            record=record,
            pre_formatter=lambda x: str(x),
        )
        fr += self.format_record_section(
            section_title='Name of medicine',
            key='medicine_name',
            record=record
        )
        fr += self.format_record_section(
            section_title='Type of medicine',
            key='medicine_type',
            record=record
        )
        fr += self.format_record_section(
            section_title='Record creation date' if record_type is RecordType.DETAILS else 'Date and time',
            key='date_time',
            record=record,
            pre_formatter=british_format_time
        )
        fr += self.format_record_section(
            section_title='Next due',
            key='next_due',
            record=record,
            pre_formatter=british_format_time
        )
        fr += self.format_record_section(
            section_title='Ailment',
            key='ailment',
            record=record
        )
        fr += self.format_record_section(
            section_title='Description',
            key='description',
            record=record
        )
        return fr

    def format_records(self, records: List[Dict]) -> str:
        """formats multiple records into a style resembling a card"""
        record_cards = []
        for record in records:
            record_cards.append(self.format_record(record=record))
        return self.divider + self.divider.join(record_cards)
