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
kaguya_bloody_stare= File('https://cdn.discordapp.com/attachments/742276773118607434/868430666646319124/8b6deb67ad70f8c8de4ec9a9a40d9008.jpg')
kaguya_angry_snort= File('https://cdn.discordapp.com/attachments/742276773118607434/868431197083168788/b8a991808f78898c72dcc9eb17745da8.jpg')
kaguya_angry_snort_2= File('https://cdn.discordapp.com/attachments/742276773118607434/868429702212255834/92b1d613cbae5df48e81af896d0cc608.jpg')
kaguya_sick_stare= File('https://cdn.discordapp.com/attachments/742276773118607434/868430996423442482/eb4999d2fc57b381cf0556cc81769623.jpg')
kaguya_thinking_hard= File('https://cdn.discordapp.com/attachments/742276773118607434/868429700874260480/91421a8ed2a0ea6ef807b15c30426e2f.jpg')
kaguya_cute_ashamed= File('https://cdn.discordapp.com/attachments/742276773118607434/868429701088165898/122bf333f8a54541a71b3d01248b805c.jpg')
kaguay_huh= File('https://cdn.discordapp.com/attachments/742276773118607434/868429701394366514/8591adf443070c57dd94f61167ae1a04.jpg')
kaguya_menace= File('https://cdn.discordapp.com/attachments/742276773118607434/868429701666971658/34e36f08274aa8fda2f3dc9d6f4f8013.jpg')
kaguya_bored= File('https://cdn.discordapp.com/attachments/742276773118607434/868429701897670666/b56be64d9c97748f00ac91fdf3037ac0.jpg')
kaguya_pencil_stare= File('https://cdn.discordapp.com/attachments/742276773118607434/868432195738533898/55022b9f7b9cf4ba7ac14c11a52030c8.jpg')
bakaguya_stare= File('https://cdn.discordapp.com/attachments/742276773118607434/868429701897670666/b56be64d9c97748f00ac91fdf3037ac0.jpg')
bakaguya_scream= File('https://cdn.discordapp.com/attachments/742276773118607434/868424456685621289/8bdb534cdff6dec58fb6fd0923fb07e6.jpg')
