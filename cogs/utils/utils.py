from io import BytesIO

import discord
import aiohttp


async def file_from_url(url: str, filename: str = 'file.png', session : aiohttp.ClientSession = None):

    asession = session if session else aiohttp.ClientSession() #Create a new session if not provided

    async with asession.get(url) as resp:
        data = await resp.content.read()

    file = discord.File(fp= BytesIO(data), filename= filename)

    if not session: # Sesssion was not provided, so we will close our created session
        await asession.close()

    return file
    

def discord_timestamp
