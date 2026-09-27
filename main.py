import asyncio
import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioVideoPiped
from flask import Flask
from threading import Thread

# --- ለ Render የፖርት ስህተት መፍትሄ (Fake Port) ---
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Abeba Music Bot is Alive!"

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
# --------------------------------------------------

API_ID = 33978718
API_HASH = "8094189df3adfa120e2be95fc0db01db"
BOT_TOKEN = "8839777691:AAEamRfPcftLXEFpTGwJMJoOar8En1BVgRk"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_app = PyTgCalls(app)

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply_text("👋 ሰላም! እኔ አበባ የሙዚቃ ቦት ነኝ። 🎵\nግሩፕ ውስጥ አድርገኸኝ /play [የዩቲዩብ ሊንክ] በማለት በቮይስ ቻት ላይ ሙዚቃ ማጫወት ትችላለህ።")

@app.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ እባክዎ የዩቲዩብ (YouTube) ሊንክ ይጨምሩ!\nምሳሌ: `/play https://youtu.be...`")
        return
    url = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    await message.reply_text("🔄 ሙዚቃው በቮይስ ቻት ላይ በመጫን ላይ ነው... እባክዎ ይጠብቁ። ⏳")
    try:
        await call_app.join_group_call(chat_id, AudioVideoPiped(url))
        await message.reply_text("🎵 ሙዚቃው በግሩፑ ቮይስ ቻት ላይ በቀጥታ እየተጫወተ ነው! 🎧")
    except Exception as e:
        await message.reply_text(f"❌ ስህተት ተከስቷል: {e}\n(ማሳሰቢያ: ግሩፑ ላይ መጀመሪያ ቮይስ ቻት መከፈቱን ያረጋግጡ!)")

@app.on_message(filters.command("stop") & filters.group)
async def stop_music(client, message):
    try:
        await call_app.leave_group_call(message.chat.id)
        await message.reply_text("🛑 ሙዚቃው ቆሟል፤ ቦቱ ከቮይስ ቻቱ ወጥቷል።")
    except Exception as e:
        await message.reply_text(f"ስህተት: {e}")

async def main():
    keep_alive() # የውሸት ፖርቱን እዚህ ጋር ይቀሰቅሰዋል
    await app.start()
    await call_app.start()
    print("🚀 ቦቱ በተሳካ ሁኔታ ሥራ ጀምሯል!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
