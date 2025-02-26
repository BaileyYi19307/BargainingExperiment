from otree.api import *
import json
import random
import time

doc = """
Main experiment
"""
random_grouping = models.BooleanField(initial = True)  # true is random

class C(BaseConstants):
    NAME_IN_URL = 'Main_Experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3         
    NUM_ROUNDS_FOR_PAYMENT = 3


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
    previousClicker=models.IntegerField(initial=0)

class Player(BasePlayer):
    gender = models.StringField(choices=["Male", "Female"])

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
    def vars_for_template(player):
        group = player.group.get_players() 
        player.gender=player.participant.gender
        players_data = {p.id_in_group: p.participant.gender for p in group}

        return {
            'player_id': player.id_in_group,  
            'players_data': players_data, 
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
                    Round_Num=player.round_number,
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

                    # Round all calculations to two decimal places
                    p.payoff = round(p_payoff, 2)

        # handle button click event
        if 'button_clicked' in data:

            current_button = data['button_id']
            player_id = player.id_in_group

            return {0: {'button_id': data["button_id"], 'player_id': player.id_in_group}}


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        prev_payoffs = player.participant.round_payoffs

        # Store payoffs for the current round
        prev_payoffs[player.round_number] = {
            p.id_in_group: float(p.payoff) for p in player.group.get_players()
        }

        # Save back into participant.vars
        player.participant.round_payoffs = prev_payoffs
        print(f"DEBUG: Updated Payoffs → {player.participant.round_payoffs}")


        #reset before next round:
        session = player.session
        session.vars['who_in_agreement'] = []
        session.vars['submittedFirstOffer'] = {"player1": None, "player2": None, "player3": None}
        session.vars['buttonClickStates'] = {}
        session.vars['whosClickedWhat'] = {1: "", 2: "", 3: ""}
        session.vars['playersClicking'] = []

        

class Round_Payoffs(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.payoff is None:
            player.payoff = 0 
        print(f"Player {player.id_in_group} - Points Earned: {player.payoff}")

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
    def vars_for_template(player):
        group = player.group.get_players() 
        player.gender=player.participant.gender
        players_data = {p.id_in_group: p.participant.gender for p in group}

        return {
            'player_id': player.id_in_group,  
            'players_data': players_data, 
            'totalNodes': player.session.config['totalNodes'],  
            'totalMoney': player.session.config['totalMoney'],
            'ratificationTime': player.session.config['ratificationTime'],
            'timeLimit': player.session.config['timeLimit'],
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
                    Round_Num=player.round_number,
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



page_sequence = [CompulsoryOffer,WaitingRoom, Main_Interface, Round_Payoffs]


#Gender Selection, Waiting Room,Multi price list and then the repeated rounds part should be Main_Interface, Round Payoffs, and then their should be experiment_end (not repeated)
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






