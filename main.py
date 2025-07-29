import requests
import time
import random
import string

WEBHOOK_URL = "https://discord.com/api/webhooks/1399569154218135653/Xi_Bs7y3hKxA3TFD1iLo8eP8coiAy74Cle6rJLEqlf05LkvWCoCWiXfOo8qYXkufYMPm" 


def generate_username():
    length = random.choice([3, 4, 5])
    username = ""

    
    patterns = {
        3: ["lll", "lln", "lnl", "nll"],
        4: ["llll", "llln", "lnll", "l_ll", "ll.n", "l.n_"],  
        5: ["lllll", "lll1l", "l1lll", "l_lll", "ll.n1"]
    }

    pattern = random.choice(patterns[length])

    for p in pattern:
        if p == "l":
            username += random.choice(string.ascii_lowercase)
        elif p == "n":
            username += random.choice(string.digits)
        elif p == "_":
            username += "_"
        elif p == ".":
            username += "."
    return username


def is_available(username):
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    return response.status_code == 404


def send_to_discord(username):
    data = {
        "content": f"🟢 متاح: `{username}`\nhttps://instagram.com/{username}"
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print(f"✅ تم الإرسال: {username}")
    else:
        print(f"❌ فشل الإرسال: {response.status_code}")


def start_checking():
    tried = set()
    while True:
        username = generate_username()
        if username in tried:
            continue
        tried.add(username)
        try:
            if is_available(username):
                send_to_discord(username)
            else:
                print(f"❌ مستخدم: {username}")
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
        time.sleep(1)  

if __name__ == "__main__":
    start_checking()
