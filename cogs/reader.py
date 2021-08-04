import random
import asyncio
from datetime import datetime
from typing import List

import discord
from discord.ext import commands

class Chapter:
	def __init__(self, index, data):
		self.data= data
		self.index = index
		self.volume = data['volume']
		self.title = data['title']
		self.folder = data['folder']

		_release_date = data['release_date']
		self.release_date = int(list(_release_date.values())[0])

		self._groups = data['groups']
		self.page_count = len(list(self._groups.values())[0])

		self.pages = [self.page(n) for n in range(1, self.page_count+1)]

	def __repr__(self):
		return f'<Chapter {self.index} title= "{self.title}" page_count= {self.page_count}>'

	def _page(self, num):
		try:
			return list(self._groups.values())[0][num-1]
		except IndexError:
			return None

	def page(self, num):
		url= f'https://guya.moe/media/manga/Kaguya-Wants-To-Be-Confessed-To/chapters/{self.folder}/{list(self._groups.keys())[0]}/'
		page = self._page(num)
		return (url + page) if page else None


# Courtesy of Daggy#1234 : https://github.com/Daggy1234/dagbot/blob/master/dagbot/utils/conventionalpag.py
class PaginatorSelect(discord.ui.Select['KaguyaPaginator']):
	def __init__(self, options: List[discord.SelectOption]) -> None:
		super().__init__(placeholder="Jump to Page..", min_values=1, max_values=1, options=options, row=1)

	async def callback(self, interaction: discord.Interaction):
		assert self.view is not None
		await self.view.process_callback(self, interaction)


class KaguyaPaginator(discord.ui.View):

	children: List[discord.ui.Button]

	def __init__(self, ctx: commands.Context,embeds: List[discord.Embed], chapter: Chapter, init_pos: int= 0):
		super().__init__(timeout=300.0)
		self.ctx = ctx
		self.chapter = chapter
		self.embeds: List[discord.Embed] = embeds
		self.embed_pos = init_pos
		self.max = len(embeds)

		for i, embed in enumerate(self.embeds):
			embed.set_footer(text=f"{i + 1}/{self.max}")
			embed.timestamp = discord.utils.utcnow()

		select_options = [discord.SelectOption(label=f"{i+1}", value=str(i)) for i in range(self.max)]
		if self.max < 25:
			self.add_item(PaginatorSelect(select_options))
		# Well due to this we can't have more than 25 pages, so fuck selects.

		
	async def on_timeout(self) -> None:
		return await super().on_timeout()

	async def interaction_check(self, interaction: discord.Interaction) -> bool:
		assert interaction.user is not None
		return interaction.user.id == self.ctx.author.id

	@discord.ui.button(emoji="\U000023ee", style=discord.ButtonStyle.primary)
	async def forward_start(self, button: discord.ui.Button, interaction: discord.Interaction):

		if self.embed_pos != 0:
			self.embed_pos = 0
			return await interaction.response.edit_message(embed=self.embeds[0])


		command= self.ctx.bot.get_command("manga")
		chapters: List[Chapter] =  self.ctx.bot.get_cog('Reader').chapters
		previous_chapter= chapters[chapters.index(self.chapter)-1].index
	
		if previous_chapter == 1:
			return interaction.response.send_message(content="That's the first chapter lol")

		await interaction.response.edit_message(content= 'Reinvoking the command...')
		await asyncio.sleep(2)
		await interaction.message.delete()

		return await command(self.ctx, previous_chapter)
		
		
	@discord.ui.button(emoji="\U000023ea", style=discord.ButtonStyle.primary)
	async def backward_next(self, button: discord.ui.Button, interaction: discord.Interaction):
		if self.embed_pos - 1 < 0:
			return await interaction.response.send_message("uh- that's the first page.", ephemeral=True)
		self.embed_pos -= 1
		await interaction.response.edit_message(embed=self.embeds[self.embed_pos])


	@discord.ui.button(emoji="\U000023f9", style=discord.ButtonStyle.primary)
	async def stop_button(self, button: discord.ui.Button, interaction: discord.Interaction):
		for button in self.children:
			button.disabled = True
		await interaction.message.delete()
		self.stop()

	@discord.ui.button(emoji="\U000023e9", style=discord.ButtonStyle.primary)
	async def forward_next(self, button: discord.ui.Button, interaction: discord.Interaction):
		if self.embed_pos + 1 >= self.max:
			return await interaction.response.send_message("That's actually the last page lol.", ephemeral=True)
		self.embed_pos += 1
		await interaction.response.edit_message(embed=self.embeds[self.embed_pos])

	@discord.ui.button(emoji="\U000023ed", style=discord.ButtonStyle.primary)
	async def backward_end(self, button: discord.ui.Button, interaction: discord.Interaction):

		if self.embed_pos != self.max - 1:
			self.embed_pos = self.max - 1
			return await interaction.response.edit_message(embed=self.embeds[self.embed_pos])

		command= self.ctx.bot.get_command("manga")
		chapters: List[Chapter] =  self.ctx.bot.get_cog('Reader').chapters

		try:
			next_chapter= chapters[chapters.index(self.chapter)+1].index
		except IndexError:
			return await interaction.response.send_message(content= 'Last chapter lol', ephemeral= True)	

		await interaction.response.edit_message(content= 'Reinvoking the command...')
		await asyncio.sleep(2)
		await interaction.message.delete()

		return await command(self.ctx, next_chapter)

	async def process_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
		assert interaction.data is not None
		opt: int = int(interaction.data["values"][0])
		await interaction.response.edit_message(embed=self.embeds[opt])



