# wolbot
Wolbot is a python powerd telegram bot for Wak On LAN tasks.


## Features
- List devices (All/Online/Offline) with status.
- Send magic packet to wake up the devices.


## Components and Frameworks used in Certi
* [Loguru](https://pypi.org/project/loguru/) a library which aims to bring enjoyable logging in Python.
* [PyYAML](https://pypi.org/project/PyYAML/) a data serialization format designed for human readability and interaction with scripting languages.
* [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/) A simple, but extensible Python implementation for the Telegram Bot API.
* [pyTelegramBotAPI](https://pypi.org/project/wakeonlan/) A small python module for wake on lan.


## How to use Wolbot
Wolbot can be installed and run as a system service or a Docker container.

1. Create new telegram bot and get the token
    Open [Telegram messenger](https://web.telegram.org/), sign in to your account or create a new one.

    Enter @Botfather in the search tab and choose this bot (Official Telegram bots have a blue checkmark beside their name.)

    [![@Botfather](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@Botfather")

    Click “Start” to activate BotFather bot.

    [![@start](https://github.com/t0mer/voicy/blob/main/screenshots/scr2-min.png?raw=true "@start")](https://github.com/t0mer/voicy/blob/main/screenshots/scr1-min.png?raw=true "@start")

    In response, you receive a list of commands to manage bots.
    Choose or type the /newbot command and send it.

    [![@newbot](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")](https://github.com/t0mer/voicy/blob/main/screenshots/scr3-min.png?raw=true "@newbot")


    Choose a name for your bot — your subscribers will see it in the conversation. And choose a username for your bot — the bot can be found by its username in searches. The username must be unique and end with the word “bot.”

    [![@username](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr4-min.png?raw=true "@username")


    After you choose a suitable name for your bot — the bot is created. You will receive a message with a link to your bot t.me/<bot_username>, recommendations to set up a profile picture, description, and a list of commands to manage your new bot.

    [![@bot_username](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")](https://github.com/t0mer/voicy/blob/main/screenshots/scr5-min.png?raw=true "@bot_username")



2. Set the following environment variables:
    * BOT_TOKEN=#Telegram bot Token generated in the previous step.
    * ALLOWED_IDS= #List of telegram id's allowed to communicate with the bot, comma-separated values.


3. If you want to run Wolbot as a ***docker container***, copy the following code into your docker-compose.yaml:
    ```yaml
    version: "3.6"
    services:
    wolbot:
        image: techblog/wolbot
        container_name: wolbot
        restart: always
        environment:
        - BOT_TOKEN= #Telegram bot Token.
        - ALLOWED_IDS= #List of telegram id's allowed to communicate with the bot, comma-separated values.
    ```
    **Make sure to set all the environment variables before running the *"docker-compose up -d"* command.


4. If you want to run Wolbot as a systemd service, clone the repository using the following command:
    ```bash
    git clone https://github.com/t0mer/wolbot
    ```
    enter the *wolbot* folder and install the dipendencies:
    ```bash
    pip3 install -r requirements.txt
    ```

    Next, create a file names **"wolbot.service"** under **/etc/systemd/system"** and paste the following content:

    ```bash
    [Unit]
    Description=Wake On Lan bot 
    After=network-online.target
    Wants=network-online.target systemd-networkd-wait-online.service
    StartLimitIntervalSec=5
    StartLimitBurst=5

    [Service]
    EnvironmentFile=/etc/environment
    KillSignal=SIGINT
    WorkingDirectory=/opt/dev/wolbot/app/
    Type=simple
    User=root
    ExecStart=/usr/bin/python3 /opt/dev/wolbot/app/app.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
    ***Make sure to adjust the path for "WorkingDirectory" and "ExecStart" accordingly to the path of the Wolbot location***

    Next, run the following command to enable and start the service:
    ```bash
    systemctl enable wolbot.service
    systemctl start wolbot.service
    ```
    To check the status of the service, run the following command:
    ```bash
    systemctl status wolbot.servies
    ```