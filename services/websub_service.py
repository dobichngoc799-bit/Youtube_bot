import requests


class WebSubService:
    HUB_URL = "https://pubsubhubbub.appspot.com/subscribe"

    def __init__(self, callback_url: str):
        self.callback_url = callback_url.rstrip("/")

    @staticmethod
    def build_topic(channel_id: str) -> str:
        return (
            "https://www.youtube.com/xml/feeds/videos.xml"
            f"?channel_id={channel_id}"
        )

    def subscribe(self, channel_id: str, lease_seconds: int = 864000):
        return self._request("subscribe", channel_id, lease_seconds)

    def unsubscribe(self, channel_id: str):
        return self._request("unsubscribe", channel_id)

    def renew(self, channel_id: str, lease_seconds: int = 864000):
        return self.subscribe(channel_id, lease_seconds)

    def _request(self, mode: str, channel_id: str, lease_seconds: int = 864000):
        payload = {
            "hub.mode": mode,
            "hub.topic": self.build_topic(channel_id),
            "hub.callback": self.callback_url,
            "hub.verify": "async",
            "hub.lease_seconds": lease_seconds,
        }

        response = requests.post(
            self.HUB_URL,
            data=payload,
            timeout=30,
        )

        return {
            "success": response.status_code in (202, 204),
            "status_code": response.status_code,
            "body": response.text,
        }