from otree.api import *
import json
import random
import time



doc = """
Your app description
"""

totalRounds = 5
random_grouping = models.BooleanField(initial = True)          # true is random
rounds_payment = random.sample(range(1, totalRounds + 1), 3)
print(f"Selected payment rounds: {rounds_payment}")

tmp = 0

class C(BaseConstants):
    NAME_IN_URL = 'Main_Experiment'
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
    
        self.session.vars['enable_compulsory_offer'] = self.session.config.get('enable_compulsory_offer', False)



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
    countDownStarted = models.BooleanField(initial=False)  # Add this line for countdown tracking


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
    Time_Since_Round_Start = models.FloatField()
    Compulsory_offer = models.IntegerField()  # Add this field
    Button_ID = models.StringField()

class Main_Interface(Page):
    @staticmethod
    def vars_for_template(player):
        session = player.session
        # retrieve the stored compulsory offer data
        compulsory_offer_data = session.vars.get('whatButtonsClicked', {})


    @staticmethod
    def live_method(player, data):
        session = player.session
        g = player.group

        #return compulsory data 
        if 'send_compulsory_data' in data:
            print("compulsory data in data")
            compulsory_offer_data = session.vars.get('whatButtonsClicked', {})
            simulated_clicks = [
                {
                    'button_id': button_id,
                    'clicked_by': player_id
                }
                for player_id, button_id in compulsory_offer_data.items()
            ]
            return {0: {'simulated_clicks': simulated_clicks}}
        
        # handle timer start
        if 'timerStarted' in data:
            session.vars['beginningTime'] = float(data['timerStarted'])

        # track previous clicker
        if 'participants' in data:
            g.previousClicker = data['participants']

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
            
            if player_id == g.previousClicker:
                g.previousClicker = player_id
                time_since = float(data['payoffs']['time_since']) 
                since_beginning = (time_since - session.vars['beginningTime']) / 1000
                currency_decay = data['payoffs']['currency_decay'] 
                p1_agree = int("clickedByUser1" in who_agrees)
                p2_agree = int("clickedByUser2" in who_agrees)
                p3_agree = int("clickedByUser3" in who_agrees)
                print(f"[Main Experiment] Current agreement state (who_agrees): {who_agrees}")

                # create report entry
                Report.create(
                    Session_Code=g.session.code,
                    Subject_ID=player.participant.code,
                    Group_Num=g.id,
                    Round_Num=player.custom_round_num,
                    SubGroup_ID=player_id,
                    S1_Points=data['payoffs']['p1_points'], 
                    S2_Points=data['payoffs']['p2_points'], 
                    S3_Points=data['payoffs']['p3_points'],  
                    P1_Agree=p1_agree,
                    P2_Agree=p2_agree,
                    P3_Agree=p3_agree,
                    NumInAgreement=len(who_agrees),
                    Timestamp=data['payoffs']['timestamp'],
                    Compulsory_offer=0,
                    Time_Since_Round_Start=since_beginning
                )

                # update payoffs and currency for each player
                for player_id in [1, 2, 3]:
                    p = g.get_player_by_id(player_id)
                    p_payoff = data['payoffs'].get(f'p{player_id}_points', 0) 
                    p.payoff = p_payoff
                    p.currency = round(p_payoff * currency_decay, 2)
                    p.ogCurrency = p_payoff * 3.00

                # store round payoffs
                round_num = player.round_number
                round_payoffs = json.loads(player.round_payoffs)
                round_payoffs[str(round_num)] = {
                    'payoff': float(player.payoff),
                    'ogCurrency': float(player.ogCurrency),
                    'currency': float(player.currency)
                }
                player.round_payoffs = json.dumps(round_payoffs)

        # handle button click event
        if 'button_clicked' in data:

            current_button = data['button_id']
            player_id = player.id_in_group

            return {0: {'button_id': data["button_id"], 'player_id': player.id_in_group}}


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.custom_round_num += 1

        

class Round_Payoffs(Page):
    @staticmethod
    def live_method(player: Player, data: dict):
        if data.get('next_clicked'):
            return {player.id_in_group: 'next'}

class Round_Payoffs(Page):
    @staticmethod
    def live_method(player: Player, data: dict):
        if data.get('next_clicked'):
            return {player.id_in_group: 'next'}


class Questionnaire(Page):
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
        return 'Main_Experiment/Questionnaire.html'



