from os import environ

SESSION_CONFIGS = [
    dict(
        name="tutorial_one",
        display_name="First Tutorial",
        app_sequence=['tutorial_one'],
        num_demo_participants=3,
    )
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = ['who_in_agreement', 'numAgree', 'beginningTime', 'previd', 'taskList', 'howManyCompleted', 'finishedAlready']

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
use_browser_bots = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

SECRET_KEY = '2027701578159'
INSTALLED_APPS = ['otree']
