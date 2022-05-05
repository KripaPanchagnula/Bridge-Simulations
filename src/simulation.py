#!/usr/bin/python3
# File src.simulation.py
"""Module containing classes to run simulations."""

from __future__ import annotations
from bisect import bisect
from typing import List, Dict
from abc import ABC

from src.deal import Deal
from src.contract import Contract
from src.types import IMPS, Hand, Card
from src.double_dummy import solve_strains, solve_leads


class Simulation(ABC):
    r""" Abstract class representing a simulation to run.

    Attributes
    ----------
    deals : list(Deal)
        List of accepted deals for the simulation.
    declarer : str
        String of declarer. Must be in the Seat enum.
    vul : bool
        Vulnerability of declaring side.

    Methods
    -------
    calculate_percentage_made(contract_scores)
        Calculates the fraction of plus scores in the list.

    calculate_imps_gained(current_scores, comparison_scores)
        Calculates the IMPs gained on each deal for the current score vs the comparison score.
    """

    def __init__(self, deals: List[Deal], declarer: str) -> None:
        r"""
        Parameters
        ----------
        deals : list(Deal)
            List of accepted deals for the simulation.
        declarer : str
            String of declarer. Must be in the Seat enum.
        """
        self.deals = deals
        self.declarer = declarer

    @staticmethod
    def calculate_percentage_made(contract_scores: List[int]) -> float:
        r"""Calculates the fraction of plus scores in the list.

        Parameters
        ----------
        contract_scores : list(int)
            List of scores for each deal of the simulation.

        Returns
        -------
        percentage_made : float
            Fraction of deals with a plus score for declarer. Between 0 and 1 inclusive.
        """
        contracts_made = len(
            list(filter(lambda score: (score >= 0), contract_scores)))
        return contracts_made/len(contract_scores)

    @staticmethod
    def calculate_imps_gained(current_scores: List[int], comparison_scores: List[int]) -> float:
        r""" Calculates the IMPs gained on each deal for the current score vs the comparison score.

        For each deal in the list, current-comparison is calculated, and then converted to a
        signed IMP score using the IMPs list.

        Parameters
        ----------
        current_scores : list(int)
            List of "my" scores for each deal of the simulation.

        comparison_scores : list(int)
            List of scores to compare against for each deal of the simulation.

        Returns
        -------
        average_imps_gained : float
            The IMPs gained by taking "my" action on the deal. Positive is a better action,
            negative is worse.
        """
        total_scores = [current_scores[i] - comparison_scores[i]
                        for i in range(len(current_scores))]
        signs = [1 if total_scores[i] >= 0 else -
                 1 for i in range(len(total_scores))]
        imps = [bisect(IMPS, abs(total_scores[i])) * signs[i]
                for i in range(len(total_scores))]
        return sum(imps)/len(total_scores)


class BestContract(Simulation):
    r""" Class representing a simulation to compare contracts on a board.

    Attributes
    ----------
    deals : list(Deal)
        List of accepted deals for the simulation.
    declarer : str
        String of declarer. Must be in the Seat enum.
    contracts : list(Contract)
        List of contracts to compare.

    Methods
    -------
    calculate_contract_scores
        Calculates the contract scores for each deal in the simulation
        and each contract specified. Positive if making, else negative.

    calculate_contracts_percentage_made
        Calculates the fraction of plus scores in the list.

    calculate_contract_imps_gained
        Calculates the IMPs gained by picking a specific contract over another.
    """

    def __init__(self, deals: List[Deal], declarer: str, contracts: List[Contract]) -> None:
        r"""
        Parameters
        ----------
        deals : list(Deal)
            List of accepted deals for the simulation.
        declarer : str
            String of declarer. Must be in the Seat enum.
        contracts : list(Contract)
            List of contracts to compare.
        """
        super().__init__(deals, declarer)
        self.contracts = contracts

    def calculate_contract_scores(self) -> Dict[Contract, List[int]]:
        r""" Calculates the contract scores for each deal in the simulation and each
        contract specified. Score is positive if contract made, else negative.
        For each deal, all strains of contract are solved and put into a list of dictionaries.
        For each contract, the score for the strain is read from the list of dictionaries
        and put into its own list.
        The contract string and list of scores is appended to the dictionary.

        Returns
        -------
        scores : dict[Contract,list(int)]
            The keys are contracts, and the value is a list of scores, one for each deal in
            the simulation.
        """
        tricks = [solve_strains(deal, self.declarer) for deal in self.deals]
        scores = {}
        for contract in self.contracts:
            strain = contract.strain
            contract_scores = [contract.calculate_score(tricks[deal_index][strain])
                               for deal_index in range(len(self.deals))]
            scores[contract] = contract_scores
        return scores

    def calculate_contracts_percentage_made(self) -> Dict[Contract, float]:
        r"""Calculates the fraction of plus scores in the list.

        Returns
        -------
        percentage_made : dict([str, float])
            Keys are contracts, values are the percentage of times that it made in the simulation.
        """
        scores = self.calculate_contract_scores()
        percentage_made = {
            self.contracts[i]: self.calculate_percentage_made(
                scores[self.contracts[i]])
            for i in range(len(self.contracts))
        }
        return percentage_made

    def calculate_contracts_imps_gained(self) -> List[List[float]]:
        r""" Calculates the IMPs gained by picking a specific contract over another.

        Returns
        -------
        imps : list(list(float))
            This is an antisymmetric matrix containing the imp gain of one contract over another.
            Rows are "my" scores, columns are comparison scores.
        """
        scores = self.calculate_contract_scores()
        imps = [[self.calculate_imps_gained(scores[self.contracts[j]], scores[self.contracts[i]])
                for i in range(len(self.contracts))] for j in range(len(self.contracts))]
        return imps


