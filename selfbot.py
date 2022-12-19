#!/usr/bin/env python3
import discord
from config import *

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")
    
    async def on_message(self, message):
        if message.author != self.user:
            return
        
        if message.content.endswith(','):
            await message.edit(content=message.content[:-1])
            await message.channel.send('!i n')
        
        elif message.content.startswith('-'):
            if message.content == '-':
                await message.delete()
                await message.channel.send('!i n')
            elif message.content == '-п':
                await message.edit(content='*Промах.*')
            elif message.content.startswith('-р'):
                if len(message.content) == 2:
                    thres = 50
                else:
                    thres = int(message.content[2:])
                await message.channel.send(f'!r 1d100<={thres}')

client = Client()
client.run(TOKEN)