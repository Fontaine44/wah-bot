import json
import re
import utils
import bot
import requests
from slack import WebClient


def handler(payload: dict, client: WebClient) -> None:
    event = payload.get('event', {})

    if event.get('user') in ["U04SWUHV4MT", "U04TDTFA9L1"]:
        return

    text = event.get('text')

    wah, wahwah = count_wah(text)

    if wah > 0 or wahwah > 0:
        # Get users dict
        users = get_users()

        channel_id = event.get('channel')
        user_id = event.get('user')

        # Increment count of user if present
        if user_id in users:
            users[user_id] += wah + wahwah
        else:
            # Add new user
            users[user_id] = wah + wahwah

        wah_count = utils.parse_wah(str(users[user_id]))

        bot_message = f"<@{user_id}> *COMBIEEENNNN?!?* \nYour wah/wah-wah count: *{wah_count}*"

        update_users(users)

        client.chat_postMessage(channel=channel_id,text=bot_message)


# Counts the number of wah and wah-wah
def count_wah(text):
    # Remove mentions
    text = re.sub("\<.*?\>", "", text)

    # Check for wah or wah-wah
    wah = text.count("5")
    wah += text.count("cinq")
    wah += text.count("five")
    wahwah = text.count("7")
    wahwah += text.count("sept")
    wahwah += 1 if text == "sept" else 0
    wahwah -= text.count("septembre")
    wahwah -= text.count("september")
    wahwah += text.count("seven")

    return wah, wahwah


def get_users():
    response = requests.get(bot.USERS_URL)
    users = response.json()
    return users


def update_users(users):
    requests.put(url=bot.USERS_URL, json=users)
    return users
