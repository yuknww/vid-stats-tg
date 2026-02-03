import datetime
import json

from sqlalchemy import select

from app.db import async_session, engine, Base
from app.models import Video, VideoSnapshot

JSON_FILE = "videos.json"

async def load_json_to_db():
    """ Загружает данные в бд """
    async with async_session() as session:
        async with session.begin():
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            with open(JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            for video_data in data.get("videos", []):
                result = await session.execute(select(Video).where(Video.id == video_data["id"]))
                existing_video = result.scalar_one_or_none()

                if not existing_video:
                    video = Video(
                        id=video_data["id"],
                        creator_id=video_data["creator_id"],
                        video_created_at=datetime.datetime.fromisoformat(video_data["video_created_at"]),
                        views_count=video_data["views_count"],
                        likes_count=video_data["likes_count"],
                        comments_count=video_data["comments_count"],
                        reports_count=video_data["reports_count"],
                        created_at=datetime.datetime.fromisoformat(video_data["created_at"]),
                        updated_at=datetime.datetime.fromisoformat(video_data["updated_at"])
                    )
                    session.add(video)

                for snap in video_data.get("snapshots", []):
                    result_snap = await session.execute(select(VideoSnapshot).where(VideoSnapshot.id == snap["id"]))
                    existing_snap = result_snap.scalar_one_or_none()

                    if not existing_snap:
                        snapshot = VideoSnapshot(
                            id=snap["id"],
                            video_id=snap["video_id"],
                            views_count=snap["views_count"],
                            likes_count=snap["likes_count"],
                            comments_count=snap["comments_count"],
                            reports_count=snap["reports_count"],
                            delta_views_count=snap["delta_views_count"],
                            delta_likes_count=snap["delta_likes_count"],
                            delta_comments_count=snap["delta_comments_count"],
                            delta_reports_count=snap["delta_reports_count"],
                            created_at=datetime.datetime.fromisoformat(snap["created_at"]),
                            updated_at=datetime.datetime.fromisoformat(snap["updated_at"])
                        )
                        session.add(snapshot)