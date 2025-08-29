import requests
import os

# === CONFIGURATION ===
WEBHOOK_URL = "WEB-HOOK HERE"  # <-- Replace with your webhook
LOG_FILE = "user_log.txt"
START_ID = 1   # starting point if no log exists


def get_last_checked():
    """Read the last checked ID from log file."""
    if not os.path.exists(LOG_FILE):
        return START_ID
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        if not lines:
            return START_ID
        last_line = lines[-1]
        try:
            return int(last_line.split()[0]) + 1
        except:
            return START_ID


def check_profile(user_id: int):
    """Check if Roblox profile exists."""
    url = f"https://www.roblox.com/users/{user_id}/profile"
    response = requests.get(url)

    if response.status_code == 200 and "Page cannot be found" not in response.text:
        return True, url
    return False, url


def send_webhook(url: str, user_id: int):
    """Send message to Discord webhook."""
    data = {
        "content": f"✅ Found profile: {url} (ID: {user_id})"
    }
    requests.post(WEBHOOK_URL, json=data)


def main():
    user_id = get_last_checked()

    while True:  # continuous scan
        found, url = check_profile(user_id)

        with open(LOG_FILE, "a") as f:
            if found:
                print(f"[FOUND] {user_id}")
                f.write(f"{user_id} found\n")
                send_webhook(url, user_id)
            else:
                print(f"[NOT FOUND] {user_id}")
                f.write(f"{user_id} not found\n")

        user_id += 1


if __name__ == "__main__":
    main()
