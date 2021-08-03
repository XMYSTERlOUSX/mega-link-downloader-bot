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
import subprocess
import os
import shutil
import time
from datetime import datetime
from asyncio import get_running_loop

from helpers.download_uplaod_helper import send_splitted_file, send_file
from helpers.files_spliiting import split_files

from functools import partial

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation

import pyrogram
from pyrogram import Client, filters

from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.getLogger("pyrogram").setLevel(logging.WARNING)

from database.blacklist import check_blacklist
from database.userchats import add_chat

from mega import Mega

mega = Mega()

# It is really not imprtant for you to enter your mega email or password in config variables!
if Config.Mega_email is not None and Config.Mega_password is not None:
    email = Config.Mega_email
    password = Config.Mega_password
    m = mega.login(email, password)
else:
    m = mega.login() # Here we make an anonymous, temporary account!
    
@Client.on_message(filters.regex(pattern=".*http.*"))
async def megadl(bot, update):
    fuser = update.from_user.id
    if check_blacklist(fuser):
        await update.reply_text("Sorry! You are Banned!")
        return
    add_chat(fuser)
    url = update.text
    if "mega.nz" in url:
        if "folder" not in url or "#F" not in url or "#N" not in url:
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
            s = None
            y = None
            tg_send_type = None
            error_text = f"""Sorry some error occured!

    Make sure your link is <b>Valid (not expired or been removed)</b>

    Make sure your link is <b>not password protected or encrypted or private</b>"""
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
            if a == 1:
                try:
                    await bot.edit_message_text(
                        chat_id=update.chat.id,
                        text=Translation.DOWNLOAD_START,
                        message_id=usermsg.message_id
                    )
                    megalink = url
                    if megalink is not None:
                        megalink = megalink.strip()
                    if update.from_user.id == int(Config.OWNER_ID):
                        s=1
                    elif update.from_user.id in Config.AUTH_USERS:
                        s=1
                    else:
                        s=0
                    if s == 1:
                        tmp_directory_for_each_user = Config.ADMIN_LOCATION + "/" + str(update.from_user.id)
                    else:
                        tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
                    if not os.path.isdir(tmp_directory_for_each_user):
                        os.makedirs(tmp_directory_for_each_user)
                    download_directory = tmp_directory_for_each_user + "/" + fname
                    splitted_files_directory = tmp_directory_for_each_user + "/" + str(fsize)
                    thumb_image_path = Config.DOWNLOAD_LOCATION + \
                      "/" + str(update.from_user.id) + ".jpg"
                    start = datetime.now()
                    time_for_mega = time.time()
                    try:
                        # Added Loop and Partial funtions with ascyncio as a solution for the bot not responding issue!
                        loop = get_running_loop()
                        await loop.run_in_executor(None, partial(download_with_progress, megalink, tmp_directory_for_each_user, usermsg, time_for_mega))
                        d=1
                    except:
                        try:
                            await bot.edit_message_text(
                                text=error_text,
                                chat_id=update.chat.id,
                                message_id=usermsg.message_id
                            )
                            if s == 0:
                                shutil.rmtree(tmp_directory_for_each_user)
                        except:
                            pass
                    if d == 1:
                        file_size = os.stat(download_directory).st_size
                        end_one = datetime.now()
                        time_taken_for_download = (end_one -start).seconds
                        if file_size > 2040108421:
                            try:
                                await bot.edit_message_text(
                                    chat_id=update.chat.id,
                                    text="<b>Detected Size</b> : " + humanbytes(file_size) + "\n" + "\n" + "<i>Splitting files...</i>\n\n<code>The downloaded file is bigger than 2GB! But due to telegram API limits I can't upload files which are bigger than 2GB 🥺. So I will split the files and upload them to you. 😇</code>",
                                    message_id=usermsg.message_id
                                )
                                splitting_size = 2040108421
                                if not os.path.exists(splitted_files_directory):
                                    os.makedirs(splitted_files_directory)
                                loop = get_running_loop()
                                await loop.run_in_executor(None, partial(split_files, download_directory, splitting_size, splitted_files_directory))
                                splitted_in_megadl = 1
                                if splitted_in_megadl == 1:
                                    for root, dirs, files in os.walk(splitted_files_directory):
                                        for filename in files:
                                            logger.info(filename)
                                            splited_file_name = filename
                                            description = splited_file_name
                                            splited_file = splitted_files_directory + "/" + splited_file_name
                                            if filename == "fs_manifest.csv":
                                                continue
                                            await bot.edit_message_text(
                                                chat_id=update.chat.id,
                                                text=Translation.UPLOAD_START,
                                                message_id=usermsg.message_id
                                            )
                                            await send_splitted_file(bot, update, tg_send_type, thumb_image_path, splited_file, tmp_directory_for_each_user, description, usermsg)
                                    end_two = datetime.now()
                                    time_taken_for_upload = (end_two - end_one).seconds
                                    await bot.edit_message_text(
                                        text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                                        chat_id=update.chat.id,
                                        message_id=usermsg.message_id,
                                        disable_web_page_preview=True
                                    )
                                    try:
                                        if s == 1:
                                            shutil.rmtree(splitted_files_directory)
                                        else:
                                            shutil.rmtree(tmp_directory_for_each_user)
                                    except:
                                        pass
                            except:
                                await bot.edit_message_text(
                                    text="sorry some error occured!",
                                    chat_id=update.chat.id,
                                    message_id=usermsg.message_id
                                )
                                try:
                                    if s == 1:
                                        shutil.rmtree(splitted_files_directory)
                                    else:
                                        shutil.rmtree(tmp_directory_for_each_user)
                                except:
                                    pass
                        else:
                            try:
                                await bot.edit_message_text(
                                    chat_id=update.chat.id,
                                    text=Translation.UPLOAD_START,
                                    message_id=usermsg.message_id
                                )
                                await send_file(bot, update, tg_send_type, thumb_image_path, download_directory, tmp_directory_for_each_user, description, usermsg)
                                end_two = datetime.now()
                                time_taken_for_upload = (end_two - end_one).seconds
                                await bot.edit_message_text(
                                    text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                                    chat_id=update.chat.id,
                                    message_id=usermsg.message_id,
                                    disable_web_page_preview=True
                                )
                                try:
                                    if s == 0:
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
                                    if s == 0:
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
                        if s == 0:
                            shutil.rmtree(tmp_directory_for_each_user)
                    except:
                        pass
        else:
            await bot.send_message(
                chat_id=update.chat.id,
                text=f"""Sorry! Folder links are not supported!""",
                reply_to_message_id=update.message_id
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=f"""<b>I am a mega.nz link downloader bot! 😑</b>\n\nThis not a mega.nz link. 😡""",
            reply_to_message_id=update.message_id
        )

def download_with_progress(megalink, tmp_directory_for_each_user, usermsg, time_for_mega):
    try:
        m.download_url(megalink, tmp_directory_for_each_user, progress_msg_for_mega=usermsg, process_start_time=time_for_mega)
    except Exception as e:
        logger.info(e)
