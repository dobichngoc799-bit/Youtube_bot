from services.youtube_client import YouTubeClient


def main():
    youtube = YouTubeClient()

    data = youtube.get_channel_by_handle("MrBeast")
    channel = youtube.normalize_channel(data)

    print(channel)


if __name__ == "__main__":
    main()