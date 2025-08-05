from utils.classificacao import categorize_rev, categorize_exp
from utils.arquivos import db_add, db_confirm, new_db
from utils.verifiers import value_verf, month_verf, type_verf, date_verf, value_verf_float
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

def edit_trans(): #aprofundar depois quando tiver beckup de cada dia, e separar melhor por mesv
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
                print("Digite somente números inteiros!")
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

def find_trans():
    transactions = db_confirm()
    if transactions is None:
        return
    cat_list = []
    trans_list = []
    trans_exist = False
    while True:
        choice = input("Como você deseja procurar sua transação? [1]Valor [2]Categoria [3]Data\nDigite: ")
        if not choice:
            print("O campo não pode ficar vazio")
        elif not re.fullmatch(r"[0-9]+", choice):
            print("Digite somente números inteiros!")
        elif (choice != "1") and (choice != "2") and (choice != "3"):
            print("Digite uma das opções dadas(1/2/3)!")
        else:
            break
    if choice == "1":
        while True:
            option = input("Pesquisar por: [1]Valor [2]Intervalo\nDigite: ")
            if not choice:
                print("O campo não pode ficar vazio")
            elif not re.fullmatch(r"[0-9]+", choice):
                print("Digite somente números inteiros!")
            elif (choice != "1") and (choice != "2"):
                print("Digite uma das opções dadas(1/2)!")
            else:
                break
        if option == "1":
            value = value_verf(input("Digite o valor que queira procurar: "))
            print("-" * 30)
            print("")
            for trans in transactions:
                if trans["value"] == value:
                    trans_exist = True
                    print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["discription"],
                            trans["date"]
                                            )) 
                    print("")
            if not trans_exist:
                print("Nenhuma transação encontrada!\n")
            print("-" * 30)  

        elif option == "2":  
            higher = value_verf_float(input("O valor é maior que: "))
            lower = value_verf_float(input("O valor é menor que: "))
            print("-" * 30)  
            print("")
            for trans in transactions:
                trans["value"] = float(str(trans["value"]).replace("R$", "").replace(".", "").replace(",", ".").strip())
                if (trans["value"] > higher) and (trans["value"] < lower):
                    trans_exist = True
                    print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["discription"],
                            trans["date"]
                                            )) 
                    print("")
            if not trans_exist:
                print("Nenhuma transação encontrada!\n")
            print("-" * 30)  

    elif choice == "2": #tem forma melhor de organizar/separar despesa e receita? aperfeicoar organizacao (cronologicamente)
        for trans in transactions:
            if trans["type"] == "Receita":
                if trans["category"] not in cat_list:
                    cat_list.append(trans["category"])
                    print(f"[{len(cat_list)}] ", end="")
                    print(trans["category"])

        for trans in transactions:
            if trans["type"] == "Despesa":
                if trans["category"] not in cat_list:
                    cat_list.append(trans["category"])
                    print(f"[{len(cat_list)}] ", end="")
                    print(trans["category"])
        while True:
            choice = input("De qual categoria você quer ver as transações: ").strip()
            if not choice:
                print("O campo não pode ficar vazio")
            elif not re.fullmatch(r"[0-9]+", choice):
                print("Digite somente números inteiros!")
            elif (int(choice) > len(cat_list)) or (int(choice) <= 0):
                print("Digite uma das opções dadas!")
            else:
                break   
        print("-" * 30)
        print("")
        for i, cat in enumerate(cat_list):
            if i == (int(choice)-1):

                trans_exist = True
                for trans in transactions:
                    if cat == trans["category"]:
                                    print(Transaction(
                                            trans["type"],
                                            trans["value"],
                                            trans["category"],
                                            trans["discription"],
                                            trans["date"]
                                                        ))  
                                    print("") 
        print("-" * 30)
            
    elif choice == "3":
        while True:
            option = input("Pesquisar por: [1]Dia/Mês/Ano [2]Periodo personalizado\nDigite: ").strip()
            if not choice:
                print("O campo não pode ficar vazio")
            elif not re.fullmatch(r"[0-9]+", option):
                print("Digite somente números inteiros!")
            elif (option != "1") and (option != "2"):
                print("Digite uma das opções dadas!")
            else:
                break
        if option == "1":
            while True:
                type = input("[1]Dia [2]Mês [3]Ano\nDigite: ").strip()
                if not choice:
                    print("O campo não pode ficar vazio")
                elif not re.fullmatch(r"[0-9]+", type):
                    print("Digite somente números inteiros!")
                elif (type != "1") and (type != "2") and (type != "3"):
                    print("Digite uma das opções dadas!")
                else:
                    break
            if type == "1":
                day = date_verf(input("Digite o dia específico que quer procurar(YYYY-MM-DD): "))


        elif option == "2":
            print("2")
