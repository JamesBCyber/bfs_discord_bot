from .media_impl import SocialMedia
from googleapiclient.discovery import build
from ...config import settings

BUILD_YOUTUBE = "youtube"
BUILD_VERSION = "v3"


class YoutubeMedia(SocialMedia):
    youtube_handle: str
    last_video_id: str

    def __new__(cls, handle: str):
        clean_handle = cls.sanitize_handle(handle)
        if not cls.validate_channel(clean_handle):
            return None

        return super().__new__(cls)

    def __init__(self, handle: str) -> None:
        self.youtube_handle = self.sanitize_handle(handle)

    @staticmethod
    def sanitize_handle(handle: str) -> str:
        """strip all text up to and including @ from urls and handles. If @ is not included, use the full text given"""
        offset = handle.find("@")
        return handle[offset + 1 :]

    @staticmethod
    def validate_channel(handle: str) -> bool:
        """handle is the @handle of the username with the @ already stripped"""
        youtube = build(
            BUILD_YOUTUBE, BUILD_VERSION, developerKey=settings.google_api_key
        )
        channels_resp = (
            youtube.channels().list(part="contentDetails", forHandle=handle).execute()
        )

        return bool(channels_resp.get("items"))

    def get_newest(self) -> str | None:
        """get url for most recent video, None if last matches most recent"""
        youtube = build(
            BUILD_YOUTUBE, BUILD_VERSION, developerKey=settings.google_api_key
        )
        channel_resp = (
            youtube.channels()
            .list(part="contentDetails", forHandle=self.youtube_handle)
            .execute()
        )

        # channel assumed to be valid and does not check empty case
        uploads_playlist_id = channel_resp["items"][0]["contentDetails"][
            "relatedPlaylists"
        ]["uploads"]

        playlist_resp = youtube.playlistItems().list(
            part="snippet", playlistId=uploads_playlist_id, maxResults=1
        )

        # assumes you have at least one video uploaded publicly
        items = playlist_resp.get("items", [])

        video_id = items[0]["snippet"]["resourceId"]["videoId"]

        if video_id == self.last_video_id:
            pass
        else:
            self.last_video_id = video_id
            return f"https://www.youtube.com/watch?v={video_id}"

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, YoutubeMedia):
            return self.youtube_handle == value.youtube_handle

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.youtube_handle)
