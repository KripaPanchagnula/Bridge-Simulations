#!/usr/bin/python3
#File: examples.mini_nt.py

"Generate 10 deals with North having a mini no trump and print them out."
from src.deal import Deal, Dealer
from src.types import Hand
from src.utils import check_is_balanced


def accept(deal: Deal) -> bool:
    r"""Accept deal if North has a mini no trump.

    Parameters
    ----------
    deal : Deal
        Deal to check condition.

    Returns
    -------
    accept : bool
        True if condition satisfied, else False.
    """
    if check_is_balanced(deal.north.shape) and 10 <= deal.north.points <= 13:
        return True
    return False


def main() -> None:
    r"Generate 10 deals with North having a mini no trump and print them out."
    dealer = Dealer([Hand([]), Hand([]), Hand([]), Hand([])], accept)
    deals = dealer.find_deals()
    for i, deal in enumerate(deals):
        print(f"deal{i}:\n{deal}\n")


if __name__ == "__main__":
    main()
