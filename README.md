# KittiesSender - Telegram Bot
Telegram bot that sends pictures of cats and can add user's picture into database

Python, Aiogram, Dropbox

# Quickstart
### Cloning repository
    git clone --depth 1 https://github.com/Tokiwokoe/KittiesSender.git
### Create a bot
Find @BotFather in Telegram and create your own bot. Copy the token
### Setting virtual environment
    python -m venv venv
    \venv\Scripts\activate
    pip install -r requirements.txt
### Copy environment variables to .env and fill it with your values
    cp .env.template .env
### Run the app locally
    python run.py

# Usage
### Start chat
To start a chat with a bot, you need to write /start or /hi to it

### Commands list
To see the list of commands you should write /help
#### Commands list:
    /start, /hi - start chat
    /help - see the commands list
    /catpic - receive a random picture of cat from bot's database
    <message with heart emoji> - show your love to bot
    <your picture> - send a picture of your cat. After passing the moderation, bot will add it to it's database