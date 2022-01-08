import socket
import ssl
from datetime import datetime
import pickle
import subprocess
import platform

import subprocess
import platform

class Server():
    # This initialisation is going to define what the server parameters are when we create a server to connect to
    def __init__(self, name, display_name, port, connection, priority):
        self.name = name
        self.display_name = display_name
        self.port = port
        self.connection = connection.lower()
        self.priority = priority.lower()

        self.history = []
        self.alert = False

    def check_connection(self):
        msg = f"Could not connect to {self.display_name} ({self.name})."
        success = False
        now = datetime.now().strftime("%d/%m/%Y %H:%M")

        try:
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.display_name} ({self.name}) is up. On port {self.port} with {self.connection} connection."
                success = True
                self.alert = False
            
            elif self.connection == "ssl":
                ssl.wrap_socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.display_name} ({self.name}) is up. On port {self.port} with {self.connection} connection."
                success = True
                self.alert = False

            # If the connection isnt't plain or ssl, we just want to ping the server
            # We've made a separate function to achieve this
            else:
                if self.ping():
                    msg = f"{self.display_name} ({self.name}) is up. On port {self.port} with {self.connection} connection."
                    success = True
                    self.alert = False


        except socket.timeout:
            msg = f"Server: {self.display_name} / {self.name} timeout. On port {self.port}."

        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = f"Server: {self.display_name} ({self.name}) {e}."

        except Exception as e:
            msg = f"Couldn't connect to server {self.display_name} ({self.name}). {e}."

        # Calling another function to log this connection attempt
        self.create_history(msg, success, now)

    def ping(self):
        try:
            # This is the ping, but the command is different for windows and unix so formatting different line depending on system
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower() == "windows" else "c", self.name ), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
            return False

    def create_history(self, msg, success, now):
        # Max amount of connections logged in history per server
        history_max = 100
        self.history.append((msg, success, now))

        while len(self.history) > history_max:
            self.history.pop(0)


if __name__ == "__main__":
    
    # Saving our server list as a pickle object
    try:
        servers = pickle.load(open("servers.pickle", "rb"))
    except:
        servers = [
            Server("github.com", "Github", 80, "plain", "high"), 
        ]


    # However, if we want to add/remove a server to our server list, the program won't recognise it because a pickle object for the existing list already exists
    # We have created a separate .py file to add a server to the pickle object. Run serverList.py to add/remove a new server without altering exsiting history. 

    for server in servers:
        server.check_connection()
        print(f'>> {len(server.history)} connection attempts logged for {server.display_name} ({server.name}). Most recent log -> {server.history[-1]} \n')


    pickle.dump(servers, open("servers.pickle", "wb"))