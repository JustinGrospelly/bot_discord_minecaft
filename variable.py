# Serveur minecraft import 
from mcstatus import JavaServer

def statu_serveur() :
    # Paramètre pour l’axer au serveur Minecraft  
    server_ip = "" # ip du serveur
    server_port = 25565 #port du serveur de base 25565

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
    return Joueur_en_linge