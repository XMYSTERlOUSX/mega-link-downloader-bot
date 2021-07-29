import os

class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "") # Make a bot from https://t.me/BotFather and enter the token here
    #If deploying on vps edit the above value as example := TG_BOT_TOKEN = "Your-bot-token-inside-inverted-commas."
    
    APP_ID = int(os.environ.get("APP_ID", 12345)) # Get this value from https://my.telegram.org/apps
    #If deploying on vps edit the above value as example := APP_ID = Your-APP_ID-without-inverted-commas
    
    API_HASH = os.environ.get("API_HASH") # Get this value from https://my.telegram.org/apps
    #If deploying on vps edit the above value as example := API_HASH = "Your-API_HASH-inside-inverted-commas."
    
    Mega_email = os.environ.get("Mega_email", "") # This is not necessary! Enter your mega email only if you have a mega.nz account with pro/business features.
    #If deploying on vps edit the above value as example := Mega_email = "Your-Mega_email-inside-inverted-commas."
    
    Mega_password = os.environ.get("Mega_password", "") # This is not necessary! Enter your mega password only if you have a mega.nz account with pro/business features.
    #If deploying on vps edit the above value as example := Mega_password = "Your-Mega_password-inside-inverted-commas."
    
    Bot_username = os.environ.get("Bot_username", "") # Your bot's telegram username (must enter with '@' in the front of the username)
    #If deploying on vps edit the above value as example := Bot_username = "Your-Bot_username-inside-inverted-commas."
    
    DOWNLOAD_LOCATION = "./DOWNLOADS" # The download location (Don't change anything in this field!)
