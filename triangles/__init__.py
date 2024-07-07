from otree.api import *
import json
import random


doc = """
Your app description
"""

totalRounds = 5
random_grouping = models.BooleanField(initial = True)          # true is random
rounds_payment = random.sample(range(1, totalRounds + 1), 3)
print(f"Selected payment rounds: {rounds_payment}")

tmp = 0

class C(BaseConstants):
    NAME_IN_URL = 'triangles'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1          # number of cycles of the entire game
    NUM_ROUNDS_FOR_PAYMENT = 3



class Subsession(BaseSubsession):
    def creating_session(self):
        if random_grouping:
            self.group_randomly()
        else:
            self.group_fixed()

        self.session.vars['payment_rounds'] = rounds_payment

        for player in self.get_players():
            player.round_payoffs = json.dumps({})


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
    custom_round_num = models.IntegerField(initial=1)
    round_payoffs = models.LongStringField(initial='{}')
    question_6_bonus = models.CurrencyField(initial = 1) #changeable question 6 variable

    # Question 5
    noticed_icons = models.StringField(
        label="5. Did you notice the icons with the sex of the participants on the screen when negotiating how to split the money?",
        choices=["Yes", "No"],
        widget=widgets.RadioSelect
    )

    # Question 6
    group_composition = models.StringField(
        label=f"6. What was the composition of the other two members in your group?  If you did not notice the icons, please provide your best guess. If you answer this question correctly you will earn a bonus of ${question_6_bonus}",
        choices=["2 women", "2 men", "1 man and 1 woman"]
    )

    # Question 7
    preferences = models.StringField(
        label="7. Which of the following best describes your preferences:",
        choices=[
            "I prefer to make the first offer in the game.",
            "I prefer to wait and see what others will propose."
        ]
    )

    # Question 8
    acceptability_scale = models.StringField(
        label="8. If two people are in agreement and are assigning me 0 token:",
        choices=[
            "I actively try to break the agreement by making an offer to share the money with only one them.",
            "I actively try to break the agreement by making an offer that shares the money with all players.",
            "I do no try to break the agreement."
        ]
    )

    # Question 9
    zero_acceptability = models.IntegerField(
        label="9. Suppose that two people are in agreement and are assigning me 0 tokens. On a scale from 1 to 10, how socially acceptable is it to try to break the agreement between them?",
        min=0, max=10
    )

    # Question 10
    masculinity_scale = models.IntegerField(
        label="10. In general, how do you see yourself? Where would you put yourself on this scale (0-10) from “0 = Very masculine” to “10 = Very feminine”? Please indicate your response below.",
        min=0, max=10
    )

    # Question 11
    q11a_acceptability_split = models.IntegerField(
        label="11. Consider the following situation: 'A group of three people are negotiating how to split a sum of money. At least two of them must agree on the split.' addspace a. In your view, how acceptable is it to split the money only between two people, with the third person getting nothing?",
        min=1, max=7,
        help_text="1 = completely unacceptable, 7 = completely acceptable"
    )
    q11b_likelihood_split = models.IntegerField(
        label="b. If three people in this country were to find themselves in this situation, how likely is it that the money will be split only between two of them, with the third person getting nothing?",
        min=1, max=7,
        help_text="1 = extremely unlikely, 7 = extremely likely"
    )

    # Question 12
    q12a_board_acceptability_split = models.IntegerField(
        label="12. Consider the following situation: 'A group of three members of a company's board are tasked with negotiating how to split a sum of 'bonus' money.At least two of them must agree on the split. addspace a. In your view, how acceptable is it to split the money only between two people, with the third person getting nothing?",
        min=1, max=7,
        help_text="1 = completely unacceptable, 7 = completely acceptable"
    )
    q12b_board_likelihood_split = models.IntegerField(
        label="b. If three people in this country were to find themselves in this situation, how likely is it that the money will be split only between two of them, with the third person getting nothing?",
        min=1, max=7,
        help_text="1 = extremely unlikely, 7 = extremely likely"
    )

    # Question 13
    risk_willingness = models.IntegerField(
        label="13. On a scale from 1 to 10 how willing are you to take risks in general? (1 = not at all willing to take risks, and 10 = very willing to take risks)",
        min=1, max=10
    )

    # Question 14
    negotiation_enjoyment = models.IntegerField(
        label="14. On a scale from 1 to 10 how much do you enjoy negotiations in general? (1 = do not enjoy negotiations, and 10 = enjoy negotiations a lot)",
        min=1, max=10
    )

    # Question 15
    winning_enjoyment = models.IntegerField(
        label="15. On a scale from 1 to 10 how much do you enjoy winning? (1 = do not enjoy winning, 10 = enjoy winning a lot)",
        min=1, max=10
    )

    # Question 16
    negotiation_self_view = models.IntegerField(
        label="16. On a scale from 1 to 10 how do you see yourself? (1 = I consider myself to be a bad negotiator, 10 = I consider myself an excellent negotiator)",
        min=1, max=10
    )

    # Question 17
    unemployment_belief = models.IntegerField(
        label="17. In the following statements, select the position in the 1 to 10 scale that best represents you. &nbsp; a. People who are unemployed ought to take any offered job to keep welfare support",
        min=1, max=10,
        help_text="1 = People who are unemployed ought to take any offered job to keep welfare support, 10 = People who are unemployed ought to be able to refuse any job they do not want"
    )
    competition_belief = models.IntegerField(
        label="b. Competition is good",
        min=1, max=10,
        help_text="1 = Competition is good, 10 = Competition is damaging"
    )
    income_distribution_belief = models.IntegerField(
        label="c. The income distribution ought to be more equal",
        min=1, max=10,
        help_text="1 = The income distribution ought to be more equal, 10 = There ought to be more economic incentive for the individual to work harder"
    )
    privatization_belief = models.IntegerField(
        label="d. More public companies ought to be privatized",
        min=1, max=10,
        help_text="1 = More public companies ought to be privatized, 10 = More companies ought to be state-owned"
    )



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

        # print(session.vars['who_in_agreement'])
        # print(session.vars['numAgree'])


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
                Report.create(Session_Code=g.session.code,Subject_ID=player.participant.code,Group_Num=g.id,Round_Num=player.custom_round_num,SubGroup_ID=data['payoffs']['5'], S1_Points=p1_score, S2_Points=p2_score, S3_Points=p3_score, P1_Agree=P1_agree, P2_Agree=P2_agree,P3_Agree=P3_agree,NumInAgreement=len(session.vars['who_in_agreement']), Timestamp=time_stamp,Time_Since_Round_Start=since_beginning)
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

                # print("1")
                # print(p1.payoff)
                # print(p2.payoff)
                # print(p3.payoff)

                round_payoffs = json.loads(player.round_payoffs)
                round_payoffs[str(round_num)] = {
                    'payoff': float(player.payoff),
                    'ogCurrency': float(player.ogCurrency),
                    'currency': float(player.currency)
                }
                player.round_payoffs = json.dumps(round_payoffs)

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


class QuestionnairePage(Page):
    form_model = 'player'
    form_fields = [
        'noticed_icons', 'group_composition', 'preferences', 'acceptability_scale',
        'zero_acceptability', 'masculinity_scale',
        'q11a_acceptability_split', 'q11b_likelihood_split',
        'q12a_board_acceptability_split', 'q12b_board_likelihood_split',
        'risk_willingness', 'negotiation_enjoyment', 'winning_enjoyment', 'negotiation_self_view',
        'unemployment_belief', 'competition_belief', 'income_distribution_belief', 'privatization_belief'
    ]

    def get_template_name(self):
        return 'triangles/QuestionnairePage.html'



class FinalPage(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.custom_round_num = 1     # reset at the final page

    @staticmethod
    def vars_for_template(player: Player):
        round_payoffs = json.loads(player.round_payoffs)
        payment_details = {round_num: round_payoffs.get(str(round_num), {}).get('currency', 0) for round_num in
                           rounds_payment}

        return {
            'payment_rounds': rounds_payment,
            'payment_details': payment_details,
            'total_payment': sum(payment_details.values())
        }


page_sequence = [WaitingRoom, MyPage, ResultsPage] * totalRounds + [QuestionnairePage, FinalPage]

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





