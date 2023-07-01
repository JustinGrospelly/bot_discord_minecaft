# importation
import discord
from discord.ext import commands
from discord.ext import tasks
import time

from variable import *

# Définition des permission (intents)
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Définition de la tache en arrière-plan 
@tasks.loop(seconds=10)
async def my_background_task():
    Joueur_en_linge = statu_serveur()

    # Si joueur en linge passé en actif (vert) est afficher le nombre de joueur 
    if Joueur_en_linge >= 1 :
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"{Joueur_en_linge} joueurs en linge"))

    # si il y a pas de joueur en linge passer le Bot en inactif (jaune) est afficher le nombre de joueur
    elif Joueur_en_linge == 0 :
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"{Joueur_en_linge} joueurs en linge"))

    # Sinon passer en ne pas déranger (rouge) est afficher erreur 
    else :
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="erreur"))

@tasks.loop(seconds=10)
async def my_background_task_2(message):
    await message.edit(content=f"Il y a {statu_serveur()} joueur connecter sur le serveur  ")

@bot.event
async def on_ready():    
    # Démarrage de la tache en arrière-plan
    my_background_task.start()

# Commande de test de fonctionnement 
@bot.command()
async def ping(ctx):
    msg = await ctx.send('pong')

# Commande pour afficher le statu du serveur en version textuelle  
@bot.command()
async def serveur(message_info) :
    # envoi tu message de base
    message = await message_info.send("go")

    # Démarrage de la tache en arrière-plan
    my_background_task_2.start(message)


bot.run('TOKEN')