from otree.api import *

doc = """
Your app description
"""

totalRounds = 5         # number of rounds being played
random_grouping = models.BooleanField(initial = True)


class C(BaseConstants):
    NAME_IN_URL = 'triangles'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1          # number of cycles of the entire game


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
    previousClicker=models.IntegerField(initial=0)
    howManyInAgreement=models.IntegerField(initial=0)
    agreementTimerStarted=models.BooleanField(initial=False)



class Player(BasePlayer):
    ogCurrency = models.FloatField(initial=0)
    currency = models.FloatField(initial=0)

# PAGES
class WaitingRoom(WaitPage):
    group_by_arrival_time = False
    title_text = "Waiting Room"
    body_text = "Wait for everyone to join before proceeding"

class Report(ExtraModel):
    subjectId = models.StringField(initial="")
    group = models.Link(Group)
    round = models.IntegerField(initial=0)
    subidgroup = models.IntegerField(initial=0)
    s1 = models.IntegerField(initial=0)
    s2 = models.IntegerField(initial=0)
    s3 = models.IntegerField(initial=0)
    numAgreement = models.IntegerField(initial=0)
    timestamp = models.FloatField(initial=0)



class MyPage(Page):
    @staticmethod
    def live_method(player, data):
        g = player.group
        print(f"Initial data received: {data}") 

        print(f"Initial state: TimerStarted={g.agreementTimerStarted}, HowManyInAgreement={g.howManyInAgreement}")

        if 'participants' in data:
            g.previousClicker = data['participants']

        if 'payoffs' in data and '6' in data['payoffs']:
            timer_status = data['payoffs']['6']
            g.agreementTimerStarted = (timer_status == "Started")
            print(f"Agreement timer status received: {timer_status}")
            print(f"Agreement timer changed to: {g.agreementTimerStarted}")

        if g.agreementTimerStarted:
            if 'numInAgreement' in data: # arrived
                current_agreements = int(data['numInAgreement'])
                print(f"Received numInAgreement: {current_agreements}")
                if current_agreements >= 2:
                    g.howManyInAgreement = current_agreements
                    # do nothing if less than 2 while the timer is active
                    print(f"Updated within timer active: {g.howManyInAgreement}")
        else:
            if 'numInAgreement' in data: # arrived
                current_agreements = int(data['numInAgreement'])
                g.howManyInAgreement = current_agreements  # always update if timer not active
                print(f"Updated with timer inactive: {g.howManyInAgreement}")
                
        print(f"Final state: TimerStarted={g.agreementTimerStarted}, HowManyInAgreement={g.howManyInAgreement}")

        if 'payoffs' in data:
            if data['payoffs']['5'] is g.previousClicker:
                print(f"The previous clicker was participant{g.previousClicker}")
                g.previousClicker=data['payoffs']['5']
                round_num=player.round_number
                p1_score=data['payoffs']['1']
                p2_score=data['payoffs']['2']
                p3_score=data['payoffs']['3']
                #change 150 to the maximum amount of time the session has
                currency_decay=100*((3-data['payoffs']['4'])/2) #decreases at a rate of 0.02 per second
                time_stamp=150-currency_decay
                print(f"The round is {round_num}")
                print(f"The data is as follows:{data}")
                print(f"There are {g.howManyInAgreement} players in agreement")
                Report.create(subjectId=player.participant.id_in_session,round=g.round_number,subidgroup=data['payoffs']['5'], s1=p1_score, s2=p2_score, s3=p3_score, numAgreement=g.howManyInAgreement, timestamp=time_stamp)
            currencyDecay = data['payoffs']['4']

            # Ensure default values if None is found
            default_payoff = 0

            p1 = g.get_player_by_id(1)
            p1_payoff = data['payoffs']['1']
            if p1_payoff is None:
                p1.payoff = default_payoff
            p1.payoff=p1_payoff
            p1.currency = round(float(p1.payoff) * currencyDecay,2)
            p1.ogCurrency = float(p1.payoff) * 3.00 

            p2 = g.get_player_by_id(2)
            p2_payoff = data['payoffs'].get('2')
            if p2_payoff is None:
                p2.payoff = default_payoff
            p2.payoff = p2_payoff
            p2.currency = round(float(p2.payoff) * currencyDecay,2)
            p2.ogCurrency = float(p2.payoff) * 3.00 


            p3 = g.get_player_by_id(3)
            p3_payoff = data['payoffs'].get('3')
            if p3_payoff is None:
                p3.payoff = default_payoff
            p3.payoff=p3_payoff
            p3.currency = round(float(p3.payoff) * currencyDecay,2)
            p3.ogCurrency = float(p3.payoff) * 3.00


        if 'button_clicked' in data:
            return {0: {'button_id': data["button_id"], 'player_id': player.id_in_group}}

class ResultsPage(Page):
    @staticmethod
    def live_method(player: Player, data: dict):
        if data.get('next_clicked'):
            return {player.id_in_group: 'next'}



class FinalPage(Page):
    pass


page_sequence = [WaitingRoom, MyPage, ResultsPage] * totalRounds + [FinalPage]

print(f"Total pages: {len(page_sequence)}")
for i, page in enumerate(page_sequence):
    print(f"Page {i + 1}: {page.__name__}")

def custom_export(players):
    yield ['subjectId', 'group', 'round', 'subidgroup', 's1', 's2', 's3', 'numAgreement', 'timestamp']
    reports = Report.filter()
    for report_no in range(len(reports)-1):
        yield [
            reports[report_no].subjectId,
            reports[report_no].group,
            reports[report_no].round,
            reports[report_no].subidgroup,
            reports[report_no].s1,
            reports[report_no].s2,
            reports[report_no].s3,
            reports[report_no].numAgreement,
            reports[report_no].timestamp,
        ]
    for report in reports:
        report.delete()
