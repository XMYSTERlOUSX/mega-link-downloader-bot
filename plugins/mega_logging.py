import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import pyrogram
from pyrogram import Client, filters
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os
import shutil
import subprocess

from database.blacklist import check_blacklist
from database.userchats import add_chat

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from mega import Mega

mega = Mega()

email = Config.Mega_email
password = Config.Mega_password
speed = "0"
# It is really not imprtant for you to enter your mega email or password in config variables!
if email is not None and password is not None:
    try:
        m = mega.login(email, password) # Logging into mega.py 
        logging_in_megacmd = subprocess.run(["mega-login", email, password]) # Logging into MEGAcmd (Helps to bypass quota limits if you use a pro/business account)
        speedlimit_in_megacmd = subprocess.run(["mega-speedlimit", speed]) # Setting the download speed limit to unlimited in MEGAcmd 😉
    except Exception as e:
        logger.info(e)
        m = mega.login()
else:
    m = mega.login() # Here we make an anonymous, temporary account for mega.py!

@Client.on_message(filters.command("mega_ini") & filters.user(int(Config.OWNER_ID)))
async def log_to_megatools(client, message):
    fuser = message.from_user.id
    if check_blacklist(fuser):
        await message.reply_text("Sorry! You are banned!")
        return
    add_chat(fuser)
    cred_location = Config.CREDENTIALS_LOCATION + "/mega.ini"
    megatools_credentials = message.reply_to_message
    if message.reply_to_message:
        await client.download_media(
            message=megatools_credentials,
            file_name=cred_location
        )
        # Using your mega.nz credentials for logging into megatools when downloading links with megatools (Helps to bypass quota limits if you use a pro/business account)
        await message.reply_text(f"<b>Your `mega.nz` credentials has been saved successfully!✅</b>\n\nIf you provided credentials of a pro/business mega account you will be able to download files without any quota problems!")
    else:
        await message.reply_text("<b>Read the readme from https://github.com/XMYSTERlOUSX/mega-link-downloader-bot/blob/main/README.md first</b>\n\nThen create a file named `mega.ini` as the instructions that was mentioned in the readme and send it to me. <b>Then as a reply to it send <code>/mega_ini</code></b>", disable_web_page_preview=True)
