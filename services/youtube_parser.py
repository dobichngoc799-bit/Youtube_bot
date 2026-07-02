import re
from urllib.parse import urlparse


class YouTubeParser:

    @staticmethod
    def parse(text: str):

        text = text.strip()

        # Channel ID
        if text.startswith("UC"):
            return {
                "type": "channel_id",
                "value": text
            }

        # @handle
        if text.startswith("@"):
            return {
                "type": "handle",
                "value": text[1:]
            }

        # URL
        if text.startswith("http://") or text.startswith("https://"):

            parsed = urlparse(text)

            path = parsed.path.strip("/")

            # youtube.com/@xxxx
            if path.startswith("@"):
                return {
                    "type": "handle",
                    "value": path[1:]
                }

            # youtube.com/channel/UC....
            match = re.match(r"channel/(UC[\w-]+)", path)

            if match:
                return {
                    "type": "channel_id",
                    "value": match.group(1)
                }

            # youtube.com/c/xxxx
            match = re.match(r"c/([^/]+)", path)

            if match:
                return {
                    "type": "custom_url",
                    "value": match.group(1)
                }

            # youtube.com/user/xxxx
            match = re.match(r"user/([^/]+)", path)

            if match:
                return {
                    "type": "legacy_user",
                    "value": match.group(1)
                }

        return None