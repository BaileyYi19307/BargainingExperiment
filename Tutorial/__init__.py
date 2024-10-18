from otree.api import *
import random

doc = """
Your app description
"""

totalRounds = 5
random_grouping = models.BooleanField(initial = True)          # true is random


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
    ogCurrency = models.FloatField(initial=0)
    currency = models.FloatField(initial=0)
    custom_round_num = models.IntegerField(initial=1)       # manual round number
    repeat_tutorial = models.BooleanField(initial=False)

class TutorialPage1(Page):
    pass

class TutorialPage2(Page):
    
    @staticmethod
    def live_method(player, data):
        session = player.session
        g = player.group

        x = [0, 5, 10, 15]
        while True:
            selected_numbers = random.choices(x, k=3)
            if sum(selected_numbers) == 15:
                break

        session.vars.setdefault('previd', [])
        previd = session.vars['previd']

        session.vars.setdefault('howManyCompleted', {})


        while selected_numbers == previd:
            x = [0, 5, 10, 15]
            while True:
                selected_numbers = random.choices(x, k=3)
                if sum(selected_numbers) == 15:
                    break
        session.vars['previd'] = selected_numbers

        rand_nums = selected_numbers
        first_coord = str(rand_nums[0])
        sec_coord = str(rand_nums[1])
        third_coord = str(rand_nums[2])

        coord = "btn" + first_coord + "_" + sec_coord + "_" + third_coord

 
        if 'getTaskList' in data:
            return {0:{'howManyCompleted':session.vars['howManyCompleted']}}

        if 'printStatus' in data:
            print(session.vars['howManyCompleted'].get('task1', 'Task1 not set'))


        if 'buttonClicked' in data:
            print('Button was clicked')
            session.vars['howManyCompleted'][data['whichTask']]=True
            print(f"The first task is{session.vars['howManyCompleted'][data['whichTask']]}")
            print(session.vars['howManyCompleted'])

        print(len(session.vars['howManyCompleted']))
        if (len(session.vars['howManyCompleted']) == 2 and all(session.vars['howManyCompleted'])):
            # all the tasks have been completed
            print("All the tasks have been completed")
            return {0:{'allTasksCompleted':1}}


        if 'participants' in data:
            g.previousClicker = data['participants']

        if 'activeParticipants' in data:
            active_participants = data['activeParticipants']

        session.vars.setdefault('who_in_agreement', [])
        session.vars['numAgree'] = len(session.vars['who_in_agreement'])
        NumAgree = session.vars['numAgree']
        WhoAgrees = session.vars['who_in_agreement']

        if 'numInAgreement' in data:
            previousNumInAgreement = NumAgree
            if data['numInAgreement'] < 2:
                if previousNumInAgreement >= 2:
                    if any(participant in WhoAgrees for participant in active_participants):
                        WhoAgrees.clear()
                else:
                    WhoAgrees.clear()
                    list(map(lambda x: WhoAgrees.append(x), active_participants))
            else:
                WhoAgrees.clear()
                list(map(lambda x: WhoAgrees.append(x), active_participants))
                session.vars['numAgree'] = len(session.vars['who_in_agreement'])

        print(session.vars['who_in_agreement'])
        print(session.vars['numAgree'])

        if 'payoffs' in data:
            if data['payoffs']['5'] == g.previousClicker:
                g.previousClicker = data['payoffs']['5']
                round_num = player.round_number
                p1_score = data['payoffs']['1']
                p2_score = data['payoffs']['2']
                p3_score = data['payoffs']['3']
                time_stamp = data['payoffs']['7']
                time_since = float(data['payoffs']['8'])
                P1_agree = 1 if "clickedByUser1" in session.vars['who_in_agreement'] else 0
                P2_agree = 1 if "clickedByUser2" in session.vars['who_in_agreement'] else 0
                P3_agree = 1 if "clickedByUser3" in session.vars['who_in_agreement'] else 0
            currencyDecay = data['payoffs']['4']

            default_payoff = 0

            p1 = g.get_player_by_id(1)
            p1_payoff = data['payoffs']['1']
            if p1_payoff is None:
                p1.payoff = default_payoff
            p1.payoff = p1_payoff
            p1.currency = round(float(p1.payoff) * currencyDecay, 2)
            p1.ogCurrency = float(p1.payoff) * 3.00

            p2 = g.get_player_by_id(2)
            p2_payoff = data['payoffs'].get('2')
            if p2_payoff is None:
                p2.payoff = default_payoff
            p2.payoff = p2_payoff
            p2.currency = round(float(p2.payoff) * currencyDecay, 2)
            p2.ogCurrency = float(p2.payoff) * 3.00

            p3 = g.get_player_by_id(3)
            p3_payoff = data['payoffs'].get('3')
            if p3_payoff is None:
                p3.payoff = default_payoff
            p3.payoff = p3_payoff
            p3.currency = round(float(p3.payoff) * currencyDecay, 2)
            p3.ogCurrency = float(p3.payoff) * 3.00

            # Send payoffs to the client
            return {0: {'payoffs': {
                'p1': p1.currency,
                'p2': p2.currency,
                'p3': p3.currency,
            }}}

        if 'button_clicked' in data:
            return {0: {'button_id': data["button_id"], 'player_id': player.id_in_group}}




    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.custom_round_num += 1


