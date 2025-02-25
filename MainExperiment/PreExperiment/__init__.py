from otree.api import *
import json


doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'PreExperiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField(choices=["Male", "Female"])
    mpl_choices=models.StringField(initial='{}')

# PAGES
class GenderSelection(Page):
    form_model = 'player'
    form_fields = ['gender']
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.gender = player.gender
        player.participant.round_payoffs={}



class MPL(Page):

    @staticmethod
    def vars_for_template(self):
        return({'totalMoney':self.session.config['totalMoney']})
    
    @staticmethod
    def live_method(player,data):
        if 'mpl_choices' in data:
            player.mpl_choices = json.dumps(data['mpl_choices']) 
            player.participant.mpl_choices = player.mpl_choices

class Results(Page):
    pass


page_sequence = [GenderSelection,MPL]
