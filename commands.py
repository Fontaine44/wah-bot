import json
import utils
import random
from slack import WebClient


# /wallofshame command
def wall_of_shame(channel_id: str, client: WebClient) -> None:

    bot_message = "This is the current wall of shame: \n\n"

    wall_of_shame = dict()

    with open('./users.json', 'r') as f:
        users = json.load(f)

        for user_id, count in users.items():
            if (count > 1):
                # Fetch user info
                result = client.users_info(user=user_id)
                # Take username
                username = result["user"]["profile"]["real_name"]
                # Add to wall of shame
                wall_of_shame[username] = count

        
        pos = 1
        while len(wall_of_shame.keys()) > 0:
            # Get user with hights count
            max_shamers = utils.max_wah(wall_of_shame)

            # Add them to wall of shame
            for shamer in max_shamers:
                bot_message += f"{pos}. {shamer[0]}: {utils.parse_wah(str(shamer[1]))}\n" 

            pos += len(max_shamers)

        bot_message += "\nShame on you!"

        client.chat_postMessage(channel=channel_id,text=bot_message)


# /surunwah command
def sur_un_wah(channel_id: str, client: WebClient) -> None:

    roll = random.randrange(1, 6)

    filename = f"./images/dice_roll_{roll}.png"

    client.files_upload(    
        file=filename,
        initial_comment="And your dice roll is...",
        channels=channel_id
    )

    if roll == 5:
        client.chat_postMessage(channel=channel_id,text="lol")
