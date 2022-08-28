#!/usr/bin/python3
#File: src.types.py
"""Module containing various types and constants."""


from __future__ import annotations
from typing import List, Dict, Optional
from enum import Enum


class Suit(Enum):
    r"""Enum containing suit information.
    Spades: S=0
    Hearts: H=1
    Diamonds: D=2
    Clubs: C=3
    """
    S = 0
    H = 1
    D = 2
    C = 3


class Strain(Enum):
    r""" Enum containing strain information. Ordering matches double dummy solver.
    Spades: S=0
    Hearts: H=1
    Diamonds: D=2
    Clubs: C=3
    No Trumps: NT=4
    """
    S = 0
    H = 1
    D = 2
    C = 3
    NT = 4


class Seat(Enum):
    r""" Enum containing seat information.
    North: N=0
    East: E=1
    South: S=2
    West: W=3
    """
    N = 0
    E = 1
    S = 2
    W = 3


Rank = Enum("Rank", zip("23456789TJQKA", range(2, 15)))  # type: ignore
Rank.__doc__ = r"""Enum containing rank information. Numbers are the same,
honours continue the sequence J=11 to A=14."""


class InvalidCardError(Exception):
    r"Class representing an invalid card exception."


class Card:
    r""" Class representing a Card object.

    Attributes
    ----------
    card : str
        String of card. Must have length 2, and be in the order Rank, Suit.
    rank : int
        Rank of card, given by the Rank enum.
    suit : int
        Suit of card, given by the Suit enum.

    Methods
    -------
    __str__
        Returns the string of the card.
    """

    def __init__(self, card: str) -> None:
        r"""
        Parameters
        ----------
        card : str
            String of card. Must have length 2, and be in the order Rank, Suit.
        """
        if card[0] not in Rank.__members__:
            raise InvalidCardError(f'Card with rank {card[0]} not valid')
        if card[1] not in Suit.__members__:
            raise InvalidCardError(f'Card with suit {card[1]} not valid')
        self.card = card
        self.rank = Rank[card[0]].value
        self.suit = Suit[card[1]].value

    def __str__(self) -> str:
        r" Returns string of card."
        return self.card

    def __hash__(self) -> int:
        return self.suit * 100 + self.rank

    def __eq__(self, other) -> bool:
        return isinstance(other, Card) and hash(self) == hash(other)


class InvalidHandError(Exception):
    r"Class representing and invalid hand exception."


