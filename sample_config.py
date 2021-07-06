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
    
    #Make a channel and add your bot as an admin to it. This channel is for logging the details when processes are started and finished.
    #Input the channel's id here.👇 If you don't know how to get the channel id send a message in the channel and forward it to https://t.me/AH_ForwarderBot and copy the chat id and enter it in the below field (must include -100 in front)
    Log_channel_id = os.environ.get("Log_channel_id", "")
    #If deploying on vps edit the above value as example := Log_channel_id = "Your-Log_channel_id-inside-inverted-commas."
    
    Log_channel_username = os.environ.get("Log_channel_username", "") # The username of the log channel you created above! (must enter with '@' in the front of the username)
    #If deploying on vps edit the above value as example := Log_channel_username = "Your-Log_channel_username-inside-inverted-commas."
    
    Bot_username = os.environ.get("Bot_username", "") # Your bot's telegram username (must enter with '@' in the front of the username)
    #If deploying on vps edit the above value as example := Bot_username = "Your-Bot_username-inside-inverted-commas."
    
    DOWNLOAD_LOCATION = "./DOWNLOADS" # The download location (Don't change anything in this field!)
