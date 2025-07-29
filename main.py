import requests
import time
import random
import string

WEBHOOK_URL = "https://discord.com/api/webhooks/1399569154218135653/Xi_Bs7y3hKxA3TFD1iLo8eP8coiAy74Cle6rJLEqlf05LkvWCoCWiXfOo8qYXkufYMPm"


def generate_username():
    length = random.choice([3, 4])
    pattern = random.choice([
        "lll",     # مثل: abc
        "lln",     # مثل: ab1
        "lnl",     # مثل: a1b
        "nll",     # مثل: 1ab
        "llln",    # مثل: abc1
        "lnll",    # مثل: a1bc
        "llll"     # مثل: abcd
    ])
    username = ""
    for p in pattern:
        if p == "l":
            username += random.choice(string.ascii_lowercase)
        else:
            username += random.choice(string.digits)
    return username

def is_available(username):
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    return response.status_code == 404  

# إرسال إلى ديسكورد
def send_to_discord(username):
    data = {
        "content": f"🟢 NEW USER @everyone this tool by M5TL $ GRAYHATX69: `{username}`\nhttps://instagram.com/{username}"
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print(f"✅ أُرسل: {username}")
    else:
        print(f"❌ فشل الإرسال: {response.status_code}")

# التشغيل المستمر
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
        time.sleep(3)  

if __name__ == "__main__":
    start_checking()