class Hand:
    r""" Class representing a Hand object, which is a list of Cards. This can be up to length 13.

    Attributes
    ----------
    hand : list(Card)
        Cards in the hand. Can be an empty list.
    spades : list(Card)
        List of spades in the hand.
    hearts : list(Card)
        List of hearts in the hand.
    diamonds : list(Card)
        List of diamonds in the hand.
    clubs : list(Card)
        List of clubs in the hand.
    shape : 4-tuple
        Shape of hand given as (S,H,D,C)
    points : int
        Number of points in the Hand, as calculated by the Milton HCP.

    Methods
    -------
    separate_into_suits
        Separates the given hand into its suits.

    calculate_points
        Calculates the point count of the hand.

    construct_from_str
        Construct a Hand object from a string representation.

    count_keycards(trumps)
        Counts the number of keycards in the hand. These are the 4 aces, plus the king of trumps.

    __str__
        Returns a string representation of the hand.
    """

    def __init__(self, hand: List[Card]) -> None:
        r"""
        Parameters
        ----------
        hand : list(Card)
            List of cards in hand. Can have length up to 13.
        """
        if len(hand) > 13:
            raise InvalidHandError(f"Hand with {len(hand)} cards not valid")
        if len(hand) > len(set(hand)):
            raise InvalidHandError("Hand with duplicated card invalid")
        self.hand = hand
        self.separate_into_suits()
        self.calculate_points()

    def separate_into_suits(self) -> None:
        r""" Splits the hand into its 4 suits, and calculates its shape.
        The separation into suits is done by checking the value of the Suit enum for each card.
        The shape is just the lengths of lists of each suit holding.
        """
        self.spades: List[Card] = []
        self.hearts: List[Card] = []
        self.diamonds: List[Card] = []
        self.clubs: List[Card] = []

        for card in self.hand:
            suit_list = {
                'S': self.spades,
                'H': self.hearts,
                'D': self.diamonds,
                'C': self.clubs
            }[Suit(card.suit).name]
            suit_list.append(card)

        self.shape = (len(self.spades), len(self.hearts),
                      len(self.diamonds), len(self.clubs))

    def calculate_points(self) -> None:
        r"""Calculates the Milton HCP value of the hand by mapping each card to its point
        count and summing them up."""
        self.points = sum(map(lambda card: Milton_HCP[card.rank], self.hand))

    @classmethod
    def construct_from_str(cls, string_hand: str) -> Hand:
        r""" Constrcuts a Hand object from a string. This must be in the form
        "spades.hearts.diamonds.clubs". The string is split by ".", and each suit forms a
        list which are then concatenated.

        Parameters
        ----------
        string_hand : str
            String representation of hand.
        """
        cards = string_hand.split('.')
        spades = [cards[0][i]+'S' for i in range(len(cards[0]))]
        hearts = [cards[1][i]+'H' for i in range(len(cards[1]))]
        diamonds = [cards[2][i]+'D' for i in range(len(cards[2]))]
        clubs = [cards[3][i]+'C' for i in range(len(cards[3]))]
        hand = spades + hearts + diamonds + clubs
        cards_in_hand = [Card(card) for card in hand]
        return cls(cards_in_hand)

    def __str__(self) -> str:
        r"""Returns a string representation of the hand.
        Initialises a string containing the suit symbol for each suit.
        For each card in the suit, append to its own string, and join together with 2 spaces.

        Returns
        -------
        hand : str
            String representation of hand in the form "spades  hearts  diamonds  clubs".
        """
        spades, hearts, diamonds, clubs = '\u2660', '\u2665', '\u2666', '\u2663'
        for spade in self.spades:
            spades += str(spade)[0]
        for heart in self.hearts:
            hearts += str(heart)[0]
        for diamond in self.diamonds:
            diamonds += str(diamond)[0]
        for club in self.clubs:
            clubs += str(club)[0]
        return spades+'  '+hearts+'  '+diamonds+'  '+clubs

    def count_keycards(self, trumps: Optional[str] = None) -> int:
        r"""Counts the number of keycards in the hand. These are the 4 aces, plus the king
        of the trump suit. If trumps are None, this just counts aces, as regular blackwood
        would do.

        Parameters
        ----------
        trumps : str, optional
            The trump suit of the contract. Default is none.

        Returns
        -------
        keycards : int
            The number of keycards held in the hand.
        """
        keycards = 0
        for card in self.hand:
            if Rank(card.rank).name == "A":
                keycards += 1
        if trumps is not None:
            if Card(f"K{trumps}") in self.hand:
                keycards += 1
        return keycards


# List of 52 cards, in the order 2S, 3S, ... AS, 2H, ... AH, 2D, ... AD, 2C, ..., AC.
Deck = [
    Card(card) for card in (Rank(rank).name+Suit(suit).name for suit in Suit for rank in Rank)
]

# Dictionary linking the rank of a card to its point count.
Milton_HCP: Dict[int, int] = {
    Rank['A'].value: 4, Rank['K'].value: 3, Rank['Q'].value: 2, Rank['J'].value: 1,
    Rank['T'].value: 0, 9: 0, 8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0
}

# List containing the lower end of each imp boundary + 5 to be bisected.
IMPS: List[int] = [
    15, 45, 85, 125, 165, 215, 265, 315, 365, 425, 495, 595, 745, 895,
    1095, 1295, 1495, 1745, 1995, 2245, 2495, 2995, 3495, 3995
]
