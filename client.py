import socket

HOST = 'localhost'    # The remote host
PORT = 9999              # The same port as used by the server


class Player :

    def __init__(self):
        self.player_class = None
        self.actions = {
            'new_player': self.new_player,
            'ask_env': self.ask_env,
            'move': self.move,
            'help': self.display_help,
            'q': self.end_session
        }

    def new_player(self):
        name = input('name: '),
        self.player_class = input('class: ')
        self.send_message(f'new|{name},{self.player_class}')

    def ask_env(self):
        res = self.send_message(f'ask_env|{self.player_class}')


    def move(self):
        direction = input('direction: ')
        self.send_message('move|{direction}')

    def display_help(self):
        print('[new, delete, list, q (quit), help]')

    def end_session(self):
        exit()

    def run(self):

        new_player()

        while True :
            if varduserv :
                ask_env()
                # faire l'env dans le terminal

                action = input('Choose action: ')
                if action not in self.actions.keys():
                    print(f'Action [{action}] not supported')
                else:
                    self.actions[action]()

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytes(message, 'UTF-8'))
            data = s.recv(1024)
        return repr(data)    

if __name__ == '__main__':
    player = Player()
    player.run()