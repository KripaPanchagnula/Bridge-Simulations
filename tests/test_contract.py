#!/usr/bin/python
#File: tests.test_contract.py
"""Module testing src.contract"""
import pytest

from src.contract import Contract, InvalidContractError


def test_invalid_contract() -> None:
    r"Checks error raise on invalid Contract instantiation"
    with pytest.raises(InvalidContractError):
        Contract.construct_from_str('8NT')
    with pytest.raises(InvalidContractError):
        Contract.construct_from_str('1X')
    with pytest.raises(InvalidContractError):
        Contract.construct_from_str('4HXXX')


def test_contract_instantiation() -> None:
    r"Checks values of Contract attributes upon instantiation"
    contract1 = Contract.construct_from_str("2D")
    assert contract1.level == 2
    assert contract1.strain == "D"
    assert contract1.doubles == 0
    assert contract1.target == 8
    assert not contract1.vul
    contract2 = Contract.construct_from_str("4HX")
    assert contract2.level == 4
    assert contract2.strain == "H"
    assert contract2.doubles == 1
    assert contract2.target == 10
    assert not contract2.vul
    contract3 = Contract.construct_from_str("1NTXX", True)
    assert contract3.level == 1
    assert contract3.strain == "NT"
    assert contract3.doubles == 2
    assert contract3.target == 7
    assert contract3.vul


def test_undoubled_undertricks() -> None:
    r"Checks values of undoubled undertricks at NV and Vul."
    nv_contract = Contract.construct_from_str('1NT')
    vul_contract = Contract.construct_from_str('1NT', True)

    assert nv_contract.calculate_undertricks_score(6) == -50
    assert vul_contract.calculate_undertricks_score(4) == -300


def test_undoubled_overtricks() -> None:
    r"Checks scores for overtricks in minor/major/NT strains."
    minor = Contract.construct_from_str('3C')
    major = Contract.construct_from_str('4H')
    nt_contract = Contract.construct_from_str('6NT')

    assert minor.calculate_overtricks_score(10) == 20
    assert major.calculate_overtricks_score(12) == 60
    assert nt_contract.calculate_overtricks_score(13) == 30


def test_doubled_undertricks() -> None:
    r" Checks doubled undetricks scores at NV/Vul"
    nv_one_off = Contract.construct_from_str('2CX')
    nv_two_off = Contract.construct_from_str('4HX')
    nv_off = Contract.construct_from_str('5DX')
    vul_off = Contract.construct_from_str('5SX', True)

    assert nv_one_off.calculate_undertricks_score(7) == -100
    assert nv_two_off.calculate_undertricks_score(8) == -300
    assert nv_off.calculate_undertricks_score(6) == -1100
    assert vul_off.calculate_undertricks_score(6) == -1400


def test_doubled_overtricks() -> None:
    r"Checks doubled overtrick scores at NV/Vul."
    non_vul = Contract.construct_from_str('1HX')
    vul_contract = Contract.construct_from_str('3DX', True)
    assert non_vul.calculate_overtricks_score(10) == 300
    assert vul_contract.calculate_overtricks_score(11) == 400


def test_redoubled_undetricks() -> None:
    r"Checks redoubled undertrick scores at NV/Vul."
    nv_one_off = Contract.construct_from_str('2CXX')
    nv_two_off = Contract.construct_from_str('4HXX')
    nv_off = Contract.construct_from_str('5DXX')
    vul_off = Contract.construct_from_str('5SXX', True)

    assert nv_one_off.calculate_undertricks_score(7) == -200
    assert nv_two_off.calculate_undertricks_score(8) == -600
    assert nv_off.calculate_undertricks_score(8) == -1000
    assert vul_off.calculate_undertricks_score(7) == -2200


def test_redoubled_overtricks() -> None:
    r"Checks redoubled overtrick scores at NV/Vul."
    non_vul = Contract.construct_from_str('1HXX')
    vul = Contract.construct_from_str('3DXX', True)
    assert non_vul.calculate_overtricks_score(10) == 600
    assert vul.calculate_overtricks_score(11) == 800


def test_score() -> None:
    r"Checks calculating overall score."
    contract1 = Contract.construct_from_str("2D")
    contract2 = Contract.construct_from_str("2HX")
    contract3 = Contract.construct_from_str("1NTXX", True)
    assert contract1.calculate_score(7) == -50
    assert contract2.calculate_score(10) == 670
    assert contract3.calculate_score(9) == 1560


def test_undoubled_partscore() -> None:
    r"Checks making undoubled partscores exactly in minor/major/NT."
    minor_partscore = Contract.construct_from_str('2D')
    major_partscore = Contract.construct_from_str('2H')
    nt_partscore = Contract.construct_from_str('1NT')

    assert minor_partscore.calculate_contract_score() == 90
    assert major_partscore.calculate_contract_score() == 110
    assert nt_partscore.calculate_contract_score() == 90


