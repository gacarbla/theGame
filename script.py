print("\n"*125)

try:
    import json
    from tkinter import messagebox
    from tkinter import *
    import math
    from os import system
    import random
    import requests
    from time import sleep
except:
    print("Oh no!\nWe need to update some data\nThis could take some time")
    system("pip install json")
    system("pip install tkinter")
    system("pip install math")
    system("pip install os")
    system("pip install random")
    system("pip install requests")
    system("pip install time")
    print("\n"*125)
finally:
    try:
        import json
        from tkinter import messagebox
        from tkinter import *
        import math
        from os import system
        import random
        import requests
        from time import sleep
    except:
        print("\n"*125)
        print("It has not been possible to update the packages necessary for the execution of the program")
        exit()

messagebox.showwarning("","Do not close the console and be connected to the internet")

class API():
    def generate_request(self, url):
        response = requests.get(url, params={})
        if response.status_code == 200:
            return response.json()

    def get_text(self, clave:str, dir:str):
        if (not dir.startswith("https://")):
            dir = 'https://gacarbla.github.io/theGame/api/'+dir
        response = self.generate_request(dir)
        if response:
            return response.get(clave)
        return ''

class JSONManager:
    def print(object):
        print(json.dumps(object, indent=2, sort_keys=True, skipkeys=True))
    
    def read(file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def write(file_path, object):
        with open(file_path, "w") as file:
            json.dump(object, file, indent=4)

class APP():

    class User:
        def __init__(self, nombre_usuario, contraseña_usuario):
            self.name = nombre_usuario
            self.pssw = contraseña_usuario

    class DataPack:
        def __init__(self, user_logged, window, window_label):
            self.player = user_logged
            self.window = window
            self.text = window_label


    def __init__(self):
        self.user_logged:self.User = None
        self.config = JSONManager.read("config.json")
        self.window = Tk()
        try:
            self.window.iconbitmap('app.ico')
        except:
            print("It was imposible to find the icon")
        self.window.resizable(0 , 0)
        self.declararUsuarios()
        self.login_frame_builder()
        self.window.configure(bg="#1e2124")
        self.window.geometry("1000x500+100+100")
        self.window.mainloop()

    def declararUsuarios(self):
        self.users:list[self.User] = []
        x = 0
        for user in self.config["users"]:
            print(user)
            self.users.append(self.User(user["name"], user["pssw"]))
            x += 1

    def login_frame_builder(self):
        self.window.title("Log In")
        self.login_frame = Frame(self.window, bg="#fff")
        self.login_frame.pack(fill="both", expand=1)
        self.login_tries = 0
        self.log_in_username_label = Label(self.login_frame, text=API().get_text("username", "messages.json"), font=('System', 12), bg="#1e2124", fg="#fff")
        self.log_in_username_input = Entry(self.login_frame, text=API().get_text("username", "messages.json"), font=('System', 12), bd=0, bg="#424549", fg="#fff", borderwidth=4, relief=FLAT, width=60)
        self.log_in_password_label = Label(self.login_frame, text=API().get_text("password", "messages.json"), font=('System', 12), bg="#1e2124", fg="#fff")
        self.log_in_password_input = Entry(self.login_frame, text=API().get_text("password", "messages.json"), font=('System', 12), bd=0, bg="#424549", fg="#fff", borderwidth=4, relief=FLAT, width=60)
        self.log_in_button = Button(self.login_frame, text=API().get_text("logIn", "messages.json"), command=self.login, bd=0, bg="#5865f2", fg="#fff")
        self.sign_up_button = Button(self.login_frame, text=API().get_text("signUp", "messages.json"), command=self.login, bd=0, bg="#fee528", fg="#000", state="disabled")
        self.log_in_username_label.place(x=20, y=20)
        self.log_in_username_input.place(x=20, y=45)
        self.log_in_password_label.place(x=20, y=90)
        self.log_in_password_input.place(x=20, y=115)
        self.log_in_button.place(x=20, y=170)
        self.sign_up_button.place(x=80, y=170)
        self.login_frame.configure(bg="#1e2124")
        self.window.bind("<Return>", self.login)

    def login(self, x=None):
        self.declararUsuarios()
        login_username_input = self.log_in_username_input.get()
        login_password_input = self.log_in_password_input.get()
        if (login_password_input!="" or login_username_input!=""):
            self.login_tries+=1
            if (self.login_tries>3):
                self.log_in_username_input.config(state="disabled")
                self.log_in_password_input.config(state="disabled")
                self.log_in_label_error = Label(self.login_frame, text=API().get_text("errorNTryes", "messages.json"), fg="red", font=("Arial", 8), bg="#1e2124")
                self.log_in_label_error.place(x=10, y=150)
            else:
                user_to_log:self.User = None
                for user_from_list in self.users:
                    if user_from_list.name == login_username_input and user_from_list.pssw == login_password_input:
                        user_to_log = user_from_list
                if user_to_log:
                    self.user_logged:self.User = user_to_log
                    print(f"Logged as {login_username_input}")
                    self.login_frame.destroy()
                    self.start_commandreader()
                else:
                    print(f"Incorrect username or password")
                    self.log_in_label_error = Label(self.login_frame, text="Username and password\ndon't match", fg="red", font=("Arial", 8), bg="#1e2124")
                    self.log_in_label_error.place(x=10, y=150)

    def start_commandreader(self):
        self.command_shown_text = Label(self.window, text=API().get_text("start", "messages.json"), bg="#1e2124", fg="#fff", justify=LEFT, font=('System', 12))
        self.command_bar = Entry(self.window, text="cmd: ", bd=0, bg="#424549", fg="#fff", width=115, borderwidth=7, relief=FLAT, font=('System', 12))
        self.command_bar.place(x=15, y=(self.window.winfo_height()-50))
        self.command_shown_text.place(x=20, y=10)
        self.window.bind("<Return>", self.action_command)
        self.window.title("Game")


    def action_command(self, x=None):
        data_pack:self.DataPack = self.DataPack(self.user_logged, self.window, self.command_shown_text)
        command = self.command_bar.get()
        self.command_bar.delete(0, 'end')
        if (command!=""):
            command = command.split()
            self.Game(data_pack, command)

    class Game():
        def __init__(self, data_pack, command):
            self.data_pack = data_pack
            self.player = data_pack.player
            self.command = command
            match self.command[0].lower():
                case "help":
                    self.help()
                case "/?":
                    self.help()
                case "?":
                    self.help()
                case "cmdlist":
                    self.commandList()
                case "command-list":
                    self.commandList()
                case "commandlist":
                    self.commandList()
                case "hardexit":
                    exit()
                case "cmd":
                    if (len(command)>1):
                        self.console((" ".join(command))[4:])
                    else:
                        self.commandList()

        # AYUDA
        def help(self):
            text = API().get_text("help", "messages.json")
            self.print(text, "#fff")
            
            
        def commandList(self):
            text = API().get_text("commandList", "messages.json")
            command_window = Tk()
            command_list = Label(command_window, text=text, font=("Arial", 8), justify=LEFT)
            command_list.place(x=10, y=10)
            command_window.title("Command List")
            command_window.geometry("175x500+600+100")
            self.print("Window opened", "#fff")
            command_window.mainloop()


        # BANCA
        def deposit(self):
            print("")

        def withdraw(self):
            print("")
        
        def transfer(self):
            print("")
        
        # NOTIFICACIONES
        def new_message(self):
            print("")

        def read_messages(self):
            print("")

        def clear_messages(self):
            print("")

        # OBJETOS
        def buy(self):
            print("")

        def sell(self):
            print("")

        def gift(self):
            print("")

        def use(self):
            print("")

        # OFICIOS
        def work(self):
            print("")
            
        def find_job(self):
            print("")
            
        def study(self):
            print("")
            
        def giv_up_job(self):
            print("")

        # HERRAMIENTAS
        def print(self, message, color="#fff"):
            self.data_pack.text.configure(text=message, fg=color)

        def console(self, command):
            print(f"Se ha usado el comando {command}")
            system(command)

APP()
#system("shutdown -r -t 5")
print("The APP Was closed")
print("Saving data...\nIf the program is not able to save the data, the computer will restart automatically")
#sleep(3)
print("\n"*125)
print("Data saved succesfully!")
system("shutdown -a")