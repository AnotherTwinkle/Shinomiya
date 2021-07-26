from discord.ext import commands
import discord
from .utils import paginator

class Kaguya(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self._get_guyamoe_json())
    
    async def _get_guyamoe_json(self):
        url= 'https://guya.moe/api/series/Kaguya-Wants-To-Be-Confessed-To'
        async with self.bot.session.get(url) as page:
            self.data = await page.json()            
    
    async def get_chapter(self, n: int):
        try:
            return Chapter(n, self.data['chapters'][str(n)])
        except KeyError:
            return None

    @commands.command()
    async def kaguya(self, ctx, ch: float, start: int= 1):

        ch = int(ch) if ch.is_integer() else ch
        # Chapters names can be floats, but always an integer when not
        # If that makes sense.

        chapter= await self.get_chapter(ch)
        if chapter is None:
            return await ctx.send('Chapter not found :(')

        pages = [chapter.page(n) for n in range(1, chapter.page_count+1)]

        if start not in range(1, len(pages)+1):
            return await ctx.send('Specified page out of range :(')

        embeds= []
        for page in pages:
            e= discord.Embed(title=f'Chapter {chapter.index}: {chapter.title}', color= ctx.me.color).set_image(url= page)
            e.add_field(name= 'Page Count', value= str(chapter.page_count), inline= True)
            e.add_field(name= 'Released', value=f'<t:{chapter.release_date}:R>')
            embeds.append(e)

        pag = paginator.PaginatorClassic(ctx, embeds)
        await ctx.send(embed=embeds[start- 1], view= pag)

class Chapter:
    def __init__(self, index, data):
        self.data= data
        self.index= index
        self.volume = data['volume']
        self.title = data['title']
        self.folder = data['folder']
        self.release_date = int(data['release_date']['1'])
        self.page_count= len(data['groups']['1'])
        print(data['groups'])

    def _page(self, num):
        try:
            return self.data['groups']['1'][num-1]
        except IndexError:
            return None

    def page(self, num):
        url= f'https://guya.moe/media/manga/Kaguya-Wants-To-Be-Confessed-To/chapters/{self.folder}/1/'
        page = self._page(num)
        return (url + page) if page else None


def setup(bot):
    bot.add_cog(Kaguya(bot))

