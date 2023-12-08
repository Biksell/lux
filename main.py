import discord
import pyktok
import re
import os
import json
import requests
import browser_cookie3
import instascrape
from bs4 import BeautifulSoup
from requests_html import HTMLSession

SESSION_ID = ""

tt_headers = {'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'en-US,en;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive'}
ig_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
    Safari/537.36 Edg/79.0.309.43",
    "cookie": f'sessionid={SESSION_ID};'
}


url_regex = '(?<=\.com/)(.+?)(?=\?|$)'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if "vm.tiktok.com/" in message.content:
        await message.delete()
        await message.channel.send("Found a tiktok")
        vid_id = re.search(r"\b\w{9,9}\b", message.content).group(0)
        pyktok.save_tiktok(message.content, True, "", "firefox")
        await message.channel.send(f"Sent by {message.author.nick}", file=discord.File(f"{vid_id}_.mp4"))
    elif "instagram.com/reel/" in message.content:
        await message.channel.send("Found a reel")
        resp = requests.get()
        await message.channel.send(f"Sent by {message.author.nick}", file=discord.File("reel.mp4"))




f = open("config.txt", "r")
client.run(f.read())
