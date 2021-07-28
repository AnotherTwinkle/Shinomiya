from typing import Optional

import discord
from discord.ext import commands
from jishaku.codeblocks import codeblock_converter


class Admin(commands.Cog):
	'''Admin control suite'''

	def __init__(self, bot):
		self.bot = bot

	@commands.is_owner()
	@commands.command(name='eval', aliases= ['run', 'rtfc'])
	async def _eval(self, ctx, *, code: codeblock_converter):
		'''Eval a piece of code'''
		jsk = self.bot.get_command("jishaku py")
		await jsk(ctx, argument=code)


	@commands.is_owner()
	@commands.command(name='sudo')
	async def _sudo(self, ctx, *, command : str):
		'''Run a command bypassing all checks'''
		sudo = self.bot.get_command("jishaku sudo")
		await sudo(ctx,command_string = command)	


	@commands.is_owner()
	@commands.command(name='su', aliases= ['runas'])
	async def _su(self, ctx, target: discord.User, *, command : str):
		'''Run a command as someone else'''
		su = self.bot.get_command("jishaku su")
		await su(ctx, target, command_string = command)


	@commands.is_owner()
	@commands.command(name='in', aliases= ['runin'] )
	async def _in(self, ctx, target: discord.TextChannel, *, command : str):
		'''Run a command for a different channel.'''

		runin = self.bot.get_command("jishaku in")
		await runin(ctx, target, command_string = command)


	@commands.is_owner()
	@commands.command(name='debug')
	async def _debug(self, ctx, *, command : str):
		'''Run a command with debug info'''
		debug = self.bot.get_command("jishaku debug")
		await debug(ctx,command_string = command)

	
	@commands.is_owner()
	@commands.command(name='echo')
	async def _echo(self, ctx, channel: Optional[discord.TextChannel], *, text):
		channel = channel or ctx.channel
		
		exceptions = (discord.HTTPException, commands.MissingPermissions)

		try:
			await channel.send(text)
		except exceptions:
			pass

		try:
			await ctx.message.delete()
		except exceptions:
			pass


def setup(bot):
	bot.add_cog(Admin(bot))
