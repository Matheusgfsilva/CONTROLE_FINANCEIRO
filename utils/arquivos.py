import os
import json
from utils.trans_class import Transaction

DB_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/financeiro.json"
EXP_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/cat_exp.json"
REV_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/cat_rev.json"

def db_confirm():
    #verifica se o arquivo existe
    if not os.path.exists(DB_PATH):
        print("\n]NÃO ENCONTREI BASE DE DADOS")
        return None
    
    #abre e carrega os dados
    with open(DB_PATH, "r") as file: #"r" é de read, ou seja, nao esta modificando nada
        try:
            transacions = json.load(file)
        except json.JSONDecodeError:
            print("\nERRO AO LER O ARQUIVO")
            return None
    
    #verifica se há clientes
    if not transacions:
        print("Nenhuma transação cadastrada!")
        return None
    
    return transacions

def db_add(type,value,category,description,date):
    #verifica se o aquivo existe, se nao cria uma lista vazia
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as file:
            try:
                transacions = json.load(file)
            except json.JSONDecodeError:
                transacions = []
    else:
        transacions = []

#adicionar o novo cliente
    new_trans = Transaction(type,value,category,description,date)
    transacions.append(new_trans.to_dict())
    print(f"\n{new_trans}")
#salva de volta no arquivo
    new_db(DB_PATH, transacions)

def db_cat_exp():
        #verifica se o arquivo existe
    if not os.path.exists(EXP_PATH):
        print("\n]NÃO ENCONTREI BASE DE DADOS")
        return None
    
    #abre e carrega os dados
    with open(EXP_PATH, "r") as file: #"r" é de read, ou seja, nao esta modificando nada
        try:
            categories = json.load(file)
        except json.JSONDecodeError:
            print("\nERRO AO LER O ARQUIVO")
            return None
    
    #verifica se há clientes
    if not categories:
        print("Nenhuma categoria cadastrada!")
        return None
    
    return categories

def db_cat_rev():
        #verifica se o arquivo existe
    if not os.path.exists(REV_PATH):
        print("\n]NÃO ENCONTREI BASE DE DADOS")
        return None
    
    #abre e carrega os dados
    with open(REV_PATH, "r") as file: #"r" é de read, ou seja, nao esta modificando nada
        try:
            categories = json.load(file)
        except json.JSONDecodeError:
            print("\nERRO AO LER O ARQUIVO")
            return None
    
    #verifica se há clientes
    if not categories:
        print("Nenhuma categoria cadastrada!")
        return None
    
    return categories

def new_db(path, list):

    with open(path, "w") as file: #"w" de write, voce esta apagando o conteudo anterior
        json.dump(list, file, indent=5) #passando a lista nova para o json