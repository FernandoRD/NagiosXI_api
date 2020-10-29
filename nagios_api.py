import requests
from tkinter import Tk, filedialog, Message, Entry, StringVar, Text, Scrollbar, LEFT, RIGHT, Y, END, W, FLAT, SUNKEN, RAISED, GROOVE, RIDGE, OUTSIDE, INSIDE
from tkinter import Button, Frame, IntVar, Radiobutton, Widget, OptionMenu
from tkinter import messagebox
import json
import re
import functions
import vis


def main():

    root = Tk()
    root.title("Nagios API")

    ################################### FRAME 0 ###################################
    frame0 = Frame(root, width=1000, height=70)
    
    for widget in frame0.winfo_children():
        widget.destroy()

    api_base = functions.load_servers()
    api_base_key = StringVar(root)
    # Definido api_object default copiando a key de api_command
    api_base_key.set(str(list(api_base.keys())[-1]))

    tit_api_base = Message(frame0, text="API Base", aspect=400)
    tit_api_base.place(x=0, y=0)
    api_base_menu = OptionMenu(frame0, api_base_key, *api_base.keys())
    api_base_menu.place(x=130, y=0)

    usr_tokens = functions.load_tokens()
    usr_token_key = StringVar(root)
    usr_token_key.set(str(list(usr_tokens.keys())[-1]))

    tit_user_token = Message(frame0, text="Token", aspect=400)
    tit_user_token.place(x=260, y=0)
    user_token_menu = OptionMenu(frame0, usr_token_key, *usr_tokens.keys())
    user_token_menu.place(x=390, y=0)

    operation = IntVar()
    operation.set(0)  # Inicializando com a opção read only
    operations = ["Applied", "Config"]

    def draw_interface_applied():
        vis.draw_interface_applied(root, frame1, frame2, frame3, usr_tokens, usr_token_key, api_base, api_base_key)
    def draw_interface_config():
        vis.draw_interface_config(root, frame1, frame2, frame3, usr_tokens, usr_token_key, api_base, api_base_key)

    Radiobutton(frame0, text=operations[0], variable=operation, command=draw_interface_applied, value=0).place(x=0, y=30)
    Radiobutton(frame0, text=operations[1], variable=operation, command=draw_interface_config, value=1).place(x=0, y=50)

    frame0.pack()
    ################################### FRAME 1 ###################################
    frame1 = Frame(root, width=1000, height=70)
    ################################### FRAME 2 ###################################
    frame2 = Frame(root, width=1000, height=400)
    ################################### FRAME 3 ###################################
    frame3 = Frame(root, width=1000, height=100)

    # Define visão padrão quando inicia o aplicativo
    draw_interface_applied()

    frame1.pack()
    frame2.pack()
    frame3.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
    