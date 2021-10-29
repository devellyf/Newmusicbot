import requests
from pyrogram import Client

from KennedyMusic.config import API_ID, API_HASH, BOT_TOKEN, BG_IMAGE
from KennedyMusic.callsmusic.callsmusic import run

response = requests.get(BG_IMAGE)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)


bot = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="KennedyMusic/handlers")
)

bot.start()
run()
