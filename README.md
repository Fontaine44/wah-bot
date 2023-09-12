# wah-bot

Automated bot for the Slack messaging app. It is built to accomplish various tasks on the McGill Engineering Games executive team Slack server.

## Installation

The bot can run on Python 3.6+.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.


```bash
pip install -r requirements.txt
```

## Usage

This bot was set using mostly the tutorial [here](https://www.pragnakalp.com/create-slack-bot-using-python-tutorial-with-examples/)

### Set up
Head to [Slack](https://api.slack.com/apps) and create your bot application.

1. Authorize the following scopes to the bot: *channels:history, chat:write, commands, files:write, users:read.*

2. Enable events subscriptions.

3. Add the bot to your Slack workspace and channels.

4. In the python project, make a _.env_ file and replace the placeholders with your real secrets:
```txt
SLACK_TOKEN = "ENTER SLACK TOKEN HERE"
SIGNING_SECRET = "ENTER SIGNING SECRET HERE"
USERS_URL = "ENTER USERS URL HERE"
```
*Note: USERS_URL is an endpoint that exposes an Oracle Bucket that contains a JSON file. It can be read and written with GET and POST respectively. You can use any other way to store and modify a JSON file.*

5. Set up the events url and the commands url:
```text
<api-url>/slack/events
<api-url>/<command-name>
```

### Development

1. Run the bot locally:
```bash
python bot.py
```
2. Expose the 5000 port with [ngrok](https://ngrok.com/).
You will get a temporary http url that exposes your port 5000. It represents your api url.
```bash
ngrok http 5000
```

### Deployment
The bot has been deployed and works perfectly on [render.com](https://render.com/)
