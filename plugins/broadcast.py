from pyrogram import Client, filters

from database.userchats import get_all_chats
import os

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

@Client.on_message(filters.command("broadcast") & filters.user(int(Config.OWNER_ID)))
async def bcast(client, message):
    if message.reply_to_message:
        MSG = message.reply_to_message
    else:
        return await message.reply_text("Reply to a Message.")
    m = await message.reply_text("`Broadcasting..`")
    ALLCHATS = get_all_chats()
    SUCE = 0
    FAIL = 0
    STR = "ERROR Report !\n\n"
    for chat in ALLCHATS:
        try:
            await MSG.copy(chat)
            SUCE += 1
        except Exception as e:
            FAIL += 1
            STR += f"{chat} - {str(e)}"
    await message.reply_text(
        f"Successfully Broadcasted to {SUCE} Chats\nFailed - {FAIL} Chats !"
    )
    if FAIL > 0:
      await m.edit_text("Generating Error Report !")
      open("ErrorReport.txt", "w").write(STR)
      await message.reply_document("ErrorReport.txt", caption="Errors on Broadcast")
      os.remove("ErrorReport.txt")
    await m.delete()

@Client.on_message(filters.command("stats") & filters.user(int(Config.OWNER_ID)))
async def gistat(_, message):
    al = get_all_chats()
    await message.reply_text(f"Total Chats in Database - {len(al)}", quote=True)
