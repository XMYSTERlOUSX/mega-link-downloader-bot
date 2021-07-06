from pyrogram import Client, filters

import os

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

@Client.on_message(filters.reply & filters.text & ~filters.edited & ~filters.group & ~filters.command("deletethumbnail"))
async def newcap(_, message):
    nc = message.reply_to_message
    if nc.media and not (nc.video_note or nc.sticker):
        await nc.copy(message.chat.id, caption=message.text)
