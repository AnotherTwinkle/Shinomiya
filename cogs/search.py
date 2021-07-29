import discord
from discord.ext import commands
from typing import List

from .utils.paginator import Paginator

class Search(commands.Cog):
	def __init__(self, bot : commands.AutoShardedBot):
		self.bot = bot
	
	async def search_in_manga(self, text : str) -> dict:
		page = 'https://guya.moe/api/search_index/Kaguya-Wants-To-Be-Confessed-To/'
		data = {'searchQuery' : text}
		async with self.bot.session.post(page, data= data) as resp:
			return await resp.json()

	def format_to_link(self, chapter: str, page : int) -> str:
		return f'https://guya.moe/{chapter}/{page}'
	
	def format_to_line(self, chapter : str, pages : List[int] ) -> str:
		string = f'`Ch {chapter}` | Pages: '
		string+= ', '.join([f'[{page}](https://guya.moe/{chapter}/{page})' for page in pages])
		return string

	def prepare_for_paginator(self, lines: List[str]) -> List[list]:
		groups= [[]]
		i = 0
		for line in lines:
			if len(''.join(groups[i])) < 1000:
				groups[i].append(line)
				continue

			groups.append([])
			i += 1
			groups[i].append(line)

		return groups


	@commands.command(name='search')
	async def _search(self, ctx: commands.Context, *, text: str):
		result = (await self.search_in_manga(text))[text]
		if not result:
			return await ctx.send('Nothing found :(')
		
		data = result[list(result.keys())[0]] # We'll only consider the first result.

		chapters = [int(x) if x.is_integer() else x for x in sorted([float(i.replace('-','.')) for i in data])]
		formatted_chapters = [str(c).replace('.','-') for c in chapters]
		lines= [self.format_to_line(chapters[c], data[formatted_chapters[c]]) for c in range(len(formatted_chapters))]
		groups = self.prepare_for_paginator(lines)

		embeds = []
		print(len(groups))
		for group in groups:
			desc = '\n'.join([line for line in group])
			embed = discord.Embed(title= f'Search results for "{text}" in Kaguya-sama main series',
									description= desc,
									color= ctx.guild.me.color)

			embeds.append(embed)

		if len(embeds) == 1:
			# No need for paginator
			return await ctx.send(embed= embeds[0])

		paginator = Paginator(ctx, embeds,)
		return await ctx.send(embed=embeds[0], view= paginator)


def setup(bot):
	bot.add_cog(Search(bot))


