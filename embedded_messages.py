import discord
import datetime
import config
from fmp_api import Query
from player import Player


#-------------------------------------------------------------------------------------
# EMBEDED MESSAGE CREATOR
#-------------------------------------------------------------------------------------
def embedded_message(
    status: str = 'info',
    author: str = None,
    author_icon: str = config.AUTHOR_ICON,
    thumbnail: str = None,
    title: str = None,
    desc: str = None,
    fields = None,
	image: str = None,
    footer_icon: str = config.PENDING_ICON,
    footer_text: str = 'Status', # this default doesn't really actually make any sense
    timestamp: datetime = datetime.datetime.now(),
    colour = 0x11BB11):

    if len(desc) > 3000:
        desc = desc[:3000]
    
    embed = discord.Embed(
        title = title,
        description = desc,
        colour = colour,
        timestamp = timestamp
        )

    if author:
        embed.set_author(name=author, icon_url=author_icon)

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
	
    if fields:
        embed.add_field(name=fields[0][0], value=fields[0][1], inline=False)

        for i in range(1, len(fields)):
            embed.add_field(name=fields[i][0], value=fields[i][1], inline=True)

    if image:
        embed.set_image(url=image)
    
    
    # footer_icon
    match status:
        case 'info':
            footer_icon = config.INFO_ICON
        case 'pending':
            footer_icon = config.PENDING_ICON
        case 'filled':
            footer_icon = config.FILLED_ICON
        case 'cancelled':
            footer_icon = config.CANCELLED_ICON
            
    embed.set_footer(text=footer_text, icon_url=footer_icon)

    return embed


#-------------------------------------------------------------------------------------
# BUTTON CLASS
#-------------------------------------------------------------------------------------
class ConfirmButtons(discord.ui.View):
    def __init__(self, symbol, quantity, buying, ctx, player: Player):
        super().__init__()
        
        self.symbol = symbol
        self.quantity = quantity
        self.query = Query(self.symbol)
        self.quantity = quantity
        self.player = player
        self.buying = buying
        self.ctx = ctx


        self.button1 = discord.ui.Button(label="Confirm Trade", style=discord.ButtonStyle.success, emoji='✔')
        self.button2 = discord.ui.Button(label="Cancel Trade", style=discord.ButtonStyle.danger, emoji='✖')

        self.button1.callback = self.button1_callback
        self.button2.callback = self.button2_callback

        self.add_item(self.button1)
        self.add_item(self.button2)


    ## CONFIRM BUTTON
    async def button1_callback(self, interaction):

        if interaction.user == self.ctx.author:

            if self.buying == True:
                valid_transaction = self.player.buy_asset(self.query, self.quantity) # add in the fee logic
            else:
                valid_transaction = self.player.sell_asset(self.query, self.quantity) # add in teh fee logic after


            if valid_transaction == True:
                await self.on_click(interaction, True)
            else:
                await interaction.response.edit_message(embed=discord.Embed(
                    title="Couldn't Process Transaction",
                    description=valid_transaction,
                    colour=0xB20D30
                ), view=None)

    
    ## CANCEL BUTTON
    async def button2_callback(self, interaction):

        if interaction.user == self.ctx.author:
            await self.on_click(interaction, False)
        

    async def on_click(self, interaction, confirmed):

        match confirmed:
            case True:
                theme_color = 0x11BB11
                foot_text = "Order Status: Filled"
            case False:
                theme_color = 0xB20D30
                foot_text = "Order Status: Cancelled"


        match self.query.exchange:
            case "CRYPTO":
                fee = self.query.price * self.quantity * 0.0015  
                thumbnail_url = config.CRYPTO_ICON
            case _:
                fee = 0.00
                thumbnail_url = self.query.image

        fields_list = [
            ["Order Type", "Market Buy"],
            ["Asset Price", f"${self.query.price:.2f}"],
            ["Quantity", self.quantity], 
            ["Order Subtotal", f"${(self.quantity * self.query.price):.2f}"],
            ["Fees", f"${(fee):.2f}"],
            ["Order Total", f"${(self.quantity * self.query.price + fee):.2f}"],
            [chr(173), chr(173)] # change this to balance remaining
        ]
        
        await interaction.response.edit_message(embed=embedded_message(
            status='cancelled',
            author=self.query.exchange,
            title=self.symbol,
            thumbnail=thumbnail_url,
            fields=fields_list,
            desc=self.query.name,
            footer_text=foot_text,
            colour=theme_color
        ), view=None)