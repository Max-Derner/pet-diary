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
            'pet_name': 'Avocato',
            'appointment_time': datetime(year=1812, month=2, day=1),
            'description': 'Got appointment to fix up gunshot wound'
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
            'description': 'seems very lethargic since vaccine'
        },
        {
            'pet_name': 'Avocato',
            'observed_time': datetime(year=1812, month=1, day=31),
            'description': 'seems to not enjoy his new friend "The Gary"'
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
            'description': 'seems to not be reacting well to the vaccine, has vomited twice today'
        },
        {
            'pet_name': 'Avocato',
            'ailment': 'gunshot wound',
            'observed_time': datetime(year=1812, month=1, day=30),
            'description': 'Got shot shortly after meeting "The Gary"'
        },
        {
            'pet_name': 'Little Cato',
            'ailment': 'vomiting',
            'observed_time': datetime(year=1809, month=4, day=3),
            'description': 'developing sores due to water immunity and not being able to wash'
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
        {
            'pet_name': 'Avocato',
            'time_of_administration': datetime(year=1808, month=3, day=23),
            'name_of_medicine': 'fix-you-up-a-tub-e-lean',
            'type_of_medicine': 'vaccine',
            'next_due': datetime(year=1809, month=3, day=23)
        },
        {
            'pet_name': 'Avocato',
            'time_of_administration': datetime(year=1809, month=3, day=23),
            'name_of_medicine': 'fix-you-up-a-tub-e-lean',
            'type_of_medicine': 'vaccine',
            'next_due': datetime(year=1810, month=3, day=23)
        },
        {
            'pet_name': 'Little Cato',
            'time_of_administration': datetime(year=1809, month=3, day=23),
            'name_of_medicine': 'fix-you-up-a-tub-e-lean',
            'type_of_medicine': 'vaccine',
            'next_due': datetime(year=1810, month=3, day=23)
        },
    ],
}
