import requests
from tkinter import Tk, filedialog, Message, Entry, StringVar, Text, Scrollbar, LEFT, RIGHT, Y, END, W, SUNKEN, OUTSIDE
from tkinter import Button, Frame, IntVar, Radiobutton, Widget, OptionMenu
from tkinter import messagebox
import json
import re

from requests.models import MissingSchema

# Monta API de consulta
def build_API(api_object, api_filter, usr_token_key, usr_tokens, api_base_key, api_base):

    api_selected_object = api_object.get()
    query = api_filter.get()
    api_token = usr_tokens.get(str(usr_token_key.get()))
    url_base = api_base.get(str(api_base_key.get()))
    api_url = "{}/{}?apikey={}&pretty=1&{}".format(url_base, api_selected_object, api_token, query)
    return api_url

# Monta API de configuração
def build_API_config(api_object, usr_token_key, usr_tokens, api_base_key, api_base, apply, option_available, given_values):

    api_config_values = dict()
    api_url_list = list()

    count = 0
    for i in given_values:
        if len(i.get()) > 0:
            v = str(option_available[count])
            api_config_values[v]=str(i.get())
        count += 1

    api_selected_object = api_object.get()
    api_token = usr_tokens.get(str(usr_token_key.get()))
    url_base = api_base.get(str(api_base_key.get()))
    apply = str(apply.get())
    api_url = "{}/{}?apikey={}&pretty=1".format(url_base, api_selected_object, api_token)
    api_url_list.append(api_url)
    api_url_list.append(api_config_values)
    api_url_list[1]["applyconfig"] = apply

    return api_url_list

# Escreve/atualiza o field que mostra a API
def update_api(api_url, frame):
    show_api = Message(frame, text=api_url, aspect=2050, anchor=W, relief=SUNKEN)
    show_api.place(x=130, y=45, width=820, height=40)

# Escreve/atualiza o field que mostra a API de config
def update_api_config(api_url_list, frame):
    show_api = Message(frame, text=api_url_list[0]+"\n"+str(api_url_list[1]), aspect=2050, anchor=W, relief=SUNKEN)
    show_api.place(x=130, y=0, width=820, height=60)

# Salva arquivos no formato desejado
def save_file(data_in, file_extension):
    save_file_dialog = filedialog.asksaveasfilename(defaultextension="." + str(file_extension))
    try:
        with open(save_file_dialog, "w+") as file_dialog:
            file_dialog.write(str(data_in))
            file_dialog.close()
            messagebox.showinfo("Arquivo", "Arquivo salvo com sucesso!")
    except FileNotFoundError:
        messagebox.showerror("Arquivo", "Arquivo de destino não pode ser salvo!")
    except Exception as msg:
        messagebox.showerror("Erro", "Erro desconhecido!\n" + str(msg))
   
# Carrega arquivos
def load_file():
    load_file_dialog = filedialog.askopenfilename()
    try:
        with open(load_file_dialog, "r+") as file_dialog:
            data_out = file_dialog.read()
            file_dialog.close()
            return str(data_out)
    #except Exception as msg:
    #    messagebox.showerror("Arquivo", "Arquivo de origem não selecionado!")
    except Exception as e:
        messagebox.showerror("Erro", "Erro desconhecido!\n {}".format(e))

# Carrega os tokens dos servidores Nagios
def load_tokens():
    data_out = dict()
    data_out_temp = list()
    try:
        with open("./tokens.txt", "r+") as file_tokens:
            data_out_temp = file_tokens.readlines()
        for i in data_out_temp:
            i.replace("'", "")
            data_out[str(i.split(":")[0])] = str(i.split(":")[1]).replace("\n","")
        return data_out
    except Exception as msg:
        messagebox.showerror("Tokens", "Não foi possível carregar!\n" + str(msg))

# Carrega as bases das APIs dos servidores nagios
def load_servers():
    data_out = dict()
    data_out_temp = list()
    try:
        with open("./servers.txt", "r+") as file_tokens:
            data_out_temp = file_tokens.readlines()
        for i in data_out_temp:
            i.replace("'", "")
            data_out[str(i.split(":")[0])] = "https://"+str(i.split(":")[1]).replace("\n","")+"/nagiosxi/api/v1"
        return data_out
    except Exception as msg:
        messagebox.showerror("Servers", "Não foi possível carregar!\n" + str(msg))

