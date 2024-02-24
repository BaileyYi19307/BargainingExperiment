from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'triangles'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    button_clicked=models.BooleanField(initial=False)


class Player(BasePlayer):
    #number of points the player has
    pass


# PAGES
class MyPage(Page):
    @staticmethod

    def live_method(player, data):
        if data.get('button_clicked'):
            colors = {1: 'red', 2: 'blue', 3: 'green'}
            player_id = player.id_in_group

            player_color = colors.get(player_id, 'grey')

            return {0: {'change_color': True, 'color': player_color}}


page_sequence = [MyPage]
