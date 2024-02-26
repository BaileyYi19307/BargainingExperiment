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
    def live_method(player: Player, data: dict):
        # Simplify by directly using the incoming data without intermediate variables
        if data.get('button_clicked'):
            # Directly return the necessary information to all players in the group
            return {0: {'button_id': data["button_id"], 'player_id': player.id_in_group}}



page_sequence = [MyPage]
