from abc import ABC, abstractmethod


class SocialMedia(ABC):
    @abstractmethod
    def get_newest(self) -> str | None:
        """get url for most recent video, None if last matches most recent"""
