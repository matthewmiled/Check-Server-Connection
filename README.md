# Check-Server-Connection
A simple networking program that establishes whether a connection can be made to an external server. 

# Usage
* Add/remove a server to the list of servers to scan by running the `serverList.py` file. Servers are stored as a class instance/object and saved to a pickle file.
* Connections with the servers in the server list are made by running the `checkServer.py` file. The result of the connection attempt is saved to a history log.
* The history log stores the result of up to 100 connection attempts before they are overwritten. This can be edited via the `history_max` variable in `checkServer.py`.
* The history log is part of the server object (which is written to the pickle file each run). 
* The program outputs whether connection to each of the servers in the server list was successful by returning the most recent log in the history. 