# Faz o request no Nagios
def get_json(type_oper, api_method, api_url, available_objects, api_selected_object):
    data_out_lst = []
    try:
        nagios_json = requests.request(api_method, api_url, verify=False)
    except Exception as e:
        messagebox.showerror("API", "Erro:{}".format(e))
    else:
        # Testa se o servidor envia uma resposta válida
        if api_method == "get" and nagios_json.status_code == 200:
            if str(nagios_json.content).find("Invalid API Key") == -1:
                if type_oper == "applied":
                    data_out = nagios_json.json()
                    i = list(dict(data_out).keys())[-1]
                    # Teste pois alguns Nagios retornam o nome da section antes do recordcount
                    if i == available_objects[str(api_selected_object)]:
                        records = int(data_out.get("recordcount"))
                    else:
                        records = int(data_out.get(str(i)).get("recordcount"))
                elif type_oper == "config" and nagios_json.status_code == 200:
                        data_out = list(nagios_json.json())
                        records = len(list(data_out))
                else:
                    records = None
                    data_out = None              
            else:
                messagebox.showerror("API", "API Inválida!!")
                records = None
                data_out = None
        else:
            messagebox.showerror("Conexão", "Erro de conexão!!")
            records = None
            data_out = None
        data_out_lst.append(records)
        data_out_lst.append(data_out)
    return data_out_lst
    
# Faz o post (criação) no Nagios
def post_json(type_oper, api_method, api_url_list, available_objects, api_selected_object):
    try:
        nagios_json = requests.post(api_url_list[0], data=api_url_list[1], verify=False)
    except ConnectionError:
        messagebox.showerror("Conexão", "API Inválida!")
    except MissingSchema:
        messagebox.showerror("Conexão", "Monte a API primeiro!")
    except Exception as e:
        print(e)
        messagebox.showerror("Conexão", "Erro desconhecido!")
    else:
        # Testa se o servidor envia uma resposta válida
        if api_method == "post" and nagios_json.status_code == 200:
            if str(nagios_json.content).find("Invalid API Key") == -1:
                if type_oper == "config" and nagios_json.status_code == 200:
                    return nagios_json.json()
            else:
                messagebox.showerror("API", "API Inválida!!")
        else:
            messagebox.showerror("Conexão", "Erro de conexão!!")
    #return nagios_json.json()

# Faz p put (alteração) no Nagios
def put_json(type_oper, api_method, api_url_list, available_objects, api_selected_object):
    temp_lst = api_url_list[0].split("?")
    temp = str(temp_lst[0])+"/"+str(api_url_list[1]['host_name'])+"?"+str(temp_lst[1])
    api_url_list[1].pop('host_name')

    try:
        nagios_json = requests.put(temp, params=api_url_list[1], verify=False)
    except ConnectionError:
        messagebox.showerror("Conexão", "API Inválida!")
    except MissingSchema:
        messagebox.showerror("Conexão", "Monte a API primeiro!")
    except Exception as e:
        print(e)
        messagebox.showerror("Conexão", "Erro desconhecido!")
    else:
        # Testa se o servidor envia uma resposta válida
        if api_method == "put" and nagios_json.status_code == 200:
            if str(nagios_json.content).find("Invalid API Key") == -1:
                if type_oper == "config" and nagios_json.status_code == 200:
                    return nagios_json.json()
            else:
                messagebox.showerror("API", "API Inválida!!")
        else:
            messagebox.showerror("Conexão", "Erro de conexão!!")
    #return nagios_json.json()

# Remove do Nagios
def delete_json(type_oper, api_method, api_url_list, available_objects, api_selected_object):
    temp_lst = api_url_list[0].split("?")
    temp = str(temp_lst[0])+"/"+str(api_url_list[1]['host_name'])+"?"+str(temp_lst[1])

    try:
        nagios_json = requests.delete(temp, verify=False)       
    except ConnectionError:
        messagebox.showerror("Conexão", "API Inválida!")
    except MissingSchema:
        messagebox.showerror("Conexão", "Monte a API primeiro!")
    except Exception as e:
        print(e)
        messagebox.showerror("Conexão", "Erro desconhecido!")
    else:
        # Testa se o servidor envia uma resposta válida
        if api_method == "delete" and nagios_json.status_code == 200:
            if str(nagios_json.content).find("Invalid API Key") == -1:
                if type_oper == "config" and nagios_json.status_code == 200:
                    return nagios_json.json()
            else:
                messagebox.showerror("API", "API Inválida!!")
        else:
            messagebox.showerror("Conexão", "Erro de conexão!!")
    #return nagios_json.json()

