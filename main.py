from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TOKEN = os.getenv("MAX_TOKEN")
API_URL = "https://platform-api.max.ru/messages"


# =========================
# отправка сообщений
# =========================
async def send_message(chat_id: int, text: str, keyboard=None):
    payload = {
        "recipient": {"chat_id": chat_id},
        "text": text
    }

    if keyboard:
        payload["attachments"] = [
            {
                "type": "inline_keyboard",
                "payload": {"buttons": keyboard}
            }
        ]

    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        await client.post(API_URL, json=payload, headers=headers)


# =========================
# webhook
# =========================
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update_type = data.get("update_type")

    # 🟢 КНОПКА НАЖАТА
    if update_type == "message_callback":
        chat_id = data["message"]["recipient"]["chat_id"]

        await send_message(chat_id, "Кнопка нажата")
        return {"ok": True}

    # 🟢 СООБЩЕНИЕ
    if update_type == "message_created":
        msg = data["message"]
        chat_id = msg["recipient"]["chat_id"]

        keyboard = [
            [
                {
                    "type": "callback",
                    "text": "Нажми меня",
                    "payload": "btn_click"
                }
            ]
        ]

        await send_message(chat_id, "Тестовое сообщение с кнопкой", keyboard)

    return {"ok": True}