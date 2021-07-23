import discord
from discord.ext import commands

import time

class Shinomiya(commands.Bot):

    def __init__(self, *options):
        intents = discord.Intents.all()
        super().__init__(intents= intents, command_prefix= self.determine_prefix, *options)

        boot_extensions = ['jishaku']
        for ext in boot_extensions:
            self.load_extension(ext)
    
    def determine_prefix(self, bot, message):
        prefixes = (
            's!',
            'k!',
            '.',
        )
        #We will add a customizable prefix later, these are the mere default.

        return commands.when_mentioned_or(*prefixes)(bot, message)

    async def on_ready(self):
        print(f'{self.user}: Ready. ({self.user.id})')
        print(f'{len(self.users)} users.')

        if not hasattr(self, 'uptime'):
            # on_ready can be fired multiple times in a single instance.
            # We only need the first call to determine uptime.

            self.uptime = time.time()

