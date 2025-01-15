from os import environ

SESSION_CONFIGS = [
    dict(
        name="Tutorial",
        display_name="Tutorial",
        app_sequence=['Tutorial'],
        num_demo_participants=3,
        totalNodes=66,  #number of nodes in the triangle
        totalPoints=18,  #total points to distribute 
        initialCurrencyValue=3.00, #starting currency value
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
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

SECRET_KEY = '2027701578159'
INSTALLED_APPS = ['otree']
