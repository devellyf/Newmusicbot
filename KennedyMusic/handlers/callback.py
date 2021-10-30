"""
MIT License
Copyright (C) 2021 KennedyXMusic
This file is part of https://github.com/KennedyProject/KennedyXMusic
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from time import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from KennedyMusic.helpers.decorators import authorized_users_only
from KennedyMusic.config import ALIVE_EMOJI as alv
from KennedyMusic.config import BOT_NAME as bn, BOT_IMG, BOT_USERNAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME, UPSTREAM_REPO
from KennedyMusic.handlers.play import cb_admin_check


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>✨ Welcome [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})!</b>

**💭 [{bn}](https://t.me/{GROUP_SUPPORT}) allows you to play music on groups through the new Telegram's voice chats!**

💡 Find out all the **Bot's commands** and how they work by clicking on the **» Commands** button!""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Add me to your group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "Command​​", callback_data="cbhelp"
                    ),
                    InlineKeyboardButton(
                        "Donate", url=f"https://t.me/{OWNER_NAME}")
                ],[
                    InlineKeyboardButton(
                        "Official Group​​", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "Official Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton(
                        "Source Code", url=f"{UPSTREAM_REPO}")
                ],[
                    InlineKeyboardButton(
                        "❔ About me​​", callback_data="cbabout"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbabout"))
async def cbabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>❓ **About  {bn}**</b> 

➠ **A powerfull bot for playing music for groups!

➠ Working with pyrogram

➠ Using Python 3.9.7

➠ Can play and download music or videos from YouTube

__{bn} licensed under the GNU General Public License v.3.0__

• Updates channel @{UPDATES_CHANNEL}
• Group Support @{GROUP_SUPPORT}
• Assistant @{ASSISTANT_NAME}
• Here is my [Owner](https://t.me/{OWNER_NAME})**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 Back​", callback_data="cbstart"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} Here is the help menu !</b>

**In this menu you can open several available command menus, in each command menu there is also a brief explanation of each command**

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Basic Command", callback_data="cbbasic"),
                    InlineKeyboardButton(
                        "Admin Command", callback_data="cbadmin"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Sudo Command", callback_data="cbsudo"),
                    InlineKeyboardButton(
                        "Ownertools", callback_data="cbowner"
                    ) 
                ],
                [
                    InlineKeyboardButton(
                        "🔙 Back", callback_data="cbstart"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} basic commands for bots

[GROUP SETTINGS]
 • `/play (title / reply to audio)` - play music via youtube
 • `/ytp (title)` - play music live
 • `/playlist` - view queue list
 • `/song (title)` - download music from youtube
 • `/search (title)` - search for music from youtube in detail
 • `/video (title)` - download music from youtube in detail
[ MORE ]
 • `/alive` - check alive bot
 • `/start` - starting bot

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 Back", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} command for group admin only!

 • `/player` - view playback status
 • `/pause` - pauses playing music
 • `/resume` - resume paused music
 • `/skip` - skip to next song
 • `/end` - mute the music
 • `/userbotjoin` - invite assistant to join the group
 • `/musicplayer (on / off)` - turn on / off the music player in your group

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 Back", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**here is the owner commands only**

 • `/stats` - show the bot statistic
 • `/broadcast` (reply to message) - send a broadcast message from bot
 • `/block` (user id - duration - reason) - block user for using your bot
 • `/unblock` (user id - reason) - unblock user you blocked for using your bot
 • `/blocklist` - show you the list of user was blocked for using your bot

📝 note: all commands owned by this bot can be executed by the owner of the bot without any exceptions.

""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} **command for sudo**

 • `/userbotleaveall - remove assistant from all groups
 • `/gcast` - send global messages via assistant
 • `/rmd` - delete downloaded files
 • `/uptime` - for see the uptime and start time bot launched
 • `/sysinfo` - to see system bot info
 • `/eval` (cmd) and `/sh` (cmd) - running evaluator or shell
if using heroku
 • `/usage` - for check you dyno heroku
 • `/update` - for build update your bot
 • `/restart` - restart/reboot your bot
 • `/setvar` (var) (value) - to update your value variable on heroku
 • `/delvar` (var) - to delete your var on heroku.

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 Back", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**HOW TO USE THIS BOT :**

1.) First, add to your group.
2.) Then make admin with all permissions except anonymous admin.
3.) Add @{ASSISTANT_NAME} to your group or type `/userbotjoin` to invite assistant.
4.) Turn on voice chat first before playing music.

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🗑 Close", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbhplay"))
async def cbhplay(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""How to play music on {bn} {alv}

• `/play (query or reply audio)` - for playing music via youtube
• `/ytp (query)` - play music directly from youtube

🔔 Updates channel [Click here](https://t.me/{UPDATES_CHANNEL})""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton("🔙 Back", callback_data="cbplayback"),
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbplayback"))
async def cbplayback(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**❌ Invalid syntax, i can't find something.**


» Try read on button **Command** to know how to play.""", 
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton("Group Support", url=f"https://t.me/{GROUP_SUPPORT}"),
                ],
                [
                   InlineKeyboardButton("Command", callback_data="cbhplay"),
                ],
                [
                   InlineKeyboardButton("🗑️ Close", callback_data="closed"),
                ],
            ]
        ),
    )
