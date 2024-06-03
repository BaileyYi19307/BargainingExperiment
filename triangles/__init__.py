from otree.api import *

doc = """
Your app description
"""

totalRounds = 5
random_grouping = models.BooleanField(initial = True)          # true is random


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

class Player(BasePlayer):
    ogCurrency = models.FloatField(initial=0)
    currency = models.FloatField(initial=0)
    custom_round_num = models.IntegerField(initial=1)       # manual round number

# PAGES
class WaitingRoom(WaitPage):
    group_by_arrival_time = False
    title_text = "Waiting Room"
    body_text = "Wait for everyone to join before proceeding"

class Report(ExtraModel):
    Session_Code=models.StringField(initial="")
    Subject_ID = models.StringField(initial="")
    Group_Num = models.IntegerField()
    Round_Num = models.IntegerField(initial=0)
    SubGroup_ID = models.IntegerField(initial=0)
    S1_Points = models.IntegerField(initial=0)
    S2_Points = models.IntegerField(initial=0)
    S3_Points = models.IntegerField(initial=0)
    P1_Agree=models.IntegerField(initial=0)
    P2_Agree=models.IntegerField(initial=0)
    P3_Agree=models.IntegerField(initial=0)
    NumInAgreement = models.IntegerField()
    Timestamp = models.StringField()
    Time_Since_Round_Start= models.FloatField()


class MyPage(Page):
    @staticmethod
    def live_method(player, data):
        session=player.session
        g = player.group

        if 'timerStarted' in data:
            session.vars['beginningTime']=float(data['timerStarted'])

        if 'participants' in data:
            g.previousClicker = data['participants']

        if 'activeParticipants' in data:
            active_participants=data['activeParticipants']

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
                        pass
                else: # only one participant is clicking on the button being updated
                    WhoAgrees.clear()
                    list(map(lambda x: WhoAgrees.append(x), active_participants))
            else:
                WhoAgrees.clear()
                list(map(lambda x: WhoAgrees.append(x), active_participants))
                session.vars['numAgree'] = len(session.vars['who_in_agreement'])

        print(session.vars['who_in_agreement'])
        print(session.vars['numAgree'])


        if 'payoffs' in data:
            if data['payoffs']['5'] is g.previousClicker:
                g.previousClicker=data['payoffs']['5']
                round_num=player.round_number
                p1_score=data['payoffs']['1']
                p2_score=data['payoffs']['2']
                p3_score=data['payoffs']['3']
                time_stamp=data['payoffs']['7']
                time_since=float(data['payoffs']['8'])
                since_beginning=(time_since-session.vars['beginningTime'])/1000
                #change 150 to the maximum amount of time the session has
                # currency_decay=100*((3-data['payoffs']['4'])/2) #decreases at a rate of 0.02 per second
                # time_stamp=150-currency_decay
                P1_agree = 1 if "clickedByUser1" in session.vars['who_in_agreement'] else 0
                P2_agree = 1 if "clickedByUser2" in session.vars['who_in_agreement'] else 0
                P3_agree = 1 if "clickedByUser3" in session.vars['who_in_agreement'] else 0

                if P1_agree or P2_agree or P3_agree:
                  Report.create(
                      Session_Code=g.session.code,
                      Subject_ID=player.participant.code,
                      Group_Num=g.id,Round_Num=player.custom_round_num,
                      SubGroup_ID=data['payoffs']['5'],
                      S1_Points=p1_score,
                      S2_Points=p2_score,
                      S3_Points=p3_score,
                      P1_Agree=P1_agree,
                      P2_Agree=P2_agree,
                      P3_Agree=P3_agree,
                      NumInAgreement=len(session.vars['who_in_agreement']),
                      Timestamp=time_stamp,
                      Time_Since_Round_Start=since_beginning
                    )
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

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.custom_round_num += 1

class ResultsPage(Page):
    @staticmethod
    def live_method(player: Player, data: dict):
        if data.get('next_clicked'):
            return {player.id_in_group: 'next'}



class FinalPage(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.custom_round_num = 1     # reset at the final page


page_sequence = [WaitingRoom, MyPage, ResultsPage] * totalRounds + [FinalPage]

print(f"Total pages: {len(page_sequence)}")
for i, page in enumerate(page_sequence):
    print(f"Page {i + 1}: {page.__name__}")


def custom_export(players):
    yield ['Session_Code','Subject_ID', 'Group_Num', 'Round_Num', 'SubGroup_ID', 'S1_Points', 'S2_Points', 'S3_Points','P1_Agree','P2_Agree','P3_Agree', 'NumInAgreement', 'Timestamp','Time_Since_Round_Start']
    reports = Report.filter()
    for report_no in range(len(reports)):
        yield [
            reports[report_no].Session_Code,
            reports[report_no].Subject_ID,
            reports[report_no].Group_Num,
            reports[report_no].Round_Num,
            reports[report_no].SubGroup_ID,
            reports[report_no].S1_Points,
            reports[report_no].S2_Points,
            reports[report_no].S3_Points,
            reports[report_no].P1_Agree,
            reports[report_no].P2_Agree,
            reports[report_no].P3_Agree,
            reports[report_no].NumInAgreement,
            reports[report_no].Timestamp,
            reports[report_no].Time_Since_Round_Start
        ]
    for report in reports:
        report.delete()



