import secrets
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, DateTime, Integer, String
from app.core.config import settings
from app.core.database import Base


class Links(Base):
    __tablename__ = "links"

    short = Column(
        String(10), primary_key=True, unique=True, index=True, nullable=False
    )
    short_url = Column(String, nullable=False)
    original_url = Column(String, nullable=False)
    access_count = Column(Integer, default=0)
    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
    )
    expired_at = Column(
        DateTime,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.short:
            self.short = secrets.token_urlsafe(5)
        if not self.short_url:
            self.short_url = str(settings.DOMAIN_URL.rstrip("/") + "/" + self.short)
        if not self.expired_at:
            self.expired_at = datetime.now(timezone.utc) + timedelta(weeks=1)
