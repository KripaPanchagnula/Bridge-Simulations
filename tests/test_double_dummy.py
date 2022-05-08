#!/usr/bin/python
#File: tests.test_double_dummy.py
"""Module testing src.double_dummy"""

import pytest

from src.double_dummy import Deal as DoubleDummyDeal, solve_strains, solve_leads
from src.deal import Deal, InvalidDealError
from src.types import Strain, Seat, Hand


deal = Deal.construct_from_strings([
    'K976542..953.532',
    'A.AQ64.AKQ62.AK6',
    'Q8.9875.JT74.Q98',
    'JT3.KJT32.8.JT74'
])


def test_invalid_solve() -> None:
    r"Tests solving an invalid deal raises an exception."
    empty_deal = Deal(
        [Hand([]), Hand([]), Hand([]), Hand([])]
    )
    with pytest.raises(InvalidDealError):
        solve_strains(empty_deal, "N")


def test_deal() -> None:
    r"Tests creation of ctypes Deal object."
    double_dummy_deal = DoubleDummyDeal.construct_deal(deal, "NT", "E")
    holdings = [
        [8948, 0, 552, 44], [16384, 20560, 28740, 24640],
        [4352, 928, 3216, 4864], [3080, 11276, 256, 3216]
    ]
    remain_cards = [
        [double_dummy_deal.remainCards[i][j] for j in range(4)] for i in range(4)
    ]
    assert Strain(double_dummy_deal.trump).name == "NT"
    assert Seat(double_dummy_deal.first).name == "S"
    assert double_dummy_deal.currentTrickSuit[:] == [0, 0, 0]
    assert double_dummy_deal.currentTrickRank[:] == [0, 0, 0]
    assert holdings == remain_cards


def test_solve_strains() -> None:
    r"""Tests double dummy solution of Board 18 from Easter Teams 2022"""
    solved = solve_strains(deal, "E")
    assert solved["NT"] == 12
    assert solved["S"] == 7
    assert solved["H"] == 13
    assert solved["D"] == 11
    assert solved["C"] == 11


def test_solve_leads() -> None:
    r"""Tests double dummy solution of Board 18 from Easter Teams 2022"""
    solved = solve_leads(deal, "NT", "E")
    assert solved["QS"] == 12
    assert solved["8S"] == 12
    assert solved["9H"] == 12
    assert solved["5H"] == 12
    assert solved["JD"] == 12
    assert solved["7D"] == 12
    assert solved["4D"] == 12
    assert solved["QC"] == 13
    assert solved["9C"] == 13
