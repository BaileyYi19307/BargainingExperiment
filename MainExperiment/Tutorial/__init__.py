from otree.api import *
import random

doc = """
Tutorial page 2
"""

random_grouping = models.BooleanField(initial = True)# true is random


class C(BaseConstants):
    NAME_IN_URL = 'Tutorial'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1          # number of cycles of the entire game


class Subsession(BaseSubsession):
    def creating_session(self):
        if 'taskList' not in self.session.vars:
            self.session.vars['taskList'] = {}
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
    previousClicker=models.IntegerField(initial=0)

class Player(BasePlayer):
    repeat_tutorial = models.BooleanField(initial=False)

class TutorialPage1(Page):
    @staticmethod
    def vars_for_template(self):
        return {
            'totalNodes': self.session.config.get('totalNodes', 0),  
            'totalMoney': self.session.config.get('totalMoney', 0),  
            'initialCurrencyValue': self.session.config.get('initialCurrencyValue', 1),  
        }


class TutorialPage2(Page):
    @staticmethod
    def vars_for_template(self):
        return {
            'totalNodes': self.session.config.get('totalNodes', 0),  
            'totalMoney': self.session.config.get('totalMoney', 0),  
            'initialCurrencyValue': self.session.config.get('initialCurrencyValue', 1),  
        }
    
    @staticmethod
    def live_method(player, data):
        session = player.session

        session.vars.setdefault('howManyCompleted', {})

        #set up the task list
        if 'getTaskList' in data:
            return {0:{'howManyCompleted':session.vars['howManyCompleted']}}

        # handle button click event
        if 'buttonClicked' in data:
            session.vars['howManyCompleted'][data['whichTask']]=True
            print(session.vars['howManyCompleted'])
            if (len(session.vars['howManyCompleted']) == 2 and all(session.vars['howManyCompleted'])):
                print("All the tasks have been completed")
                return {0:{'allTasksCompleted':1}}




class TutorialPage3(Page):
    @staticmethod
    def vars_for_template(self):
        return {
            'totalNodes': self.session.config.get('totalNodes', 0),  
            'totalMoney': self.session.config.get('totalMoney', 0),  
            'ratificationTime':self.session.config['ratificationTime'],
        }
    


import math 
import random
class TutorialPage4(Page):
    
    @staticmethod
    def vars_for_template(player):
        group = player.group.get_players() 

        return {
            'player_id': player.id_in_group,  
            'totalNodes': player.session.config['totalNodes'],  
            'totalMoney': player.session.config['totalMoney'],
            'ratificationTime': player.session.config['ratificationTime'],
            'timeLimit': player.session.config['timeLimit'],
        }


    @staticmethod
    def live_method(player, data):
        session = player.session
        groupId = player.group
        session.vars.setdefault('beginningTime', 0)
        session.vars.setdefault('taskList', {})
        session.vars.setdefault('alreadyFinished', False)


        if "botsChoose" in data:
            #want to make them both choose
            #get the list of buttons available
            allButtons=data["allButtonsList"]
            otherPlayers = list(range(1,len(player.group.get_players())+1))

            #remove this player from the list
            otherPlayers.remove(player.id_in_group)
            #pick two random, using sample
            bot1choice, bot2choice = random.sample(allButtons,2)
            print(bot1choice, bot2choice)
            simulated_clicks={"simulated_clicks":{otherPlayers[0]:bot1choice,otherPlayers[1]:bot2choice}}
            
            return {player.id_in_group:simulated_clicks}
        

        # handle timer start
        if 'timerStarted' in data:
            session.vars['beginningTime'] = float(data['timerStarted'])

        # track previous clicker
        if 'participants' in data:
            groupId.previousClicker = data['participants']

        # track active participants in agreement
        if 'activeParticipants' in data:
            active_participants = data['activeParticipants']

        session.vars.setdefault('who_in_agreement', [])
        who_agrees = session.vars['who_in_agreement']
        num_agree = len(who_agrees)
        session.vars['numAgree'] = num_agree

        # handle agreement logic
        if 'numInAgreement' in data:
            if data['numInAgreement'] < 2:
                if num_agree >= 2 and any(participant in who_agrees for participant in active_participants):
                    who_agrees.clear()
                else:
                    who_agrees.clear()
                    who_agrees.extend(active_participants)
            else:
                who_agrees.clear()
                who_agrees.extend(active_participants)
                session.vars['numAgree'] = len(who_agrees)

        # handle payoffs
        if 'payoffs' in data:
            player_id = data['payoffs']['player_id']
            
            if player_id == groupId.previousClicker:
                groupId.previousClicker = player_id

                for player_id in [1, 2, 3]:
                    p = groupId.get_player_by_id(player_id)
                    p_payoff = data['payoffs'].get(f'p{player_id}_points', 0)

                    # Rrund all calculations to two decimal places
                    p.payoff = round(p_payoff, 2)

        print("checking the data", data)
        if 'getMeTaskList' in data:
            print("HI IM IN GET ME TASK LIST")
            return {player.id_in_group:{'taskList':session.vars['taskList'],'alreadyFinished':session.vars['alreadyFinished']}}


        if 'buttonClicked' in data:
            print('Button was clicked')
            session.vars['taskList'][data['whichTask']]=True
            print(f"The first task is{session.vars['taskList'][data['whichTask']]}")
            print(session.vars['taskList'])


        # handle button click event
        if 'button_clicked' in data:
            print(data["button_id"])
            player_id = player.id_in_group
            return {player_id: {"user_clicked":data["button_id"]}}
    
        if not session.vars['alreadyFinished'] and len(session.vars['taskList']) == 4 and all(session.vars['taskList'].values()):
            # All the tasks have been completed for the first time
            print("All the tasks have been completed")
            session.vars['alreadyFinished'] = True
            return {player.id_in_group: {'allTasksCompleted': 1, 'tasksDone':session.vars['taskList']}}




    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        #reset before next round:
        session = player.session
        session.vars['who_in_agreement'] = []
        session.vars['submittedFirstOffer'] = {"player1": None, "player2": None, "player3": None}
        session.vars['buttonClickStates'] = {}
        session.vars['whosClickedWhat'] = {1: "", 2: "", 3: ""}
        session.vars['playersClicking'] = []

class TutorialPage5(Page):
    @staticmethod
    def vars_for_template(player):
        group = player.group.get_players() 

        return {
            'player_id': player.id_in_group,  
            'totalNodes': player.session.config['totalNodes'],  
            'totalMoney': player.session.config['totalMoney'],
            'ratificationTime': player.session.config['ratificationTime'],
            'timeLimit': player.session.config['timeLimit'],
        }


page_sequence = [TutorialPage1,TutorialPage2,TutorialPage3,TutorialPage4,TutorialPage5]








