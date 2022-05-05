#!/usr/bin/python3
#File: src.contract.py
"""Module containing contract class."""


from __future__ import annotations
from src.types import Strain


class Contract:

    r""" Class representing a Contract, containing information about level, strain, doubles
    and vulnerability.

    Attributes
    ----------
    level : int
        Level of contract. Must be between 1 and 7 inclusive.
    strain : str
        Strain of contract. Must be in the Strain enum.
    doubles : int
        State of contract: undoubled, doubled or redoubled. Default is undoubled.
    vul : bool
        Vulnerability of declaring side. Default is false for NV.
    target : int
        Number of tricks for contract to succeed. This is level + 6.

    Methods
    -------
    construct_from_str(contract, vul)
        Class method which takes a string containing all contract information and
        vulnerability information.

    calculate_undertricks_score(tricks)
        Calculates the score for declaring side where tricks < target

    calculate_overtricks_score(tricks)
        Calculates the score for the declaring side where tricks > target.
        This does not include the score for making the contract.

    calculate_contract_score
        Calculates the score for making the contract exactly.

    calculate_score(tricks)
        If tricks < target, returns the undertrick score. Else returns overtrick+contract score.

    __str__
        String representation of contract,
    """

    def __init__(self, level: int, strain: str, doubles: int = 0, vul: bool = False) -> None:
        r"""
        Parameters
        ----------
        level : int
            Level of contract. Must be between 1 and 7 inclusive.
        strain : str
            Strain of contract. Must be in the Strain enum.
        doubles : int, optional
            State of contract: undoubled, doubled or redoubled. Default is undoubled.
        vul : bool, optional
            Vulnerability of declaring side. Default is false for NV.
        """
        self.level = level
        self.strain = strain
        self.doubles = doubles
        self.vul = vul
        self.target = self.level + 6

    def __str__(self) -> str:
        r"Returns string representation of contract."
        doubles = self.doubles * "X"
        return f"{self.level}{self.strain}{doubles}"

    def __hash__(self) -> int:
        return self.level * 100 + Strain[self.strain].value

    def __eq__(self, other) -> bool:
        return isinstance(other, Contract) and hash(self) == hash(other)

    @classmethod
    def construct_from_str(cls, contract: str, vul: bool = False) -> Contract:
        r"""
        Parameters
        ----------
        contract : str
            String represenation of contract. In the form of "level""strain""doubles"
        vul : bool, optional
            Vulnerability of declaring side. Default is false for NV.
        """
        doubles = contract.count('X')
        level, strain = int(contract[0]), contract.strip('X')[1:]
        return cls(level, strain, doubles, vul)

    def calculate_undertricks_score(self, tricks: int) -> int:
        r""" Calculates the score for the declaring side when not making the contract.
        NV undertricks are 50 each, vul 100 each.
        Doubled NV undertricks are 300*(under-1) when 3 or more off, else 100 or 300.
        Vul undertricks are 300*(under-1) when 2 or more off, else 200.
        Redoubled undertricks are twice doubled undertricks.

        Parameters
        ----------
        tricks : int
            Number of tricks taken. Should be less than the target.

        Returns
        -------
        undertrick_score : int
            Score for declaring side. Should be negative.
        """
        if self.doubles == 0:
            return (tricks - self.target) * 100 if self.vul else (tricks - self.target) * 50
        if self.vul:
            return ((tricks - self.target) * 300 + 100) * self.doubles
        if tricks - self.target == -1:
            return -100 * self.doubles
        if tricks - self.target == -2:
            return -300 * self.doubles
        return ((tricks - self.target + 1) * 300 + 100) * self.doubles

    def calculate_overtricks_score(self, tricks: int) -> int:
        r""" Calculates the score made on top of what's given for making the contract
        exactly for declarer.
        Undoubled minor overtricks are 20 each, for majors/NT are 30 each.
        Doubled overtricks are 100 if NV, 200 at vul.
        Redoubled ovetricks are twice doubled overtricks.

        Parameters
        ----------
        tricks : int
            Number of tricks taken. Should be greater than or equal to the target.

        Returns
        -------
        overtrick_score : int
            Score for declaring side to be added onto the score for the contract.
        """
        minors = ['C', 'D']
        if self.doubles != 0:
            if self.vul:
                return (tricks - self.target) * 200 * self.doubles
            return (tricks - self.target) * 100 * self.doubles

        if self.strain in minors:
            return (tricks - self.target) * 20
        return (tricks - self.target) * 30

    def calculate_contract_score(self) -> int:
        r""" Calculate the score for making the contract exactly.
        Trick score is level * 20 for the minors, level * 30 for the majors,
        40 + (level - 1)*30 for NT.
        This is multiplied by 1,2,4 if contract is undoubled, doubled, redoubled respectively.
        If the contract is doubled, redoubled there is an insult bonus of 50, 100 respectively.
        Part score bonus is 50. Game bonus is available when trick_score >= 100 and is 300 at NV
        , 500 at Vul.
        Small slam bonus is 500 at NV, 750 at Vul. Available if making a 6 level contract.
        Grand slam bonus is 1000 at NV, 1500 at Vul. Available if making a 7 level contract.

        Returns
        -------
        score : int
            Sum of trick_score, part_score_bonus, game_bonus,
            small_slam_bonus, grand_slam_bonus, insult.
        """
        minors, majors = ['C', 'D'], ['H', 'S']
        trick_score = 0
        if self.strain in minors:
            trick_score += (20 * self.level) * 2 ** self.doubles
        elif self.strain in majors:
            trick_score += (30 * self.level) * 2 ** self.doubles
        else:
            trick_score += (30 * self.level + 10) * 2 ** self.doubles
        part_score_or_game_bonus = (
            500 if self.vul else 300) if trick_score >= 100 else 50
        small_slam_bonus = (self.level == 6) * (500 + 250 * self.vul)
        grand_slam_bonus = (self.level == 7) * (1000 + 500 * self.vul)
        insult = 50 * self.doubles

        return trick_score + part_score_or_game_bonus + small_slam_bonus + grand_slam_bonus + insult

    def calculate_score(self, tricks: int) -> int:
        r""" Calculates the overall score of a contract for a specified number of tricks.

        If tricks < target, just the undertrick score is calculated.
        Else the contract+overtrick score is calculated.

        Parameters
        ----------
        tricks : int
            Number of tricks taken.

        Returns
        -------
        score : int
            Score for the contract and result given.
        """
        if tricks - self.target < 0:
            return self.calculate_undertricks_score(tricks)
        return self.calculate_contract_score() + self.calculate_overtricks_score(tricks)
