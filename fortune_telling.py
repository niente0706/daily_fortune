import os
import discord
from dotenv import load_dotenv
import google.generativeai as genai
import datetime
from discord.ext import tasks
from flask import Flask
import threading

# Flask server settings
app = Flask(__name__)

@app.route("/")
def home():
    return "Daily Fortune Bot is running!"

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# thread for Flask server
threading.Thread(target=run_http_server).start()

# load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Gemini API settings
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Discord Bot settings
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Load prompt from file
def load_prompt():
    with open("/home/niente0706/daily_fortune_bot/prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"占いBotが起動しました!")
    loop.start()

@client.event
async def on_disconnect():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"占いBotが停止しました!")

@tasks.loop(seconds=60)
async def loop():
    now = datetime.datetime.now().strftime("%H:%M")
    if now == '07:00':
        prompt = load_prompt()
        response = model.generate_content(prompt)
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(response.text)

# Start the bot
client.run(DISCORD_TOKEN)
