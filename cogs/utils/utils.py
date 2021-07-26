from io import BytesIO
import time
import aiohttp
import traceback

from discord.ext import commands
import discord


async def file_from_url(url: str, filename: str = 'file.png', session : aiohttp.ClientSession = None):
	asession = session if session else aiohttp.ClientSession() #Create a new session if not provided

	async with asession.get(url) as resp:
		data = await resp.content.read()

	file = discord.File(fp= BytesIO(data), filename= filename)
	if not session: # Sesssion was not provided, so we will close our created session
		await asession.close()

	return file
	

def get_timedelta(humandelta):
	multipliers = {'s' : 1, 'm' : 60, 'h' : 60*60, 'd' : 60*60*24, 'w' : 3600*24*7,
			'm' : 3600*24*30, 'y' : 3600*24*365} 
	
	value, multiplier =  humandelta[:-1], humandelta[-1]
	return value * multipliers[multiplier]
	

def discord_timestamp(target: int= time.time(), style : str = 'f'):
	valid = ['t','T','d','D','f','F','R']
	#https://github.com/discord/discord-api-docs/blob/ff4d9d8ea6493405a8823492338880c47fb02996/docs/Reference.md#timestamp-styles
	if style not in valid:
		raise commands.BadArgument('Invalid timestamp style')

	return f'<t:{target}:{style}>'
	

async def send_traceback(destination: discord.abc.Messageable, verbosity: int, *exc_info):
	etype, value, trace = exc_info
	traceback_content = "".join(traceback.format_exception(etype, value, trace, verbosity)).replace("``", "`\u200b`")

	paginator = commands.Paginator(prefix='py')
	for line in traceback_content.split('\n'):
		paginator.add_line(line)

	message = None

	for page in paginator.pages:
		message = await destination.send(f'```{page}')

	return message