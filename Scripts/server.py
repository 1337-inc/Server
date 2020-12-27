import socket
import threading
import pickle

class Server :
    def __init__(self) :
        """creating a new socket object"""
        self.HEADER = 64
        self.PORT = 5050
        self.SERVER =  socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try :
            self.server.bind(self.ADDR)
        except Exception as exception :
            print(exception)
        self.save_dict = {}
        self.print_list = []
        self.client_connect = True
        self.connected = True

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
        self.client_connect = True
        self.print_list += [f"[NEW CONNECTION] {addr} connected."]
        while self.client_connect:
            try :
                self.save_dict = self.file_access()
                msg = self.recieve(conn)
                if msg == self.DISCONNECT_MESSAGE:
                    self.client_connect = False
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
                            self.print_list += [self.save_dict]
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
                    self.print_list += [f"new dict is {self.save_dict}"]
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
                self.client_connect = False
        print("Client connection ended")
        conn.close()
        self.print_list += [f"[Terminated] connection terminated for {addr}"]

    def start(self):
        print("here in start!!")
        self.print_list += ["[STARTING] server is starting..."]
        self.server.listen()
        self.print_list += [f"[LISTENING] Server is listening on {self.SERVER}"]
        count_ = 0
        while self.connected :
            if count_ == 0 :
                print("server while")
                count_ += 1
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr),daemon=True)
            thread.start()
            self.print_list += [f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}"]
        print("Server while check ended!")


if __name__ == "__main__" :
    server = Server()
    server.start()