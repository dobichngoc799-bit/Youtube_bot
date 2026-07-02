from database import SessionLocal
from models import ApiKey


def main():
    db = SessionLocal()

    try:
        keys = db.query(ApiKey).all()

        print(f"Total keys: {len(keys)}")

        if not keys:
            print("Database chưa có API key.")
            return

        for key in keys:
            print("-" * 60)
            print(f"ID            : {key.id}")
            print(f"API Key       : {key.api_key}")
            print(f"Active        : {key.is_active}")
            print(f"Rotation Index: {key.rotation_index}")
            print(f"Quota Used    : {key.quota_used}")
            print(f"Last Error    : {key.last_error}")
            print(f"Last Used     : {key.last_used}")

    finally:
        db.close()


if __name__ == "__main__":
    main()