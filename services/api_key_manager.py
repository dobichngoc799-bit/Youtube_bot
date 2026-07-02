from datetime import datetime
from sqlalchemy.orm import Session
from models import ApiKey


class ApiKeyManager:
    def __init__(self, db: Session):
        self.db = db

    def add_key(self, api_key: str):
        api_key = api_key.strip()

        if not api_key:
            return False, "API key trống."

        existing = self.db.query(ApiKey).filter(ApiKey.api_key == api_key).first()
        if existing:
            return False, "API key đã tồn tại."

        new_key = ApiKey(api_key=api_key)
        self.db.add(new_key)
        self.db.commit()

        return True, "Đã thêm API key."

    def get_available_key(self):
        keys = (
            self.db.query(ApiKey)
            .filter(ApiKey.is_active == True)
            .order_by(ApiKey.rotation_index.asc(), ApiKey.id.asc())
            .all()
        )

        if not keys:
            return None

        key = keys[0]

        key.last_used = datetime.utcnow()

        max_index = (
            self.db.query(ApiKey.rotation_index)
            .order_by(ApiKey.rotation_index.desc())
            .first()
        )

        current_max = max_index[0] if max_index else 0

        key.rotation_index = current_max + 1

        self.db.commit()

        return key.api_key

    def mark_error(self, api_key: str, error: str):
        key = self.db.query(ApiKey).filter(ApiKey.api_key == api_key).first()

        if not key:
            return

        key.last_error = error

        if "quota" in error.lower() or "403" in error:
            key.is_active = False

        self.db.commit()

    def list_keys(self):
        return self.db.query(ApiKey).order_by(ApiKey.id.asc()).all()

    def disable_key(self, key_id: int):
        key = self.db.query(ApiKey).filter(ApiKey.id == key_id).first()

        if not key:
            return False, "Không tìm thấy API key."

        key.is_active = False
        self.db.commit()

        return True, "Đã tắt API key."

    def enable_key(self, key_id: int):
        key = self.db.query(ApiKey).filter(ApiKey.id == key_id).first()

        if not key:
            return False, "Không tìm thấy API key."

        key.is_active = True
        key.last_error = None
        self.db.commit()

        return True, "Đã bật lại API key."
    def remove_key(self, key_id: int):
        key = self.db.query(ApiKey).filter(ApiKey.id == key_id).first()

        if not key:
            return False, "Không tìm thấy API key."

        self.db.delete(key)
        self.db.commit()

        return True, "Đã xóa API key."

    def get_key(self, key_id: int):
        return self.db.query(ApiKey).filter(ApiKey.id == key_id).first()

