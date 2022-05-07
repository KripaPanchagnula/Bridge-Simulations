#!/usr/bin/python3
#File: examples.weak_two.py

"Generate 10 deals with South having a weak 2H with a shortage and print them out."
from src.deal import Dealer, Deal
from src.types import Hand
from src.utils import check_if_shortage


def accept(deal: Deal) -> bool:
    r"""Accept deal if South has a weak 2 in hearts with a shortage.

    Parameters
    ----------
    deal : Deal
        Deal to check condition.

    Returns
    -------
    accept : bool
        True if condition satisfied, else False.
    """
    if (len(deal.south.hearts) == 6 and 3 <= deal.south.points < 10
            and check_if_shortage(deal.south.shape)):
        return True
    return False


def main() -> None:
    r"Generate 10 deals with South having a weak 2H with a shortage and print them out."
    dealer = Dealer([Hand([]), Hand([]), Hand([]), Hand([])], accept)
    deals = dealer.find_deals()
    for i, deal in enumerate(deals):
        print(f"deal{i}:\n{deal}\n")


if __name__ == "__main__":
    main()
