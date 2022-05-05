#!/usr/bin/python
#File: tests.test_types.py
"""Module testing src.types"""

from src.types import Suit, Strain, Seat, Rank, Card, Hand


def test_suit() -> None:
    r"Checks values of Suit enum."
    suits = ["S", "H", "D", "C"]
    for i in range(4):
        assert Suit[suits[i]].value == i
        assert Suit(i).name == suits[i]


def test_strain():
    r"Checks values of Strain enum."
    strains = ["S", "H", "D", "C", "NT"]
    for i in range(5):
        assert Strain[strains[i]].value == i
        assert Strain(i).name == strains[i]


def test_seat():
    r"Checks values of Seat enum."
    seats = ["N", "E", "S", "W"]
    for i in range(4):
        assert Seat[seats[i]].value == i
        assert Seat(i).name == seats[i]


def test_rank():
    r"Checks values of Rank enum."
    ints, strings = list(range(2, 15)), [str(
        i) for i in range(2, 10)] + ["T", "J", "Q", "K", "A"]
    for i in range(13):
        number, string = ints[i], strings[i]
        assert Rank[string].value == number
        assert Rank(number).name == string


def test_card():
    r"Checks construction attributes of a Card."
    spade_ace, beer_card, club_deuce = Card('AS'), Card('7D'), Card('2C')
    assert spade_ace.rank == 14
    assert spade_ace.suit == 0
    assert beer_card.rank == 7
    assert beer_card.suit == 2
    assert club_deuce.rank == 2
    assert club_deuce.suit == 3


def test_hand():
    r"Checks attributes of a Hand."
    hand = Hand.construct_from_str('AKQJT3.5.Q.A9872')
    assert hand.shape == (6, 1, 1, 5)
    assert hand.points == 16
    assert str(hand) == '\u2660AKQJT3  \u26655  \u2666Q  \u2663A9872'
