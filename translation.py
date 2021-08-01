import os

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

class Translation(object):
    START_TEXT = f"""<b>Hello there,</b>
    
I am a <b>Mega Link Downloader</b> bot!

Just enter your mega.nz link and I will return the file/video to you!😇

💠 I can set custom captions and custom thumbnails too!

✨ <b>I am open source so you can make your own bot from here!👇</b>

https://github.com/XMYSTERlOUSX/mega-link-downloader-bot"""
    
    DOWNLOAD_START = "𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝘁𝗼 𝗠𝘆 𝗦𝗲𝗿𝘃𝗲𝗿📥"
    UPLOAD_START = "<b>𝗨𝗽𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗧𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗡𝗼𝘄  📤...</b>"
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS =  "Downloaded in <b>{}</b> seconds.\n\nUploaded in <b>{}</b> seconds.\n\n<b>Thanks For Using This Free Service, Subscribe To @botzupdate For More Amazing Bots</b>"
    SAVED_CUSTOM_THUMB_NAIL = "𝗖𝘂𝘀𝘁𝗼𝗺 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗜𝘀 𝗦𝗮𝘃𝗲𝗱. 𝗧𝗵𝗶𝘀 𝗜𝗺𝗮𝗴𝗲 𝗪𝗶𝗹𝗹 𝗕𝗲 𝗨𝘀𝗲𝗱 𝗜𝗻 𝗬𝗼𝘂𝗿 𝗡𝗲𝘅𝘁 𝗨𝗽𝗹𝗼𝗮𝗱𝘀 📁.\n\nIf you want to delete it send\n /deletethumbnail anytime!"
    DEL_ETED_CUSTOM_THUMB_NAIL = "𝗖𝘂𝘀𝘁𝗼𝗺 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗖𝗹𝗲𝗮𝗿𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ❌.\nYou will now get an auto generated thumbnail for your video uploads!"

    HELP_USER = f"""<b><u>🍁Hi I am a Mega Link Downloader Bot.. 🍁</u></b>
 
<u>How to use me:-</u>

<b>Just Send me a mega.nz file link!</b>

<b>Important:-</b> 

- Folder links are not supported and your file should not be bigger than 2GB because I can't upload files which are bigger than 2Gb due to telegram API limits!

- Your link should be valid(not expired or been removed) and should not be password protected or encrypted or private!

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
