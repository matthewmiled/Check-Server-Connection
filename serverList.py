import pickle
from checkServer import Server

servers = pickle.load(open("servers.pickle", "rb"))

choice = input("Press 1 for add a new server or 2 for remove existing server: ")

if choice == "1":
    serverName = input("Enter a server address to add: ")
    serverDisplayName = input("Enter a display server name: ")
    port = input("Enter a port number as integer: ")
    connection = input("Enter a connection type (ping, plain or ssl): ")
    priority = input("Enter a priority (high or low): ")

    new_server = Server(serverName, serverDisplayName, port, connection, priority)
    servers.append(new_server)

    pickle.dump(servers, open("servers.pickle", "wb"))

if choice == "2":
    serverName = input("Enter a server name to remove: ")
    removed = False
    for server in servers:
        if server.name.lower() == serverName.lower():
           servers.remove(server)
           print("Server removed")
           removed = True
        
    if removed == False:
        print("Server doesn't exist in list")

    pickle.dump(servers, open("servers.pickle", "wb"))
    