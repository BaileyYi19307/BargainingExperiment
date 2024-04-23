from otree.api import *


doc = """
Your app description
"""

totalRounds = 5
random_grouping = models.BooleanField(initial = True)

class C(BaseConstants):
    NAME_IN_URL = 'triangles'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        if random_grouping:
            self.group_randomly()
        else:
            self.group_fixed()

    def group_fixed(self):
        players = self.get_players()
        group_size = 3
        group_matrix = [players[i:i + group_size] for i in range(0, len(players), group_size)]
        self.set_group_matrix(group_matrix)


class Group(BaseGroup):
    button_clicked=models.BooleanField(initial=False)


class Player(BasePlayer):
    #number of points the player has
    pass


# PAGES
class WaitingRoom(WaitPage):
    group_by_arrival_time = False
    title_text = "Waiting Room"
    body_text = "Wait for everyone to join before proceeding"


class MyPage(Page):
    # class MyPage(Page):
    #     @staticmethod
    #     def vars_for_template(player: Player):
    #         n = 15
    #         points = 12
    #         return {
    #             'total_nodes': n,
    #             'total_points': points
    #         }

    @staticmethod
    def live_method(player: Player, data: dict):
        if data.get('button_clicked'):
            return {0: {'button_id': data["button_id"], 'player_id': player.id_in_group}}

class ResultsPage(Page):
    @staticmethod
    def live_method(player: Player, data: dict):
        if data.get('next_clicked'):
            return {player.id_in_group: 'next'}



class FinalPage(Page):
    pass







page_sequence = [WaitingRoom, MyPage, ResultsPage] * totalRounds + [FinalPage]