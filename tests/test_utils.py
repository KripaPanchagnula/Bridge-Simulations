#!/usr/bin/python
#File: tests.test_utils.py
"""Module testing src.utils"""
from src.utils import (convert_card_to_number, convert_number_to_card, generate_allowed_shapes,
                       check_if_shortage, check_is_balanced, print_imp_table, print_percentages)
from src.types import Deck, Card
from src.contract import Contract


def test_convert_card_to_number() -> None:
    r"Checks converting list of cards to list of numbers"
    numbers_list = [100*suit +
                    rank for suit in range(4) for rank in range(2, 15)]
    converted_list = [convert_card_to_number(card) for card in Deck]
    assert numbers_list == converted_list, "Numbers of cards don't match up"


def test_convert_number_to_card() -> None:
    r"Checks converting list of numbers into Cards"
    numbers_list = [100*suit +
                    rank for suit in range(4) for rank in range(2, 15)]
    converted_list = [convert_number_to_card(num) for num in numbers_list]
    for cards in range(52):
        card, deck_card = converted_list[cards], Deck[cards]
        assert card.card == deck_card.card, \
            f"{str(card)} doesn't match up to Deck card {str(deck_card)}"


def test_generate_allowed_shapes() -> None:
    r"Checks generation of allowed hand shapes."
    test_shapes = ["5/4-3-1", "4/3/4-2/", "/4-3//5-1/"]
    check_shapes = [
        [(5, 4, 3, 1), (5, 4, 1, 3), (5, 3, 4, 1),
         (5, 3, 1, 4), (5, 1, 4, 3), (5, 1, 3, 4)],
        [(4, 3, 4, 2), (4, 3, 2, 4)],
        [(4, 3, 5, 1), (4, 3, 1, 5), (3, 4, 5, 1), (3, 4, 1, 5)]
    ]
    for i in range(3):
        test_shape, check_shape = test_shapes[i], check_shapes[i]
        allowed_shapes = generate_allowed_shapes(test_shape)
        assert allowed_shapes == check_shape, \
            f"Incorrect permutations of{test_shape} generated as {allowed_shapes}"


def test_is_balanced() -> None:
    r"Checks if hand shape is bal/semi-bal/unbal."
    bal, semi_bal, unbal = (3, 4, 4, 2), (2, 2, 4, 5), (1, 3, 5, 4)
    assert check_is_balanced(bal)
    assert check_is_balanced(semi_bal, True)
    assert not check_is_balanced(unbal)


def test_has_shortage() -> None:
    r"Checks if hand shape has a singleton/void."
    bal, singleton, void = (3, 5, 3, 2), (5, 1, 3, 4), (6, 2, 0, 5)
    assert not check_if_shortage(bal)
    assert check_if_shortage(singleton)
    assert check_if_shortage(void)


def test_print_table() -> None:
    r"Checks the printing of the cross table"
    contracts = [Contract.construct_from_str("3NT"),
                 Contract.construct_from_str("4S"), Contract.construct_from_str("5C"), ]
    imps = [[0, 13, 2], [-13, 0, -12], [-2, 12, 0]]
    cross_table = print_imp_table(contracts, imps)
    cross_string = "\t3NT\t4S\t5C\t\n3NT\t0\t13\t2\n4S\t-13\t0\t-12\n5C\t-2\t12\t0\n"
    assert cross_table == cross_string


def test_print_percentage() -> None:
    r"Checks the printing of the percentage table"
    leads = [Card("QS"), Card("TH"), Card("6D"), Card("3C")]
    percentages = [0.7, 0.1, 0.2, 0.8]
    percentage_table = print_percentages(leads, percentages)
    percentage_str = "QS\tTH\t6D\t3C\t\n0.7\t0.1\t0.2\t0.8"
    print("\n", percentage_table)
    assert percentage_table == percentage_str
