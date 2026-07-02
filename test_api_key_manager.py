from database import SessionLocal
from services.api_key_manager import ApiKeyManager

db = SessionLocal()
manager = ApiKeyManager(db)

ok, msg = manager.add_key("TEST_KEY_123")
print(ok, msg)

key = manager.get_available_key()
print("Available key:", key)

keys = manager.list_keys()

for item in keys:
    print(
        item.id,
        item.api_key,
        "active=" + str(item.is_active),
        "last_used=" + str(item.last_used),
        "error=" + str(item.last_error)
    )

db.close()
