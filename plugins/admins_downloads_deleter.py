from pyrogram import Client, filters

import os
import shutil

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

@Client.on_message(filters.command("delmyfolder"))
async def megadl(bot, update):
    if update.from_user.id == Config.OWNER_ID:
        allowed=1
    elif update.from_user.id in Config.AUTH_USERS:
        allowed=1
    else:
        allowed=0
    if allowed == 1:
        admin_downloads_directory = Config.ADMIN_LOCATION + "/" + str(update.from_user.id)
        if os.path.isdir(admin_downloads_directory):
            try:
                shutil.rmtree(admin_downloads_directory)
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=f"""<b>The download directory for admins and auth users has been deleted successfully! ✅</b>\n\nNow your server will be fresh as new! 😇""",
                    reply_to_message_id=update.message_id
                )
            except:
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=f"""Sorry🥺 Some error occured while trying to delete your folder! 😕""",
                    reply_to_message_id=update.message_id
                )
        else:
            await bot.send_message(
                chat_id=update.chat.id,
                text=f"""Your download directory doesn't exist! Download some files first and after all the downloads are completed and has been uploaded to telegram send /delmyfolder in order to delete owner's and auth user's file from the server and to make the server fresh!""",
                reply_to_message_id=update.message_id
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=f"""This command is only for the owner and auth users of this bot!""",
            reply_to_message_id=update.message_id
        )
