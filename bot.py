import os
import slack
import message
import commands
import utils
from dotenv import load_dotenv
from flask import Flask, Response, request, jsonify
from slackeventsapi import SlackEventAdapter
from threading import Thread


# Setup secrets
if not load_dotenv():
    raise RuntimeError("No environment variables were set.")

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SIGNING_SECRET = os.getenv("SIGNING_SECRET")
USERS_URL = os.getenv("USERS_URL")
JOKES_URL = os.getenv("JOKES_URL")
TENOR_KEY = os.getenv("TENOR_KEY")

# Verify secrets are set
utils.check_secrets(SLACK_TOKEN, SIGNING_SECRET, USERS_URL, JOKES_URL)


app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

client = slack.WebClient(token=SLACK_TOKEN)

@slack_event_adapter.on('message')
def message_event(payload):
    message.handler(payload, client)


@app.route('/wallofshame', methods=['POST'])
def wall_of_shame_event():
    commands.wall_of_shame(request.form, client)
    return Response(), 200


@app.route('/surunwah', methods=['POST'])
def sur_un_wah_event():
    commands.sur_un_wah(request.form, client)
    return Response(), 200

@app.route('/joke', methods=['POST'])
def joke_event():
    commands.joke(request.form, client)
    return Response(), 200

@app.route('/rats', methods=['POST'])
def rats_event():
    Thread(target=commands.rats, args=[request.form, client]).start()
    return Response(), 200


@app.route('/health', methods=['GET'])
def health_check():
    return "healthy"


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        return message.get_users()
    if request.method == "POST":
        new_users = request.get_json()
        users = message.update_users(new_users)
        return jsonify(users)


if __name__ == "__main__":
    app.run(debug=True)