# Remove caracteres indesejados do JSON para salvamento
def format_json(data_in):
    data_out_temp = data_in
    print(len(data_out_temp))
    records = re.search(r"(?<=recordcount\'\:\s\')\d+", data_out_temp)
    print(records)
    data_out_temp = re.sub("(?<!:\s)\"(?!\,)", "", data_out_temp)
    data_out_temp = re.sub("recordcount\':\s\.*?\s\'", "recordcount\': "+records.group()+"\,"+" \"", data_out_temp)
    data_out_temp = re.sub("(?<=long_output\'\:)(.*?)(?=\, \')", " \'removed due to import json problem\'", data_out_temp)
    data_out_temp = re.sub("\{\'", "{\"", data_out_temp)
    data_out_temp = re.sub("\'\}", "\"}", data_out_temp)
    data_out_temp = re.sub("\', \'", "\", \"", data_out_temp)
    data_out_temp = re.sub("\': \'", "\": \"", data_out_temp)
    data_out_temp = re.sub("\':\s", "\": ", data_out_temp)
    data_out_temp = re.sub("\,\s\'", ", \"", data_out_temp)
    data_out_temp = re.sub("\'", "", data_out_temp)

    data_out = str(data_out_temp).replace("'", '"')
    caracter = ["\\"]
    for i in caracter:
        data_out_temp = str(data_out)
        data_out = data_out_temp.replace(i, "")
    return data_out

# Função para coversão do json para csv usando como delimitador o #
def convert_json():
    # data_out_rec teve de ser declarada fora da função e receber o valor via append pois estava se perdendo na recursão
    data_out_rec = []
    # Função recursiva que lê o objeto passado e tem como condição de parada achar um valor tipo lista dentro de um dicionário
    def list_test(dict_object):
        if type(dict_object) is list:
            data_out_rec.append(dict_object)
        elif type(dict_object) is dict:
            for i in dict_object:
                list_test(dict_object[i])
        else:
            pass
        return data_out_rec

    data_out = ""
    temp_file=str(load_file())
    
    try:
        json_temp_formated = format_json(temp_file)
    except Exception as e:
        print("convert_json/format_json: {}".format(e))
    else:
        try:
            json_temp = json.loads(json_temp_formated)
        except Exception as e:
            print("convert_json: {}".format(e))
            return "ERRO"
        else:
            object_type = list(json_temp.keys())[1]
            # Chama a função recusiva que lê o objeto passado
            # Devido ao "append" na função recursiva a resposta está vindo como [[]]
            processed_list = list_test(json_temp[object_type])[0]
            # Pega o primeiro elemento da lista (dict) retorna as keys e converte para uma lista que será a primeira linha do CSV
            keys_obj = list(processed_list[0].keys())
            # Limpeza dos caracteres para a primeira liha do CSV
            caracter = ["{", "}", "[", "]"]
            # Conversão de delimitador ", '" para "#'" que será usado no excel como delimitador
            # Foi feito assim pois alguns valores do json possuem virgula e isto estava desformatando na hora de importar no excel
            data_out_temp = str(keys_obj).replace(", '", "#'")
            data_out_keys = None
            for j in caracter:
                data_out_keys = data_out_temp.replace(j, "")
                data_out_temp = data_out_keys
            # Escrevendo 1a linha da data_out que será gravada em arquivo
            data_out += data_out_keys
            data_out += "\n"
            # Processamento analogo ao da 1a linha do CSV para o corpo do CSV
            for i in range(0, len(processed_list)):
                data_out_temp = str(processed_list[i])
                caracter = ["{", "}", "[", "]"]
                for j in caracter:
                    data_out_body = data_out_temp.replace(j, "")
                    data_out_temp = data_out_body
                # Faço da # o delimitador pois os dados do JSON do Nagios possuem valores que contem vírgulas
                data_out += data_out_temp.replace(", '", "#'", len(keys_obj) - 1)
                data_out += "\n"
            save_file(data_out, "csv")

# Sai do programa
def quit_program(root):
    if messagebox.askyesno("Verificando", "Gostaria mesmo de encerrar?"):
        root.quit()