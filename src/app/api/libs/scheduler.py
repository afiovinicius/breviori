from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import contextmanager
from datetime import datetime, timezone
from src.app.core.database import SessionLocal
from src.app.models.short import Links

scheduler = AsyncIOScheduler()


@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def delete_expired_links():
    with get_session() as db:
        now = datetime.now(timezone.utc)
        expired_links = db.query(Links).filter(Links.expired_at <= now).all()

        if expired_links:
            for link in expired_links:
                db.delete(link)
            db.commit()
            print(f"{len(expired_links)} links expirados foram deletados.")
        else:
            print("Nenhum link expirado encontrado.")


async def start_scheduler():
    scheduler.add_job(delete_expired_links, "interval", hours=24)
    scheduler.start()
