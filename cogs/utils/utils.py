from io import BytesIO
import time
import aiohttp

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
	

def discord_timestamp(target: int= time.time(), style : str = 'f'):
	valid = ['t','T','d','D','f','F','R']
	#https://github.com/discord/discord-api-docs/blob/ff4d9d8ea6493405a8823492338880c47fb02996/docs/Reference.md#timestamp-styles
	if style not in valid:
		raise commands.BadArgument('Invalid timestamp style')

	return f'<t:{target}:{style}>'
	

