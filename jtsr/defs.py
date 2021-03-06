import enum

CONFIG_FILE = 'config.ini'

MAXIMUM_FATIGUE = 300.0

ABBRV_LIST = {
    'PRT':'Partisan',
    'SG':'Siege Gun',       
    'GM':'Guided Missile',
    'SUP':'Supply',
    'BAT':'Battleship',
    'DES':'Destroyer',
    'RA':'Recon Aircraft',
    'HBO':'Heavy Bomber',
    'BO':'Bomber',
    'FI':'Fighter',
    'COM':'Commando',
    'PAR':'Paratrooper',
    'MG':'Machine Gun',
    'MOR':'Mortar',
    'HVY':'Heavy Weapon',
    'HAA':'Heavy Anti-Air',
    'REC':'Recon',
    'ENG':'Engineer',
    'AT':'Anti-Tank',
    'ROC':'Rocket',
    'HART':'Heavy Artillery',
    'ART':'Artillery',
    'ARM':'Armor',
    'INF':'Infantry',
    'HQ':'Headquarters',
    'HEL':'???',
    'NAV':'???',
    'AIR':'???',
    'RL':'???',
    'TRK':'???',
    'HT':'???',
    'PM':'???',
    'AC':'???',
    'MOT':'???',
    'MC':'???',
    'MNT':'???',
    'BI':'???',
    'SKI':'???',
    'FT':'???'
}

class EType(enum.Enum):
    FORMATION=0,
    UNIT=1

class Side(enum.Enum):
    ALLIES=0,
    AXIS=1

AXIS= [
    'Austro-Hungarian',
    'Chinese',
    'East-German',
    'Egyptian',
    'Finnish',
    'French-Vichy',
    'German',
    'German-SS',
    'Hungarian',
    'Iranian',
    'Iranian-Guards',
    'Iraqi',
    'Italian',
    'Japanese',
    'Jordanian',
    'Luftwaffe',
    'North-Korean',
    'North-Vietnamese',
    'Republican-Guard',
    'Rumanian',
    'Slovakian',
    'Warsaw-Pact'
]
ALLIES = [
    'American',
    'American-AB',
    'American-Marine',
    'Austria',
    'Belgian',
    'British',
    'British-AB',
    'Canadian',
    'Commonwealth',
    'Czechoslovakia',
    'Denmark',
    'Free-French',
    'French',
    'Greecian',
    'Italian-Allied',
    'Kuwaiti',
    'NATO',
    'Netherland',
    'NKVD',
    'Norwegian',
    'Polish',
    'Rumanian-Allied',
    'Russian-Guards',
    'South-Korean',
    'South-Vietnamese',
    'Syrian',
    'Taiwan',
    'Vietnam-Marines',
    'West-German',
    'Yugoslavian'
]