class TutorialPage3(Page):
    @staticmethod
    def live_method(player,data):
        if 'button_clicked' in data:
            print(data['button_id'])
            print("lol")
            return {0: {'button_id': data["button_id"], 'origin_panel': data["origin_panel"], "button_clicked": data["button_clicked"],"panelId":data['panel_id']}}

class TutorialPage4(Page):

    @staticmethod
    def live_method(player, data):
        session = player.session
        g = player.group

        x = [0, 5, 10, 15]
        while True:
            selected_numbers = random.choices(x, k=3)
            if sum(selected_numbers) == 15:
                break

        session.vars.setdefault('previd', [])
        previd = session.vars['previd']

        session.vars.setdefault('taskList', {})

        session.vars.setdefault('alreadyFinished', False)

        while selected_numbers == previd:
            x = [0, 5, 10, 15]
            while True:
                selected_numbers = random.choices(x, k=3)
                if sum(selected_numbers) == 15:
                    break
        session.vars['previd'] = selected_numbers

        rand_nums = selected_numbers
        first_coord = str(rand_nums[0])
        sec_coord = str(rand_nums[1])
        third_coord = str(rand_nums[2])

        coord = "btn" + first_coord + "_" + sec_coord + "_" + third_coord

        if 'printStatus' in data:
            print(session.vars['taskList'].get('task1', 'Task1 not set'))


        if 'buttonClicked' in data:
            print('Button was clicked')
            session.vars['taskList'][data['whichTask']]=True
            print(f"The first task is{session.vars['taskList'][data['whichTask']]}")
            print(session.vars['taskList'])

        print(len(session.vars['taskList']))
        if not session.vars['alreadyFinished'] and len(session.vars['taskList']) == 4 and all(session.vars['taskList'].values()):
            # All the tasks have been completed for the first time
            print("All the tasks have been completed")
            session.vars['alreadyFinished'] = True
            return {0: {'allTasksCompleted': 1, 'tasksDone':session.vars['taskList']}}


        if data == "player1bot":
            return {0: {'button_id': coord, 'player_id': 2}}

        if data == "player2bot":
            return {0: {'button_id': coord, 'player_id': 3}}

        if 'participants' in data:
            g.previousClicker = data['participants']

        if 'activeParticipants' in data:
            active_participants = data['activeParticipants']

        session.vars.setdefault('who_in_agreement', [])
        session.vars['numAgree'] = len(session.vars['who_in_agreement'])
        NumAgree = session.vars['numAgree']
        WhoAgrees = session.vars['who_in_agreement']

        if 'numInAgreement' in data:
            previousNumInAgreement = NumAgree
            if data['numInAgreement'] < 2:
                if previousNumInAgreement >= 2:
                    if any(participant in WhoAgrees for participant in active_participants):
                        WhoAgrees.clear()
                else:
                    WhoAgrees.clear()
                    list(map(lambda x: WhoAgrees.append(x), active_participants))
            else:
                WhoAgrees.clear()
                list(map(lambda x: WhoAgrees.append(x), active_participants))
                session.vars['numAgree'] = len(session.vars['who_in_agreement'])

        print(session.vars['who_in_agreement'])
        print(session.vars['numAgree'])

        if 'payoffs' in data:
            if data['payoffs']['5'] == g.previousClicker:
                g.previousClicker = data['payoffs']['5']
                round_num = player.round_number
                p1_score = data['payoffs']['1']
                p2_score = data['payoffs']['2']
                p3_score = data['payoffs']['3']
                time_stamp = data['payoffs']['7']
                time_since = float(data['payoffs']['8'])
                P1_agree = 1 if "clickedByUser1" in session.vars['who_in_agreement'] else 0
                P2_agree = 1 if "clickedByUser2" in session.vars['who_in_agreement'] else 0
                P3_agree = 1 if "clickedByUser3" in session.vars['who_in_agreement'] else 0
            currencyDecay = data['payoffs']['4']

            default_payoff = 0

            p1 = g.get_player_by_id(1)
            p1_payoff = data['payoffs']['1']
            if p1_payoff is None:
                p1.payoff = default_payoff
            p1.payoff = p1_payoff
            p1.currency = round(float(p1.payoff) * currencyDecay, 2)
            p1.ogCurrency = float(p1.payoff) * 3.00

            p2 = g.get_player_by_id(2)
            p2_payoff = data['payoffs'].get('2')
            if p2_payoff is None:
                p2.payoff = default_payoff
            p2.payoff = p2_payoff
            p2.currency = round(float(p2.payoff) * currencyDecay, 2)
            p2.ogCurrency = float(p2.payoff) * 3.00

            p3 = g.get_player_by_id(3)
            p3_payoff = data['payoffs'].get('3')
            if p3_payoff is None:
                p3.payoff = default_payoff
            p3.payoff = p3_payoff
            p3.currency = round(float(p3.payoff) * currencyDecay, 2)
            p3.ogCurrency = float(p3.payoff) * 3.00

            # Send payoffs to the client
            return {0: {'payoffs': {
                'p1': p1.currency,
                'p2': p2.currency,
                'p3': p3.currency,
            }}}

        if 'button_clicked' in data:
            return {0: {'button_id': data["button_id"], 'player_id': player.id_in_group}}

        if 'getMeTaskList' in data:
            return {0:{'taskList':session.vars['taskList'],'alreadyFinished':session.vars['alreadyFinished']}}


class TutorialPage5(Page):
    pass


page_sequence = [TutorialPage1,TutorialPage2,TutorialPage3,TutorialPage4,TutorialPage5]








