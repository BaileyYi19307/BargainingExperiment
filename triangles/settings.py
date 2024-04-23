from os import environ


SESSION_CONFIGS = [
    dict(
        # put all the sessions you want to run here
        name="triangles",
        display_name="show one button",
        app_sequence=['triangles'],
        num_demo_participants=3,
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
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
#
# {#function liveRecv(data) {#}
# {#    var buttonId = data.button_id;#}
# {#    var button = document.getElementById(buttonId);#}
# {#    var btn = buttonStates[buttonId];#}
# {##}
# {#    // Loop through all buttons to check their states#}
# {#    // Loop through all buttons to check their states#}
# {#    Object.keys(buttonStates).forEach(function(key) {#}
# {#        var state = buttonStates[key];#}
# {#        var prevButton = document.getElementById(key);#}
# {##}
# {#        if (prevButton !== button) {#}
# {#            if (data.player_id == 1) {#}
# {#                if (state.clickedByUser1 && state.clickedByUser2) {#}
# {#                    prevButton.classList.remove('both-borders', 'red-border');#}
# {#                } else if (state.clickedByUser1 && !state.clickedByUser2) {#}
# {#                    prevButton.classList.remove('red-border');#}
# {#                }#}
# {#                state.clickedByUser1=false;#}
# {##}
# {#            } else if (data.player_id == 2) {#}
# {#                if (state.clickedByUser1 && state.clickedByUser2) {#}
# {#                    prevButton.classList.remove('both-borders', 'blue-border');#}
# {#                } else if (state.clickedByUser2 && !state.clickedByUser1) {#}
# {#                    prevButton.classList.remove('blue-border');#}
# {#                }#}
# {#                state.clickedByUser=false;#}
# {#            }#}
# {#        }#}
# {#    });#}
# {##}
# {##}
# {#    // Proceed with the logic for handling button clicks based on the player's interaction#}
# {#    if (!btn.clickedByUser1) {#}
# {#        // Handle the case when the button has not been clicked by player 1#}
# {#        if (!btn.clickedByUser2) {#}
# {#            if (data.player_id == 1) {#}
# {#                button.classList.toggle('red-border', true);#}
# {#                btn.clickedByUser1 = true;#}
# {#            } else {#}
# {#                button.classList.toggle('blue-border', true);#}
# {#                btn.clickedByUser2 = true;#}
# {#            }#}
# {#        } else {#}
# {#            if (data.player_id == 1) {#}
# {#                button.classList.toggle('red-border', true);#}
# {#                button.classList.toggle('both-borders', true);#}
# {#                btn.clickedByUser1 = true;#}
# {#            } else if (data.player_id == 2) {#}
# {#                button.classList.toggle('red-border', false);#}
# {#                button.classList.toggle('blue-border', false);#}
# {#                btn.clickedByUser2 = false;#}
# {#            }#}
# {#        }#}
# {#    } else {#}
# {#        // Handle the case when the button has been clicked by player 1#}
# {#        if (!btn.clickedByUser2) {#}
# {#            if (data.player_id == 1) {#}
# {#                button.classList.toggle('red-border', false);#}
# {#                btn.clickedByUser1 = false;#}
# {#            } else {#}
# {#                button.classList.toggle('blue-border', true);#}
# {#                button.classList.toggle('both-borders', true);#}
# {#                btn.clickedByUser2 = true;#}
# {#            }#}
# {#        } else {#}
# {#            if (data.player_id == 1) {#}
# {#                button.classList.toggle('red-border', false);#}
# {#                btn.clickedByUser1 = false;#}
# {#                button.classList.toggle('both-borders', false);#}
# {##}
# {#            } else {#}
# {#                button.classList.toggle('blue-border', false);#}
# {#                btn.clickedByUser2 = false;#}
# {#                button.classList.toggle('both-borders', false);#}
# {##}
# {#            }#}
# {##}
# {#        }#}
# {#    }#}
