from bfs_discord_bot.modules.social_media import youtube
from enum import Enum

from ..modules.social_media import YoutubeMedia
from dataclasses import dataclass

SOCIAL_MEDIA_TRACKER_KEY = "social_media_tracker_key"  # Database[SOCIAL_MEDIA_TRACKER_KEY] = SocialMediaTracker()


@dataclass
class SocialMediaTracker:
    """Tracker to aid in social media lookups and updates"""

    YOUTUBE_KEY = "youtube"

    youtube_channels: set[YoutubeMedia]

    def __init__(self, youtube_channels=None) -> None:
        if youtube_channels is None:
            self.youtube_channels = set()
        else:
            self.youtube_channels = youtube_channels

    def to_dict(self) -> dict:
        return {YoutubeMedia: list(self.youtube_channels)}

    @classmethod
    def from_dict(cls, data: dict) -> SocialMediaTracker:
        return cls(data[YoutubeMedia])

    def update(self) -> None:
        pass

    def add_channel(self, type: SocialMediaTracker):
        pass


class SocialMediaType(Enum):
    Youtube = 1
