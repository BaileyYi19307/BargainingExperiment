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
    class MyPage(Page):
        @staticmethod
        def vars_for_template(player: Player):
            n = 10
            points = 12
            return {
                'total_nodes': n,
                'total_points': points
            }

    @staticmethod
    def live_method(player: Player, data: dict):
        if data.get('button_clicked'):
            return {0: {'button_id': data["button_id"], 'player_id': player.id_in_group}}



page_sequence = [MyPage]
