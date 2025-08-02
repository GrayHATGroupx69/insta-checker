import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import aiohttp

BOT_TOKENS = [
    "MTM5MzUyODM3NzcwNDU3OTE4NA.G4_OmG.n-GC68tsitv21SEpoFc5jpTN-eeCbUSda5Jyxk",
]

intents = discord.Intents.all()
bots = []
voice_clients = {}
queues = {}
loop_flags = {}


def play_next(ctx, guild_id):
    if queues[guild_id]:
        source = queues[guild_id].pop(0)
        voice_clients[guild_id].play(source, after=lambda e: play_next(ctx, guild_id))
    else:
        loop_flags[guild_id] = False


for token in BOT_TOKENS:
    bot = commands.Bot(command_prefix="-", intents=intents)
    bots.append(bot)

    @bot.event
    async def on_ready():
        print(f"{bot.user.name} is ready!")

    @bot.command()
    async def setchannels(ctx, channel_id: int):
        print(f"setchannels command called with channel_id: {channel_id}")
        channel = bot.get_channel(channel_id)
        if channel:
            print(f"Channel found: {channel.name} (type: {type(channel)})")
            if isinstance(channel, discord.VoiceChannel):
                print("Attempting to connect to the voice channel...")
                try:
                    voice_client = await channel.connect(reconnect=True)
                    voice_clients[ctx.guild.id] = voice_client
                    await ctx.send(f"All bots joined channel {channel.name}")
                except Exception as e:
                    print(f"Error: {e}")
                    await ctx.send("Failed to connect to the voice channel.")
            else:
                print("The provided channel ID is not a voice channel.")
                await ctx.send("The provided channel ID is not a voice channel.")
        else:
            print("Channel not found!")
            await ctx.send("Invalid channel ID!")

    @bot.command()
    async def setbotchannel(ctx, bot_mention: discord.Member, channel_id: int):
        if bot_mention.id == bot.user.id:
            channel = bot.get_channel(channel_id)
            if channel:
                voice_client = await channel.connect(reconnect=True)
                voice_clients[ctx.guild.id] = voice_client
                await ctx.send(f"{bot.user.name} joined channel {channel.name}")
            else:
                await ctx.send("Invalid channel ID!")

    @bot.command(aliases=["p"])
    async def play(ctx, *, query: str):
        guild_id = ctx.guild.id
        if guild_id not in queues:
            queues[guild_id] = []
        if guild_id not in loop_flags:
            loop_flags[guild_id] = False

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': 'in_playlist',
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0',
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)['entries'][0]
                url = info['url']
                print(f"Playing URL: {url}")
                source = discord.FFmpegPCMAudio(
                    url,
                    before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                    options="-vn"
                )
                queues[guild_id].append(source)

            if not voice_clients[guild_id].is_playing():
                play_next(ctx, guild_id)
            await ctx.send(f"Added {query} to the queue!")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send("Failed to play the song. Please try again.")

    @bot.command(aliases=["s"])
    async def skip(ctx):
        guild_id = ctx.guild.id
        if voice_clients[guild_id].is_playing():
            voice_clients[guild_id].stop()
            play_next(ctx, guild_id)
            await ctx.send("Skipped the current song!")

    @bot.command(aliases=["loop"])
    async def repeat(ctx):
        guild_id = ctx.guild.id
        loop_flags[guild_id] = not loop_flags[guild_id]
        await ctx.send(f"Looping is now {'enabled' if loop_flags[guild_id] else 'disabled'}.")

    @bot.command()
    async def setbotavatar(ctx, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    await bot.user.edit(avatar=data)
                    await ctx.send("Avatar updated successfully!")

    @bot.command()
    async def setbotname(ctx, *, name: str):
        await bot.user.edit(username=name)
        await ctx.send(f"Bot name changed to {name}")

    @bot.command()
    async def setbotbio(ctx, *, bio: str):
        await bot.user.edit(about_me=bio)
        await ctx.send(f"Bot bio updated to: {bio}")


print("Starting the bot...")

async def main():
    print("Inside main function...")
    for bot, token in zip(bots, BOT_TOKENS):
        print(f"Starting bot with token: {token[:10]}...")
        asyncio.create_task(bot.start(token))
    print("All bots started.")
    await asyncio.Event().wait()  # Keep the loop running indefinitely


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())

