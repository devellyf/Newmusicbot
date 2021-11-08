import requests
from pytgcalls import idle
from KennedyMusic.callsmusic import run
from pyrogram import Client as Bot
from KennedyMusic.helpers.database import clean_restart_stage
from KennedyMusic.config import API_HASH, API_ID, BG_IMAGE, BOT_TOKEN


response = requests.get(BG_IMAGE)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)


bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="KennedyMusic/handlers"),
).start()


async def load_start():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[INFO]: SENDING RESTART STATUS")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted the Bot Successfully.**",
            )
        except Exception:
            pass
        await bot.send_message(LOG_CHANNEL, "✅ KennedyMusic Is Now Online")
       
run()
idle()
