from __future__ import annotations
from core.Profile import Profile

from core.strategies.FacebookStrategy import FacebookStrategy
from core.strategies.TwitterStrategy import TwitterStrategy
from core.strategies.InstagramStrategy import InstagramStrategy
from core.strategies.YoutubeStrategy import YoutubeStrategy

from exceptions.exceptions import (
    SocialNetworkNotRecognizedException,
    MissingSocialNetworkException,
)


class Context:
    """
    This is the context class that will contain the recently added record and the
    strategy that will be used to transform it.
    """

    def __init__(self, raw_profile) -> None:
        """
        The __init__ method to initialize the context. This context will support
        dynamic setting (or changing) of the strategy.
        """

        self._strategy = self.select_strategy(raw_profile)
        self.raw_profile = raw_profile

    @property
    def strategy(self) -> Strategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It will work
        with any strategy.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        This is the dynamic setter of the strategy.
        """

        self._strategy = strategy

    def process_profile(self) -> None:
        """
        This is the polymorphic method called by the context that will delegate the
        implementation of the strategy to any of the subclasses.
        """

        self._strategy.process_profile()

    def select_strategy(self, raw_profile):
        try:
            if "partition_key" in raw_profile:
                social_network = raw_profile.get("partition_key").get("S").split("#")[1]
            else:
                raise MissingSocialNetworkException

            if social_network == "TW":
                return TwitterStrategy(raw_profile)
            if social_network == "FB":
                return FacebookStrategy(raw_profile)
            if social_network == "YT":
                return YoutubeStrategy(raw_profile)
            if social_network == "IG":
                return InstagramStrategy(raw_profile)
            else:
                raise SocialNetworkNotRecognizedException

        except MissingSocialNetworkException:
            print("There is no social network in the raw profile's partition_key")

        except SocialNetworkNotRecognizedException:
            print(
                "The raw profile contains a social network that does not have an associated strategy."
            )