def test_undoubled_game() -> None:
    r"Checks making undoubled games exactly in minor/major/NT."
    minor_game_nv = Contract.construct_from_str('5C')
    major_game_nv = Contract.construct_from_str('4S')
    nt_game_nv = Contract.construct_from_str('4NT')
    minor_game_vul = Contract.construct_from_str('5C', True)
    major_game_vul = Contract.construct_from_str('4S', True)
    nt_game_vul = Contract.construct_from_str('4NT', True)

    assert minor_game_nv.calculate_contract_score() == 400
    assert minor_game_vul.calculate_contract_score() == 600
    assert major_game_nv.calculate_contract_score() == 420
    assert major_game_vul.calculate_contract_score() == 620
    assert nt_game_nv.calculate_contract_score() == 430
    assert nt_game_vul.calculate_contract_score() == 630


def test_undoubled_small_slam() -> None:
    r"Checks making undoubled small slams exactly in minor/major/NT at NV/Vul."
    minor_small_slam_nv = Contract.construct_from_str('6C')
    major_small_slam_nv = Contract.construct_from_str('6H')
    nt_small_slam_nv = Contract.construct_from_str('6NT')
    minor_small_slam_vul = Contract.construct_from_str('6C', True)
    major_small_slam_vul = Contract.construct_from_str('6H', True)
    nt_small_slam_vul = Contract.construct_from_str('6NT', True)

    assert minor_small_slam_nv.calculate_contract_score() == 920
    assert minor_small_slam_vul.calculate_contract_score() == 1370
    assert major_small_slam_nv.calculate_contract_score() == 980
    assert major_small_slam_vul.calculate_contract_score() == 1430
    assert nt_small_slam_nv.calculate_contract_score() == 990
    assert nt_small_slam_vul.calculate_contract_score() == 1440


def test_undoubled_grand_slam() -> None:
    r"Checks making undoubled grand slams exactly in minor/major/NT at NV/Vul."

    minor_grand_slam_nv = Contract.construct_from_str('7D')
    major_grand_slam_nv = Contract.construct_from_str('7S')
    nt_grand_slam_nv = Contract.construct_from_str('7NT')
    minor_grand_slam_vul = Contract.construct_from_str('7D', True)
    major_grand_slam_vul = Contract.construct_from_str('7S', True)
    nt_grand_slam_vul = Contract.construct_from_str('7NT', True)

    assert minor_grand_slam_nv.calculate_contract_score() == 1440
    assert minor_grand_slam_vul.calculate_contract_score() == 2140
    assert major_grand_slam_nv.calculate_contract_score() == 1510
    assert major_grand_slam_vul.calculate_contract_score() == 2210
    assert nt_grand_slam_nv.calculate_contract_score() == 1520
    assert nt_grand_slam_vul.calculate_contract_score() == 2220


def test_doubled_partscore() -> None:
    r"Checks making doubled partscores exactly in minor/major/NT."
    minor_partscore = Contract.construct_from_str('2DX')
    major_partscore = Contract.construct_from_str('1SX')

    assert minor_partscore.calculate_contract_score() == 180
    assert major_partscore.calculate_contract_score() == 160


def test_doubled_game() -> None:
    r"Checks making doubled into games exactly in minor/major/NT at NV/Vul."
    minor_game_nv = Contract.construct_from_str('4CX')
    major_game_nv = Contract.construct_from_str('2HX')
    nt_game_nv = Contract.construct_from_str('3NTX')
    minor_game_vul = Contract.construct_from_str('4CX', True)
    major_game_vul = Contract.construct_from_str('2HX', True)
    nt_game_vul = Contract.construct_from_str('3NTX', True)

    assert minor_game_nv.calculate_contract_score() == 510
    assert minor_game_vul.calculate_contract_score() == 710
    assert major_game_nv.calculate_contract_score() == 470
    assert major_game_vul.calculate_contract_score() == 670
    assert nt_game_nv.calculate_contract_score() == 550
    assert nt_game_vul.calculate_contract_score() == 750


def test_redoubled_partscore() -> None:
    r"Checks making redoubled partscores exactly in minor."
    minor_partscore = Contract.construct_from_str('1CXX')

    assert minor_partscore.calculate_contract_score() == 230


def test_redoubled_game() -> None:
    r"Checks making redoubled into games exactly in minor/major/NT at NV/Vul."

    minor_game_nv = Contract.construct_from_str('2DXX')
    major_game_nv = Contract.construct_from_str('1SXX')
    nt_game_nv = Contract.construct_from_str('1NTXX')
    minor_game_vul = Contract.construct_from_str('2DXX', True)
    major_game_vul = Contract.construct_from_str('1SXX', True)
    nt_game_vul = Contract.construct_from_str('1NTXX', True)

    assert minor_game_nv.calculate_contract_score() == 560
    assert minor_game_vul.calculate_contract_score() == 760
    assert major_game_nv.calculate_contract_score() == 520
    assert major_game_vul.calculate_contract_score() == 720
    assert nt_game_nv.calculate_contract_score() == 560
    assert nt_game_vul.calculate_contract_score() == 760


def test_contract_str() -> None:
    r"Checks the contract string is correct"
    undoubled = Contract.construct_from_str('5C')
    doubled = Contract.construct_from_str('2HX')
    redoubled = Contract.construct_from_str('1NTXX')
    assert str(undoubled) == '5C'
    assert str(doubled) == '2HX'
    assert str(redoubled) == '1NTXX'
