from models import Channel
from services.youtube_client import YouTubeClient


class ChannelService:
    def __init__(self, db):
        self.db = db
        self.youtube = YouTubeClient()

    def add_channel(self, channel_input: str):
        channel_input = channel_input.strip()

        if not channel_input:
            return False, "Vui lòng nhập channel handle hoặc channel ID."

        if channel_input.startswith("UC"):
            data = self.youtube.get_channel(channel_input)
        else:
            data = self.youtube.get_channel_by_handle(channel_input)

        channel_data = self.youtube.normalize_channel(data)

        if not channel_data:
            return False, "Không tìm thấy kênh YouTube."

        existing = (
            self.db.query(Channel)
            .filter(Channel.channel_id == channel_data["channel_id"])
            .first()
        )

        if existing:
            return False, "Kênh này đã được theo dõi."

        channel = Channel(
            channel_id=channel_data["channel_id"],
            channel_name=channel_data["channel_name"],
            handle=channel_data["handle"],
            upload_playlist=channel_data["upload_playlist"],
            thumbnail=channel_data["thumbnail"],
            subscriber_count=channel_data["subscriber_count"],
            video_count=channel_data["video_count"],
            last_video_id=channel_data["last_video_id"],
            is_active=True,
        )

        self.db.add(channel)
        self.db.commit()

        return True, f"Đã thêm kênh: {channel.channel_name}"

    def list_channels(self):
        return (
            self.db.query(Channel)
            .order_by(Channel.id.asc())
            .all()
        )

    def remove_channel(self, channel_db_id: int):
        channel = (
            self.db.query(Channel)
            .filter(Channel.id == channel_db_id)
            .first()
        )

        if not channel:
            return False, "Không tìm thấy kênh."

        self.db.delete(channel)
        self.db.commit()

        return True, f"Đã xóa kênh: {channel.channel_name}"