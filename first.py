import discord
import random
import os
from discord.ext import commands,tasks
from itertools import cycle

client = commands.Bot(command_prefix = '^')
status = cycle(['s1','s2','cyberpunk'])
#status
@client.event
async def on_ready():
    change_status.start()
    print('ready!')

@tasks.loop(seconds= 10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball','test'])
async def _8ball(ctx,*,question):
    response = [
                 'It is decidedly so',
                 'Without a doubt',
                 'Yes - definitely',
                 'You may rely on it',
                 'As I see it', 'yes',
                 'Most likely',
                 'Outlook good',
                 'Yes',
                 'Signs point to yes',
                 'Reply hazy', 'try again',
                 'Ask again later',
                 'Better not tell you now',
                 'Cannot predict now',
                 'Concentrate and ask again',
                 'Dont count on it',
                 'My reply is no',
                 'My sources say no',
                 'Outlook not so good',
                 'Very doubtful']
    await ctx.send(f'Question:{question}\nAnswer: {random.choice(response)}')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx,member : discord.Member, *,reason = None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx,member : discord.Member, *,reason = None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *,member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')

#@client.command()
#async def unload(ctx,extension):
    #client.unload_extension(f'cogs.{extension}')

#for filename in os.listdir('./cogs'):
    #if filename.endswith('.py'):
        #client.load_extension(f'cogs.{filename[:-3]}')

client.run('NjE4ODIxMjE3MzM1NTA5MDEy.XW_RIw.7QVa-BQMbUOQJ5agr6VJTUVMbHo')
