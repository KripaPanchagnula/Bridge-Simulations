#!/usr/bin/python3
#File: examples.points.py


"Generate 10 deals with East having >=22 points and print them out."
from src.deal import Dealer, Deal
from src.types import Hand


def accept(deal: Deal) -> bool:
    r"""Accept deal if East has at least 22 points.

    Parameters
    ----------
    deal : Deal
        Deal to check condition.

    Returns
    -------
    accept : bool
        True if condition satisfied, else False.
    """
    if deal.east.points >= 22:
        return True
    return False


def main() -> None:
    r"Generate 10 deals with East having >=22 points and print them out."
    dealer = Dealer([Hand([]), Hand([]), Hand([]), Hand([])], accept)
    deals = dealer.find_deals()
    for i, deal in enumerate(deals):
        print(f"deal{i}:\n{deal}\n")


if __name__ == "__main__":
    main()