class Reader(commands.Cog):
	'''A set of commands related to reading the kaguya-sama manga.'''

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.bot.loop.create_task(self.cache_chapters())

	async def cache_chapters(self):
		url= 'https://guya.moe/api/series/Kaguya-Wants-To-Be-Confessed-To'
		async with self.bot.session.get(url) as page:
			self.data = await page.json()

		chdata = self.data['chapters']
		self.chapters : List[Chapter]=  []
		for n in chdata.keys():
			self.chapters.append(Chapter(float(n), chdata[str(n)]))


	async def get_chapter(self, n: float):
		chapter = [chapter for chapter in self.chapters if chapter.index == n]
		return chapter[0] if chapter else None

	@commands.command(name= 'read', aliases= ['manga', 'chapter'], brief= 'Read a kaguya-sama chapter')
	async def _readmanga(self, ctx: commands.Context, ch: float= 1.0, start: int= 1):
		'''
		Allows you to read the entire Kaguya-sama manga series on discord. Extra chapters are supported too!
		This sends a paginator that can be used to move throught pages and chapters and a dropdown is provided to jump to pages easily.

		**Usage:**
		`read <chapter> [page]`
		Note that `page` is optional.

		**Examples:**
		`read 4`
		`read 101.5`
		`read 5 4` (Starts from page 4)
		'''

		ch = int(ch) if ch.is_integer() else ch
		# Chapters indexes can be floats.

		chapter= await self.get_chapter(ch)
		if chapter is None:
			return await ctx.send('Chapter not found :(')

		if start not in range(1, len(chapter.pages)+1):
			return await ctx.send('Specified page out of range :(')

		embeds= []
		for page in chapter.pages:
			e= discord.Embed(title=f'{chapter.title}', color= ctx.me.color).set_image(url= page)
			e.add_field(name= 'Chapter', value= str(ch), inline= True)
			e.add_field(name= 'Page Count', value= str(chapter.page_count), inline= True)
			e.add_field(name= 'Released', value=f'<t:{chapter.release_date}:R>')
			embeds.append(e)

		paginator = KaguyaPaginator(ctx, embeds, chapter, start-1)
		return await ctx.send(content= f'{ctx.author.mention} Press the \U000023ee and \U000023ed buttons twice to go to the previous/next chapter!',
							embed=embeds[start- 1], view= paginator)
	
	
	@commands.command(name= 'randomchapter', aliases= ['randommanga', 'randomanga', 'randmanga'], brief= 'Read a random chapter')
	async def _read_random_manga(self, ctx: commands.Context):
		f'''
		Read a random kaguya-sama chapter.
		'''

		chapter= float(random.choice(self.chapters).index)
		return await self._readmanga(ctx, chapter)


	@commands.command(name= 'randompage', brief= 'Read from a random page.')
	async def _read_random_page(self, ctx: commands.Context):
		'''
		Read from a random page of a random kaguya-sama chapter.
		'''

		chapter= random.choice(self.chapters)
		page = random.choice(range(1, chapter.page_count + 1))
		return await self._readmanga(ctx, float(chapter.index), page)


def setup(bot):
	bot.add_cog(Reader(bot))

