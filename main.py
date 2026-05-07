from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "Бот работает"}

from fastapi import Request

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(data)
    return {"ok": True}