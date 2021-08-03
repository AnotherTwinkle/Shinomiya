import discord
from discord.ext import commands
from typing import List

from .utils.paginator import Paginator


class Search(commands.Cog):
	'''Search the manga.'''

	def __init__(self, bot : commands.AutoShardedBot):
		self.bot = bot
	
	async def search_in_manga(self, text : str) -> dict:
		page = 'https://guya.moe/api/search_index/Kaguya-Wants-To-Be-Confessed-To/'
		data = {'searchQuery' : text}
		async with self.bot.session.post(page, data= data) as resp:
			return await resp.json()

	def pick_common_entries(self, data : dict) -> dict:
		dicts= [list(val.values())[0] for val in data.values()]	
		keys = set.intersection(*tuple(set(d.keys()) for d in dicts))

		results = {}
		for key in keys:
			l = []
			for d in dicts:
				l.append(d[key])

			c = self.onlycommon(l)
			if c is not None:
				results[key] = c

		return results

	def onlycommon(self, lists: list) -> list:
		if len(lists) == 1:
			return lists[0]
		s = list(set(lists[0]).intersection(*lists))
		
		if s:
			return s
		return None


	def format_to_link(self, chapter: str, page : int) -> str:
		return f'https://guya.moe/{chapter}/{page}'
	
	def format_to_line(self, chapter : str, pages : List[int] ) -> str:
		string = f'`Ch. {chapter.replace("-" , ".")}` | Pages: '
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

	@commands.command(name='search', aliases= ['searchtext'])
	async def _search(self, ctx: commands.Context, *, text: str):
		'''
		Search the whole manga for a certain piece of text!
		This is just `guya.moe`'s search api, implemented and formatted for discord.

		Please note that this search is extremely inaccurate in certain cases.
		The api actually provides invidiual search results for each word if your query is multi-worded.  The final results are provided by me crossmatching those results in a number of ways.
		Due to this and how the api provides the results, there's no way to tell if your query (if multi-worded) is literally in the page or the words of the query are in different parts of the page text. 
		For example, searching "hey there" will assume that "hey, go there" is a valid result.
		Along with that, there might be some bugs with my crossmatching, producing invalid results.


		**Examples:**
		`search shinomiya`
		`search never gonna give you up`
		'''

		await ctx.trigger_typing() # Tends to take some time.
		result = (await self.search_in_manga(text))

		if not result:
			return await ctx.send('Nothing found :(')
		
		try:
			if len(text.split()) > 1:
				data= self.pick_common_entries(result)
			else:
				data= list(result[text].values())[0] # We'll only consider the first result.
		except IndexError:
			return await ctx.send('Ran into an error, sorry.')

		if not data:
			return await ctx.send('Nothing found :(')

		chapters = [int(x) if x.is_integer() else x 
					for x in sorted([float(i.replace('-','.')) 
					for i in data])]

		formatted_chapters = [str(c).replace('.','-') for c in chapters]

		lines= [self.format_to_line(formatted_chapters[c], data[formatted_chapters[c]])
				for c in range(len(formatted_chapters))]

		groups = self.prepare_for_paginator(lines)

		embeds = []
		for group in groups:
			desc = '\n'.join([line for line in group])
			embed = discord.Embed(title= f'Search results for "{text}" in Kaguya-sama main series',
									description= desc,
									color= ctx.me.color)

			embeds.append(embed)

		if len(embeds) == 1:
			# No need for paginator
			return await ctx.send(embed= embeds[0])

		paginator = Paginator(ctx, embeds)
		return await ctx.send(embed=embeds[0], view= paginator)


def setup(bot):
	bot.add_cog(Search(bot))


