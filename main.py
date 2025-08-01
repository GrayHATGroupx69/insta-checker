import asyncio
import os
import configparser
from discord.ext import tasks
import discord

CONFIG_FILE = "config.ini"

class SelfBot(discord.Client):
    def __init__(self, messages, user_id, delay):
        super().__init__()
        self.messages = messages
        self.user_id = user_id
        self.delay = delay
        self.current_index = 0
        self.send_messages = self.create_send_loop()

    def create_send_loop(self):
        @tasks.loop(seconds=0.1)
        async def loop():
            await self.wait_until_ready()

            user = self.get_user(self.user_id)
            if user is None:
                print(f"❌ Can't find user in cache. Make sure the user messaged you before.")
                await self.close()
                return

            try:
                dm = await user.create_dm()
                message = self.messages[self.current_index]
                await dm.send(message)
                print(f"✅ Sent: {message}")
                self.current_index = (self.current_index + 1) % len(self.messages)
            except Exception as e:
                print(f"⚠️ Error sending message: {e}")

            await asyncio.sleep(self.delay)

        return loop

    async def on_ready(self):
        print(f'✅ Logged in as {self.user} (ID: {self.user.id})')
        print('--------------------------')
        self.send_messages.start()

def save_config(token, user_id):
    config = configparser.ConfigParser()
    config["DISCORD"] = {
        "token": token,
        "user_id": str(user_id)
    }
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        return None
    config.read(CONFIG_FILE)
    if "DISCORD" in config and "token" in config["DISCORD"] and "user_id" in config["DISCORD"]:
        token = config["DISCORD"]["token"]
        user_id = int(config["DISCORD"]["user_id"])
        return token, user_id
    return None

def main():
    config_data = load_config()
    if config_data is None:
        token = input("Enter your Discord token: ")
        user_id = int(input("Enter target user ID (for DMs): "))
        save_config(token, user_id)
        print(f"Config saved to {CONFIG_FILE}.")
    else:
        token, user_id = config_data
        print(f"Loaded config from {CONFIG_FILE}.")

    delay = 0.5  # سرعة الإرسال: كل نصف ثانية

    if not os.path.exists("messages.txt"):
        print("❌ messages.txt not found.")
        return

    with open("messages.txt", "r", encoding="utf-8") as file:
        messages = [line.strip() for line in file if line.strip()]

    if not messages:
        print("❌ messages.txt is empty.")
        return

    client = SelfBot(messages, user_id, delay)
    client.run(token)

if __name__ == "__main__":
    main()
