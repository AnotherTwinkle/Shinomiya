import discord
from discord.ext import commands
from discord.utils import oauth_url


class Meta(commands.Cog):
	'''Information and stuff.'''
	
	def __init__(self, bot):
		self.bot= bot
		self.original_help_command = bot.help_command
		bot.help_command = Help()
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self.original_help_command
		return super().cog_unload()
	
	@commands.command(name='ping')
	async def _ping(self, ctx: commands.Context):
		'''Pong!'''
		return await ctx.send(f'Pong. {round(self.bot.latency*1000)} ms.')

	@commands.command(name='guyamoe')
	async def _guyamoe(self, ctx: commands.Context):
		'''Sends you the guya.moe site link'''
		return await ctx.send(f'The reader and the search is powered by https://guya.moe')

	@commands.command(name='invite', aliases=['join'])
	async def _invite(self, ctx: commands.Context):
		'''Sends the bot's invite url'''

		perms= discord.Permissions.none()
		return await ctx.send(oauth_url(self.bot.user.id, permissions= perms)+ '&scope=applications.commands')
		# Because discord will soon force slash commands down our throats

	@commands.command(name='source', aliases=['repo'])
	async def _source(self, ctx: commands.Context):
		'''It\'s open source lol.'''
		return await ctx.send('https://github.com/AnotherTwinkle/Shinomiya')

	@commands.command(name='botinfo', hidden= True)
	async def _info(self, ctx: commands.Context):
		'''Numbers'''
		return await ctx.send(f'{len(self.bot.guilds)} guilds. {sum([guild.member_count for guild in self.bot.guilds])} members.')


class Help(commands.MinimalHelpCommand):
	def get_ending_note(self):
		command_name = self.invoked_with
		return "Use `{0}{1} [command]` for more info on a command.\n" \
			   "You can also use `{0}{1} [category]` for more info on a category.".format(self.context.clean_prefix, command_name)


	def get_opening_note(self):
		return "A Kaguya-sama related bot."

	def common_command_formatting(self, embed_like, command):
		embed_like.title = command.name
		if command.description:
			embed_like.description = f'{command.description}\n\n{command.help}'
		else:
			embed_like.description = command.help or 'No help found...'
			
	async def send_command_help(self, command):
		embed = discord.Embed(colour= self.context.me.color)
		self.common_command_formatting(embed, command)
		await self.context.send(embed=embed)
		
	async def send_pages(self):
		ctx= self.context
		bot= ctx.bot
		destination = self.get_destination()
		for page in self.paginator.pages:
			embed = discord.Embed(title='Help',description= page, color= ctx.me.color, timestamp= discord.utils.utcnow())
			embed.set_thumbnail(url= bot.user.avatar.url)
			embed.set_author(name= bot.user, icon_url= bot.user.avatar.url)
			await destination.send(embed= embed)

	def add_subcommand_formatting(self, command):
		fmt = '`{0}{1}` \N{EN DASH} {2}\n' if command.short_doc else '`{0}{1}`'
		self.paginator.add_line(fmt.format(self.context.clean_prefix, command.qualified_name, command.short_doc))

	def get_command_signature(self, command):
		return '**%s%s %s**' % (self.context.clean_prefix, command.qualified_name, command.signature)

	def add_bot_commands_formatting(self, commands, heading):
		if commands:
			# U+2002 Middle Dot
			joined = '\u2002'.join(f'**`{c.name}`**' for c in commands)
			self.paginator.add_line('• **%s**' % heading)
			self.paginator.add_line(f'\N{EN DASH} {joined}\n')


def setup(bot):
	bot.add_cog(Meta(bot))