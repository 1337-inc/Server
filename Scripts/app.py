import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
from Scripts.server import Server
import threading
import time

class Root(ThemedTk) :
    def __init__(self,**kwargs) :
        ThemedTk.__init__(self, theme="black", **kwargs)
        self.title = "Server Interface"
        self.geometry("500x700")
        self.configure(bg="#424242")
        # self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW",self.exit)
        self.logs_connect = True
        self.styles()
        self.update()
        self.server_thread = threading.Thread(target=server.start,daemon=True)
        self.server_thread.start()
        self.display()

    def exit(self) :
        server.client_connect = False
        server.connected = False
        self.logs_connect = False
        self.quit()

    def styles(self) :
        style = ttk.Style()
        style.configure("head.TLabel",background="#424242",font= ("bahnschrift",30,"underline"))
        style.configure("copy_text.TLabel",background="#424242",font= ("HP Simplified Hans",15))
        style.configure("logs.TLabel",background="#424242",font= ("HP Simplified Hans",20))

    def display(self) :
        def onFrameConfigure(canvas):
            """Reset the scroll region to encompass the inner frame."""
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_mousewheel(event):
            """Enables scroll with the mousewheel."""
            shift = (event.state & 0x1) != 0
            scroll = -1 if event.delta > 0 else 1
            if shift:
                canvas.xview_scroll(scroll, "units")
            else:
                canvas.yview_scroll(scroll, "units")

        def logs_populate() :
            diff = len(server.print_list)-self.cursor
            if diff != 0 :
                print(server.print_list)
                print(f" here inside condition. Sursor is : {self.cursor}")
                logs_text.config(state=tk.NORMAL)
                insert_list = server.print_list[-1:-(diff+1):-1]
                for text in insert_list[-1::-1] :
                    logs_text.insert(f"{self.cursor+1}.0",str(text)+"\n")
                    print(f"insertion done at {self.cursor+1}")
                    self.cursor += 1
                self.update()
                logs_text.tag_add("1", "1.0", tk.END)
                logs_text.config(state=tk.DISABLED)
                if self.count == 0 :
                    print("here in while of app")
                    self.count += 1
                    logs_text.tag_config("1", foreground="green", font=("bahnschrift semibold condensed",15))
            if self.logs_connect :
                self.after(500,logs_populate)

        tk.Grid.columnconfigure(self, 0, weight=1)
        head = ttk.Label(self,text="Server Interface",style="head.TLabel")
        head.grid(row=0,column=0,pady=30)
        # ip_address = server.get_gateway_ip()
        ip_address = server.SERVER
        ip_text = tk.Text(self,bg="#424242",width=35,height=10,relief=tk.FLAT)
        ip_text.insert("1.0",str(ip_address))
        ip_text.tag_add("1", "1.0", tk.END)
        ip_text.tag_config("1", foreground="white", font=("HP Simplified Hans",25,"bold"))
        ip_text.grid(row=1,column=0,pady=50)
        ip_text.configure(state=tk.DISABLED)
        self.update()
        copy_lbl = ttk.Label(self,
                            text="Copy the above IP address and paste it in the box \nprovided for it in the game when asked fo it.",
                            style="copy_text.TLabel")
        copy_lbl.grid(row=1,column=0)
        logs = ttk.Label(self,text="Server Logs",style="logs.TLabel")
        logs.place(relx=0.03,rely=0.48)
        self.update()

        logs_frame = ttk.Frame(self,width=450,height=300)
        logs_frame.place(relx=0.045,rely=0.55)
        canvas = tk.Canvas(logs_frame, background="black", width=450, height=300)
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        frame = ttk.Frame(canvas)
        vsb = ttk.Scrollbar(logs_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

        logs_text = tk.Text(frame,bg="black")
        logs_text.grid()
        self.cursor,self.count = 0,0
        self.update()
        
        logs_populate()

# start the server
server = Server()
if __name__ == "__main__" :
    root = Root()


    root.mainloop()