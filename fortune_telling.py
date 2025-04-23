import os
import discord
from dotenv import load_dotenv
import google.generativeai as genai
import datetime
from discord.ext import tasks

# 環境変数の取得
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # 数値で指定（例: 123456789012345678）

# Gemini APIの設定
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Discord Botの設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# プロンプトファイルの読み込み
def load_prompt():
    with open("/home/niente0706/daily_fortune_bot/prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")
    loop.start()  # Bot準備完了後にタスクを開始

# 毎日7時に定時実行
@tasks.loop(seconds=60)
async def loop():
    now = datetime.datetime.now().strftime("%H:%M")
    if now == '07:00':
        prompt = load_prompt()
        response = model.generate_content(prompt)
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(response.text)

# Botの起動
client.run(DISCORD_TOKEN)
