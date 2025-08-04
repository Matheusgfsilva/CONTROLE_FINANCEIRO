from utils.classificacao import categorize_rev, categorize_exp
from utils.arquivos import db_add, db_confirm, new_db
from utils.verifiers import value_verf, month_verf, type_verf, date_verf
from utils.trans_class import Transaction
import datetime
import re
import json
DB_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/financeiro.json"



def revenue():
    type = "Receita"

    value = str(input("Valor: ").strip())
    value = value_verf(value)

    category = categorize_rev()

    discription = input("Descrição: ")

    date = datetime.date.today().isoformat()

    db_add(type, value, category, discription, date)

def expense():
    type = "Despesa"

    value = input("Valor: ").strip()
    value = value_verf(value)

    categorie = categorize_exp()

    discription = input("Descrição: ").strip().capitalize()
    
    date = datetime.date.today().isoformat()

    db_add(type, value, categorie, discription, date)

def edit_trans(): #aprofundar depois quando tiver beckup de cada dia, e separar melhor por mes
    transactions = db_confirm()
    if transactions is None:
        return
    new_trans = []
    mon_exist = False
    mon_list = []
    month_input = month_verf()
    print("-"*30)
    for trans in transactions:
        month = datetime.datetime.fromisoformat(trans["date"]).month
        if str(month) == month_input:
            mon_exist = True
            mon_list.append(trans)
            print("")
            print(f"[{len(mon_list)}] ", end="")
            print(Transaction(
                trans["type"],
                trans["value"],
                trans["category"],
                trans["discription"],
                trans["date"]
                              ))    
        else:
            new_trans.append(trans)


    if mon_exist == True:
        while True:
            choice = input("Qual o número da transação que deseja editar: ").strip()
            if not choice:
                print("O campo não pode ficar vazio!")
            elif not re.fullmatch(r"[0-9]+", choice):
                print("Digite somente números!")
            elif int(choice) > len(mon_list) or int(choice) < 1:
                print("Digite um dos números mostrados!")
            else:
                break
        
        for i, mon in enumerate(mon_list):
            if i == (int(choice)-1):
                new_type = type_verf()
                new_value = value_verf(input("Digite o novo valor: "))
                new_category = categorize_rev()
                new_discription = input("Digite a nova descrição: ")
                new_date = date_verf()#datetime.datetime.fromisoformat(input("Digite a nova data(YYYY-MM-DD): "))
                mon = Transaction(new_type,new_value,new_category,new_discription,new_date)
                new_trans.append(mon.to_dict())
                print(new_trans)
      
            else:
                new_trans.append(mon)
                print(new_trans) 
        
        new_db(DB_PATH, new_trans)

    elif mon_exist == False:
        print("Não há nenhuma transação registrada nesse mês!", end="")

    print("")
    print("-"*30)

def deleteall():
    transactions = db_confirm()
    if transactions == None:
        return
    confirm = input("Tem certeza que deseja deletar TODAS os transações [S]/[N]?").strip().upper()
    while True:
        if confirm == "S":
            trans_empty = []
            new_db(DB_PATH, trans_empty)
            print("Transações deletadas!")
            break
        elif confirm == "N":
            print("Nenhuma transação deletada!")
            break
        elif not confirm:
            print("O campo não pode ficar vazio!")
        else:
            print("Digite um caractere válido!")
        confirm = input("Tem certeza que deseja deletar TODAS os transações [S]/[N]?").strip().upper()