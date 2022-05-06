#!/usr/bin/python
#File: tests.test_deal.py
"""Module testing src.deal"""

from random import randint
import pytest

from src.deal import generate_deal, remove_dealt_cards, calculate_total_possible_deals, Deal, Dealer, InvalidDealError
from src.types import Hand, Card, Deck


def test_deal_generation() -> None:
    r"Checks whether 13 cards in each suit dealt, and 40 points in pack."
    large_no = randint(0, int(5e28))
    deal = generate_deal(large_no, Hand([]), Hand([]), Hand([]), Hand([]))
    spades = (len(deal.north.spades) + len(deal.east.spades)
              + len(deal.south.spades) + len(deal.west.spades))
    hearts = (len(deal.north.hearts) + len(deal.east.hearts)
              + len(deal.south.hearts) + len(deal.west.hearts))
    diamonds = (len(deal.north.diamonds) + len(deal.east.diamonds)
                + len(deal.south.diamonds) + len(deal.west.diamonds))
    clubs = (len(deal.north.clubs) + len(deal.east.clubs)
             + len(deal.south.clubs) + len(deal.west.clubs))
    points = deal.north.points + deal.east.points + \
        deal.south.points + deal.west.points
    assert isinstance(deal, Deal)
    assert spades == 13
    assert hearts == 13
    assert diamonds == 13
    assert clubs == 13
    assert points == 40


def test_removing_dealt_cards() -> None:
    r"Checks if the expected cards are removed from hands."
    north = Hand.construct_from_str('AKQJT98765432...')
    east = Hand.construct_from_str('.AKQJT98765432..')
    south = Hand.construct_from_str('..AKQJT98765432.')
    clubs = [Card('2C'), Card('3C'), Card('4C'), Card('5C'), Card('6C'), Card('7C'),
             Card('8C'), Card('9C'), Card('TC'), Card('JC'), Card('QC'), Card('KC'), Card('AC')]
    available_cards = remove_dealt_cards(north, east, south, Hand([]))
    for i in range(13):
        assert available_cards[i].card == clubs[i].card
    deck = remove_dealt_cards(Hand([]), Hand([]), Hand([]), Hand([]))
    for i in range(52):
        assert deck[i].card == Deck[i].card


def test_calculating_total_possible_deals() -> None:
    r"Checks if correct number of total deals is calculated."
    north = Hand.construct_from_str('AKQJT98765432...')
    east = Hand.construct_from_str('.AKQJT98765432..')
    south = Hand.construct_from_str('..AKQJT98765432.')
    assert calculate_total_possible_deals(north, east, south, Hand([])) == 1


def test_dealer() -> None:
    r""" Checks if Dealer prepares valid deals.
    4 types of functions:
        accept all
        north points >=20
        north spades >=6
        north diamonds=0
    Find 50 deals in each - takes 5s to run."""
    def strong(deal: Deal) -> bool:
        if deal.north.points > 20:
            return True
        return False

    def spades(deal: Deal) -> bool:
        if len(deal.north.spades) >= 6:
            return True
        return False

    def void(deal: Deal) -> bool:
        if len(deal.north.diamonds) == 0:
            return True
        return False
    hands = [Hand([]), Hand([]), Hand([]), Hand([])]
    deal_strong = Dealer(hands, strong, 50)
    deal_spades = Dealer(hands, spades, 50)
    deal_void = Dealer(hands, void, 50)
    strong_hands = deal_strong.find_deals()
    spades_hands = deal_spades.find_deals()
    void_hands = deal_void.find_deals()
    deals = Dealer(hands, deals_to_find=50)
    dealt_hands = deals.find_deals()
    for i in range(50):
        deal = dealt_hands[i]
        points = deal.north.points+deal.east.points+deal.south.points+deal.west.points
        assert points == 40
        assert strong_hands[i].north.points >= 20
        assert len(spades_hands[i].north.spades) >= 6
        assert len(void_hands[i].north.diamonds) == 0


def test_deal_strings() -> None:
    r"Checks construction of deal from strings, and its representation"
    deal = Deal.construct_from_strings([
        'A732.J984.A9.AK7',
        'KT98654.K653.5.9',
        'Q.2.KQ843.QJT652',
        'J.AQT7.JT762.843'
    ])
    north = "N:\u2660A732  \u2665J984  \u2666A9  \u2663AK7\n"
    east = "E:\u2660KT98654  \u2665K653  \u26665  \u26639\n"
    south = "S:\u2660Q  \u26652  \u2666KQ843  \u2663QJT652\n"
    west = "W:\u2660J  \u2665AQT7  \u2666JT762  \u2663843"
    assert str(deal) == (north+east+south+west)

def test_invalid_deal() -> None:
    with pytest.raises(InvalidDealError):
        duplicate_card = Deal.construct_from_strings([
        'A732.J984.A9.AK7',
        'AT98654.K653.5.9',
        'Q.2.KQ843.QJT652',
        'J.AQT7.JT762.843'
        ])
    with pytest.raises(InvalidDealError):
        large_no = randint(0, int(1e20))
        deal = generate_deal(large_no, Hand.construct_from_str('A.KQ..'), Hand.construct_from_str('A...'), Hand([]), Hand([]))
