import socket 
import threading
import pickle

class Server :
    def __init__(self) :
        self.HEADER = 64
        self.PORT = 5050
        self.SERVER =  socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.save_dict = {}

    def file_access(self) :
        with open("project_data\\savedata.dat","rb") as save_file :
            try :
                save_dict = pickle.load(save_file)
            except EOFError :
                save_dict = {}
            return save_dict

    def file_dump(self) :
        with open("project_data\\savedata.dat","wb") as save_file :
            pickle.dump(self.save_dict,save_file)

    def recieve(self,conn) :
        msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(self.FORMAT)
            return msg

    def handle_client(self,conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            try :
                self.save_dict = self.file_access()
                msg = self.recieve(conn)
                if msg == self.DISCONNECT_MESSAGE:
                    connected = False
                elif msg == "Save Data" :
                    player_id = conn.recv(5000)
                    try :
                        name,code = pickle.loads(player_id)
                    except EOFError :
                        pass
                    if (name,code) not in self.save_dict :
                        conn.send("Available".encode(self.FORMAT))
                        msg1 = self.recieve(conn)
                        if msg1 == "Game Data" :
                            game_data = conn.recv(5000)
                            #msg = pickle.loads(msg_data)
                            self.save_dict[(name,code)] = game_data
                            print(self.save_dict)
                            conn.send("Success".encode(self.FORMAT))
                    else :
                        conn.send("Exists".encode(self.FORMAT))
                        msg1 = self.recieve(conn)
                        if msg1 == "Game Data" :
                            game_data = conn.recv(5000)
                            self.save_dict[(name,code)] = game_data
                            conn.send("Success".encode(self.FORMAT))
                elif msg == "Wipe" :
                    self.save_dict.pop((name,code))
                    print(f"new dict is ",self.save_dict)
                elif msg == "Load" :
                    player_id = conn.recv(5000)
                    try :
                        name,code = pickle.loads(player_id)
                    except EOFError :
                        pass
                    if (name,code) in self.save_dict :
                        conn.send("Present".encode(self.FORMAT))
                        conn.send(self.save_dict[(name,code)])
                    else :
                        conn.send("Absent".encode(self.FORMAT))
                elif msg == "Check Data" :
                    player_id = conn.recv(5000)
                    try :
                        name,code = pickle.loads(player_id)
                    except EOFError :
                        pass
                    if (name,code) in self.save_dict :
                        conn.send("Exists".encode(self.FORMAT))
                    else :
                        conn.send("New".encode(self.FORMAT))
                self.file_dump()
            except ConnectionResetError :
                connected = False

        conn.close()
        print(f"[Terminated] connection terminated for {addr}")
            

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
server = Server()
server.start()