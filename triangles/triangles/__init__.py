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

    #the server
    def live_method(player, data):
        # Check if the message received indicates a button click
        if data.get('button_clicked'):
            # Broadcast a message to all clients in the group to change the button color
            return {1: {'change_color': True},
                    2: {'change_color': True}}


page_sequence = [MyPage]
