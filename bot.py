
import os
import discord
from discord.ext import commands
import requests

TOKEN = os.environ.get("DISCORD_TOKEN")
API_KEY = os.environ.get("API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot King Commerce ativo como {bot.user}")

@bot.command()
async def cotacao(ctx):
    try:
        response = requests.post(
            "https://bytemax.exchange/api/create_order",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "source_amount": 100,
                "source_currency": "BRL",
                "target_currency": "CNYBM"
            }
        )
        data = response.json().get("order_data", {})
        if "target_amount" in data:
            taxa = data["target_amount"] / data["source_amount"]
            await ctx.send(f"📈 1 BRL ≈ ¥{taxa - 0.09:.2f} CNYBM")
        else:
            await ctx.send("❌ Não foi possível obter a cotação.")
    except Exception as e:
        await ctx.send(f"Erro ao buscar cotação: {e}")

bot.run(TOKEN)
