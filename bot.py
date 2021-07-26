import discord
from discord.ext import commands
import config
import asyncpg
import aiohttp
import time
from cogs import db
from cogs.utils import assets, context

class Shinomiya(commands.Bot):

	def __init__(self, *options):
		intents = discord.Intents.all()
		super().__init__(intents= intents, command_prefix= self.determine_prefix, *options)

		boot_extensions = ['jishaku','cogs.kaguya']
		for ext in boot_extensions:
			self.load_extension(ext)

		if hasattr(config, 'owner_ids'):
			self.owner_ids = set(config.owner_ids)


	def determine_prefix(self, bot, message):
		prefixes = (
			's!',
			'k!',
			'.',
		)
		#We will add a customizable prefix later, these are the mere defaults.

		return commands.when_mentioned_or(*prefixes)(bot, message)

	async def get_context(self, message, *, cls= None):
		return await super().get_context(message, cls= cls or context.Context)
	

	async def start(self, *args, **kwargs):
		self.session = aiohttp.ClientSession(loop= self.loop)
		self.pool = await asyncpg.create_pool(config.postgresql, min_size= 5, max_size= 5)
		await db.initialize_db(self.pool)
		await super().start(*args, **kwargs)


	async def close(self, *args, **kwargs):
		await self.session.close()
		await self.pool.close()		
		print(f'[{round(time.time())}]: Shuting down...')
		await super().close(*args, **kwargs)


	async def on_ready(self):
		print(f'{self.user}: Ready. ({self.user.id})')
		print(f'{len(self.users)} users.')

		if not hasattr(self, 'uptime'):
			# on_ready can be fired multiple times in a single instance.
			# We only need the first call to determine uptime.

			self.uptime = time.time()


	async def on_command_error(self, ctx, error):
		if hasattr(ctx.command,'on_error'):
			return

		error = getattr(error, 'original', error)
		ignored = (commands.CommandNotFound)

		if isinstance(error, ignored):
			pass
		
		elif isinstance(error, commands.NotOwner):
			await ctx.reply(content='My my, trying to use owner commands are we?', 
							file=(await assets.kawai_koto.file()))


		elif isinstance(error, commands.MissingPermissions):
			await ctx.reply(content='Disgrace to humanity, Cattle in human form. Trying to use a command without enough permissions.',
							file=(await assets.kaguya_cattle_stare.file()))

		else:
			 raise error


if __name__ == '__main__':
	bot = Shinomiya()
	bot.run(config.token)

