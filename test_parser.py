from services.youtube_parser import YouTubeParser

tests = [

    "@MrBeast",

    "UCX6OQ3DkcsbYNE6H8uQQuVA",

    "https://www.youtube.com/@MrBeast",

    "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA",

    "https://www.youtube.com/c/LinusTechTips",

    "https://www.youtube.com/user/PewDiePie"

]

for item in tests:

    print(item)

    print(YouTubeParser.parse(item))

    print("-" * 50)