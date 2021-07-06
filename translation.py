# The code you are about to see below is a work of an absolute(100%) noob. 
# Ok now go ahead you will see what I mean!

# Solely coded by xmysteriousx


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import json
import math
import os
import shutil
import time
from datetime import datetime
from PIL import Image

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
from pyrogram import Client, filters

logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from helper_funcs.help_Nekmo_ffmpeg import take_screen_shot
from helper_funcs.help_uploadbot import DownLoadFile
from helper_funcs.help_Nekmo_ffmpeg import generate_screen_shots

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel

from mega import Mega

mega = Mega()

# It is really not imprtant for you to enter your mega emai or password in config variables!
if Config.Mega_email is not None and Config.Mega_password is not None:
    email = Config.Mega_email
    password = Config.Mega_password
    m = mega.login(email, password)
else:
    m = mega.login() # Here we make an anonymous, temperory account!
    
@Client.on_message(filters.regex(pattern=".*http.*"))
async def megadl(bot, update):
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("🤭 Sorry Dude, You are **B A N N E D 🤣🤣🤣**")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="<b>Looks like you haven't joined my update channel yet. So can you please join before using me😇</b>",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="📣 Click 𝗛𝗘𝗥𝗘 To Join 📣", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        except Exception:
            await update.reply_text("Something Wrong. Contact my Support Group")
            return
    url = update.text
    if "mega" in url and ("folder" not in url or "#F" not in url or "#N" not in url):
        usermsg = await bot.send_message(
            chat_id=update.chat.id,
            text=f"""<b>Processing...⏳</b>""",
            reply_to_message_id=update.message_id
        )
        description = ""
        megalink = None
        a = None
        b = None
        c = None
        d = None
        e = None
        g = None
        y = None
        tg_send_type = None
        error_text = f"""Sorry some error occured!
                        
Make sure your link is <b>Valid (not expired or been removed)</b>
Make sure your link is <b>not password protected or encrypted or private</b>
Make sure your link is <b>not a folder link (must be a file link)</b>
Make sure your link is <b>not bigger than 2GB(Telegram Api limits😕)</b>"""
        try:
            linkinfo = m.get_public_url_info(url)
            logger.info(linkinfo)
            if "|" in linkinfo:
                info_parts = linkinfo.split("|")
                fsize = info_parts[0]
                fname = info_parts[1]
                logger.info(fsize)
                logger.info(fname)
                a=1
            if a == 1:
                if ".mp4" in fname or ".mkv" in fname:
                    tg_send_type="vid"
                else:
                    tg_send_type="doc"
            if ".mp4" in fname:
                description_parts = fname.split(".mp4")
                description = description_parts[0]
                logger.info(description)
            elif ".mkv" in fname:
                description_parts = fname.split(".mkv")
                description = description_parts[0]
                logger.info(description)
        except:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text=error_text,
                message_id=usermsg.message_id
            )
        if a ==1:
            max_file_size = 2040109465.6
            the_file_size = int(fsize)
            if the_file_size>max_file_size:
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=f"""Looks like your link is bigger than 2GB! <b>But due to telegram API limits I can't upload files which bigger than 2GB🥺</b>""",
                    message_id=usermsg.message_id
                )
            else:
                c=1
        if c == 1:
            size_in_mb = int(the_file_size / 1024 / 1024)
            size_in_gb = int(the_file_size / 1024 / 1024 / 1024)
            gb_in_bytes = 1073741824
            if the_file_size>gb_in_bytes:
                display_size = f"""{size_in_gb}GB"""
            else:
                display_size = f"""{size_in_mb}MB"""
            try:
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text="<b>Files detected</b> : " + fname + "\n" + "<b>Size</b> : " + display_size + "\n" + "\n" + Translation.DOWNLOAD_START,
                    message_id=usermsg.message_id
                )
                megalink = url
                if megalink is not None:
                    megalink = megalink.strip()
                tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
                if not os.path.isdir(tmp_directory_for_each_user):
                    os.makedirs(tmp_directory_for_each_user)
                download_directory = tmp_directory_for_each_user + "/" + fname
                thumb_image_path = Config.DOWNLOAD_LOCATION + \
                  "/" + str(update.from_user.id) + ".jpg"
                try:
                    channelmsg = await bot.send_message(
                    chat_id=Config.Log_channel_id,
                    text=f"""<b>Task Ongoing! A Download is in progress...⚠️</b>\n\nNow {Config.Bot_username} will not respond to you.\n\nPlease wait until you see a message below this saying 'Task is finished'! and then you will be able to use me ({Config.Bot_username})"""
                    )
                    y=1
                except:
                    pass
                start = datetime.now()
                try:
                    m.download_url(megalink, tmp_directory_for_each_user)
                    d=1
                except:
                    try:
                        await bot.edit_message_text(
                            text=error_text,
                            chat_id=update.chat.id,
                            message_id=usermsg.message_id
                        )
                        if y == 1:
                            await bot.send_message(
                            chat_id=Config.Log_channel_id,
                            text=f"""<b>This task is finished! Now other users can use me ✅</b>\n\nIf you see this message as the last message in the channel it means {Config.Bot_username} will respond to you now.\n\n<b>Now send the link to me ({Config.Bot_username}) quickly</b> before other users use me again!😅""",
                            reply_to_message_id=channelmsg.message_id
                            )
                        shutil.rmtree(tmp_directory_for_each_user)
                    except:
                        pass
                if d == 1:
                    if y == 1:
                        try:
                            await bot.send_message(
                            chat_id=Config.Log_channel_id,
                            text=f"""<b>This task is finished! Now other users can use me ✅</b>\n\nIf you see this message as the last message in the channel it means {Config.Bot_username} will respond to you now.\n\n<b>Now send the link to me ({Config.Bot_username}) quickly</b> before other users use me again!😅""",
                            reply_to_message_id=channelmsg.message_id
                            )
                        except:
                            pass
                    try:
                        end_one = datetime.now()
                        time_taken_for_download = (end_one -start).seconds
                        await bot.edit_message_text(
                            chat_id=update.chat.id,
                            text=Translation.UPLOAD_START,
                            message_id=usermsg.message_id
                        )
                        width = 0
                        height = 0
                        duration = 0
                        if tg_send_type != "doc":
                            metadata = extractMetadata(createParser(download_directory))
                            if metadata is not None:
                                if metadata.has("duration"):
                                    duration = metadata.get('duration').seconds
                        if os.path.exists(thumb_image_path):
                            width = 0
                            height = 0
                            metadata = extractMetadata(createParser(thumb_image_path))
                            if metadata.has("width"):
                                width = metadata.get("width")
                            if metadata.has("height"):
                                height = metadata.get("height")
                            Image.open(thumb_image_path).convert(
                                "RGB").save(thumb_image_path)
                            img = Image.open(thumb_image_path)
                            if tg_send_type == "doc":
                                img.resize((320, height))
                            else:
                                img.resize((90, height))
                            img = Image.open(thumb_image_path)
                        else:
                            thumb_image_path = await take_screen_shot(
                                download_directory,
                                tmp_directory_for_each_user,
                                (duration / 2)
                            )
                        start_time = time.time()
                        if tg_send_type == "vid":
                            myvid = await bot.send_video(
                                chat_id=update.chat.id,
                                video=download_directory,
                                caption=description,
                                parse_mode="HTML",
                                duration=duration,
                                width= 300,
                                height= 200,
                                supports_streaming=True,
                                thumb=thumb_image_path,
                                # reply_markup=reply_markup,
                                reply_to_message_id=update.message_id,
                                progress=progress_for_pyrogram,
                                progress_args=(
                                    Translation.UPLOAD_START,
                                    usermsg,
                                    start_time
                                )
                            )
                            await myvid.forward(-1001385524030)
                        elif tg_send_type == "doc":
                            mydoc = await bot.send_document(
                                chat_id=update.chat.id,
                                document=download_directory,
                                thumb=thumb_image_path,
                                caption=description,
                                parse_mode="HTML",
                                # reply_markup=reply_markup,
                                reply_to_message_id=update.message_id,
                                progress=progress_for_pyrogram,
                                progress_args=(
                                    Translation.UPLOAD_START,
                                    usermsg,
                                    start_time
                                )
                            )
                            await mydoc.forward(-1001385524030)
                        end_two = datetime.now()
                        time_taken_for_upload = (end_two - end_one).seconds
                        #
                        await bot.edit_message_text(
                            text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                            chat_id=update.chat.id,
                            message_id=usermsg.message_id,
                            disable_web_page_preview=True
                        )
                        try:
                            shutil.rmtree(tmp_directory_for_each_user)
                        except:
                            pass
                    except:
                        await bot.edit_message_text(
                            text=error_text,
                            chat_id=update.chat.id,
                            message_id=usermsg.message_id
                        )
                        try:
                            shutil.rmtree(tmp_directory_for_each_user)
                        except:
                            pass
            except:
                await bot.edit_message_text(
                    text=error_text,
                    chat_id=update.chat.id,
                    message_id=usermsg.message_id
                )
                try:
                    shutil.rmtree(tmp_directory_for_each_user)
                except:
                    pass
               
