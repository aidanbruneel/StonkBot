import discord
import datetime


AUTHOR_ICON: str = 'https://cdn-icons-png.flaticon.com/512/7204/7204762.png' # 'https://pbs.twimg.com/profile_images/1403830481414541312/s8Bbr2cE_400x400.jpg'
PENDING_ICON: str = 'https://cdn-icons-png.flaticon.com/512/6877/6877368.png'
FILLED_ICON: str = 'https://cdn-icons-png.flaticon.com/512/6877/6877354.png'
INFO_ICON: str = 'https://cdn-icons-png.flaticon.com/512/6829/6829454.png'
CANCELLED_ICON = 'https://cdn-icons-png.flaticon.com/512/7042/7042911.png'
# Icon author (needs to be credited): https://www.flaticon.com/authors/radhe-icon


def embedded_message(
    status: str = 'info',
    author: str = None,
    author_icon: str = AUTHOR_ICON,
    thumbnail: str = None,
    title: str = None,
    desc: str = None,
    fields = [[]],
	image: str = None,
    footer_icon: str = PENDING_ICON,
    footer_text: str = 'Status', # this default doesn't really actually make any sense
    timestamp: datetime = datetime.datetime.now(),
    colour = 0x11BB11):
    
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
            footer_icon = INFO_ICON
        case 'pending':
            footer_icon = PENDING_ICON
        case 'filled':
            footer_icon = FILLED_ICON
        case 'cancelled':
            footer_icon = CANCELLED_ICON
            
    embed.set_footer(text=footer_text, icon_url=footer_icon)

    return embed	
