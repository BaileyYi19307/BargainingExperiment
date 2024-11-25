from os import environ


SESSION_CONFIGS = [
    dict(
        name="Main_Experiment",
        display_name="show one button",
        app_sequence=['Main_Experiment'],
        num_demo_participants=3,
        random_proposer_treatment=True,  # enable random proposer mode
        compulsory_offer_treatment=True,  # enable compulsory offer

    )
]



# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['expiry']
SESSION_FIELDS = ['who_in_agreement','numAgree','beginningTime','playersClicking','whosClickedWhat','buttonClickStates','experiment_started']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True


ROOMS = [
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '2027701578159'

INSTALLED_APPS = ['otree']
