# Lux Discord bot made by Biksel
# Credit for Instagram Reel scraping goes to https://github.com/riad-azz/instagram-video-downloader

import discord
import os
import subprocess
import re
import ffmpeg
import random
import string

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
    if "tiktok.com/" in message.content or "www.instagram.com/reel" in message.content: # Got rate limited / banned, need to find another way to do this
        #link = re.findall(r'(https?://(?:www\.)?(?:instagram\.com/reel|tiktok\.com)\S*?/p/\w{11}/?)', message.content)
        link = message.content
        msg = await message.channel.send("Downloading video...")
        command = None
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if "tiktok" in link:
            command = f'yt-dlp {link} -o "{name}.%(ext)s" --force-overwrites"' #-f "best[format_id^=h264][format_id$=-1]
        elif "instagram" in link:
            command = f'yt-dlp {link} -o "{name}.%(ext)s" --force-overwrites --cookies-from-browser firefox'
        subprocess.run(command, shell=True, cwd="C:\programming\lux")
        for file in os.listdir("."):
            if ".mp3" in file:
                msg = await msg.edit(content="Slideshows are not supported as of yet")
                clean_downloads()
                return None
        msg = await msg.edit(content="Uploading video...")
        '''
        input = ffmpeg.input("tiktok.mp4")
        out = ffmpeg.output(input, "out.mp4", acodec="copy", vcodec="libx264", preset="ultrafast")
        ffmpeg.run(out)'''
        try:
            await message.channel.send(f"Sent by {message.author.name}", file=discord.File(f'{name}.mp4'))
        except Exception as e:
            msg = await msg.edit(content = e)
            if "instagram" in link:
                msg = await msg.edit(content="File too large, converting...")
                subprocess.run(f"ffmpeg -i {name}.mp4 -vcodec libx264 -crf 51 -preset ultrafast out.mp4")
                name = "out"
                await message.channel.send(f"Sent by {message.author.name} (downscaled)", file=discord.File(f'{name}.mp4'))
        await msg.delete()
        await message.delete()
        clean_downloads()

    ''' #deprecated
    if "www.instagram.com/reel" in message.content and not message.author.bot:
        print("Found reel")
        r = requests.get(f"http://localhost:3000/api/video?url={message.content}")
        print(r.status_code)
        raw_link = json.loads(r.text)["data"]["videoUrl"]
        urllib.request.urlretrieve(raw_link, "reel.mp4")
        await message.channel.send(message.author.name + ": " + str(message.content).replace("instagram.com", "ddinstagram.com"))
        await message.delete()
        clean_downloads()
    '''

    if "x.com" in message.content and not message.author.bot:
        await message.channel.send(message.author.name + ": " + str(message.content).replace("x.com", "fixvx.com"))
        await message.delete()
    if "twitter.com" in message.content and not message.author.bot:
        await message.channel.send(message.author.name + ": " + str(message.content).replace("twitter.com", "fxtwitter.com"))
        await message.delete()

    if "Thanks Lux" in message.content:
        await message.channel.send(f"It's my pleasure, {message.author.name}")

client.run(f.readline())
