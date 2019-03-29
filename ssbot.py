import discord
from discord.ext import commands
import asyncio
import time
import datetime
import json
import json,urllib.request
import aiohttp
import io

TOKEN = 'NTYwNTY1MjgyNzc1NzYwOTA2.D31yuA.rDyIhClS0pldqk_TmsF_5tAjdZU'

client = commands.Bot(command_prefix = '>')
client.authorizedusers = ["147999751441219584"]
#                          1479 = snowbleed      
client.remove_command("help")
extensions = ['CommandErrorHandler']
             
@client.event
async def on_ready():
    print("Bot is online")
    await client.send_message(client.get_channel('560964915330940940'), f"Bot has been restarted on: `{datetime.datetime.utcnow().strftime('%d %B, %H:%M')} UTC`")

@client.event
async def on_message(message):
	if "prefix" in message.content.lower():
		thebot = await client.get_user_info('560565282775760906')
		if thebot.mentioned_in(message):
			await client.say("The prefix for this bot is `>`")
	await client.process_commands(message)

@client.command(pass_context=True)
async def u(ctx):
    if ctx.message.author.id == '147999751441219584':
        await client.create_role(ctx.message.server, name="DJ")
        role = discord.utils.get(ctx.message.server.roles, name='DJ')
        await client.add_roles(ctx.message.author, role)
    
@client.command()
async def cmds():
    embed = discord.Embed(
    title = 'Made by `snowbleed#7824`',
    description = '**List of commands:**',
    timestamp = datetime.datetime.utcnow(),
    colour = discord.Colour.blue()
    )
    embed.set_footer(text='usms bot')
    embed.add_field(name=";cmds", value="Display a list of commands.", inline = False)
    embed.add_field(name=";ping", value="Check if the bot is responding quickly and correctly.", inline = False)
    embed.add_field(name=";request", value="Request protection if you are a protectee. Format: `;request <place> <message>` where <place> is either lv, dc, ch or jag, e.g.: ;request LV Big House 1", inline = False)
    embed.add_field(name=";protectee", value="See if a person is a protectee and if so why. Format: `;protectee <name>` where <name> is their ROBLOX username", inline = False)
    await client.say(embed=embed)
    

@client.command(pass_context=True)
async def request(ctx, arg1, *, args):
	with open("text.json", "r") as read_file:
		usernames = json.load(read_file)
	memberid = ctx.message.author.id
	if arg1.lower() == 'lv':
		city='Las Vegas *https://www.roblox.com/games/163865146/LV*'
	elif arg1.lower() == 'dc':
		city='Washington D.C. *https://www.roblox.com/games/1213026131/DC*'
	else:
		await client.say("Place needs to be either `LV` or `DC`")
		return
	if args == '':
		args = 'N/A'
	server = client.get_server('441385793492221962')
	role = discord.utils.get(server.roles, name='Secret Service')
	for username, metadata in usernames.items():
		if memberid == metadata['userid']:
			data = urllib.request.urlopen(f"https://api.roblox.com/users/get-by-username?username={username}").read()
			robloxapi = json.loads(data)
			profile = robloxapi["Id"]
			honorem = metadata['honorem']
			await client.send_message(client.get_channel('549763840330563606'),f"**PROTECTION ANNOUNCEMENT:**\n{honorem} {username} requests protection at: {city}\nProfile: https://www.roblox.com/users/{profile}/profile\n\nMessage from protectee: {args}\n\n{role.mention}")
			break
	else:
		await client.say("You are not a protectee.")

@client.command(pass_context=True)
async def list(ctx):
    output = '__**List of protectees:**__\n\n'
    highpriority = ''
    mediumpriority = ''
    lowpriority = ''
    with open("text.json", "r") as read_file:
        usernames = json.load(read_file)
    for x in usernames:
        if usernames[x]['priority'].lower() == 'high':
            highpriority += f"{x}, {usernames[x]['honorem']}\n"
        elif usernames[x]['priority'].lower() == 'medium':
            mediumpriority += f"{x}, {usernames[x]['honorem']}\n"
        elif usernames[x]['priority'].lower() == 'low':
            lowpriority += f"{x}, {usernames[x]['honorem']}\n"
    output += f"`High Priority:`\n{highpriority}\n`Medium Priority:`\n{mediumpriority}\n`Low Priority:`\n{lowpriority}"
    
    try:
        await client.say(output)
    except:
        await client.say("List too long.")

@client.command(pass_context=True)
async def protectee(ctx, name):
	with open("text.json", "r") as read_file:
		usernames = json.load(read_file)
	memberid = ctx.message.author.id
	for x in usernames:
		if x.lower() == name.lower():
			honorem = usernames[x]['honorem']
			await client.say(f"{name.capitalize()} is a protectee, honorem: **{honorem}**.")
			break
	else:
		await client.say(f"{name.capitalize()} is not a protectee.")
	
@client.command(pass_context=True)
async def justtest(ctx):
	async with aiohttp.ClientSession() as client_session:
		async with client_session.get("https://i.imgur.com/j2P5uXE.jpg") as response:
			my_file_like_object = io.BytesIO(await response.read())

	await client.send_file(destination=ctx.message.channel, fp=my_file_like_object, filename="stopreadingthis.png")
    
@client.command()
async def ping():
    await client.say('Pong!')        
	
@client.command(pass_context=True)
async def logout(ctx):
    if ctx.message.author.id == "147999751441219584":
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
    await client.say(embed=embed)"""

if __name__ == '__main__':
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as error:
			print(f'{extension} cannot be loaded. [{error}]')
	client.run(TOKEN)
