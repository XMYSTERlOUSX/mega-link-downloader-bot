from pyrogram import Client, filters

from database.blacklist import add_blacklist, get_blacklisted, remove_blacklist

import os

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
  

@Client.on_message(filters.command("black") & filters.user(int(Config.OWNER_ID)))
async def black_user(_, message):
    try:
        bl = int(message.text.split(" ", maxsplit=1)[1])
    except IndexError:
        return await message.reply_text("<b>Send This command in the below format👇</b>\n\n<code>/black <userid></code> (Replace 'userid' with the user's telegram id of who you want to ban from the bot!)")
    add_blacklist(bl)
    await message.reply_text(f"Blacklisted {bl} !")


@Client.on_message(filters.command("unblack") & filters.user(int(Config.OWNER_ID)))
async def unblack_user(_, message):
    try:
        bl = int(message.text.split(" ", maxsplit=1)[1])
    except IndexError:
        return await message.reply_text("<b>Send This command in the below format👇</b>\n\n<code>/unblack <userid></code> (Replace 'userid' with the user's telegram id of who you want to unban from the bot!)")
    te = remove_blacklist(bl)
    await message.reply_text(te)


@Client.on_message(filters.command("listblack") & filters.user(int(Config.OWNER_ID)))
async def liblack(_, message):
    m = await message.reply_text("`...`")
    al = get_blacklisted()
    TE = "List of Blacklisted User !"
    for on in al:
        TE += "\n" + str(on)
    await m.edit_text(TE)