START_TEXT = f"""<b>Hello there,</b>
    
I am a <b>Mega Link Downloader</b> bot!

Just enter your mega.nz link and I will return the file/video to you!😇

💠 I can set custom captions and custom thumbnails too!

✨ <b>I am open source so you can make your own bot from here!👇</b>

https://github.com/XMYSTERlOUSX/mega-link-downloader-bot

<b>Note</b>:- When downloading one link bot can be unresponsive for other users. See {Config.Log_channel_username) to check if another task is happening or not. 

🛑 <i>If you see</i> <b>"Task Ongoing! A Download is in progress...⚠️"</b> <i>message as the last message of the channel {Config.Log_channel_username) please wait until you see the message</i> <b>"Task finished! Now other users can use me ✅"</b> <i>and then send your link to me!</i>


<b>Before sending me anything first read the instructions by pressing /help</b>"""
    
DOWNLOAD_START = "<b>𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗜𝗻𝘁𝗼 𝗠𝘆 𝗦𝗲𝗿𝘃𝗲𝗿 𝗡𝗼𝘄 ⚠️</b> \n\n<code>Please Wait Uploading Will Start Soon...</code>"
UPLOAD_START = "<b>𝗨𝗽𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗧𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗡𝗼𝘄 📁..</b>"
AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS =  "Downloaded in <b>{}</b> seconds.\n\nUploaded in <b>{}</b> seconds.\n\n<b>Thanks For Using This Free Service, Subscribe To @botzupdate For More Amazing Bots</b>"
SAVED_CUSTOM_THUMB_NAIL = "𝗖𝘂𝘀𝘁𝗼𝗺 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗜𝘀 𝗦𝗮𝘃𝗲𝗱. 𝗧𝗵𝗶𝘀 𝗜𝗺𝗮𝗴𝗲 𝗪𝗶𝗹𝗹 𝗕𝗲 𝗨𝘀𝗲𝗱 𝗜𝗻 𝗬𝗼𝘂𝗿 𝗡𝗲𝘅𝘁 𝗨𝗽𝗹𝗼𝗮𝗱𝘀 📁.\n\nIf you want to delete it send\n /deletethumbnail anytime!"
DEL_ETED_CUSTOM_THUMB_NAIL = "𝗖𝘂𝘀𝘁𝗼𝗺 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗖𝗹𝗲𝗮𝗿𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ❌.\nYou will now get an auto generated thumbnail for your video uploads!"

