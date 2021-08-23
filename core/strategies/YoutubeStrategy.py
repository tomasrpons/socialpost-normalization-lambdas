from abc import ABC, abstractmethod
from typing import Dict
from datetime import datetime

from exceptions.exceptions import MissingKeyValueException
from core.Profile import Profile
from core.strategies.Strategy import Strategy


class YoutubeStrategy(Strategy):
    """
    Implementation to normalize RAW Youtube raw profile.
    """

    def process_profile(self):
        self.profile.common_processed_profile = self.process_common_profile()
        self.profile.metric_processed_profile = self.process_metric_profile()

    def process_common_profile(self):

        try:
            partition_key = self.profile.raw_profile.get("partition_key").get("S")
            client_uuid = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("meta")
                .get("M")
                .get("client_uuid")
                .get("S")
            )
            social_network = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("meta")
                .get("M")
                .get("social_network")
                .get("S")
            )
            profile_id = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("meta")
                .get("M")
                .get("profile_id")
                .get("S")
            )
            profile_username = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("data")
                .get("M")
                .get("items")
                .get("L")[0]
                .get("M")
                .get("snippet")
                .get("M")
                .get("title")
                .get("S")
            )
            profile_name = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("data")
                .get("M")
                .get("items")
                .get("L")[0]
                .get("M")
                .get("snippet")
                .get("M")
                .get("title")
                .get("S")
            )
            profile_url = "https://www.youtube.com/channel/{}".format(profile_id)
            profile_image_url = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("data")
                .get("M")
                .get("items")
                .get("L")[0]
                .get("M")
                .get("snippet")
                .get("M")
                .get("thumbnails")
                .get("M")
                .get("high")
                .get("M")
                .get("url")
                .get("S")
            )
            return {
                "partition_key": partition_key,
                "client_uuid": client_uuid,
                "social_network": social_network,
                "profile_id": profile_id,
                "profile_username": profile_username,
                "profile_name": profile_name,
                "profile_url": profile_url,
                "profile_image_url": profile_image_url,
            }
        except MissingKeyValueException:
            print("Raw profile is missing a (key,value) pair")

    def process_metric_profile(self):
        """
        This method will recieve a RAW Twitter profile, normalize it and return it.
        """
        try:
            client_uuid = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("meta")
                .get("M")
                .get("client_uuid")
                .get("S")
            )
            social_network = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("meta")
                .get("M")
                .get("social_network")
                .get("S")
            )
            profile_id = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("meta")
                .get("M")
                .get("profile_id")
                .get("S")
            )
            partition_key = f"{client_uuid}#{social_network}"
            metrics_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            sort_key = f"{profile_id}#{metrics_datetime}"
            followers = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("data")
                .get("M")
                .get("items")
                .get("L")[0]
                .get("M")
                .get("statistics")
                .get("M")
                .get("subscriberCount")
                .get("S")
            )
            followed = None
            posts = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("data")
                .get("M")
                .get("items")
                .get("L")[0]
                .get("M")
                .get("statistics")
                .get("M")
                .get("videoCount")
                .get("S")
            )
            video_play_count = (
                self.profile.raw_profile.get("data")
                .get("M")
                .get("data")
                .get("M")
                .get("items")
                .get("L")[0]
                .get("M")
                .get("statistics")
                .get("M")
                .get("viewCount")
                .get("S")
            )
            fb_fan_count = None
            fb_talking_about_count = None
            return {
                "partition_key": partition_key,
                "sort_key": sort_key,
                "social_network": social_network,
                "client_uuid": client_uuid,
                "profile_id": profile_id,
                "metrics_datetime": metrics_datetime,
                "posts": posts,
                "video_play_count": video_play_count,
                "followers": followers,
                "followed": followed,
                "fb_fan_count": fb_fan_count,
                "fb_talking_about_count": fb_talking_about_count,
            }
        except MissingKeyValueException:
            print("Raw profile is missing a (key,value) pair")
