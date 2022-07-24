import os

class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "1821820125:AAEex8_oT3Diq2XDrB_FwAVFqXhHDGSsRTM") 

    APP_ID = int(os.environ.get("APP_ID", 6817364))

    API_HASH = os.environ.get("API_HASH", "b2aea0b75ceca34bf5333107ac526c02")

    Mega_email = os.environ.get("Mega_email", "None")

    Mega_password = os.environ.get("Mega_password", "None") 

    Bot_username = os.environ.get("Bot_username", "@G3X11bot")

    OWNER_ID = os.environ.get("OWNER_ID", "887108671")

    REDIS_URI = os.environ.get("REDIS_URI", "redis-12446.c54.ap-northeast-1-2.ec2.cloud.redislabs.com:12446") # Get This Value from http://redislabs.com/try-free (If you don't know how to obtain the a video tutorial is available here:- https://t.me/botzupdate/5)
 
    REDIS_PASS = os.environ.get("REDIS_PASS", "msNOFZlm9kQYisMtNxjNpjCQBj9APVj7") # Get This Value from http://redislabs.com/try-free (If you don't know how to obtain the a video tutorial is available here:- https://t.me/botzupdate/5)

    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "887108671").split()) # Id's of the telegram users, who you want to allow for multitasking - downloading multiple links at once!
    #AUTH_USERS = set(int(x) for x in (id1, id2)) 👈 Type exactly as that and replace id1 and id2 with the id's of the telegram users, who you want to allow for multitasking. You cand add many users like that!
    
    DOWNLOAD_LOCATION = "./DOWNLOADS" # The download location for users. (Don't change anything in this field!)
    ADMIN_LOCATION = "./ADOWNLOADS" # The download location for auth users. (Don't change anything in this field!)
    CREDENTIALS_LOCATION = "./CREDENTIALS" # Location where your mega.nz credentials for megatools gets saved if you provide them. (Don't change anything in this field!)
