import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import math
import os
import time
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation


async def send_splitted_file(bot, update, tg_send_type, thumb_image_path, splited_file, tmp_directory_for_each_user, description, usermsg)
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

async def send_file(bot, update, tg_send_type, thumb_image_path, download_directory, tmp_directory_for_each_user, description, usermsg)
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
