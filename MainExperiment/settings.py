from os import environ

SESSION_CONFIGS = [
    dict(
        name="Tutorial",
        display_name="Tutorial",
        app_sequence=['Tutorial'],
        num_demo_participants=3,
        totalNodes=66,  
        totalMoney=54,  
        timeLimit=1,
        initialCurrencyValue=3.00,  
        ratificationTime=10,
        num_rounds=3,  
  
    ),
    dict(
        name="Main_Experiment",
        display_name="Triangle Experiment",
        app_sequence=['PreExperiment','Main_Experiment','ExperimentEnd'], 
        num_demo_participants=3,
        compulsory_offer_treatment=False,  
        totalNodes=66,  
        totalMoney=54,  
        initialCurrencyValue=3.00,  
        ratificationTime=10,  
        timeLimit=3,  
        num_rounds=3,
    ),
]


# SESSION_CONFIGS = [
#     dict(
#         name="Main_Experiment",
#         display_name="Triangle Experiment",
#         app_sequence=['Main_Experiment'],
#         num_demo_participants=3,
#         compulsory_offer_treatment=True,  # enable compulsory offer
#         totalNodes=66,  #number of nodes in the triangle
#         totalPoints=18,  #total points to distribute 
#         initialCurrencyValue=3.00, #starting currency value
#         ratificationTime=10, #time for ratification/agreement countdown
#         timeLimit=3, #time limit for the experiment round
#     )
# ]



# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)


PARTICIPANT_FIELDS = ['expiry','gender','mpl_choices','round_payoffs','taskList','alreadyFinished','howManyCompleted']
# SESSION_FIELDS = ['who_in_agreement','numAgree','beginningTime','playersClicking','whosClickedWhat','buttonClickStates','experiment_started', 'submittedFirstOffer']
SESSION_FIELDS = [
    'who_in_agreement', 'numAgree', 'beginningTime', 'previd', 'taskList', 
    'howManyCompleted', 'finishedAlready', 'playersClicking', 'whosClickedWhat', 
    'buttonClickStates', 'experiment_started', 'submittedFirstOffer','selected_rounds'
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


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

INSTALLED_APPS = ['otree', 'Main_Experiment', 'Tutorial']