class CompulsoryOffer(Page):

    @staticmethod
    def before_next_page(player,timeout_happened):
        session = player.session
        print("The buttons clicked during the compulsory offer round were:")
        print(session.vars['whatButtonsClicked'])
        session.vars['main_experiment_start_time'] = time.time()
        

    @staticmethod
    def live_method(player, data):
        session = player.session
        g = player.group


        # track previous clicker
        if 'participants' in data:
            print("3) tracked previous clicker to be",data['participants'])
            g.previousClicker = data['participants']

        # track active participants in agreement
        if 'activeParticipants' in data:
            active_participants = data['activeParticipants']
            print(f"[Compulsory Experiment] Active partcipants are: {who_agrees}")


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
            print("payofs is IN THE DATA!!!!!")
            print(data)
            player_id = data['payoffs']['player_id']
            if player_id == g.previousClicker:
                g.previousClicker = player_id
                time_since = float(data['payoffs']['time_since']) 
                currency_decay = data['payoffs']['currency_decay'] 

                p1_agree = int("clickedByUser1" in who_agrees)
                p2_agree = int("clickedByUser2" in who_agrees)
                p3_agree = int("clickedByUser3" in who_agrees)
                print(f"[Compulsory Experiment] Current agreement state (who_agrees): {who_agrees}")

                # create report entry
                Report.create(
                    Session_Code=g.session.code,
                    Subject_ID=player.participant.code,
                    Group_Num=g.id,
                    Round_Num=player.custom_round_num,
                    SubGroup_ID=player_id,
                    S1_Points=data['payoffs']['p1_points'], 
                    S2_Points=data['payoffs']['p2_points'], 
                    S3_Points=data['payoffs']['p3_points'],  
                    P1_Agree=p1_agree,
                    P2_Agree=p2_agree,
                    P3_Agree=p3_agree,
                    NumInAgreement=len(who_agrees),
                    Compulsory_offer=1,
                    Timestamp=data['payoffs']['timestamp'],
                )

                # update payoffs and currency for each player
                for player_id in [1, 2, 3]:
                    p = g.get_player_by_id(player_id)
                    p_payoff = data['payoffs'].get(f'p{player_id}_points', 0) 
                    p.payoff = p_payoff
                    p.currency = round(p_payoff * currency_decay, 2)
                    p.ogCurrency = p_payoff * 3.00

                # store round payoffs
                round_num = player.round_number
                round_payoffs = json.loads(player.round_payoffs)
                round_payoffs[str(round_num)] = {
                    'payoff': float(player.payoff),
                    'ogCurrency': float(player.ogCurrency),
                    'currency': float(player.currency)
                }
                player.round_payoffs = json.dumps(round_payoffs)
        # check how many players have clicked so far
        # if all players have clicked, then send back all Player's clicked

        # In the live method, adjust the handling of the button clicks:
        if 'button_clicked' in data:
            current_time = time.time()
            time_since_start = current_time - session.vars.get('compulsory_offer_start_time', current_time)
            player_id = player.id_in_group


            current_button = data['button_id']

            session.vars.setdefault('playersClicking', [])
            who_clicked = session.vars['playersClicking']

            session.vars.setdefault('whatButtonsClicked',{})
            #update what button clicked
            session.vars['whatButtonsClicked'][player.id_in_group]=current_button

            # Add the current player to the list if they haven't clicked yet
            if player.id_in_group not in who_clicked:
                who_clicked.append(player.id_in_group)

            # Store button click state for the player (store the clicked button)
            session.vars.setdefault(f'player_{player.id_in_group}_click', data['button_id'])


            # Check if all players have clicked
            allPlayersClicked = len(who_clicked) == 3

            if allPlayersClicked:
                print("ALL PLAYERS HAVE CLICKED")

                #if the random proposer treatment is on
                if session.config.get('random_proposer_treatment', False):
                    # Randomly select one button to display as the "random proposer"
                    if 'selected_button' not in session.vars:
                        selected_player_id = random.choice(list(session.vars['whatButtonsClicked'].keys()))
                        selected_button = session.vars['whatButtonsClicked'][selected_player_id]
                        session.vars['selected_button'] = {
                            'button_id': selected_button,
                            'player_id': selected_player_id,
                        }
                    # Return the selected button and notify all players
                        print('selected button is',)
                        return {
                            0: {
                                'selected_button': session.vars['selected_button']['button_id'],
                                'selected_player': session.vars['selected_button']['player_id'],
                                'players_info': session.vars['whatButtonsClicked'],
                                'allPlayersClicked': True,
                            }
                        }
                #otherwise, just let everyone know which buttons clicked
                return {0: {'button_id': data['button_id'], 'player_id': player.id_in_group, 'players_info': session.vars['whatButtonsClicked'],'allPlayersClicked':allPlayersClicked}}
            
            print("4) returning button_id",data['button_id'],"clicked by",player.id_in_group,"with",session.vars['whatButtonsClicked'],"and if all players clicked or not",allPlayersClicked)
            # Otherwise, return only the current player's click info
            return {0: {'button_id': data['button_id'], 'player_id': player.id_in_group, 'players_info': session.vars['whatButtonsClicked'],'allPlayersClicked':allPlayersClicked}}

class Experiment_End(Page):
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




page_sequence = [WaitingRoom,CompulsoryOffer, Main_Interface, Round_Payoffs] * totalRounds + [Questionnaire, Experiment_End]

print(f"Total pages: {len(page_sequence)}")
for i, page in enumerate(page_sequence):
    print(f"Page {i + 1}: {page.__name__}")


def custom_export(players):
    yield ['Session_Code','Subject_ID', 'Group_Num', 'Round_Num', 'SubGroup_ID', 'S1_Points', 'S2_Points', 'S3_Points','P1_Agree','P2_Agree','P3_Agree', 'NumInAgreement', 'Timestamp','Compulsory_offer','Time_Since_Round_Start']
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
            reports[report_no].Compulsory_offer,
            reports[report_no].Time_Since_Round_Start
        ]
    for report in reports:
        report.delete()





