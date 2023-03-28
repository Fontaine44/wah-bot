import os
import slack
import message
import commands
import utils
from dotenv import load_dotenv
from flask import Flask, Response, request
from slackeventsapi import SlackEventAdapter


# Setup secrets
load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SIGNING_SECRET = os.getenv("SIGNING_SECRET")

# Verify secrets are set
utils.checkSecrets(SLACK_TOKEN, SIGNING_SECRET)


app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

client = slack.WebClient(token=SLACK_TOKEN)

@slack_event_adapter.on('message')
def message_event(payload):
    message.handler(payload, client)


@app.route('/wallofshame', methods=['POST'])
def wall_of_shame_event():
    commands.wall_of_shame(request.form.get('channel_id'), client)
    return Response(), 200


@app.route('/surunwah', methods=['POST'])
def sur_un_wah_event():
    commands.sur_un_wah(request.form.get('channel_id'), client)
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)