import discord
from discord.ext import commands
import logging

import settings
import fmp_api as api

# -----------------------------------------------------------------------------------------
# LOGGER
# -----------------------------------------------------------------------------------------
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# -----------------------------------------------------------------------------------------
# BOT LOGIN
# -----------------------------------------------------------------------------------------
bot = discord.Bot(debug_guilds=settings.DEBUG_GUILD_IDS)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Will need to load json files on login

# -----------------------------------------------------------------------------------------
# COMMANDS
# -----------------------------------------------------------------------------------------
buy_commands = bot.create_group("buy", "Buy an asset")
sell_commands = bot.create_group("sell", "Sell an asset")

@buy_commands.command(name="stock", description="Buy stock.")
async def stock(
    ctx: discord.ApplicationContext,
    ticker: discord.Option(str, "Enter ticker"),
    quantity: discord.Option(int, "Enter desired quantity to buy")
    ):
    ticker = ticker.upper()
    price = api.get_price(ticker, 'stock')

    await ctx.respond(f"Bought {quantity} {ticker} for ${(price * quantity):.2f}!")

@buy_commands.command(name="crypto", description="Buy crypto.")
async def crypto(
    ctx: discord.ApplicationContext,
    ticker: discord.Option(str, "Enter ticker"),
    quantity: discord.Option(int, "Enter desired quantity to buy")
    ):
    ticker = ticker.upper()
    price = api.get_price(ticker, 'crypto')

    await ctx.respond(f"Bought {quantity} {ticker} for ${(price * quantity):.2f}!")

@sell_commands.command(name="stock", description="Sell stock.")
async def sell(
    ctx: discord.ApplicationContext,
    ticker: discord.Option(str, "Enter asset ticker"),
    quantity: discord.Option(int, "Enter desired quantity to sell")
    ):
    ticker = ticker.upper()
    price = api.get_price(ticker, 'stock')
    await ctx.respond(f"Sold {quantity} {ticker} for ${(price * quantity):.2f}!")

@sell_commands.command(name="crypto", description="Sell crypto.")
async def sell(
    ctx: discord.ApplicationContext,
    ticker: discord.Option(str, "Enter asset ticker"),
    quantity: discord.Option(int, "Enter desired quantity to sell")
    ):
    ticker = ticker.upper()
    price = api.get_price(ticker, 'crypto')
    await ctx.respond(f"Sold {quantity} {ticker} for ${(price * quantity):.2f}!")

# -----------------------------------------------------------------------------------------
# WORK IN PROGRESS: COGS (Having a lot of issues. See /cogs/orders.py)
# -----------------------------------------------------------------------------------------
# cogs_list = ['orders']
# for cog in cogs_list:
#     bot.load_extension(f'cogs.{cog}')

bot.run(settings.BOT_TOKEN)