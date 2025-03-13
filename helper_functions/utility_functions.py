import requests


def get_user_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json().get("ip")
    except Exception as e:

        # logger

        # raise error instead of returning 0

        return 0


def get_access_count_for_user(user_ip):
    try:
        with open('user_access_cnt.txt', 'r') as file:
            # Read all lines in the file
            lines = file.readlines()

        # Loop through the lines to find the user_ip
        for line in lines:
            stored_ip, access_cnt = line.strip().split(' : ')
            if stored_ip == user_ip:
                return int(access_cnt)  # Return the access count as integer
        return 0  # Return 0 if user_ip is not found in the file
    except FileNotFoundError:
        return 0  # Return 0 if the file doesn't exist yet


def increase_access_cnt(user_ip):
    # Read current data from the file
    try:
        with open('user_access_cnt.txt', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []  # If the file doesn't exist, we start with an empty list

    user_found = False
    updated_lines = []

    # Loop through the lines and update the count for the user_ip
    for line in lines:
        stored_ip, access_cnt = line.strip().split(' : ')
        if stored_ip == user_ip:
            access_cnt = int(access_cnt) + 1  # Increase the count by 1
            updated_lines.append(f"{stored_ip} : {access_cnt}\n")
            user_found = True
        else:
            updated_lines.append(line)

    # If user_ip was not found, add a new entry for the user
    if not user_found:
        updated_lines.append(f"{user_ip} : 1\n")

    # Write the updated data back to the file
    with open('user_access_cnt.txt', 'w') as file:
        file.writelines(updated_lines)