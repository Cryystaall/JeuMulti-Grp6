import socket
import json
import time

class GameClient:
    def __init__(self, host: str = 'localhost', port: int = 12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_id = None
        self.player_name = None

    def connect(self):
        """Se connecte au serveur"""
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connecté au serveur.")
        except Exception as e:
            print(f"Erreur de connexion: {str(e)}")

    def send_message(self, message: dict):
        """Envoie un message au serveur"""
        try:
            self.client_socket.send(json.dumps(message).encode())
        except Exception as e:
            print(f"Erreur d'envoi: {str(e)}")

    def receive_message(self):
        """Reçoit un message du serveur"""
        try:
            data = self.client_socket.recv(1024).decode()
            if data:
                message = json.loads(data)
                return message
        except Exception as e:
            print(f"Erreur de réception: {str(e)}")
        return None

    def handle_server_message(self, message: dict):
        """Gère les messages reçus du serveur"""
        message_type = message.get("type")

        if message_type == "role_assignment":
            print(f"Ton rôle est : {message['role']}")
        elif message_type == "chat":
            print(f"[{message['player']}] {message['content']}")
        elif message_type == "player_list":
            print("Joueurs connectés :")
            for player in message["players"]:
                print(f"- {player}")
        elif message_type == "game_state":
            print(f"\nÉtat du jeu - Joueur actuel: {message['current_player']}")
            if message["is_your_turn"]:
                print("C'est ton tour !")
            print(f"Environnement : {message['environment']}")
            print(f"Statut : {message['player_status']}")
        elif message_type == "error":
            print(f"Erreur: {message['content']}")

    def start_game(self):
        """Demande au serveur de démarrer le jeu"""
        if self.game_id:
            self.send_message({
                "type": "start_game",
                "game_id": self.game_id
            })

    def join_game(self, game_id: str, player_name: str):
        """Rejoint une partie"""
        self.game_id = game_id
        self.player_name = player_name
        self.send_message({
            "type": "connection",
            "game_id": game_id,
            "name": player_name
        })

    def move(self, direction: int):
        """Envoie un mouvement au serveur"""
        if self.game_id:
            self.send_message({
                "type": "move",
                "game_id": self.game_id,
                "direction": direction
            })

    def run(self):
        """Exécute le client"""
        self.connect()

        # Rejoindre une partie
        game_id = input("Entrez l'ID de la partie : ")
        player_name = input("Entrez votre nom : ")
        self.join_game(game_id, player_name)

        # Attente du rôle
        while True:
            message = self.receive_message()
            if message:
                self.handle_server_message(message)
                if message.get("type") == "role_assignment":
                    break

        # Demander de commencer la partie
        start_game = input("Souhaitez-vous démarrer la partie ? (oui/non) : ")
        if start_game.lower() == "oui":
            self.start_game()

        # Gérer le jeu
        while True:
            message = self.receive_message()
            if message:
                self.handle_server_message(message)

                if message.get("type") == "game_state" and message["is_your_turn"]:
                    # Demander un mouvement à l'utilisateur
                    direction = input("Entrez une direction (1=haut, 2=gauche, 3=bas, 4=droite) : ")
                    if direction in ['1', '2', '3', '4']:
                        self.move(int(direction))
                    else:
                        print("Direction invalide. Essayez encore.")

            time.sleep(1)  # Attente avant la prochaine réception pour ne pas surcharger

    def close(self):
        """Ferme la connexion avec le serveur"""
        self.client_socket.close()

if __name__ == "__main__":
    client = GameClient()
    try:
        client.run()
    except KeyboardInterrupt:
        print("\nDéconnexion...")
        client.close()
