import os
import json
from utils.trans_class import Transaction

DB_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/financeiro.json"
CAT_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/categorias.json"

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

def db_add(type,value,category,discription,date):
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
    new_trans = Transaction(type,value,category,discription,date)
    transacions.append(new_trans.to_dict())
    print(f"\n{new_trans}")
#salva de volta no arquivo
    with open(DB_PATH, "w") as file:
        json.dump(transacions, file, indent=5)

def db_cat():
        #verifica se o arquivo existe
    if not os.path.exists(CAT_PATH):
        print("\n]NÃO ENCONTREI BASE DE DADOS")
        return None
    
    #abre e carrega os dados
    with open(CAT_PATH, "r") as file: #"r" é de read, ou seja, nao esta modificando nada
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