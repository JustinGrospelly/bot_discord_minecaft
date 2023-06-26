# Discord import
import discord
from discord.ext import commands
from discord.ext import tasks

# Serveur minecraft import 
from mcstatus import JavaServer

# Définition des permission (intents)
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Définition de la tache en arrière-plan 
@tasks.loop(seconds=10)
async def my_background_task(server_ip, server_port):
    Joueur_en_linge = 0

    try :
        # Créer une instance de MinecraftServer avec l'adresse IP et le port
        server = JavaServer.lookup(f"{server_ip}:{server_port}")

        # Obtenir l'état du serveur
        status = server.status()

        # Récupérer le nombre de joueurs connectés
        Joueur_en_linge = status.players.online
    except TimeoutError:
        print("TimeoutError")
    except Exception as e:
        print("Erreur :", e)
    
    # Si joueur en linge passé en actif (vert) est afficher le nombre de joueur 
    if Joueur_en_linge >= 1 :
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"{Joueur_en_linge} joueurs en linge"))

    # si il y a pas de joueur en linge passer le Bot en inactif (jaune) est afficher le nombre de joueur
    elif Joueur_en_linge == 0 :
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"{Joueur_en_linge} joueurs en linge"))

    # Sinon passer en ne pas déranger (rouge) est afficher erreur 
    else :
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="erreur"))


@bot.event
async def on_ready():
    # Paramètre pour l’axer au serveur Minecraft  
    server_ip = "" # Ip du serveur
    server_port = 25565 # Port du serveur de base 25565
    
    # Démarrage de la tache en arrière-plan
    my_background_task.start(server_ip, server_port)

# Commande de test de fonctionnement 
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('token') # Le token de vautre bot