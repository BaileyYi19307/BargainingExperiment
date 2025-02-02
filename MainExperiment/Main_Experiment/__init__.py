from otree.api import *
import json
import random
import time

doc = """
Your app description
"""

totalRounds = 3 #how many iterations of the experiment
howManyRounds=2 #how many rounds selected for final payout


random_grouping = models.BooleanField(initial = True)  # true is random
rounds_payment = random.sample(range(1, totalRounds + 1), howManyRounds)
print(f"Selected payment rounds: {rounds_payment}")

tmp = 0

class C(BaseConstants):
    NAME_IN_URL = 'Main_Experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1          # number of cycles of the entire game
    NUM_ROUNDS_FOR_PAYMENT = 3


global enable_compuslory_offer

class Subsession(BaseSubsession):
    def creating_session(self):
        if random_grouping:
            self.group_randomly()
        else:
            self.group_fixed()

        self.session.vars['payment_rounds'] = rounds_payment

        for player in self.get_players():
            player.round_payoffs = json.dumps({})
    
        enable_compulsory_offer = self.session.config.get('enable_compulsory_offer', False)

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
    firstOfferSubmitted = models.StringField(initial=None)  # Add this line for countdown tracking
    all_mpl_choices = models.LongStringField(initial='{}')  # Store choices from all rounds as JSON
    all_round_currencies = models.LongStringField(initial='{}')  # Store all round currencies as JSON
    pointsEarned = models.FloatField(initial=0)  # Default to 0



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
    Compulsory_offer = models.IntegerField()
    Button_ID = models.StringField()
    Random_Proposer_Treatment=models.IntegerField()

class Main_Interface(Page):
    @staticmethod
    def vars_for_template(self):
        return{
            'totalNodes':self.session.config['totalNodes'],  
            'totalPoints':self.session.config['totalPoints'],
            'initialCurrencyValue':self.session.config['initialCurrencyValue'],
            'ratificationTime':self.session.config['ratificationTime'],
            'timeLimit':self.session.config['timeLimit'],
        }


    @staticmethod
    def live_method(player, data):
        session = player.session
        groupId = player.group
        session.vars.setdefault('beginningTime', 0)

        #return compulsory data 
        if 'send_compulsory_data' in data:
            compulsory_offer_data = session.vars.get('whosClickedWhat', {})
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
                time_since = float(data['payoffs']['time_since']) 
                since_beginning = (time_since - session.vars['beginningTime']) / 1000

                currency_decay = data['payoffs']['currency_decay'] 
                p1_agree = int("clickedByUser1" in who_agrees)
                p2_agree = int("clickedByUser2" in who_agrees)
                p3_agree = int("clickedByUser3" in who_agrees)

                # create report entry
                Report.create(
                    Session_Code=groupId.session.code,
                    Subject_ID=player.participant.code,
                    Group_Num=groupId.id,
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
                    Random_Proposer_Treatment=0,
                    Compulsory_offer=0,
                    Time_Since_Round_Start=since_beginning
                )

                for player_id in [1, 2, 3]:
                    p = groupId.get_player_by_id(player_id)
                    p_payoff = data['payoffs'].get(f'p{player_id}_points', 0)

                    p.pointsEarned = round(p_payoff, 2)  # Assign the rounded payoff to pointsEarned
                    # Round all calculations to two decimal places
                    p.payoff = p_payoff
                    p.currency = round(p_payoff * currency_decay, 2)
                    p.ogCurrency = round(p_payoff * 3.00, 2)

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
        # fetch the current round's currency
        current_round = player.custom_round_num
        current_currency = player.currency
        
        # load existing round currencies
        all_round_currencies = json.loads(player.all_round_currencies)
        
        # update with the current round's data
        all_round_currencies[str(current_round)] = current_currency
        
        # save back to the field
        player.all_round_currencies = json.dumps(all_round_currencies)
        
        # debugging output
        print(f"Updated All Round Currencies: {all_round_currencies}")

        #reset before next round:
        session = player.session
        session.vars['who_in_agreement'] = []
        session.vars['submittedFirstOffer'] = {"player1": None, "player2": None, "player3": None}
        session.vars['buttonClickStates'] = {}
        session.vars['whosClickedWhat'] = {1: "", 2: "", 3: ""}
        session.vars['playersClicking'] = []
        player.custom_round_num += 1

        

