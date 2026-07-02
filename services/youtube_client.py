from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from database import SessionLocal
from services.api_key_manager import ApiKeyManager


class YouTubeClient:
    def __init__(self):
        self.db = SessionLocal()
        self.key_manager = ApiKeyManager(self.db)

    def _build_service(self):
        api_key = self.key_manager.get_available_key()

        if not api_key:
            raise Exception("Không còn API Key khả dụng.")

        service = build(
            "youtube",
            "v3",
            developerKey=api_key,
            cache_discovery=False
        )

        return service, api_key

    def execute(self, func):
        while True:
            service, api_key = self._build_service()

            try:
                return func(service)

            except HttpError as e:
                error_text = str(e)

                print(f"[API ERROR] {error_text}")

                if "quotaExceeded" in error_text or "403" in error_text:
                    self.key_manager.mark_error(api_key, error_text)
                    print(f"API Key bị vô hiệu hóa: {api_key[:10]}...")
                    continue

                raise

            except Exception:
                raise
    def get_channel(self, channel_id):
        def request(service):
            return service.channels().list(
                part="snippet,statistics,contentDetails",
                id=channel_id
            ).execute()

        return self.execute(request)
