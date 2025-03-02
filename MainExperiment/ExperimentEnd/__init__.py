from otree.api import *
import json
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ExperimentEnd'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass


class Player(BasePlayer):
    selected_rounds=models.LongStringField(initial="")
    results_data=models.LongStringField(initial="")
    total_payment=models.CurrencyField(initial=0)
    bonus=models.CurrencyField(initial=0)


# PAGES

class Experiment_End(Page):

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.bonus=player.total_payment

    @staticmethod
    def vars_for_template(player):
        if 'selected_rounds' not in player.session.vars:
            num_rounds = player.session.config['num_rounds']
            rounds = list(range(1, num_rounds + 1))
            player.session.vars['selected_rounds'] = sorted(random.sample(rounds, 2))

        rounds_selected = player.session.vars['selected_rounds']
        print("\n" + "=" * 50)
        print(f"Rounds selected for ALL participants: {rounds_selected}")
        print("=" * 50 + "\n")

        results_data = {}

        for p in player.group.get_players():
            results_data[p.id_in_group] = []

            print(f"\n Processing Player {p.id_in_group} ")
            print("-" * 50)

            for round_num in rounds_selected:
                # 50% chance of choosing MLP or Negotiation
                mpl_or_negotiation = random.choice(["MLP", "Negotiation"])
                subChoice = None
                payoff = 0

                if mpl_or_negotiation == "MLP":
                    print(f"  ▶ Round {round_num}: **MLP selected**")

                    mpl_choices = json.loads(p.participant.mpl_choices)
                    row_selected = random.choice(list(range(len(mpl_choices))))

                    if mpl_choices[row_selected] == "Negotiation":
                        subChoice = "Negotiation"
                        payoff = p.participant.round_payoffs[round_num][p.id_in_group]
                        print(f"    🔹 MLP → **Negotiation** | Row Selected: {row_selected} | Payoff: {payoff}")
                    else:
                        subChoice = "Fixed Payoff"
                        payoff = row_selected
                        print(f"    🔹 MLP → **Fixed Payoff** | Row Selected: {row_selected} | Payoff: {payoff}")

                elif mpl_or_negotiation == "Negotiation":
                    row_selected = "N/A"
                    payoff = p.participant.round_payoffs[round_num][p.id_in_group]
                    print(f"  ▶ Round {round_num}: **Direct Negotiation** | Payoff: {payoff}")

                results_data[p.id_in_group].append({
                    'round': round_num,
                    'method': mpl_or_negotiation,
                    'row_selected': row_selected,  # Show row only for MLP
                    'subChoice': subChoice if mpl_or_negotiation == "MLP" else None,  # Only show sub-choice if MLP
                    'payoff': payoff
                })

            print("-" * 50)

        print("\n **Final Results Data:**")
        for pid, rounds in results_data.items():
            print(f"  - Player {pid}: {rounds}")
        print("=" * 50 + "\n")

        total_payment = sum(r['payoff'] for r in results_data[player.id_in_group])  # Calculate total earnings for this player
        player.selected_rounds=json.dumps(rounds_selected)
        player.results_data=json.dumps(results_data[player.id_in_group])
        player.total_payment=total_payment
        player.participant.payoff = total_payment

        
        return {
            'selected_rounds': rounds_selected,
            'results_data': results_data[player.id_in_group],
            'total_payment': total_payment
        }

    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     player.custom_round_num = 1  # Reset at the final page

    # @staticmethod
    # def vars_for_template(player: Player):
    #     exchange_rate = player.session.config['initialCurrencyValue']  # Exchange rate (e.g., 1 point = 3 USD)
    #     all_round_points = {
    #         round_num: round(currency / exchange_rate, 2)
    #         for round_num, currency in all_round_currencies.items()
    #     }

    #     # Load MPL choices
    #     all_mpl_choices = json.loads(player.all_mpl_choices)

    #     # Select two random payment rounds and sort them
    #     payment_rounds = sorted(rounds_payment)

    #     total_payoff = 0
    #     payment_details = []

    #     # Calculate payoff details for the selected rounds
    #     for round_num in payment_rounds:
    #         round_str = str(round_num)
    #         round_currency = all_round_currencies.get(round_str, 0)
    #         round_points = all_round_points.get(round_str, 0)
    #         mpl_choices = all_mpl_choices.get(round_str, [])

    #         # Randomly decide between negotiation and MPL
    #         use_negotiation = random.choice([True, False])
    #         round_detail = {"round": round_num, "show_points": False}  # Default show_points to False
    #         fixed_money = None  


    #         if use_negotiation:
    #             # Negotiation chosen
    #             round_detail.update({
    #                 "payment_type": "Negotiation",
    #                 "points_earned": round_points,
    #                 "money_earned": round_currency,
    #                 "mpl_row": None,
    #                 "mpl_choice": None,
    #                 "show_points": True,  # Points are shown for negotiation
    #                 "details": "Payoff was determined through negotiation",
    #             })
    #             total_payoff += round_currency
    #         else:
    #             # MPL chosen
    #             if mpl_choices:
    #                 selected_index = random.randint(0, len(mpl_choices) - 1)
    #                 selected_value = mpl_choices[selected_index]
    #                 if selected_value == -1:  # Negotiation selected via MPL
    #                     round_detail.update({
    #                         "payment_type": "Multi-Price List",
    #                         "points_earned": round_points,
    #                         "money_earned": round_currency,
    #                         "mpl_row": selected_index,
    #                         "show_points": True,  # Points are shown for negotiation
    #                         "mpl_choice": "Negotiation",
    #                         "details": f"The row chosen was {selected_index}. You chose \"Negotiation\" over a fixed payout of {fixed_money} for this row",
    #                     })
    #                     total_payoff += round_currency
    #                 else:
    #                     # Fixed amount selected
    #                     fixed_money = int(selected_value)
    #                     fixed_points = round(fixed_money / exchange_rate, 2)
    #                     round_detail.update({
    #                         "payment_type": "Multi-Price List",
    #                         "points_earned": fixed_points,
    #                         "money_earned": fixed_money,
    #                         "show_points": False,  # Points are hidden for fixed money
    #                         "mpl_row": selected_index,
    #                         "mpl_choice": "Fixed Money",
    #                         "details": f"The row chosen was {selected_index}. You chose a fixed payout of {fixed_money} USD over \"Negotiation\" for this row",
    #                     })
    #                     total_payoff += fixed_money
    #             else:
    #                 # No MPL choices available
    #                 round_detail.update({
    #                     "payment_type": "Multi-Price List",
    #                     "points_earned": 0,
    #                     "money_earned": 0,
    #                     "mpl_row": None,
    #                     "mpl_choice": None,
    #                     "show_points": False,  # Points are hidden when no MPL choices
    #                     "details": "No Multi-Price List choices were available for this round",
    #                 })

    #         payment_details.append(round_detail)

    #     # Finalize total payment and output
    #     return {
    #         "payment_rounds": payment_rounds,  # Sorted rounds
    #         "payment_details": payment_details,  # Detailed breakdown for frontend
    #         "total_payment": round(total_payoff, 2),  # Total money earned
    #     }


page_sequence = [Experiment_End]
