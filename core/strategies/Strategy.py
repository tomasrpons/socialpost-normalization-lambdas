from abc import ABC, abstractmethod
from typing import Dict

from core.Profile import Profile


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    def __init__(self, raw_profile):
        self.profile = Profile(raw_profile)

    @abstractmethod
    def process_profile(self):
        pass


"""
Concrete Strategies implement the algorithm while following the base Strategy
interface. The interface makes them interchangeable in the Context.
"""
