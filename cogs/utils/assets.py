from . import utils

class File:
    '''
    A special object for our assets.
    This takes a attachment url string, and it's possible to get a discord.File() out of this.

    For example-

    `await channel.send(content= assets.kawai_koto)`

    This wil send the attachment url to get target channel, which discord hides if there's no other content present in
    the message.

    Aternatively-

    `await channel.send(file= (await assets.kawai_koto.file()))`

    .file() returns a discord.File() object, therefore this method can be used to upload attachments directly.
    '''
    def __init__(self, url: str):
        self.url= url

    def __str__(self):
        return self.url

    async def file(self):
        return await utils.file_from_url(self.url)
        


kawai_koto= File('https://i.ytimg.com/vi/9-TA73BBJlM/maxresdefault.jpg')
kaguya_murder_stare= File('https://cdn.discordapp.com/attachments/868114073517187122/868401876394197012/unknown.png')
kaguya_cattle_stare= File('https://cdn.discordapp.com/attachments/868114073517187122/868402259204145162/IMG_20210723_155302.png')
