import os

class Config(object):
    TG_BOT_TOKEN = os.environ.get("6321472592:AAHJTDga-GFIlg50UA3TuG9b2dluQOVe11c", "") # Make a bot from https://t.me/BotFather and enter the token here
    #If deploying on vps edit the above value as example := TG_BOT_TOKEN = "Your-bot-token-inside-inverted-commas."
    
    APP_ID = int(os.environ.get(23501911, 12345)) # Get this value from https://my.telegram.org/apps
    #If deploying on vps edit the above value as example := APP_ID = Your-APP_ID-without-inverted-commas
    
    API_HASH = os.environ.get("f80588fb5cc3756d2dbeeabd938a2fbe", "") # Get this value from https://my.telegram.org/apps
    #If deploying on vps edit the above value as example := API_HASH = "Your-API_HASH-inside-inverted-commas."
    
    Mega_email = os.environ.get("Mega_email", "None") # This is not necessary! Enter your mega email only if you have a mega.nz account with pro/business features.
    #If deploying on vps edit the above value as example := Mega_email = "Your-Mega_email-inside-inverted-commas."
    
    Mega_password = os.environ.get("Mega_password", "None") # This is not necessary! Enter your mega password only if you have a mega.nz account with pro/business features.
    #If deploying on vps edit the above value as example := Mega_password = "Your-Mega_password-inside-inverted-commas."
     
    Bot_username = os.environ.get("@NIMA_MEGA_BOT", "") # Your bot's telegram username (must enter with '@' in the front of the username)
    #If deploying on vps edit the above value as example := Bot_username = "Your-Bot_username-inside-inverted-commas."
    
    OWNER_ID = os.environ.get(6461448461, None) # Your(owner's) telegram id
    #If deploying on vps edit the above value as example := OWNER_ID = Your-telegram id-without-inverted-commas
    
    REDIS_URI = os.environ.get("redis-10033.c302.asia-northeast1-1.gce.cloud.redislabs.com:10033", None) # Get This Value from   (If you don't know how to obtain the a video tutorial is available here:- https://t.me/botzupdate/5)
    #If deploying on vps edit the above value as example := REDIS_URI = "Your-Redis-Endpoint-inside-inverted-commas."
    
    REDIS_PASS = os.environ.get("WkcONiwWICNVTe5JfTOA7oh1joczRlcw", None) # Get This Value from http://redislabs.com/try-free (If you don't know how to obtain the a video tutorial is available here:- https://t.me/botzupdate/5)
    #If deploying on vps edit the above value as example := REDIS_PASS = "Your-Redis-Password-inside-inverted-commas."

    AUTH_USERS = set(int(x) for x in os.environ.get("6461448461, 5373519610", "").split()) # Id's of the telegram users, who you want to allow for multitasking - downloading multiple links at once!
    
    #If deploying on heroku separate the ids by space. (don't put commas. Only separate each of the id's with space)
    
    #If deploying on vps edit the above value as example := 
    #AUTH_USERS = set(int(x) for x in (id1, id2)) 👈 Type exactly as that and replace id1 and id2 with the id's of the telegram users, who you want to allow for multitasking. You cand add many users like that!
    
    DOWNLOAD_LOCATION = "./DOWNLOADS" # The download location for users. (Don't change anything in this field!)
    ADMIN_LOCATION = "./ADOWNLOADS" # The download location for auth users. (Don't change anything in this field!)
    CREDENTIALS_LOCATION = "./CREDENTIALS" # Location where your mega.nz credentials for megatools gets saved if you provide them. (Don't change anything in this field!)
