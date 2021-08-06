import discord
from discord.ext import commands
from .utils import utils

class Logging(commands.Cog):
	'''A cog to log the bot's command usage and other stuff using a webhook.'''

	def __init__(self, bot):
		self.bot= bot
		self.webhook= bot.webhook

	@commands.Cog.listener()
	async def on_command_completion(self, ctx):
		author= ctx.author
		guild= ctx.guild
		channel= ctx.channel
		command= ctx.command
		content= ctx.message.content

		message= f'{author}(`{author.id}`) used `{command.name}`\n> {content}\n'
		message+= f'- in `#{channel.name}`(`{channel.id}`) on {guild.name}(`{guild.id}`)\n\n'

		await self.webhook.send(message)

	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if hasattr(ctx.command, 'on_error'):
			return

		ignored = (commands.CommandNotFound)
		if isinstance(error, ignored):
			return

		author= ctx.author
		guild= ctx.guild
		channel= ctx.channel
		command= ctx.command
		content= ctx.message.content
	
		message= f'[**ERROR**]{author}(`{author.id}`) used `{command.name}`\n>{content}\n'
		message+= f'- in `#{channel.name}`(`{channel.id}`) on {guild.name}(`{guild.id}`)\n\n'
		await self.webhook.send(message)
		await utils.send_traceback(self.webhook, 0, type(error), error, error.__traceback__)

	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		message= f'[**JOIN**] Joined {guild.name}(`{guild.id}`) with {guild.member_count} members.'
		await self.webhook.send(message)

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		message= f'[**LEAVE**] Removed from {guild.name}(`{guild.id}`) with {guild.member_count} members.'
		await self.webhook.send(message)

def setup(bot):
	bot.add_cog(Logging(bot))