import discord
import logging

from embedded_messages import embedded_message
import settings
from data_plotting import plot
from fmp_api import Query


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
# ORDER COMMANDS
# -----------------------------------------------------------------------------------------
# TODO: let the user ac buy the stocks and add them to json portfolio, ensure that user has funds to purchase, dm after purchase final receipt
@bot.command(name="buy", description="Buy an asset.")
async def buy_asset(
    ctx: discord.ApplicationContext,
    symbol: discord.Option(str, "Enter asset symbol"),
    quantity: discord.Option(float, "Enter desired quantity to buy")
    ):
    symbol = symbol.upper()
    query = Query(symbol)
    
    if(query.quote is None):
        await ctx.respond(f"Could not find {symbol}. Please try again.")
    else:
        if query.exchange == "CRYPTO":
            fee = query.price * quantity * 0.0015
        else:
            fee = 0.00

        fields_list = [
            ["Order Type", "Market Buy"],
            ["Asset Price", f"${query.price:.2f}"],
            ["Quantity", quantity], 
            ["Order Subtotal", f"${(quantity * query.price):.2f}"],
            ["Fees", f"${(fee):.2f}"],
            ["Order Total", f"${(quantity * query.price + fee):.2f}"],
            [chr(173), chr(173)] # change this to balance remaining
        ]

        # if query.image

        if query.exchange == "CRYPTO":
            await ctx.respond(embed=embedded_message(
                status='pending',
                author=query.exchange,
                title=symbol,
                desc=query.name,
                fields=fields_list,
                footer_text="Order Status: Pending",
                colour=0x11BB11))
        else:
            await ctx.respond(embed=embedded_message(
                status='pending',
                author=query.exchange,
                thumbnail=query.image,
                title=symbol,
                desc=query.name,
                fields=fields_list,
                footer_text="Order Status: Pending",
                colour=0x11BB11))


# remove the final if query.exchange and have only one await statement
@bot.command(name='sell', description="Sell an asset.")
async def sell_asset(
    ctx: discord.ApplicationContext,
    symbol: discord.Option(str, "Enter asset symbol"),
    quantity: discord.Option(float, "Enter desired quantity to sell")
    ):
    symbol = symbol.upper()
    query = Query(symbol)

    if(query.quote is None):
        await ctx.respond(f"Could not find {symbol}. Please try again.")
    else:

        if query.exchange == "CRYPTO":
            fee = query.price * quantity * 0.0015
        else:
            fee = 0.00

        fields_list = [
            ["Order Type", "Market Sell"],
            ["Asset Price", f"${query.price:.2f}"],
            ["Quantity", quantity], 
            ["Order Subtotal", f"${(quantity * query.price):.2f}"],
            ["Fees", f"${(fee):.2f}"],
            ["Order Total", f"${(quantity * query.price - fee):.2f}"],
            [chr(173), chr(173)]
        ]

        if query.exchange == "CRYPTO":
            await ctx.respond(embed=embedded_message(
                status='pending',
                author=query.exchange,
                title=symbol,
                desc=query.name,
                fields=fields_list,
                footer_text="Order Status: Pending",
                colour=0xB20D30))
        else:
            await ctx.respond(embed=embedded_message(
                status='pending',
                author=query.exchange,
                thumbnail=query.image,
                title=symbol,
                desc=query.name,
                fields=fields_list,
                footer_text="Order Status: Pending",
                colour=0xB20D30))


# -----------------------------------------------------------------------------------------
# ASSET COMMANDS
# -----------------------------------------------------------------------------------------
display_commands = bot.create_group('display', description="Display ")

# @display_commands.command(name='info', description="Display information about an company.")
# async def info(
#     ctx: discord.ApplicationContext,
#     symbol: discord.Option(str, "Enter asset symbol")
#     ):
#     symbol = symbol.upper()
#     await ctx.respond(f"Wow! This is some info!")

# @display_commands.command(name='plot', description="Display performance plot of an asset.")
# async def plot(
#     ctx: discord.ApplicationContext,
#     symbol: discord.Option(str, "Enter asset symbol")
#     ):
#     symbol = symbol.upper()
#     await ctx.respond(f"Wow! This is a plot!")

@display_commands.command(name='quote', description="Display quote of an asset.")
async def quote(
    ctx: discord.ApplicationContext,
    symbol: discord.Option(str, "Enter asset symbol")
    ):
    symbol = symbol.upper()
    # query = Query(symbol)
    # query.
    # embed = discord.Embed( 
    #     title = "embedded title",
    #     description = "embedded message",  #description is the text that you want to output
    #     colour = 15158332
    #     )
          
    await ctx.respond("in progress")
    #await embeddedDefault(ctx)


# -----------------------------------------------------------------------------------------
# BUTTON TESTING
# -----------------------------------------------------------------------------------------
# make two button classes one more confirm and one for cancelling
# button style success for buying, danger for canceling

# @bot.command(name='confirm', description='Confirm trade with buttons')
# async def confirm(ctx: discord.ApplicationContext):

#     button1 = discord.ui.Button(label="Confirm Trade", style=discord.ButtonStyle.success)
#     button2 = discord.ui.Button(label="Cancel Trade", style=discord.ButtonStyle.danger)

#     view = discord.ui.View()
#     view.add_item(button1)
#     view.add_item(button2)
#     await ctx.respond("here are the buttons", view=view)

bot.run(settings.BOT_TOKEN)
