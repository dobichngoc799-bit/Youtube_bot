from config import config

print("APP:", config.APP_NAME)
print("HOST:", config.HOST)
print("PORT:", config.PORT)
print("DEBUG:", config.DEBUG)
print("DATABASE:", config.DATABASE_URL)
print("YOUTUBE API KEYS:", len(config.YOUTUBE_API_KEYS))