class BestLead(Simulation):
    r""" Class representing a simulation to compare leads on a board.

    Attributes
    ----------
    deals : list(Deal)
        List of accepted deals for the simulation.
    declarer : str
        String of declarer. Must be in the Seat enum.
    hand : Hand
        Opening leader's hand.
    contract : Contract
        Contract to lead against.

    Methods
    -------
    calculate_lead_scores
        Calculates the scores for each card led for each deal in the simulation.
        Positive if contract is beaten, else negative.

    calculate_leads_percentage_beaten
        Calculates the fraction of minus scores in the list, which are the number of times
        the contract was beaten.

    calculate_leads_imps_gained
        Calculates the IMPs gained by picking a specific lead over another.
    """

    def __init__(self, deals: List[Deal], declarer: str, hand: Hand,
                 contract: Contract) -> None:
        r"""
        Parameters
        ----------
        deals : list(Deal)
            List of accepted deals for the simulation.
        declarer : str
            String of declarer. Must be in the Seat enum.
        hand : Hand
            Opening leader's hand.
        contract : Contract
            Contract to lead against.
        """
        super().__init__(deals, declarer)
        self.hand = hand
        self.contract = contract

    def calculate_lead_scores(self) -> Dict[Card, List[int]]:
        r""" Calculates the scores for each card led for each deal in the simulation.
        The score is positive if the contract is beaten, else negative.
        For each deal, the valid leads are solved, and a list of valid leads is created.
        For each lead, the score for each deal is read from the list of dictionaries.
        The lead string and list of scores is appended to a dictionary.

        Returns
        -------
        scores : dict[str,list(int)]
            The keys are Cards, and the value is a list of scores, one for each deal
            in the simulation.
        """
        tricks = [solve_leads(deal, self.contract.strain, self.declarer)
                  for deal in self.deals]
        valid_leads = list(tricks[0].keys())
        scores = {}
        for lead in valid_leads:
            lead_scores = [self.contract.calculate_score(tricks[deal_index][lead]) * -1
                           for deal_index in range(len(self.deals))]
            scores[Card(lead)] = lead_scores
        return scores

    def calculate_percentage_beaten(self) -> Dict[Card, float]:
        r"""Calculates the fraction of minus scores in the list, which are the number of times
        the contract was beaten.

        Returns
        -------
        percentage_beaten : dict([str, float])
            Keys are Cards, values are the percentage of times that it beat the contract
            in the simulation.
        """
        scores = self.calculate_lead_scores()
        leads = list(scores.keys())
        percentage_beaten = {
            leads[i]: self.calculate_percentage_made(scores[leads[i]])
            for i in range(len(scores.keys()))
        }
        return percentage_beaten

    def calculate_leads_imps_gained(self) -> List[List[float]]:
        r""" Calculates the IMPs gained by picking a specific lead over another.

        Returns
        -------
        imps : list(list(float))
            This is an antisymmetric matrix containing the imp gain of one lead over another.
            Rows are "my" scores, columns are comparison scores.
        """
        scores = self.calculate_lead_scores()
        leads = list(scores.keys())
        imps = [[self.calculate_imps_gained(scores[leads[j]],
                                            scores[leads[i]])
                for i in range(len(leads))] for j in range(len(leads))]
        return imps
