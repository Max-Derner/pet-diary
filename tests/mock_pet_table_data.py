from datetime import datetime


test_data = {
    'details':
    [
        {
            'pet_name': 'Avocato',
            'date_of_birth': datetime(year=1807, month=12, day=23),
            'colour': 'tuxedo',
            'gender': 'man',
            'breed': 'Ventrexian',
            'microchip_number': 2
        },
        {
            'pet_name': 'Little Cato',
            'date_of_birth': datetime(year=1809, month=12, day=23),
            'colour': 'ginger',
            'gender': 'boy',
            'breed': 'Ventrexian',
            'microchip_number': 3
        },
    ],
    'appointment':
    [
        {
            'pet_name': 'Avocato',
            'appointment_time': datetime(year=1808, month=3, day=23),
            'description': 'Got to get first vaccination'
        },
        {
            'pet_name': 'Little Cato',
            'appointment_time': datetime(year=1809, month=3, day=23),
            'description': 'Got to get first vaccination'
        },
    ],
    'observation':
    [
        {
            'pet_name': 'Avocato',
            'observed_time': datetime(year=1808, month=3, day=29),
            'description': 'seems vary lethargic since vaccine'
        },
        {
            'pet_name': 'Little Cato',
            'observed_time': datetime(year=1809, month=3, day=29),
            'description': 'has become immune to rain since vaccine'
        },
    ],
    'illness':
    [
        {
            'pet_name': 'Avocato',
            'ailment': 'vomiting',
            'observed_time': datetime(year=1808, month=4, day=3),
            'description': 'seems to not be reacting well to the vaccine, has vomited twice today'  # noqa: E501
        },
        {
            'pet_name': 'Little Cato',
            'ailment': 'vomiting',
            'observed_time': datetime(year=1809, month=4, day=3),
            'description': 'developing sores due to water immunity and not being able to wash'  # noqa: E501
        },
    ],
    'medication':
    [
        {
            'pet_name': 'Avocato',
            'time_of_administration': datetime(year=1808, month=4, day=4),
            'name_of_medicine': 'feel-better-a-loxin',
            'type_of_medicine': 'antiemetic',
            'next_due': datetime(year=1808, month=4, day=5)
        },
        {
            'pet_name': 'Avocato',
            'time_of_administration': datetime(year=1808, month=4, day=6),
            'name_of_medicine': 'Abaddon - destroyer of fleas',
            'type_of_medicine': 'deflea',
            'next_due': datetime(year=1808, month=7, day=6)
        },
        {
            'pet_name': 'Avocato',
            'time_of_administration': datetime(year=1808, month=4, day=13),
            'name_of_medicine': 'Abaddon - destroyer of parasites',
            'type_of_medicine': 'deworm',
            'next_due': datetime(year=1808, month=7, day=13)
        },
        {
            'pet_name': 'Little Cato',
            'time_of_administration': datetime(year=1809, month=4, day=6),
            'name_of_medicine': 'Abaddon - destroyer of fleas',
            'type_of_medicine': 'deflea',
            'next_due': datetime(year=1809, month=7, day=6)
        },
        {
            'pet_name': 'Little Cato',
            'time_of_administration': datetime(year=1809, month=4, day=13),
            'name_of_medicine': 'Abaddon - destroyer of parasites',
            'type_of_medicine': 'deworm',
            'next_due': datetime(year=1809, month=7, day=13)
        },
    ],
}
