from services.youtube_client import YouTubeClient

youtube = YouTubeClient()

result = youtube.get_channel(
    "UCX6OQ3DkcsbYNE6H8uQQuVA"
)

print(result)
