#!/usr/bin/python3
# File:src.double_dummy.py
"""Module containing classes and functions to interact with the double dummy solver."""


from __future__ import annotations
from typing import Dict, Tuple
import ctypes
from src.types import Strain, Seat, Card, Rank, Suit
from src.deal import Deal as Board


DLL = ctypes.WinDLL('src\\dds-64.dll')
SolveBoardStatus = {
    1: "No fault",
    -1: "Unknown fault",
    -2: "Zero cards",
    -3: "Target > tricks left",
    -4: "Duplicated cards",
    -5: "Target < -1",
    -7: "Target > 13",
    -8: "Solutions < 1",
    -9: "Solutions > 3",
    -10: "> 52 cards",
    -12: "Invalid deal.currentTrick{Suit,Rank}",
    -13: "Card played in current trick is also remaining",
    -14: "Wrong number of remaining cards in a hand",
    -15: "threadIndex < 0 or >=noOfThreads, noOfThreads is the configured "
         "maximum number of threads",
}


class Deal(ctypes.Structure):
    r"""Class encoding the Deal Struct from dds.

    Attributes
    ----------
    trump : int
        Strain of contract indexed by Strain enum.
    first : int
        Person leading to the trick indexed by Seat enum.
    currentTrickSuit : list(int)
        Up to 3 cards already played to the trick, indexed by Suit enum.
    currentTrickRank : list(int)
        Up to 3 cards already played to the trick, indexed by Rank enum.
    remainCards: list(list(int))
        First index is by Seat enum, second index is by Suit enum.
        The value itself is a 16 bit int, 2 lowest bits are set to 0.
        Bit is 1 if Rank+2 in holding, else 0.
    """
    _fields_ = [
        ("trump", ctypes.c_int),
        ("first", ctypes.c_int),
        ("currentTrickSuit", ctypes.c_int * 3),
        ("currentTrickRank", ctypes.c_int * 3),
        ("remainCards", ctypes.c_uint * 4 * 4)
    ]

    @classmethod
    def construct_deal(cls, deal: Board, strain: str, declarer: str) -> Deal:
        r"""Class method to construct deal from predefined Deal object.
        Calculates holdings of each player in each suit, which is a 16 bit int,
        2 lowest bits are set to 0. Bit is 1 if Rank+2 in holding, else 0.

        Attributes
        ----------
        deal : Deal
            Deal object as defined in src.deal.
        strain : str
            Strain of contract.
        declarer : str
            Declarer of contract.

        Returns
        -------
        deal : Deal
            Deal object as defined in src.double_dummy
        """
        trumps = Strain[strain].value
        leader = (Seat[declarer].value + 1) % 4
        self = cls(trump=trumps, first=leader, currentTrickSuit=(ctypes.c_int * 3)(0, 0, 0),
                   currentTrickRank=(ctypes.c_int * 3)(0, 0, 0),
                   remain_cards=(ctypes.c_int * 4 * 4)((0, 0, 0, 0), (0, 0, 0, 0),  # type:ignore
                                                       (0, 0, 0, 0), (0, 0, 0, 0)))  # type:ignore
        for seat, hand in enumerate(deal.deal):
            suited_hand = [hand.spades, hand.hearts, hand.diamonds, hand.clubs]
            for suit, holding in enumerate(suited_hand):
                self.remainCards[seat][suit] = sum(
                    1 << card.rank for card in holding)
        return self


class FutureTricks(ctypes.Structure):
    r"""Class encoding the futureTricks Struct from dds.

    Attributes
    ----------
    nodes : int
        Number of nodes searched by the DD solver.
    cards : int
        Number of cards for which a result is returned, omitting touching cards.
    suit : list(int)
        Suit of each card returned, encoded by Suit enum.
    rank : list(int)
        Rank of the returned card, encoded by Rank enum.
    equals : list(int)
        Lower ranked equivalent cards. 16 bit int, 2 lowest bits are set to 0.
        Bit is 1 if Rank+2 in holding, else 0.
    score : list(int)
        -1 means target not reached, else target of max number of tricks.

    """
    _fields_ = [
        ("nodes", ctypes.c_int),
        ("cards", ctypes.c_int),
        ("suit", ctypes.c_int * 13),
        ("rank", ctypes.c_int * 13),
        ("equals", ctypes.c_int * 13),
        ("score", ctypes.c_int * 13),
    ]


def solve_board(deal: Board, strain: str, declarer: str,
                double_dummy_solver_modes: Tuple[int, int, int]) -> FutureTricks:
    r"""Calls the SolveBoard function within the double dummy solver and returns FutureTricks
    to be used by other solve functions. DDS definitions are found
    https://github.com/dds-bridge/dds/blob/develop/doc/dll-description.md

    Constructs a Deal object as defined in src.double_dummy, and calls the DLL function
    to SolveBoard.

    Parameters
    ----------
    deal : Deal
        Deal object as defined by src.deal
    strain : str
        Strain of contract.
    declarer : str
        Declarer of contract.
    double_dummy_solver_modes : 3-tuple(int)
        target, solution, mode integers as defined in DDS.

    Returns
    -------
    future_tricks : FutureTricks
        FutureTricks object to be used by wrapper solve functions.
    """
    target, solutions, mode = double_dummy_solver_modes
    c_deal = Deal.construct_deal(deal, strain, declarer)
    future_tricks = FutureTricks()
    status = DLL.SolveBoard(c_deal, target, solutions,
                            mode, ctypes.byref(future_tricks), 0)
    if status != 1:
        raise Exception(f"""SolveBoard failed with status {status},
                        meaning {SolveBoardStatus[status]}""")
    return future_tricks


def solve_strains(deal: Board, declarer: str) -> Dict[str, int]:
    r""" Solves deal for maximum number of tricks in each strain.
    Parameters
    ----------
    deal : Deal
        Deal object as defined by src.deal
    declarer : str
        Declarer of contract.

    Returns
    -------
    scores : dict(str, int)
        Keys are strains, values maximum number of tricks.
    """
    scores = {}
    for strains in range(5):
        strain_string = Strain(strains).name
        future_tricks = solve_board(deal, strain_string, declarer, (-1, 1, 1))
        best_score = 13-future_tricks.score[0]
        scores[strain_string] = best_score
    return scores


def solve_leads(deal: Board, strain: str, declarer: str) -> Dict[str, int]:
    r"""Calculates the number of tricks for declarer for any unique lead,
    by ignoring touching cards.
    FutureTricks.rank and FutureTricks.suit are integers, and are converted to their
    string representation by the Rank/Suit enum respectively.

    Parameters
    ----------
    deal : Deal
        Deal object as defined by src.deal
    strain : str
        Strain of contract.
    declarer : str
        Declarer of contract.

    Returns
    -------
    scores : dict(str, int)
        Keys are cards, values are scores.
    """
    future_tricks = solve_board(deal, strain, declarer, (-1, 3, 1))
    scores = {
        str(Card(Rank(future_tricks.rank[i]).name+Suit(future_tricks.suit[i]).name)):
        13 - future_tricks.score[i] for i in range(future_tricks.cards)
    }
    return scores
