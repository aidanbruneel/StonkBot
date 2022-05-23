import discord
import logging

from embedded_messages import embedded_message, ConfirmButtons
import config
from fmp_api import Query
from player import Player, make_leaderboard


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
bot = discord.Bot(debug_guilds=config.DEBUG_GUILD_IDS)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Will need to load json files on login


# -----------------------------------------------------------------------------------------
# ORDER COMMANDS
# -----------------------------------------------------------------------------------------
@bot.command(name="buy", description="Buy an asset.")
async def buy_asset(
    ctx: discord.ApplicationContext,
    symbol: discord.Option(str, "Enter asset symbol"),
    quantity: discord.Option(float, "Enter desired quantity to buy")
    ):
    player = Player(str(ctx.author.id), str(ctx.author))

    symbol = symbol.upper()
    query = Query(symbol)
    
    if(query.quote is None):
        await ctx.respond(f"Could not find {symbol}. Please try again.")
    else:
        match query.exchange:
            case "CRYPTO":
                fee = query.price * quantity * 0.0015
                thumbnail_url = config.CRYPTO_ICON
            case _:
                fee = 0.00
                thumbnail_url = query.image

        fields_list = [
            ["Order Type", "Market Buy"],
            ["Asset Price", f"${query.price:.2f}"],
            ["Quantity", quantity], 
            ["Order Subtotal", f"${(quantity * query.price):.2f}"],
            ["Fees", f"${(fee):.2f}"],
            ["Order Total", f"${(quantity * query.price + fee):.2f}"],
            [chr(173), chr(173)] # change this to balance remaining
        ]

        view = ConfirmButtons(symbol, quantity, True, ctx, player)
        await ctx.respond(embed=embedded_message(
            status='pending',
            author=query.exchange,
            thumbnail=thumbnail_url,
            title=symbol,
            desc=query.name,
            fields=fields_list,
            footer_text="Order Status: Pending",
            colour=0xEEB902), view=view)


# remove the final if query.exchange and have only one await statement
@bot.command(name='sell', description="Sell an asset.")
async def sell_asset(
    ctx: discord.ApplicationContext,
    symbol: discord.Option(str, "Enter asset symbol"),
    quantity: discord.Option(float, "Enter desired quantity to sell")
    ):
    player = Player(str(ctx.author.id), str(ctx.author.id))
    
    symbol = symbol.upper()
    query = Query(symbol)

    if(query.quote is None):
        await ctx.respond(f"Could not find {symbol}. Please try again.")
    else:
        match query.exchange:
            case "CRYPTO":
                fee = query.price * quantity * 0.0015
                thumbnail_url = config.CRYPTO_ICON
            case _:
                fee = 0.00
                thumbnail_url = query.image

        fields_list = [
            ["Order Type", "Market Sell"],
            ["Asset Price", f"${query.price:.2f}"],
            ["Quantity", quantity], 
            ["Order Subtotal", f"${(quantity * query.price):.2f}"],
            ["Fees", f"${(fee):.2f}"],
            ["Order Total", f"${(quantity * query.price - fee):.2f}"],
            [chr(173), chr(173)]
        ]

        view = ConfirmButtons(symbol, quantity, False, ctx, player)
        await ctx.respond(embed=embedded_message(
            status='pending',
            author=query.exchange,
            thumbnail=thumbnail_url,
            title=symbol,
            desc=query.name,
            fields=fields_list,
            footer_text="Order Status: Pending",
            colour=0xEEB902), view=view)


# -----------------------------------------------------------------------------------------
# ASSET COMMANDS
# -----------------------------------------------------------------------------------------
@bot.command(name='profile', description="Display user profile")
async def profile(ctx: discord.ApplicationContext):
    player = Player(str(ctx.author.id), str(ctx.author))
    await ctx.respond(f"**Profile**\n{ctx.author.display_name}\n**Net Worth**\n${(player.get_net_worth()):.2f}\n**Cash (Buying Power)**\n${(player.profile['cash']):.2f}\n**Portfolio**\n{player.profile['portfolio']}", ephemeral = True)

@bot.command(name='leaderboard', description='Display a leaderboard of the current players')
async def leaderboard(ctx: discord.ApplicationContext):
    
    data = make_leaderboard()

    leaderboard_top = ""

    for i in range(min(len(data))):
        leaderboard_top += f"**{i + 1}. {data[i][0]} - ${data[i][1]:.2f}**\n"

    if len(data) == 0:
        await ctx.respond(embed=embedded_message(
            author="Your Stonk Bot",
            title="LEADERBOARD",
            desc="No Winners"
        ))
    else:
        await ctx.respond(embed=embedded_message(
            author="Your Stonk Bot",
            title="THE MOON BOARD",
            desc=leaderboard_top,
            footer_text="AMAZING JOB ~ Your Stonk Broker",
            colour=0xD88C9A,
            thumbnail='https://cdn.discordapp.com/attachments/976929148264128593/978117534538678292/unknown.png'
        ))



@bot.command(name='quote', description="Display quote of an asset.")
async def quote(
    ctx: discord.ApplicationContext,
    symbol: discord.Option(str, "Enter asset symbol")
    ):
    symbol = symbol.upper()
    query = Query(symbol)

    if(query.quote is None):
        await ctx.respond(f"Could not find {symbol}. Please try again.")
    else:
        match query.exchange:
            case "CRYPTO":
                thumbnail_url = config.CRYPTO_ICON
            case _:
                thumbnail_url = query.image
        fields_list = [
            ["Asset Price", f"${(query.price):.2f}"],

            ["Price Change", f"${(query.price):.2f} ({(query.change_percent):.2f}%)"],
            ["Volume ", f"{query.volume}"],
            ["Avg Volume", f"{query.avg_volume}"],

            ["Open", f"${(query.open):.2f}"],
            ["High", f"${(query.day_high):.2f}"],
            ["Low", f"${(query.day_low):.2f}"],

            ["Previous Close", f"${(query.previous_close):.2f}"],
            ["Year High", f"${(query.year_high):.2f}"],
            ["Year Low", f"${(query.year_low):.2f}"],

            ["Market Cap", f"${query.market_cap}"],
            ["P/E Ratio",  '-' if query.exchange == 'CRYPTO' else f"{(query.pe_ratio)}"],
            ["Earnings Per Share", '-' if query.exchange == 'CRYPTO' else f"${(query.eps):.2f}"],

            ["50-Day Average", f"${(query.price_avg_50d):.2f}"],
            ["200-Day Average", f"${(query.price_avg_200d):.2f}"],
            ["Shares Outstanding", f"{(query.shares_outstanding):.2f}"]
            ]
            
        await ctx.respond(embed=embedded_message(
            status='info',
            author=query.exchange,
            thumbnail=thumbnail_url,
            title=symbol,
            desc=query.name,
            fields=fields_list,
            footer_text="Quote",
            colour=0x3F84E5), ephemeral=True)

bot.run(config.BOT_TOKEN)
