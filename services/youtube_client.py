import requests

from database import SessionLocal
from services.api_key_manager import ApiKeyManager


class YouTubeClient:
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self):
        self.db = SessionLocal()
        self.key_manager = ApiKeyManager(self.db)

    def _get_api_key(self):
        api_key = self.key_manager.get_available_key()

        if not api_key:
            raise RuntimeError("Không còn API key khả dụng.")

        return api_key

    def _request(self, endpoint: str, params: dict):
        while True:
            api_key = self._get_api_key()

            try:
                response = requests.get(
                    f"{self.BASE_URL}/{endpoint}",
                    params={
                        **params,
                        "key": api_key,
                    },
                    timeout=15,
                )
            except requests.RequestException as exc:
                raise RuntimeError(
                    f"Lỗi kết nối YouTube API: {exc}"
                ) from exc

            if response.status_code == 403:
                self.key_manager.mark_error(api_key, response.text)
                continue

            if not response.ok:
                raise RuntimeError(
                    f"YouTube API error {response.status_code}: {response.text}"
                )

            return response.json()

    def get_channel(self, channel_id: str):
        if not channel_id:
            raise ValueError("channel_id không được để trống.")

        return self._request(
            "channels",
            {
                "part": "snippet,statistics,contentDetails",
                "id": channel_id.strip(),
            },
        )

    def get_channel_by_handle(self, handle: str):
        if not handle:
            raise ValueError("handle không được để trống.")

        handle = handle.strip()

        if handle.startswith("@"):
            handle = handle[1:]

        return self._request(
            "channels",
            {
                "part": "snippet,statistics,contentDetails",
                "forHandle": handle,
            },
        )

    def normalize_channel(self, data: dict):
        items = data.get("items", [])

        if not items:
            return None

        item = items[0]

        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})
        content_details = item.get("contentDetails", {})
        related_playlists = content_details.get(
            "relatedPlaylists",
            {},
        )

        return {
            "channel_id": item.get("id"),
            "channel_name": snippet.get("title"),
            "handle": snippet.get("customUrl"),
            "upload_playlist": related_playlists.get("uploads"),
            "thumbnail": (
                snippet.get("thumbnails", {})
                .get("high", {})
                .get("url")
            ),
            "subscriber_count": int(
                statistics.get("subscriberCount", 0)
            ),
            "video_count": int(
                statistics.get("videoCount", 0)
            ),
            "last_video_id": None,
        }