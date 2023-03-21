import json
import re
import utils
from slack import WebClient


def handler(payload: dict, client: WebClient) -> None:
    event = payload.get('event', {})

    if event.get('bot_id') == "B04T2AW8T9A":
        return

    text = event.get('text')

    # Remove mentions
    text = re.sub("\<.*?\>", "", text)

    wah = text.count("5")
    wahwah = text.count("7")

    if wah > 0 or wahwah > 0:

        with open('./users.json', 'r+') as f:
            users = json.load(f)

            channel_id = event.get('channel')
            user_id = event.get('user')

            if user_id in users:
                users[user_id] += wah + wahwah
            else:
                users[user_id] = wah + wahwah

            wah_count = utils.parse_wah(str(users[user_id]))

            bot_message = f"<@{user_id}> *COMBIEEENNNN?!?* \nYour wah/wah-wah count: *{wah_count}*"

            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(users, f, indent=4)
            f.truncate()     # remove remaining part

            client.chat_postMessage(channel=channel_id,text=bot_message)