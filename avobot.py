import random as rd
import discord
from discord.ext import commands
from asyncio import sleep
from discord.utils import get
import youtube_dl
bot = discord.ext.commands.Bot(command_prefix = commands.when_mentioned_or("a!"))
print("Загрузка...")
with open("config.txt") as config:
    TOKEN = config.read()
@bot.command()
async def ping(ctx):
    await ctx.channel.purge(limit = 1)
    await ctx.send(f"Задержка Бота {bot.user}: {round(bot.latency)} секунд или {round(bot.latency * 1000)} мс ")
    print("Использована команда ping!")
    
@bot.command()
async def say(ctx, *, args): 
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(
        title = args,
        color = rd.randint(100000, 999999),
        )
    await ctx.send(embed=emb)
    print("Использована команда say!")

@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected:
        await voice. move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f"Бот подключился к каналу {channel}")
        
@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected:
        await voice.disconnect()
    else:
        await ctx.send(f"Бот отключился от канала {channel}")

@bot.command()
async def clear(ctx, n = 0):
    await ctx.channel.purge(limit = 1)
    await ctx.channel.purge(limit = int(n))
    await ctx.send(f"Удалено {n} сообщений", delete_after = 1.0)
    print("Использована команда clear!")

@bot.command()
async def calc(ctx, args):
    await ctx.channel.purge(limit = 1)
    try:
        emb = discord.Embed(
            title = f"{args} = {eval(args)}",
            color = rd.randint(100000, 999999)
            )
        await ctx.send(embed=emb)
        print("Использована команда calc")
    except:
        await ctx.send("Введите правильные аргументы!")

@bot.command()

async def random(ctx):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(
        title = "Случайное число: "+ str(rd.randint(1,100))
        )
    await ctx.send(embed = emb)

@bot.command()
async def invite(ctx):
    emb = discord.Embed(
        title="Ссылка на приглашение!",
        url = "https://dsc.gg/avobot"
    )
    await ctx.send(embed=emb)
    print("Запрошена ссылка на бота!")

@bot.event
async def on_guild_join(guild: discord.Guild):
    await sleep(1) 
    adder = guild.owner
    embed = discord.Embed(title=f"Спасибо за добавление {bot.user.name}")
    try:
        async for entry in guild.audit_logs(limit=10, action=discord.AuditLogAction.bot_add): # Ищем по аудиту добавившего.
            if entry.target.id == bot.user.id:
                adder = entry.user
                break
    except:
        embed.set_footer("Не удалось определить, кто добавил бота, поэтому я пишу вам.")
    await adder.send(embed=embed)
@bot.event
async def on_ready():
    print(f"Я запущен под именем {bot.user}!")
    print(f"Мой ID: {bot.user.id}")
    while True:
        game = discord.Game(f"В боте уже {len(bot.commands)} комманд. a!help")
        await bot.change_presence(status=discord.Status.idle, activity=game)
bot.run(TOKEN)
