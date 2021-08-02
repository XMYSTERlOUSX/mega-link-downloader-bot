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
from PIL import Image

from functools import partial
from fsplit.filesplit import Filesplit

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

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from database.blacklist import check_blacklist
from database.userchats import add_chat

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
                max_file_size = 2040108421
                the_file_size = int(fsize)
                if the_file_size>max_file_size:
                    await bot.edit_message_text(
                        chat_id=update.chat.id,
                        text=f"""Looks like your link is bigger than 2GB! <b>But due to telegram API limits I can't upload files which are bigger than 2GB🥺</b>""",
                        message_id=usermsg.message_id
                    )
                else:
                    c=1
            if c == 1:
                try:
                    await bot.edit_message_text(
                        chat_id=update.chat.id,
                        text=Translation.DOWNLOAD_START,
                        message_id=usermsg.message_id
                    )
                    megalink = url
                    if megalink is not None:
                        megalink = megalink.strip()
                    if update.from_user.id == Config.OWNER_ID:
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
                                            width = 0
                                            height = 0
                                            duration = 0
                                            if tg_send_type != "doc":
                                                metadata = extractMetadata(createParser(splited_file))
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
                                                    splited_file,
                                                    tmp_directory_for_each_user,
                                                    (duration / 2)
                                                )
                                            start_time = time.time()
                                            if tg_send_type == "vid":
                                                await update.reply_chat_action("upload_video")
                                                megavid = await bot.send_video(
                                                    chat_id=update.chat.id,
                                                    video=splited_file,
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
                                            elif tg_send_type == "doc":
                                                await update.reply_chat_action("upload_document")
                                                megadoc = await bot.send_document(
                                                    chat_id=update.chat.id,
                                                    document=splited_file,
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
                                    await update.reply_chat_action("upload_video")
                                    megavid = await bot.send_video(
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
                                elif tg_send_type == "doc":
                                    await update.reply_chat_action("upload_document")
                                    megadoc = await bot.send_document(
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

        
async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        bot_name = Config.Bot_username
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n\n○ <b>Percentage ⚡️ :</b> {2}%\n\n○ <b>Finished ✅ :</b> ".format(
            ''.join(["●" for i in range(math.floor(percentage / 5))]),
            ''.join(["○" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\n\n○ <b>Speed 🚀 :</b> {2}/s\n\n○ <b>Time left 🌝 :</b> {3}\n\n<b>uploading by {4}</b>\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s",
            bot_name
        )
        try:
            await message.edit(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]
  
async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None

def download_with_progress(megalink, tmp_directory_for_each_user, usermsg, time_for_mega):
    try:
        m.download_url(megalink, tmp_directory_for_each_user, progress_msg_for_mega=usermsg, process_start_time=time_for_mega)
    except Exception as e:
        logger.info(e)

def split_files(download_directory, splitting_size, splitted_files_directory):
    try:
        fs = Filesplit()
        fs.split(
            file=download_directory,
            split_size=splitting_size,
            output_dir=splitted_files_directory,
        )
    except:
        pass
