
# Replace 5 and 7 in a string
def parse_wah(text: str) -> str:

    # Replace 5 and 7 in 
    if text.count("5") > 0 and text.count("7") > 0:
        text = text.replace("5", "wah ")
        text = text.replace("7", "wah-wah ")
    elif text.count("5") > 0:
        text = text.replace("5", "wah")
    elif text.count("7") > 0:
        text = text.replace("7", "wah-wah")

    return text


# Returns a list containing the most user(s) with the most wah
# and removes it from the wall
def max_wah(wall_of_shame: dict) -> list:
    max_shamers = list()
    current_max = 0

    shamers = wall_of_shame.copy()

    for user, count in shamers.items():
        if count > current_max:
            # Replace current shamers in wall_of_shame
            for shamer in max_shamers:
                wall_of_shame[shamer[0]] = shamer[1]
            
            # Build new list with new max
            max_shamers = [(user, wall_of_shame.pop(user))]

            current_max = count

        elif count == current_max:
            max_shamers.append((user, wall_of_shame.pop(user)))
    return max_shamers


# Raises an error if the secret is None
def checkSecrets(token, signing, users_url):
    if (token is None):
        raise RuntimeError("SLACK_TOKEN environment variable is missing")
    
    if (signing is None):
        raise RuntimeError("SIGNING_SECRET environment variable is missing")
    
    if (users_url is None):
        raise RuntimeError("USERS_URL environment variable is missing")