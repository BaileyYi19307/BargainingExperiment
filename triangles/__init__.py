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
    ogCurrency=models.FloatField(initial=0)
    currency=models.FloatField(initial=0)

    pass

# PAGES
class WaitingRoom(WaitPage):
    group_by_arrival_time = False
    title_text = "Waiting Room"
    body_text = "Wait for everyone to join before proceeding"

# PAGES
class MyPage(Page):

    @staticmethod
    def live_method(player, data):
        if 'button_clicked' in data:
            return {0: {'button_id': data["button_id"], 'player_id': player.id_in_group}}
        if 'payoffs' in data:
            g = player.group
            currencyDecay = data['payoffs']['4']

            # Ensure default values if None is found
            default_payoff = 0

            # Handling for Player 1
            p1 = g.get_player_by_id(1)
            p1_payoff = data['payoffs']['1']
            print(p1_payoff)
            if p1_payoff is None:
                p1.payoff = default_payoff
            p1.payoff=p1_payoff
            p1.currency = round(float(p1.payoff) * currencyDecay,2)
            p1.ogCurrency = float(p1.payoff) * 3.00  # Adjust the 3 as necessary

            # Handling for Player 2
            p2 = g.get_player_by_id(2)
            p2_payoff = data['payoffs'].get('2')
            if p2_payoff is None:
                p2.payoff = default_payoff
            p2.payoff = p2_payoff
            p2.currency = round(float(p2.payoff) * currencyDecay,2)
            p2.ogCurrency = float(p2.payoff) * 3.00  # Adjust the 3 as necessary

            # Handling for Player 3
            p3 = g.get_player_by_id(3)
            p3_payoff = data['payoffs'].get('3')
            if p3_payoff is None:
                p3.payoff = default_payoff
            p3.payoff=p3_payoff
            p3.currency = round(float(p3.payoff) * currencyDecay,2)
            p3.ogCurrency = float(p3.payoff) * 3.00  # Adjust the 3 as necessary


class ResultsPage(Page):
    @staticmethod
    def live_method(player: Player, data: dict):
        if data.get('next_clicked'):
            return {player.id_in_group: 'next'}



class FinalPage(Page):
    pass


page_sequence = [WaitingRoom, MyPage, ResultsPage] * totalRounds + [FinalPage]
