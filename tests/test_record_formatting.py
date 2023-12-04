from datetime import datetime
from app.support.record_formatting import str_to_column, format_record
from app.support.data_access_layer.records.pet_table_models import RecordType


def tests_str_to_column():
    long_text = 'I am a sample of text that is supposed to be big enough that it can get wrapped'
    expected_text = "I am a\nsample of\ntext that\nis\nsupposed\nto be big\nenough\nthat it\ncan get\nwrapped"

    wrapped_text = str_to_column(string=long_text, column_width=10)

    assert wrapped_text == expected_text


def tests_format_record():
    monster_record = {
        'name': 'pet name',
        'breed': 'pets breed',
        'dob': datetime(year=2023, month=12, day=4).timestamp(),
        'gender': 'pets gender',
        'colour': 'colour of pet',
        'microchip_number': 1,
        'date_time': datetime(year=2023, month=1, day=1).timestamp(),
        'medicine_name': 'precise name of medication',
        'medicine_type': 'deflea, deworm, etc',
        'ailment': 'vomiting, lathargy, etc',
        'description': 'description of ailment, vet appointment, observation, etc',
        'next_due': datetime(year=2023, month=2, day=2).timestamp(),
        'record_type': RecordType.APPOINTMENT.value
    }
    expected_formatting = """             ~~- -~- Appointment Record -~- -~~             
Pet:                Pet Name
Breed:              Pets Breed
Date of Birth:      Monday, 4 December 2023 - 12:00 AM
Gender:             Pets Gender
Colour:             Colour Of Pet
Microchip number:   1
Name of medicine:   Precise Name Of Medication
Type of medicine:   Deflea, Deworm, Etc
Date and time:      Sunday, 1 January 2023 - 12:00 AM
Next due:           Thursday, 2 February 2023 - 12:00 AM
Ailment:            Vomiting, Lathargy, Etc
Description:        description of ailment, vet appointment,
                    observation, etc
"""

    formatted_record = format_record(record=monster_record)

    assert formatted_record == expected_formatting
