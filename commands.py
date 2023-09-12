import random
import message
import utils
from datetime import datetime
from slack import WebClient
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo # type: ignore


# /wallofshame command
def wall_of_shame(payload: dict, client: WebClient) -> None:
    channel_id = payload.get('channel_id')
    user_id = payload.get('user_id')

    date_time = datetime.now(ZoneInfo("America/Montreal"))
    date_time = date_time.strftime("%Y-%m-%d, %H:%M:%S")
    date_time = utils.parse_wah(date_time)

    bot_message = f"Hey <@{user_id}>,\nHere is the current wall of shame as of _{date_time}_ : \n\n"

    wall_of_shame = dict()

    users = message.get_users() # Get list of users from json file

    # Get username of all users and add them to wall of shame dict with their count
    for user_id, count in users.items():
        if (count > 1):
            # Fetch user info
            result = client.users_info(user=user_id)
            # Take username
            username = result["user"]["profile"]["real_name"]
            # Add to wall of shame
            wall_of_shame[username] = count

    
    # Build wall of shame leaderboard string
    pos = 1
    while len(wall_of_shame.keys()) > 0:
        # Get user with hight count
        max_shamers = utils.max_wah(wall_of_shame)

        # Add them to wall of shame
        for shamer in max_shamers:
            text_pos = utils.parse_wah(str(pos))
            bot_message += f"*{text_pos}.* _{shamer[0]}_: {utils.parse_wah(str(shamer[1]))}\n" 

        pos += len(max_shamers)

    bot_message += "\nShame on you!"

    client.chat_postMessage(channel=channel_id,text=bot_message)


# /surunwah command
def sur_un_wah(payload: str, client: WebClient) -> None:
    channel_id = payload.get('channel_id')
    user_id = payload.get('user_id')

    roll = random.randrange(1, 6)

    filename = f"./images/dice_roll_{roll}.png"

    client.files_upload(    
        file=filename,
        initial_comment=f"<@{user_id}>, your dice roll is...",
        channels=channel_id
    )

    if roll == 5:
        client.chat_postMessage(channel=channel_id,text="lol")
