import random
import string
import requests
import time

WEBHOOK = "https://discord.com/api/webhooks/1399859992714280961/8wxU1bU7u7f3YNpPqmrnSX96PKvnibr0KE1h6rdHnHSOVe3thFISikr_pZy58nndFyKc"
headers = {"User-Agent": "Mozilla/5.0"}

def generate_username():
    patterns = [
        lambda: ''.join(random.choices(string.ascii_lowercase, k=4)),
        lambda: random.choice(string.ascii_lowercase) + random.choice(string.digits) + ''.join(random.choices(string.ascii_lowercase, k=2)),
        lambda: ''.join(random.choices(string.ascii_lowercase, k=5)),
        lambda: random.choice(string.ascii_lowercase) + ''.join(random.choices(string.digits, k=2)) + random.choice(string.ascii_lowercase),
        lambda: ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
    ]
    return random.choice(patterns)()

def check_username(user):
    url = f"https://www.instagram.com/{user}/"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.status_code == 404
    except:
        return False

def send(content):
    data = {"content": content}
    try:
        requests.post(WEBHOOK, json=data)
    except:
        pass

while True:
    user = generate_username()
    if check_username(user):
        send(f"AVAILABLE USER ({user})\n@everyone\nTOOL BY grayhatx69")
        print(f"[✅] {user} is available")
    else:
        send(f"user ({user}) is taken\nTOOL BY grayhatx69")
        print(f"[❌] {user} is taken")
    time.sleep(3)
