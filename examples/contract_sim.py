#!/usr/bin/python3
#File: examples.contract_sim.py

"Runs a contract simulation over 10 hands."
from src.deal import Dealer, Deal
from src.simulation import BestContract
from src.types import Hand
from src.contract import Contract
from src.utils import print_imp_table, print_percentages, check_is_balanced

def accept(deal:Deal) -> bool:
    r"""Accept deal if North has a strong no trump and south has 10 points with 5-3-3-2 shape.

    Parameters
    ----------
    deal : Deal
        Deal to check condition.

    Returns
    -------
    accept : bool
        True if condition satisfied, else False.
    """
    if (check_is_balanced(deal.north.shape) and 15<=deal.north.points<=17
    and deal.south.shape==(5,3,3,2) and deal.south.points==10):
        return True
    return False

def main():
    r"""
    Generate 10 deals where north has strong nt and south has 10 points 5-3-3-2.
    Run simulation with 3NT/4S contract to see which makes more often and gains more imps.
    Prints out the percentage and imps table.
    """
    dealer = Dealer([Hand([]), Hand([]), Hand([]), Hand([])], accept)
    deals = dealer.find_deals()
    contracts = [Contract.construct_from_str("3NT"), Contract.construct_from_str("4S")]
    simulation = BestContract(deals, "N", contracts)
    percentage = simulation.calculate_contracts_percentage_made()
    imps = simulation.calculate_contracts_imps_gained()
    percentage_table = print_percentages(contracts, list(percentage.values()))
    imps_table = print_imp_table(contracts, imps)
    print(f"{percentage_table}\n\n{imps_table}")

if __name__ == "__main__":
    main()
