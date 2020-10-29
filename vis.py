import requests
from tkinter import Checkbutton, Tk, filedialog, Message, Entry, StringVar, Text, Scrollbar, LEFT, RIGHT, Y, END, W, SUNKEN, OUTSIDE
from tkinter import Button, Frame, IntVar, Radiobutton, Widget, OptionMenu, Scrollbar
from tkinter import messagebox
import json
import re

from requests.models import MissingSchema
import functions
import objects

api_url = ""
# Cria os widgets de botões para a visão read only
def draw_interface_applied(root, frame1, frame2, frame3, usr_tokens, usr_token_key, api_base, api_base_key):

    for widget in frame1.winfo_children():
        widget.destroy()
    for widget in frame2.winfo_children():
        widget.destroy()
    for widget in frame3.winfo_children():
        widget.destroy()

    # cada dicionário tem 2 funções as keys são o que se escolhe no menu e os valores são o que a vem no JSON (fiz um de - para com os dados no help do Nagios
    
    available_objects = objects.available_objects
    api_object = StringVar(root)
    # Definido api_object default copiando a key de available_objects
    api_object.set("objects/hoststatus")

    tit_api_object_menu = Message(frame1, text="API Objects", aspect=400)
    tit_api_object_menu.place(x=1, y=10)
    api_object_menu = OptionMenu(frame1, api_object, *available_objects)
    api_object_menu.place(x=130, y=5)

    for widget in frame2.winfo_children():
        widget.destroy()

    tit_api_filter = Message(frame2, text="Search Parameters", aspect=600)
    tit_api_filter.place(x=1, y=0)
    api_filter = Entry(frame2)
    api_filter.place(x=130, y=0, width=400, height=20)
    #api_filter.insert(END, "name=lk:apple")

    titulo_show_api = Message(frame2, text="Get API", aspect=400)
    titulo_show_api.place(x=1, y=40)
    show_api = Message(frame2, aspect=2050, anchor=W, relief=SUNKEN)
    show_api.place(x=130, y=45, width=820, height=40)


    text_area_json = Text(frame2, width=111, height=12)
    text_area_scroll = Scrollbar(frame2, command=text_area_json.yview)
    text_area_scroll.place(x=940, y=100, height=200)

    text_area_json.place(x=50, y=100)
    text_area_json.insert(END, "JSON Contents")
    text_area_json.config(yscrollcommand=text_area_scroll.set)
    

    for widget in frame3.winfo_children():
        widget.destroy()

    def button_build_API():
        global api_url
        api_url = functions.build_API(api_object, api_filter, usr_token_key, usr_tokens, api_base_key, api_base)
        functions.update_api(api_url, frame2)

    button_build_API = Button(frame3, text="Build API", command=button_build_API)
    button_build_API.place(x=50, y=10, width=150, height=30)

    def button_get_json():
        api_selected_object = str(api_object.get())
        type_oper = "applied"
        api_method = "get"
        try:
            list_json = functions.get_json(type_oper, api_method, api_url, available_objects, api_selected_object)
        except ConnectionError:
            messagebox.showerror("Conexão", "API Inválida!")
        except MissingSchema:
            messagebox.showerror("Conexão", "Monte a API primeiro!")
        except Exception as e:
            print(e)
            messagebox.showerror("Conexão", "Erro desconhecido!")
        else:
            # Antes de jogar na tela o JSON ele testa o tamanho, se for muito grande pergunta se quer salvar em arquivo direto
            if int(list_json[0]) > 50:
                if messagebox.askyesno("Resposta muito grande", "Gostaria de salvar em arquivo?"):
                    functions.save_file(list_json[1], "json")
            else:
                text_area_json.delete(1.0, END)
                text_area_json.insert(END, list_json[1])

    button_get_jason = Button(frame3, text="Get JSON", command=button_get_json)
    button_get_jason.place(x=210, y=10, width=150, height=30)

    def button_clear_text():
        global api_url
        api_url = ""
        text_area_json.delete(1.0, END)
        # text_area_json.insert(END, resposta)

    button_clear = Button(frame3, text="Clear", command=button_clear_text)
    button_clear.place(x=370, y=10, width=150, height=30)

    def button_save_json():
        functions.save_file(text_area_json.get(1.0, END), "json")

    button_save = Button(frame3, text="Save JSON", command=button_save_json)
    button_save.place(x=50, y=60, width=150, height=30)

    def button_load_json():
        text_area_json.delete(1.0, END)
        text_area_json.insert(END, json.loads(functions.load_file()))

    button_load = Button(frame3, text="Load JSON", command=button_load_json)
    button_load.place(x=210, y=60, width=150, height=30)

    def button_convert_json():
        functions.convert_json()
    
    button_convert = Button(frame3, text="JSON -> CSV", command=button_convert_json)
    button_convert.place(x=370, y=60, width=150, height=30)

    def button_quit_program():
        functions.quit_program(root)

    button_quit = Button(frame3, text="Quit", command=button_quit_program)
    button_quit.place(x=800, y=10, width=150, height=30)

