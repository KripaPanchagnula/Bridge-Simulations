#!/usr/bin/python
#File: tests.test_simulation.py
"""Module testing src.simulation"""

from src.simulation import BestContract, BestLead
from src.deal import Deal
from src.contract import Contract
from src.types import Card, Hand

deal1 = Deal.construct_from_strings([
    'K976542..953.532',
    'A.AQ64.AKQ62.AK6',
    'Q8.9875.JT74.Q98',
    'JT3.KJT32.8.JT74'
])
deal2 = Deal.construct_from_strings([
    'Q8.9875.JT74.Q98',
    'JT3.KJT32.8.JT74',
    'K976542..953.532',
    'A.AQ64.AKQ62.AK6',
])
deal3 = Deal.construct_from_strings([
    'K976542..953.532',
    'JT3.KJT32.8.JT74',
    'Q8.9875.JT74.Q98',
    'A.AQ64.AKQ62.AK6',
])


def test_best_contract() -> None:
    r"Checks all the functions in BestContract. Deals are Board 18 from Easter Teams 2022"
    clubs, diamonds = Contract.construct_from_str(
        '6C'), Contract.construct_from_str('6D')
    contracts = BestContract([deal1, deal2], "E", [clubs, diamonds])
    scores = contracts.calculate_contract_scores()
    assert scores[clubs] == [-50, 920]
    assert scores[diamonds] == [-50, 920]
    percentages = contracts.calculate_contracts_percentage_made()
    assert percentages[clubs] == 0.5
    assert percentages[diamonds] == 0.5
    imps = contracts.calculate_contracts_imps_gained()
    assert imps == [[0, 0], [0, 0]]


def test_best_lead() -> None:
    r"Checks all the functions in BestLead. Deals are Board 18 from Easter Teams 2022"
    no_trumps = Contract.construct_from_str('6NT')
    leads = BestLead([deal1, deal3], "E", Hand.construct_from_str(
        'Q8.9875.JT74.Q98'), no_trumps)
    scores = leads.calculate_lead_scores()

    assert scores[Card("QS")] == [-990, -1020]
    assert scores[Card("8S")] == [-990, -1020]
    assert scores[Card("9H")] == [-990, -1020]
    assert scores[Card("5H")] == [-990, -1020]
    assert scores[Card("JD")] == [-990, -1020]
    assert scores[Card("7D")] == [-990, -1020]
    assert scores[Card("4D")] == [-990, -1020]
    assert scores[Card("QC")] == [-1020, -1020]
    assert scores[Card("9C")] == [-1020, -1020]

    percentage = leads.calculate_percentage_beaten()
    assert percentage[Card("QS")] == 0
    assert percentage[Card("8S")] == 0
    assert percentage[Card("9H")] == 0
    assert percentage[Card("5H")] == 0
    assert percentage[Card("JD")] == 0
    assert percentage[Card("7D")] == 0
    assert percentage[Card("4D")] == 0
    assert percentage[Card("QC")] == 0
    assert percentage[Card("9C")] == 0

    imps = leads.calculate_leads_imps_gained()
    imp_table = [
        [0, 0, 0, 0, 0, 0, 0, 0.5, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0.5, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0.5, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0.5, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0.5, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0.5, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0.5, 0.5],
        [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0, 0],
        [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0, 0]
    ]
    assert imps == imp_table