HELP_USER = f"""<b><u>🍁Hi am a Mega Link Downloader Bot.. 🍁</u></b>
 
<u>How to use me:-</u>

<b>Just Send me a mega.nz file link!</b>

<b>Important:-</b> 

- Folder links are not supported and your file should not be bigger than 2GB because I can't upload files which are bigger than 2Gb due to telegram API limits!)

- Your link should be valid(not expired or been removed) and should not be password protected or encrypted or private!

- When downloading one link bot can be unresponsive for other users. See {Config.Log_channel_username) to check if another task is happening or not. 

🛑 <i>If you see</i> <b>"Task Ongoing! A Download is in progress...⚠️"</b> <i>message as the last message of the channel {Config.Log_channel_username) please wait until you see the message</i> <b>"Task finished! Now other users can use me ✅"</b> <i>and then send your link to me!</i>

❇️ <b>If you want a custom thumbnail for your uploads send a photo before sending the mega link!.</b> <i>(This step is Optional)</i>

💠 It means it is not necessary to send an image to include as an thumbnail.
If you don't send a thumbnail the video/file will be uploaded with an auto genarated thumbnail from the video.
The thumbnail you send will be used for your next uploads!

press /deletethumbnail if you want to delete the previously saved thumbnail.
(Then the video will be uploaded with an auto-genarated thumbnail!)

❇️ <b>Special feature</b> :- <i>Set caption to any file you want!</i>

💠 Select an uploaded file/video or forward me <b>Any Telegram File</b> and Just write the text you want to be on the file as a reply to the File by selecting it (as replying to a message😅) and the text you wrote will be attached as caption!😍

Ex:- <a href="https://telegra.ph/file/2177d8611f68d63a34c88.jpg">Send Like This! It's Easy🥳</a>

✨ <b>I am open source so you can make your own bot from here!👇</b>

https://github.com/XMYSTERlOUSX/mega-link-downloader-bot"""
