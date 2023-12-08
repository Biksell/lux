import discord
import pyktok
import os

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

pyktok.specify_browser("firefox")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if "tiktok.com/" in message.content:
        #vid_id = re.search(r"\b\w{9,9}\b", message.content).group(0)
        print(pyktok.get_tiktok_json(message.content))
        pyktok.save_tiktok(message.content, True, "", "firefox")
        for file in os.listdir("."):
            if os.path.isfile(file) and ".mp4" in file:
                outfile = file
        await message.channel.send(f"Sent by {message.author.name}", file=discord.File(outfile))
        await message.delete()
        for file in os.listdir("."):
            if os.path.isfile(file) and (".mp4" in file or ".jpg" in file):
                os.remove(file)
    if "x.com" in message.content and not message.author.bot:
        await message.channel.send(message.author.name + ": " + str(message.content).replace("x.com", "fixvx.com"))
        await message.delete()
    if "twitter.com" in message.content and not message.author.bot:
        await message.channel.send(message.author.name + ": " + str(message.content).replace("twitter.com", "fxtwitter.com"))
        await message.delete()

client.run(f.readline())
