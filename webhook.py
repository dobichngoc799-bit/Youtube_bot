from fastapi import FastAPI, Request, Response

from database import SessionLocal, init_db
from services.youtube_parser import YouTubeParser
from services.notification_service import NotificationService


app = FastAPI(
    title="YouTube WebSub Webhook",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/webhook")
async def verify_subscription(request: Request):
    challenge = request.query_params.get("hub.challenge")

    if not challenge:
        return Response(status_code=400)

    return Response(
        content=challenge,
        media_type="text/plain",
        status_code=200,
    )


@app.post("/webhook")
async def receive_notification(request: Request):
    body = await request.body()
    xml_body = body.decode("utf-8")

    video_data = YouTubeParser.parse_websub_xml(xml_body)

    if not video_data:
        return Response(status_code=204)

    db = SessionLocal()

    try:
        service = NotificationService(db)
        ok, msg = service.send_video_notification(video_data)
        print(msg)

    except Exception as exc:
        print(f"Webhook error: {exc}")

    finally:
        db.close()

    return Response(status_code=204)