# Desenha os widgets de botões para a visão de config
def draw_interface_config(root, frame1, frame2, frame3, usr_tokens, usr_token_key, api_base, api_base_key):

    for widget in frame1.winfo_children():
        widget.destroy()
    for widget in frame2.winfo_children():
        widget.destroy()
    for widget in frame3.winfo_children():
        widget.destroy()

    # Listas com as opções de configuração
    available_objects_config = objects.available_objects_config
    options_available_host = objects.options_available_host
    options_available_service = objects.options_available_service
    options_available_hostgroup = objects.options_available_hostgroup
    options_available_servicegroup = objects.options_available_servicegroup
    options_available_command = objects.options_available_command
    options_available_contact = objects.options_available_contact
    options_available_contactgroup = objects.options_available_contactgroup
    options_available_timeperiod = objects.options_available_timeperiod

    api_object = StringVar(root)
    # Definido api_object default copiando a key de available_objects
    api_object.set("config/host")

    tit_api_object_menu_config = Message(frame1, text="API Objects", aspect=400)
    tit_api_object_menu_config.place(x=1, y=36)
    api_object_menu_config = OptionMenu(frame1, api_object, *available_objects_config)
    api_object_menu_config.place(x=128, y=36)

    def draw_buttons_config_get():
        #global api_filter

        for widget in frame2.winfo_children():
            widget.destroy()
        for widget in frame3.winfo_children():
            widget.destroy()

        tit_api_filter = Message(frame2, text="Search Parameters", aspect=600)
        tit_api_filter.place(x=1, y=0)
        api_filter = Entry(frame2)
        api_filter.place(x=130, y=0, width=400, height=20)
        #api_filter.insert(END, "name=lk:apple")

        titulo_show_api = Message(frame2, text="Get API", aspect=400)
        titulo_show_api.place(x=1, y=40)
        show_api = Message(frame2, aspect=2050, anchor=W, relief=SUNKEN)
        show_api.place(x=130, y=45, width=820, height=40)

        text_area_json = Text(frame2, width=111, height=12)
        text_area_scroll = Scrollbar(frame2, command=text_area_json.yview)
        text_area_scroll.place(x=940, y=100, height=200)

        text_area_json.place(x=50, y=100)
        text_area_json.insert(END, "JSON Contents")
        text_area_json.config(yscrollcommand=text_area_scroll.set)

        def button_build_API():
            global api_url
            api_url = functions.build_API(api_object, api_filter, usr_token_key, usr_tokens, api_base_key, api_base)
            functions.update_api(api_url, frame2)

        button_build_API = Button(frame3, text="Build API", command=button_build_API)
        button_build_API.place(x=50, y=10, width=150, height=30)

        def button_get_json_config():
            api_selected_object = str(api_object.get())
            type_oper="config"
            try:
                list_json = functions.get_json(type_oper, api_methods[int(api_method_rb.get())], api_url, available_objects_config, api_selected_object)
            except ConnectionError:
                messagebox.showerror("Conexão", "API Inválida!")
            except MissingSchema:
                messagebox.showerror("Conexão", "Monte a API primeiro!")
            except Exception as e:
                print(e)
                messagebox.showerror("Conexão", "Erro desconhecido!")
            else:
                # Antes de jogar na tela o JSON ele testa o tamanho, se for muito grande pergunta se quer salvar em arquivo direto
                if int(list_json[0]) > 50:
                    if messagebox.askyesno("Resposta muito grande", "Gostaria de salvar em arquivo?"):
                        functions.save_file(list_json[1], "json")
                else:
                    text_area_json.delete(1.0, END)
                    text_area_json.insert(END, list_json[1])

        button_get_jason_config = Button(frame3, text="Get JSON Config", command=button_get_json_config)
        button_get_jason_config.place(x=210, y=10, width=150, height=30)

        def button_clear_text():
            global api_url
            api_url = ""
            text_area_json.delete(1.0, END)
            # text_area_json.insert(END, resposta)

        button_clear = Button(frame3, text="Clear", command=button_clear_text)
        button_clear.place(x=370, y=10, width=150, height=30)

        def button_save_json():
            functions.save_file(text_area_json.get(1.0, END), "json")

        button_save = Button(frame3, text="Save JSON", command=button_save_json)
        button_save.place(x=50, y=60, width=150, height=30)

        def button_load_json():
            text_area_json.delete(1.0, END)
            text_area_json.insert(END, json.loads(functions.load_file()))

        button_load = Button(frame3, text="Load JSON", command=button_load_json)
        button_load.place(x=210, y=60, width=150, height=30)

        def button_convert_json():
            functions.convert_json()

        button_convert = Button(frame3, text="JSON -> CSV", command=button_convert_json)
        button_convert.place(x=370, y=60, width=150, height=30)

        def button_quit_program():
            functions.quit_program(root)

        button_quit = Button(frame3, text="Quit", command=button_quit_program)
        button_quit.place(x=800, y=10, width=150, height=30)


    def draw_buttons_config_post():
        for widget in frame2.winfo_children():
            widget.destroy()
        for widget in frame3.winfo_children():
            widget.destroy()

        titulo_show_api = Message(frame2, text="Post API", aspect=400)
        titulo_show_api.place(x=0, y=0)
        show_api = Message(frame2, text="", aspect=2050, anchor=W, relief=SUNKEN)
        show_api.place(x=130, y=0, width=820, height=60)
        
        option_available = None
        if api_object.get() == "config/host":
            option_available = options_available_host["post"]
        if api_object.get() == "config/hostgroup":
            option_available = options_available_hostgroup["post"]
        if api_object.get() == "config/service":
            option_available = options_available_service["post"]
        if api_object.get() == "config/servicegroup":
            option_available = options_available_servicegroup["post"]
        if api_object.get() == "config/command":
            option_available = options_available_command["post"]
        if api_object.get() == "config/contact":
            option_available = options_available_contact["post"]
        if api_object.get() == "config/contactgroup":
            option_available = options_available_contactgroup["post"]
        if api_object.get() == "config/timeperiod":
            option_available = options_available_timeperiod["post"]

        y_axis = 80
        given_values = list()            
        for i in option_available:
            tit_option = Message(frame2, text="{}".format(i), aspect=600)
            tit_option.place(x=1, y=y_axis)
            option_value = Entry(frame2)
            option_value.place(x=170, y=y_axis, width=360, height=20)
            given_values.append(option_value)
            y_axis += 23

        apply_value = IntVar()
        apply_value_check = Checkbutton(frame2, text="Apply?", variable=apply_value)
        apply_value_check.place(x=165, y=y_axis)

        text_area_json = Text(frame2, width=50, height=12)
        text_area_scroll = Scrollbar(frame2)

        text_area_json.place(x=550, y=80)
        text_area_json.insert(END, "JSON Contents")
        #text_area_json.pack(side=LEFT, fill=Y)
        #text_area_scroll.pack(side=RIGHT, fill=Y)
        text_area_json.config(yscrollcommand=text_area_scroll.set)
        text_area_scroll.config(command=text_area_json.yview)

        def button_build_API_config():
            
            functions.update_api_config(functions.build_API_config(api_object, usr_token_key, usr_tokens, api_base_key, api_base, apply_value, option_available, given_values), frame2)

        button_build_API_config = Button(frame3, text="Build API", command=button_build_API_config)
        button_build_API_config.place(x=50, y=10, width=150, height=30)

        def button_post_json_config():
            api_selected_object = str(api_object.get())
            type_oper="config"
            #print("API METHOD: {}".format(int(api_method_rb.get())))api_object, api_config_values, usr_token_key, usr_tokens, api_base_key, api_base, apply
            api_url_list = functions.build_API_config(api_object, usr_token_key, usr_tokens, api_base_key, api_base, apply_value, option_available, given_values)
            response_json = functions.post_json(type_oper, api_methods[int(api_method_rb.get())], api_url_list, available_objects_config, api_selected_object)
            # Antes de jogar na tela o JSON ele testa o tamanho, se for muito grande pergunta se quer salvar em arquivo direto
            if len(response_json) > 50:
                if messagebox.askyesno("Resposta muito grande", "Gostaria de salvar em arquivo?"):
                    functions.save_file(response_json, "json")
            else:
                text_area_json.delete(1.0, END)
                text_area_json.insert(END, response_json)

        button_post_jason_config = Button(frame3, text="Post JSON Config", command=button_post_json_config)
        button_post_jason_config.place(x=210, y=10, width=150, height=30)

        def button_clear_text():
            text_area_json.delete(1.0, END)
            # text_area_json.insert(END, resposta)

        button_clear = Button(frame3, text="Clear Response", command=button_clear_text)
        button_clear.place(x=370, y=10, width=150, height=30)

        def button_quit_program():
            functions.quit_program(root)

        button_quit = Button(frame3, text="Quit", command=button_quit_program)
        button_quit.place(x=800, y=10, width=150, height=30)


    def draw_buttons_config_put():
        for widget in frame2.winfo_children():
            widget.destroy()
        for widget in frame3.winfo_children():
            widget.destroy()

        titulo_show_api = Message(frame2, text="Put API", aspect=400)
        titulo_show_api.place(x=0, y=0)
        show_api = Message(frame2, text="", aspect=2050, anchor=W, relief=SUNKEN)
        show_api.place(x=130, y=0, width=820, height=60)

        option_available = None
        if api_object.get() == "config/host":
            option_available = options_available_host["put"]
        if api_object.get() == "config/hostgroup":
            option_available = options_available_hostgroup["put"]
        if api_object.get() == "config/service":
            option_available = options_available_service["put"]
        if api_object.get() == "config/servicegroup":
            option_available = options_available_servicegroup["put"]
        if api_object.get() == "config/command":
            option_available = options_available_command["put"]
        if api_object.get() == "config/contact":
            option_available = options_available_contact["put"]
        if api_object.get() == "config/contactgroup":
            option_available = options_available_contactgroup["put"]
        if api_object.get() == "config/timeperiod":
            option_available = options_available_timeperiod["put"]

        y_axis = 80
        given_values = list()            
        for i in option_available:
            tit_option = Message(frame2, text="{}".format(i), aspect=600)
            tit_option.place(x=1, y=y_axis)
            option_value = Entry(frame2)
            option_value.place(x=170, y=y_axis, width=360, height=20)
            given_values.append(option_value)
            y_axis += 23

        apply_value = IntVar()
        apply_value_check = Checkbutton(frame2, text="Apply?", variable=apply_value)
        apply_value_check.place(x=165, y=y_axis)

        text_area_json = Text(frame2, width=50, height=12)
        text_area_scroll = Scrollbar(frame2)

        text_area_json.place(x=550, y=80)
        text_area_json.insert(END, "JSON Contents")
        #text_area_json.pack(side=LEFT, fill=Y)
        #text_area_scroll.pack(side=RIGHT, fill=Y)
        text_area_json.config(yscrollcommand=text_area_scroll.set)
        text_area_scroll.config(command=text_area_json.yview)

        def button_build_API_config():
            
            functions.update_api_config(functions.build_API_config(api_object, usr_token_key, usr_tokens, api_base_key, api_base, apply_value, option_available, given_values), frame2)

        button_build_API_config = Button(frame3, text="Build API", command=button_build_API_config)
        button_build_API_config.place(x=50, y=10, width=150, height=30)

        def button_put_json_config():
            api_selected_object = str(api_object.get())
            type_oper="config"
            #print("API METHOD: {}".format(int(api_method_rb.get())))api_object, api_config_values, usr_token_key, usr_tokens, api_base_key, api_base, apply
            api_url_list = functions.build_API_config(api_object, usr_token_key, usr_tokens, api_base_key, api_base, apply_value, option_available, given_values)
            response_json = functions.put_json(type_oper, api_methods[int(api_method_rb.get())], api_url_list, available_objects_config, api_selected_object)
            # Antes de jogar na tela o JSON ele testa o tamanho, se for muito grande pergunta se quer salvar em arquivo direto
            if len(response_json) > 50:
                if messagebox.askyesno("Resposta muito grande", "Gostaria de salvar em arquivo?"):
                    functions.save_file(response_json, "json")
            else:
                text_area_json.delete(1.0, END)
                text_area_json.insert(END, response_json)

        button_put_jason_config = Button(frame3, text="Put JSON Config", command=button_put_json_config)
        button_put_jason_config.place(x=210, y=10, width=150, height=30)

        def button_clear_text():
            text_area_json.delete(1.0, END)
            # text_area_json.insert(END, resposta)

        button_clear = Button(frame3, text="Clear Response", command=button_clear_text)
        button_clear.place(x=370, y=10, width=150, height=30)

        def button_quit_program():
            functions.quit_program(root)

        button_quit = Button(frame3, text="Quit", command=button_quit_program)
        button_quit.place(x=800, y=10, width=150, height=30)


    def draw_buttons_config_delete():
        for widget in frame2.winfo_children():
            widget.destroy()
        for widget in frame3.winfo_children():
            widget.destroy()

        titulo_show_api = Message(frame2, text="Delete API", aspect=400)
        titulo_show_api.place(x=0, y=0)
        show_api = Message(frame2, text="", aspect=2050, anchor=W, relief=SUNKEN)
        show_api.place(x=130, y=0, width=820, height=60)

        option_available = None
        if api_object.get() == "config/host":
            option_available = options_available_host["delete"]
        if api_object.get() == "config/hostgroup":
            option_available = options_available_hostgroup["delete"]
        if api_object.get() == "config/service":
            option_available = options_available_service["delete"]
        if api_object.get() == "config/servicegroup":
            option_available = options_available_servicegroup["delete"]
        if api_object.get() == "config/command":
            option_available = options_available_command["delete"]
        if api_object.get() == "config/contact":
            option_available = options_available_contact["delete"]
        if api_object.get() == "config/contactgroup":
            option_available = options_available_contactgroup["delete"]
        if api_object.get() == "config/timeperiod":
            option_available = options_available_timeperiod["delete"]

        y_axis = 80
        given_values = list()            
        for i in option_available:
            tit_option = Message(frame2, text="{}".format(i), aspect=600)
            tit_option.place(x=1, y=y_axis)
            option_value = Entry(frame2)
            option_value.place(x=170, y=y_axis, width=360, height=20)
            given_values.append(option_value)
            y_axis += 23

        apply_value = IntVar()
        apply_value_check = Checkbutton(frame2, text="Apply?", variable=apply_value)
        apply_value_check.place(x=165, y=y_axis)

        text_area_json = Text(frame2, width=50, height=12)
        text_area_scroll = Scrollbar(frame2)

        text_area_json.place(x=550, y=80)
        text_area_json.insert(END, "JSON Contents")
        #text_area_json.pack(side=LEFT, fill=Y)
        #text_area_scroll.pack(side=RIGHT, fill=Y)
        text_area_json.config(yscrollcommand=text_area_scroll.set)
        text_area_scroll.config(command=text_area_json.yview)

        def button_build_API_config():
            
            functions.update_api_config(functions.build_API_config(api_object, usr_token_key, usr_tokens, api_base_key, api_base, apply_value, option_available, given_values), frame2)

        button_build_API_config = Button(frame3, text="Build API", command=button_build_API_config)
        button_build_API_config.place(x=50, y=10, width=150, height=30)

        def button_delete_json_config():
            api_selected_object = str(api_object.get())
            type_oper="config"
            #print("API METHOD: {}".format(int(api_method_rb.get())))api_object, api_config_values, usr_token_key, usr_tokens, api_base_key, api_base, apply
            api_url_list = functions.build_API_config(api_object, usr_token_key, usr_tokens, api_base_key, api_base, apply_value, option_available, given_values)
            response_json = functions.delete_json(type_oper, api_methods[int(api_method_rb.get())], api_url_list, available_objects_config, api_selected_object)
            # Antes de jogar na tela o JSON ele testa o tamanho, se for muito grande pergunta se quer salvar em arquivo direto
            if len(response_json) > 50:
                if messagebox.askyesno("Resposta muito grande", "Gostaria de salvar em arquivo?"):
                    functions.save_file(response_json, "json")
            else:
                text_area_json.delete(1.0, END)
                text_area_json.insert(END, response_json)

        button_put_jason_config = Button(frame3, text="Delete JSON Config", command=button_delete_json_config)
        button_put_jason_config.place(x=210, y=10, width=150, height=30)

        def button_clear_text():
            text_area_json.delete(1.0, END)
            # text_area_json.insert(END, resposta)

        button_clear = Button(frame3, text="Clear Response", command=button_clear_text)
        button_clear.place(x=370, y=10, width=150, height=30)

        def button_quit_program():
            functions.quit_program(root)

        button_quit = Button(frame3, text="Quit", command=button_quit_program)
        button_quit.place(x=800, y=10, width=150, height=30)

# Visualização principal
    api_method_rb = IntVar()
    api_method_rb.set(0)
    
    tit_api_method = Message(frame1, text="API Method", aspect=400)
    tit_api_method.place(x=1, y=10)

    Radiobutton(frame1, text="Get", variable = api_method_rb, command=draw_buttons_config_get, value = 0).place(x=130, y=10)
    Radiobutton(frame1, text="Post", variable = api_method_rb, command=draw_buttons_config_post, value = 1).place(x=230, y=10)        
    Radiobutton(frame1, text="Put", variable = api_method_rb, command=draw_buttons_config_put, value = 2).place(x=330, y=10)
    Radiobutton(frame1, text="Delete", variable = api_method_rb, command=draw_buttons_config_delete, value = 3).place(x=430, y=10)
    api_methods = ["get", "post", "put", "delete"]

    # Desenhando os botoes do get como padrão
    draw_buttons_config_get()

    def button_quit_program():
        functions.quit_program(root)

    button_quit = Button(frame3, text="Quit", command=button_quit_program)
    button_quit.place(x=800, y=10, width=150, height=30)