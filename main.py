#!/usr/bin/env python

import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
login_phone = os.getenv('LOGIN_PHONE')
port = os.getenv('PORT')

client = TelegramClient('Stealgram', api_id, api_hash)

async def fetch_last_telegram_message():
    await client.start(login_phone)
    messages = await client.get_messages(777000, 5)
    await client.disconnect()
    return messages

@app.get("/")
async def root():
    msgs = await fetch_last_telegram_message()
    content = "<ul>"
    for msg in msgs:
        content += "<li>" + str(msg.message) + "</li>"
        content += "</br>"
    content += "</ul>"
    return Response(content, media_type="text/html")
    # return StreamingResponse(content, media_type="text/html")

if __name__ == "__main__":
    uvicorn.run(app, host="*", port=int(port))