class Round_Payoffs(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.pointsEarned is None:
            player.pointsEarned = 0 
        print(f"Player {player.id_in_group} - Points Earned: {player.pointsEarned}")

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
    def vars_for_template(self):
        return{
            'totalNodes':self.session.config['totalNodes'],  
            'totalPoints':self.session.config['totalPoints'],
            'initialCurrencyValue':self.session.config['initialCurrencyValue'],
            'ratificationTime':self.session.config['ratificationTime'],
            'timeLimit':self.session.config['timeLimit'],
        }

    def is_displayed(player):
        # only display this page if the treatment is enabled
        return player.session.config.get('compulsory_offer_treatment', False)

    @staticmethod
    def before_next_page(player,timeout_happened):
        session = player.session
        session.vars['main_experiment_start_time'] = time.time()

    @staticmethod
    def live_method(player, data): #receives data from client
        session = player.session
        groupId = player.group
        playerId=player.id_in_group

        # track previous clicker
        if 'participants' in data:
            groupId.previousClicker = data['participants']

        # track active participants in agreement
        if 'activeParticipants' in data:
            active_participants = data['activeParticipants']

        if 'experiment_started' in data:
            session.vars['experiment_started'] = float(data['experiment_started'])

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
            buttonClicked=data['payoffs']['button_id']
            current_button_state = session.vars['buttonClickStates'][buttonClicked]

            player_id = data['payoffs']['player_id']
            if player_id == groupId.previousClicker:
                groupId.previousClicker = player_id
                time_since = float(data['payoffs']['time_since']) 
                currency_decay = data['payoffs']['currency_decay'] 
                since_beginning = (time_since - session.vars['experiment_started']) / 1000
                
                random_proposer_treatment = 1 if session.config.get('random_proposer_treatment', False) else 0

                p1_agree = int(current_button_state["clickedByUser1"])
                p2_agree = int(current_button_state["clickedByUser2"])
                p3_agree = int(current_button_state["clickedByUser3"])

                # create report entry
                Report.create(
                    Session_Code=groupId.session.code,
                    Subject_ID=player.participant.code,
                    Group_Num=groupId.id,
                    Round_Num=player.custom_round_num,
                    SubGroup_ID=player_id,
                    S1_Points=data['payoffs']['p1_points'], 
                    S2_Points=data['payoffs']['p2_points'], 
                    S3_Points=data['payoffs']['p3_points'],  
                    P1_Agree=p1_agree,
                    P2_Agree=p2_agree,
                    P3_Agree=p3_agree,
                    NumInAgreement=p1_agree+p2_agree+p3_agree,
                    Compulsory_offer=1,
                    Random_Proposer_Treatment=random_proposer_treatment,
                    Timestamp=data['payoffs']['timestamp'],
                    Time_Since_Round_Start=since_beginning
                )

                # update payoffs and currency for each player
                for player_id in [1, 2, 3]:
                    p = groupId.get_player_by_id(player_id)
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


        #how many players have submitted a first offer?
        submittedFirstOffer=session.vars.setdefault('submittedFirstOffer', {"player1":None,"player2":None,"player3":None})


        #has a first offer been submitted? 
        if 'firstOfferSubmitted' in data:   
            #yes, mark it so that player X has submitted first offer
            submittedFirstOffer[f"player{playerId}"]=True
            #check if all players have submitted a first offer
            allFirstOffersSubmitted=all(offerSubmitted==True for offerSubmitted in submittedFirstOffer.values())
            #if they have, send back "allFirstOffersSubmitted"
            if allFirstOffersSubmitted:
                return {
                0: {
                    'button_id': session.vars['whosClickedWhat'][playerId],
                    'player_id': player.id_in_group,
                    'players_info': session.vars['whosClickedWhat'],
                    'allFirstOffersSubmitted': allFirstOffersSubmitted,
                    'firstOfferSubmitted': submittedFirstOffer
                }
            }
            #otherwise, just send back that this player has submitted a first offer
            else:
                return {0:{'firstOfferSubmitted': submittedFirstOffer}}


        #if a button has been clicked
        if 'button_clicked' in data:
            #record some variables
            current_time = time.time()
            time_since_start = current_time - session.vars.get('compulsory_offer_start_time', current_time)
            player_id = player.id_in_group
            current_button = data['button_id']

            # initialize submittedFirstOffer if not already done
            submittedFirstOffer = session.vars.setdefault(
                'submittedFirstOffer', {"player1": None, "player2": None, "player3": None}
            )

            # check if the player's first offer is already submitted
            if submittedFirstOffer[f"player{player_id}"] == True:
                # if yes, no further changes allowed
                return {
                    player_id: {
                        'message': 'Your first offer has already been submitted. No changes allowed.',
                        'button_id': session.vars['whosClickedWhat'][player_id],  # send their last clicked button
                        'players_info': session.vars.get('whosClickedWhat', {}),
                        'allPlayersClicked': False,
                    }
                }

            # proceed with button click handling if the player is not locked
            session.vars.setdefault('buttonClickStates', {})
            session.vars['buttonClickStates'].setdefault(current_button, {
                'clickedByUser1': False,
                'clickedByUser2': False,
                'clickedByUser3': False,
            })

            # toggle the button click state
            player_key = f'clickedByUser{player_id}'
            current_state = session.vars['buttonClickStates'][current_button][player_key]
            session.vars['buttonClickStates'][current_button][player_key] = not current_state

            # track who has clicked what
            session.vars.setdefault('whosClickedWhat', {1: "", 2: "", 3: ""})
            whosClickedWhat = session.vars['whosClickedWhat']

            if whosClickedWhat[player_id] == current_button:
                whosClickedWhat[player_id] = ""
            else:
                whosClickedWhat[player_id] = current_button

            # add the player to the list of who clicked
            session.vars.setdefault('playersClicking', [])
            who_clicked = session.vars['playersClicking']
            if player_id not in who_clicked:
                who_clicked.append(player_id)

            # Check if all players have clicked
            allFirstOffersSubmitted=all(offerSubmitted==True for offerSubmitted in submittedFirstOffer.values())
            

            if allFirstOffersSubmitted:
                #deal with the random proposer treatment
                if session.config.get('random_proposer_treatment', False):
                    if 'selected_button' not in session.vars:
                        selected_player_id = random.choice(list(whosClickedWhat.keys()))
                        selected_button = whosClickedWhat[selected_player_id]
                        session.vars['selected_button'] = {
                            'button_id': selected_button,
                            'player_id': selected_player_id,
                        }
                    return {
                        0: {
                            'selected_button': session.vars['selected_button']['button_id'],
                            'selected_player': session.vars['selected_button']['player_id'],
                            'players_info': whosClickedWhat,
                            'button_id': data['button_id'],
                            'allFirstOffersSubmitted': allFirstOffersSubmitted,
                        }
                    }

            return {
                0: {
                    'button_id': data['button_id'],
                    'player_id': player.id_in_group,
                    'players_info': whosClickedWhat,
                    'allFirstOffersSubmitted': allFirstOffersSubmitted,
                }
            }

class Experiment_End(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.custom_round_num = 1  # Reset at the final page

    @staticmethod
    def vars_for_template(player: Player):
        # Load round payoffs and calculate points
        all_round_currencies = json.loads(player.all_round_currencies)
        exchange_rate = player.session.config['initialCurrencyValue']  # Exchange rate (e.g., 1 point = 3 USD)
        all_round_points = {
            round_num: round(currency / exchange_rate, 2)
            for round_num, currency in all_round_currencies.items()
        }

        # Load MPL choices
        all_mpl_choices = json.loads(player.all_mpl_choices)

        # Select two random payment rounds and sort them
        payment_rounds = sorted(rounds_payment)

        total_payoff = 0
        payment_details = []

        # Calculate payoff details for the selected rounds
        for round_num in payment_rounds:
            round_str = str(round_num)
            round_currency = all_round_currencies.get(round_str, 0)
            round_points = all_round_points.get(round_str, 0)
            mpl_choices = all_mpl_choices.get(round_str, [])

            # Randomly decide between negotiation and MPL
            use_negotiation = random.choice([True, False])
            round_detail = {"round": round_num, "show_points": False}  # Default show_points to False
            fixed_money = None  


            if use_negotiation:
                # Negotiation chosen
                round_detail.update({
                    "payment_type": "Negotiation",
                    "points_earned": round_points,
                    "money_earned": round_currency,
                    "mpl_row": None,
                    "mpl_choice": None,
                    "show_points": True,  # Points are shown for negotiation
                    "details": "Payoff was determined through negotiation",
                })
                total_payoff += round_currency
            else:
                # MPL chosen
                if mpl_choices:
                    selected_index = random.randint(0, len(mpl_choices) - 1)
                    selected_value = mpl_choices[selected_index]
                    if selected_value == -1:  # Negotiation selected via MPL
                        round_detail.update({
                            "payment_type": "Multi-Price List",
                            "points_earned": round_points,
                            "money_earned": round_currency,
                            "mpl_row": selected_index,
                            "show_points": True,  # Points are shown for negotiation
                            "mpl_choice": "Negotiation",
                            "details": f"The row chosen was {selected_index}. You chose \"Negotiation\" over a fixed payout of {fixed_money} for this row",
                        })
                        total_payoff += round_currency
                    else:
                        # Fixed amount selected
                        fixed_money = int(selected_value)
                        fixed_points = round(fixed_money / exchange_rate, 2)
                        round_detail.update({
                            "payment_type": "Multi-Price List",
                            "points_earned": fixed_points,
                            "money_earned": fixed_money,
                            "show_points": False,  # Points are hidden for fixed money
                            "mpl_row": selected_index,
                            "mpl_choice": "Fixed Money",
                            "details": f"The row chosen was {selected_index}. You chose a fixed payout of {fixed_money} USD over \"Negotiation\" for this row",
                        })
                        total_payoff += fixed_money
                else:
                    # No MPL choices available
                    round_detail.update({
                        "payment_type": "Multi-Price List",
                        "points_earned": 0,
                        "money_earned": 0,
                        "mpl_row": None,
                        "mpl_choice": None,
                        "show_points": False,  # Points are hidden when no MPL choices
                        "details": "No Multi-Price List choices were available for this round",
                    })

            payment_details.append(round_detail)

        # Finalize total payment and output
        return {
            "payment_rounds": payment_rounds,  # Sorted rounds
            "payment_details": payment_details,  # Detailed breakdown for frontend
            "total_payment": round(total_payoff, 2),  # Total money earned
        }




class MLP(Page):

    @staticmethod
    def vars_for_template(self):
        return({'totalPoints':self.session.config['totalPoints'],
                'currency':self.session.config['totalPoints']*self.session.config['initialCurrencyValue']})
    

    @staticmethod
    def live_method(player,data):
        if 'mpl_choices' in data:
            #retrieve existing MPL choices
            all_choices = json.loads(player.all_mpl_choices)

            print("Round:",player.custom_round_num,"Player:",player.id_in_group)
            #update choices for current round
            current_round=player.custom_round_num
            all_choices[current_round] = data['mpl_choices']

            #save back to model
            player.all_mpl_choices = json.dumps(all_choices)

#MLP,WaitingRoom,CompulsoryOffer, 
#Questionnaire, 
page_sequence = [MLP,WaitingRoom,CompulsoryOffer, Main_Interface, Round_Payoffs] * totalRounds + [Experiment_End]



print(f"Total pages: {len(page_sequence)}")
for i, page in enumerate(page_sequence):
    print(f"Page {i + 1}: {page.__name__}")


def custom_export(players):
    yield ['Session_Code','Subject_ID', 'Group_Num', 'Round_Num', 'SubGroup_ID', 'S1_Points', 'S2_Points', 'S3_Points','P1_Agree','P2_Agree','P3_Agree', 'NumInAgreement', 'Timestamp','Compulsory_offer','Random_Proposer_Treatment','Time_Since_Round_Start']
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
            reports[report_no].Random_Proposer_Treatment,
            reports[report_no].Time_Since_Round_Start
        ]
    for report in reports:
        report.delete()






