# Mega Link Downloader Bot
<p align="center"><b>This is a telegram bot to download mega.nz links and return them as files/videos - Made by a 100% noob!</b></p>

<p align="center">(When I mean noob I really mean noob!)</p>

<b>You can find a live version of this bot in telegram as [@mega_downloader_robot](https://t.me/mega_downloader_robot)</b>

Created with ❤️ by <b>[@xmysteriousx](https://t.me/xmysteriousx)</b> as a part of [@mysterious_uploader_robot](https://t.me/mysterious_uploader_robot)

<p align="center"><a href="https://t.me/rezoth_tm"><img src="https://img.shields.io/badge/Telegram-Join%20Telegram%20Group-blue.svg?logo=telegram"></a></p>

Please be kind to star and fork this repo!✨😇
<br>

---

## Features 💫
 - Mega accounts are not needed!
 - Parallel download are supported! (This means many users can use the bot at the same time. 😇)
 - Multitasking is also supported ! (This means You (owner) and telegram users who you set as auth users will be able to download multiple links at the same time! 😋)
 - No quota limits will be occurred!
 - Custom thumbnail support!
 - Custom caption support!
 - Attractive progress bar when downloading and uploading files! 🙈
 - Ban unwanted users!
 - See your bot's user count!
 - Broadcast any message to every user of your bot!
 - Ability to download any file under 5GB! (If you provide a pro/business account when deploying there will be no file size limits! 😍)

<b>Note</b> :- Due to telegram API limits I can't upload files which are bigger than 2GB so such files will be spliited and uploaded to you!

---

## Deploying Methods

<details>
  <summary><b>Deploying to Heroku</b></summary>

<br>

- Choose Europe as server location when deploying. (Beacuse downloadings will be a little fast!).
- Examples of needed bot variables are mentioned below in this readme!
 
 <b>Note</b> :- It's best if you deploy on a vps because with heroku downloadings can be slow! 😕

<br>
  
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/XMYSTERlOUSX/mega-link-downloader-bot)
</details>

<details>
  <summary><b>Deploying on a VPS</b></summary>

<br>

**Make a vps (Recommended - Ubuntu 20.04 (LTS) x64 vps from a location/region near New Zealand) and log in to it.**
- Then execute the below commands. 👇
```sh  
sudo apt update
```
```sh  
sudo apt upgrade
```
```sh  
apt-get update
```
```sh  
apt-get install tmux
```
```sh  
tmux
```
**Now there are two methods to go further!**
- Method 1
  
  - Fork my repo. In the repo go inside to the `sample_config.py` and copy all the code in it. In your forked repo, create a file named `config.py` and paste the whole code in it. 
  - Then edit the values in it with your values! (Inside your `config.py` file you will see the examples of how to edit the fields.)
  - Then execute the below commands. 👇

```sh  
git clone You_forked_repo_url
```
```sh  
apt install python3-pip
```
```sh  
apt install ffmpeg
```
```sh  
cd mega-link-downloader-bot
```
```sh  
pip3 install -r requirements.txt
```
```sh  
python3 bot.py
```
Now If you did everything correctly bot will be running successfully! 🥳

- Method 2

  - Execute the below commands. 👇

```sh  
git clone https://github.com/XMYSTERlOUSX/mega-link-downloader-bot
```
```sh  
apt install python3-pip
```
```sh  
apt install ffmpeg
```
```sh  
cd mega-link-downloader-bot
```
```sh  
pip3 install -r requirements.txt
```
```sh  
cp sample_config.py config.py
```
```sh  
nano config.py
```
  - Now you will be inside the `config.py` file.
  - Then edit the values in it with your values! (Inside your `config.py` file you will see the examples of how to edit the fields.)
  - (For pasting letters, copy any value you want and take the curser to the place you want by arrow keys and right click the mouse! 😅)
  - After editing all with appropriate values as mentioned in the config file press Ctrl + X from your keyboard.
  - Then press y in your keyboard.
  - Then execute the below command. 👇
  
```sh  
python3 bot.py
```
Now If you did everything correctly, the bot will be running successfully! 🥳
</details>

---

## Variables
- `API_ID` -  Get this value from https://my.telegram.org/apps
- `API_HASH` - Get This Value from https://my.telegram.org/apps
- `TG_BOT_TOKEN` - Make a bot from https://t.me/BotFather and enter the token here.
- `Mega_email` - This is not necessary! Enter your mega email only if you have a mega.nz account with pro/business features.
- `Mega_password` - This is not necessary! Enter your mega password only if you have a mega.nz account with pro/business features.
- `Bot_username` - Your bot's telegram username. (must enter with '@' in the front of the username)
- `AUTH_USERS` - Id's of the telegram users, who you want to allow for multitasking - downloading multiple links at once!
- `OWNER_ID` - Your(owner's) telegram id
- `REDIS_URI` - Get This Value from https://app.redislabs.com/#/login
- `REDIS_PASS` - Get This Value from https://app.redislabs.com/#/login

---

## Bot Commands

<details>
  <summary><b>Normal User Commands</b></summary>

<br>

- `/start` - To check if the bot is alive!
- `/help` - To get the detailed help guide of using the bot!
- `/deletethumbnail` - To delete your saved custom thumbnail!
</details>

<details>
  <summary><b>Admin Commands</b></summary>

<br>

- `/delmyfolder` - To delete the download folder of the owner and the auth users. <br>
(Since owner and auth users support multitasking their downloads folder will not get deleted automatically!. So If you want to clean up the server storage hit that command and delete your download folder after all of your current downloads got uploaded. If you are on heroku free dynos this doesn't really matter but if you are on a vps please remember to do it once in a while!)<br>
<b>Note :- Do not send this command while links are being downloaded and uploaded!</b><br>
 
- `/black` - To ban unwanted users from the bot! <br>
(<b>Syntax of sending the commnad to the bot is</b>:- <code>/black</code> <i>userid</i>)<br>

- `/unblack` - To unban banned users from the bot! <br>
(<b>Syntax of sending the commnad to the bot is</b>:- <code>/unblack</code> <i>userid</i>)<br>
 
- `/lisblack` - To get the telegram id list of banned user's from the bot!<br>
 
- `/broadcast` - To broadcast a message to all the users of the bot! <br>
(<b>Syntax of sending the commnad to the bot is</b>:- <code>/broadcast</code> <i>as a reply to the message that you want to broadcast!</i>)<br>

- `/stats` - To get the total number of users who has used your bot!
</details>

---

### Reason for making this open source :-

<b>For the help of any guy like me in this world who is wondering how to make a bot for downloading mega links, or for whoever that is finding a code to download mega links; thought to make this public. 😇❤️</b>

---

## Credits, and Thanks to

* [Odwyersoftware](https://github.com/odwyersoftware) for the awesome [Python library](https://github.com/odwyersoftware/mega.py) of [mega.nz-API](https://mega.nz/API)
* [ProThinkerGang](https://github.com/ProThinkerGang) for the database module code!
* [Dan](https://github.com/delivrance) for [pyrogram](https://github.com/Pyrogram)

<b>Project written and created by</b> - [XMYSTERIOUSX](https://github.com/XMYSTERlOUSX)

---

#### LICENSE
- GPLv3
