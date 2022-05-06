#!/usr/bin/python3
#File: examples.contract_sim.py

"Runs a lead simulation over 10 hands."
from src.deal import Dealer, Deal
from src.simulation import BestLead
from src.types import Hand
from src.contract import Contract
from src.utils import print_imp_table, print_percentages, check_is_balanced

def accept(deal:Deal) -> bool:
    r"""Accept deal if East has a strong no trump and west has a raise to game without
    using stayman. West is constrained to be any 4-3-3-3 or other balanced shapes w/o 5M/6m and
    can have between 10 and 14 points.

    Parameters
    ----------
    deal : Deal
        Deal to check condition.

    Returns
    -------
    accept : bool
        True if condition satisfied, else False.
    """
    west_shapes = [(4,3,3,3),(3,4,3,3),(3,3,3,4),(3,3,4,3),
    (3,3,5,2),(3,3,2,5),(2,3,4,4),(3,2,4,4)]
    if (check_is_balanced(deal.east.shape) and 15<=deal.north.points<=17
    and deal.west.shape in west_shapes and 10<=deal.west.points==14):
        return True
    return False

def main():
    r"""
    Generate 10 deals where EW bid 1NT-3NT and the South hand is on lead with "Q9.8654.654.5432".
    West is constrained to be any 4-3-3-3 or other balanced shapes w/o 5M/6m.
    """
    dealer = Dealer([Hand([]), Hand([]), Hand.construct_from_str('Q9.8654.654.5432'), Hand([])],
                     accept)
    deals = dealer.find_deals()
    simulation = BestLead(deals, "E", Hand.construct_from_str('Q9.8654.654.5432'),
                        Contract.construct_from_str("3NT"))
    scores = simulation.calculate_lead_scores()
    percentage = simulation.calculate_percentage_beaten()
    leads = list(percentage.keys())
    imps = simulation.calculate_leads_imps_gained()
    percentage_table = print_percentages(leads, list(percentage.values()))
    imps_table = print_imp_table(leads, imps)
    print(f"{scores}\n\n{percentage_table}\n\n{imps_table}")

if __name__ == "__main__":
    main()
