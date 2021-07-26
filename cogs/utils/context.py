import io

import discord
from discord.ext import commands

class Context(commands.Context):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


	async def send(self, content= None, **kwargs):
		'''Sends a messsage, sends a file if the message is too big'''

		if content and len(content) > 2000:
			file = io.BytesIO(content.encode())
			kwargs.pop(file, None)
			return await super().send(file= discord.File(file, filename= 'chunky_message.txt'), **kwargs)

		return await super().send(content, **kwargs)


	async def send_help(self, command=None):
		'''Shows the help command for the specified command if given.

		If no command is given, then it'll show help for the current
		command.
		'''
		cmd = self.bot.get_command('help')
		command = command or self.command.qualified_name
		await self.invoke(cmd, command=command)

	
	
	