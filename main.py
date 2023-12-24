# Lux Discord bot made by Biksel
# Credit for Instagram Reel scraping goes to https://github.com/riad-azz/instagram-video-downloader

import discord
import os
import subprocess
import re
import ffmpeg

f = open("config.txt", "r")

SESSION_ID = f.readline()

tt_headers = {'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'en-US,en;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive'}

url_regex = '(?<=\.com/)(.+?)(?=\?|$)'


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def start_ig_downloader():
    subprocess.run("npm run dev", shell=True, cwd="C:\programming\instagram-video-downloader")

def clean_downloads():
    for file in os.listdir("."):
            if os.path.isfile(file) and (".mp4" in file or ".jpeg" in file or ".mp3" in file):
                os.remove(file)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    #t = threading.Thread(target=start_ig_downloader, daemon=True)
    #t.start()

@client.event
async def on_message(message):
    if "tiktok.com/" in message.content: # Got rate limited / banned, need to find another way to do this
        link = str(re.findall(r'\bhttps?://.*[(tiktok|douyin)]\S+', message.content)[0])
        msg = await message.channel.send("Downloading video...")
        subprocess.run(f'yt-dlp {link} -o "tiktok.%(ext)s"', shell=True, cwd="C:\programming\lux")
        msg = await msg.edit(content="Converting video...")
        for file in os.listdir("."):
            if ".mp3" in file:
                msg = await msg.edit("Slideshows are not supported as of yet")
                return
        input = ffmpeg.input("tiktok.mp4")
        out = ffmpeg.output(input, "out.mp4", acodec="copy", vcodec="libx264")
        ffmpeg.run(out)
        await message.channel.send(f"Sent by {message.author.name}", file=discord.File("out.mp4"))
        await msg.delete()
        await message.delete()
        clean_downloads()

    if "www.instagram.com" in message.content and not message.author.bot:
        # Deprecated, TODO add separate functionality to download shit
        '''print("Found reel")
        r = requests.get(f"http://localhost:3000/api/video?url={message.content}")
        print(r.status_code)
        raw_link = json.loads(r.text)["data"]["videoUrl"]
        urllib.request.urlretrieve(raw_link, "reel.mp4")'''
        await message.channel.send(message.author.name + ": " + str(message.content).replace("instagram.com", "ddinstagram.com"))
        await message.delete()
        clean_downloads()

    if "x.com" in message.content and not message.author.bot:
        await message.channel.send(message.author.name + ": " + str(message.content).replace("x.com", "fixvx.com"))
        await message.delete()
    if "twitter.com" in message.content and not message.author.bot:
        await message.channel.send(message.author.name + ": " + str(message.content).replace("twitter.com", "fxtwitter.com"))
        await message.delete()

    if "Thanks Lux" in message.content():
        await message.channel.send(f"It's my plesasure, {message.author.name}")

client.run(f.readline())
