from decimal import Decimal
from typing import List, Dict
from .common.misc import british_format_time
from .data_access_layer.records.pet_table_models import RecordType

RECORD_CARD_WIDTH = 60


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
        fr += 'Date of Birth:'.ljust(justification) + f'{british_format_time(float(dob))}\n'  # noqa: E501
    if (gender := record.get('gender')) is not None:
        fr += 'Gender:'.ljust(justification) + f'{gender.title()}\n'
    if (colour := record.get('colour')) is not None:
        fr += 'Colour:'.ljust(justification) + f'{colour.title()}\n'
    if (chip_num := record.get('microchip_number')) is not None:
        fr += 'Microchip number:'.ljust(justification) + f'{chip_num}\n'
    if (medicine_name := record.get('medicine_name')) is not None:
        fr += 'Name of medicine:'.ljust(justification) + f'{medicine_name.title()}\n'  # noqa: E501
    if (medicine_type := record.get('medicine_type')) is not None:
        fr += 'Type of medicine:'.ljust(justification) + f'{medicine_type.title()}\n'  # noqa: E501
    if record_type is not RecordType.DETAILS.value:  # no one needs to know when you added a details record  # noqa: E501
        # but date_time is in every record
        fr += 'Date and time:'.ljust(justification) + f'{british_format_time(float(record["date_time"]))}\n'  # noqa: E501
    if (next_due := record.get('next_due')) is not None:
        fr += 'Next due:'.ljust(justification) + f'{british_format_time(float(next_due))}\n'  # noqa: E501
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
        description_column[0] = section_title + description_column[0][len(section_title):]  # noqa: E501
        description_section = '\n'.join(description_column) + '\n'
        fr += description_section
    return fr


def str_to_column(string: str, column_width: int) -> str:
    """Forces text into a column, newspaper style"""
    string_lines = []
    while len(string) > 0:
        next_line: str = string[:column_width]
        if (len(string) >= column_width and string[column_width] == ' ') or len(next_line) < column_width:  # noqa: E501
            string = string[len(next_line):].lstrip(' ')
        elif (last_space_idx := next_line.rfind(' ')) != -1:
            next_line = next_line[:last_space_idx]
            string = string[len(next_line):].lstrip(' ')
        elif (last_hyphen_idx := next_line.rfind('-')) != -1:
            next_line = next_line[:last_hyphen_idx + 1]
            string = string[len(next_line):]
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
    divider = '='.ljust(RECORD_CARD_WIDTH, '=')
    return f'\n{divider}\n'.join(record_cards)


def tidy_data_types_for_record(record: Dict) -> Dict:
    for key, value in record.items():
        if isinstance(value, Decimal):
            record[key] = float(value)
    return record


def tidy_data_types_for_records(records: List[Dict]) -> List[Dict]:
    tidy_records = []
    for record in records:
        tidy_records.append(tidy_data_types_for_record(record=record))
    return tidy_records
