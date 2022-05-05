#!/usr/bin/python3
#File: examples.space_ace.py

"Generate 10 deals with West having AS and print them out."
from src.deal import Dealer, Deal
from src.types import Hand, Card


def accept(deal: Deal) -> bool:
    r"""Accept deal if West has the Ace of Spades.

    Parameters
    ----------
    deal : Deal
        Deal to check condition.

    Returns
    -------
    accept : bool
        True if condition satisfied, else False.
    """
    if Card("AS") in deal.west.hand:
        return True
    return False


def main() -> None:
    r"Generate 10 deals with West having AS and print them out."
    dealer = Dealer([Hand([]), Hand([]), Hand([]), Hand([])], accept)
    deals = dealer.find_deals()
    for i, deal in enumerate(deals):
        print(f"deal{i}:\n{deal}\n")


if __name__ == "__main__":
    main()
