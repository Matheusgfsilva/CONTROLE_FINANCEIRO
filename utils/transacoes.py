from utils.classificacao import categorize_rev, categorize_exp
from utils.arquivos import db_add, db_confirm, new_db
from utils.verifiers import value_verf, month_verf, type_verf, date_verf, value_verf_float, year_verf, quit
from utils.trans_class import Transaction
import datetime
import re
import json
DB_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/financeiro.json"




def revenue():
    type = "Receita"

    value = value_verf(str(input("Valor: ").strip()))
    if quit(value):
        return

    category = categorize_rev()
    if quit(category):
        return

    description = input("Descrição: ")
    if quit(description):
        return

    date = datetime.date.today().isoformat()

    db_add(type, value, category, description, date)

def expense():
    type = "Despesa"

    value = value_verf(input("Valor: ").strip())
    if quit(value):
        return

    category = categorize_exp()
    if quit(category):
        return

    description = input("Descrição: ").strip().capitalize()
    if quit(description):
        return
    
    date = datetime.date.today().isoformat()

    db_add(type, value, category, description, date)

def edit_trans(): #aprofundar depois quando tiver beckup de cada dia, e separar melhor por mesv
    transactions = db_confirm()
    if transactions is None:
        return
    

    while True:
        choice = input("Como você deseja procurar sua transação? [1]Valor [2]Categoria [3]Data\nDigite: ")
        if quit(choice):
            return
        if not choice:
            print("O campo não pode ficar vazio")
        elif not re.fullmatch(r"[0-9]+", choice):
            print("Digite somente números naturais!")
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
                print("Digite somente números naturais!")
            elif (choice != "1") and (choice != "2"):
                print("Digite uma das opções dadas(1/2)!")
            else:
                break
        if option == "1":
            value = value_verf(input("Digite o valor que queira procurar: "))
            if quit(value):
                return
            print("-" * 30)
            print("")
            for trans in transactions:
                if trans["value"] == value:
                    trans_exist = True
                    print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                                            )) 
                    print("")
            if not trans_exist:
                print("Nenhuma transação encontrada!\n")
            print("-" * 30)  

        elif option == "2":  
            higher = value_verf_float(input("O valor é maior que: "))
            if quit(higher):
                return
            lower = value_verf_float(input("O valor é menor que: "))
            if quit(lower):
                return
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
                            trans["description"],
                            trans["date"]
                                            )) 
                    print("")
            if not trans_exist:
                print("Nenhuma transação encontrada!\n")
            print("-" * 30)  

    elif choice == "2": #tem forma melhor de organizar/separar despesa e receita? aperfeicoar organizacao (cronologicamente)
        while True:
            cat_list = []
            trans_list = []
            new_trans = []
            trans_exist = False
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
                if quit(choice):
                    return
                if not choice:
                    print("O campo não pode ficar vazio")
                elif not re.fullmatch(r"[0-9]+", choice):
                    print("Digite somente números naturais!")
                elif (int(choice) > len(cat_list)) or (int(choice) <= 0):
                    print("Digite uma das opções dadas!")
                else:
                    break   
            print("-" * 30)
            print("")
            for i, cat in enumerate(cat_list):
                if i == (int(choice)-1):
                    for trans in transactions:
                        if trans["category"] == cat:
                            trans_list.append(trans)
                            trans_exist = True
                            print(f"[{len(trans_list)}] ", end="")
                            print(Transaction(
                                    trans["type"],
                                    trans["value"],
                                    trans["category"],
                                    trans["description"],
                                    trans["date"]
                                                ))  
                            print("") 

            print("-" * 30)
            if trans_exist == True:
                    while True:  
                        choice = input("Qual o número da transação que deseja editar: ").strip()
                        if quit(choice):
                            return
                        if not choice:
                            print("O campo não pode ficar vazio!")
                        elif not re.fullmatch(r"[0-9]+", choice):
                            print("Digite somente números naturais!")
                        elif int(choice) > len(trans_list) or int(choice) < 1:
                            print("Digite um dos números mostrados!")
                        else:
                            break
                    
                    for i, trans in enumerate(trans_list):
                        if i == (int(choice)-1):
                            print("-" * 30)
                            print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                                        ))
                            print("-" * 30)
                    
                    while True:
                        confimation = input("Essa é a transação que você deseja editar[S/N]? ").strip().upper()
                        if quit(confimation):
                            return
                        if not confimation:
                            print("O campo não pode ficar vazio!")
                        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                            print("Digite somente letras!")
                        elif not (confimation == "S" or confimation == "N"):
                            print("Digite uma das opções dadas(S/N)")
                        else:
                            break
                    if confimation == "S":
                        break
                    elif confimation == "N":
                        continue


            new_type = type_verf()
            if quit(new_type):
                return
            new_value = value_verf(input("Digite o novo valor: "))
            if quit(new_value):
                return
            if new_type == "Receita":
                new_category = categorize_rev()
                if quit(new_category):
                    return
            elif new_type == "Despesa":
                new_category = categorize_exp()
                if quit(new_category):
                    return
                new_description = input("Digite a nova descrição: ")
                if quit(new_description):
                    return
                new_date = date_verf(input("Digite a nova data: "))#datetime.datetime.fromisoformat(input("Digite a nova data(YYYY-MM-DD): "))
                if quit(new_date):
                    return
                trans = Transaction(new_type,new_value,new_category,new_description,new_date)
                new_trans.append(trans.to_dict())
                
            else:
                new_trans.append(trans)  
            
            new_db(DB_PATH, new_trans)
                 
    elif choice == "3":
        while True:
            option = input("Pesquisar por: [1]Dia/Mês/Ano [2]Periodo personalizado\nDigite: ").strip()
            if not choice:
                print("O campo não pode ficar vazio")
            elif not re.fullmatch(r"[0-9]+", option):
                print("Digite somente números naturais!")
            elif (option != "1") and (option != "2"):
                print("Digite uma das opções dadas!")
            else:
                break
        if option == "1":
            while True:
                type = input("[1]Dia [2]Mês [3]Ano\nDigite: ").strip()
                if quit(type):
                    return
                if not choice:
                    print("O campo não pode ficar vazio")
                elif not re.fullmatch(r"[0-9]+", type):
                    print("Digite somente números naturais!")
                elif (type != "1") and (type != "2") and (type != "3"):
                    print("Digite uma das opções dadas!")
                else:
                    break
        if type == "1":
            while True:
                trans_exist = False
                trans_list = []
                new_trans = []
                day = date_verf(input("Digite o dia específico que quer procurar(YYYY-MM-DD): "))
                if quit(day):
                    return
                print("-" * 30)
                print("")
                for trans in transactions:
                    if trans["date"] == day:
                        trans_list.append(trans)
                        trans_exist = True
                        print(f"[{len(trans_list)}] ", end="")
                        print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                                            ))  
                        print("") 
                    
                    else:
                        new_trans.append(trans)
                if not trans_exist:
                    print("Nenhuma transação encontrada\n")
                print("-" * 30)

                if not trans_exist:
                    continue
                
                if trans_exist == True:
                    while True:  
                        choice = input("Qual o número da transação que deseja editar: ").strip()
                        if quit(choice):
                            return
                        if not choice:
                            print("O campo não pode ficar vazio!")
                        elif not re.fullmatch(r"[0-9]+", choice):
                            print("Digite somente números naturais!")
                        elif int(choice) > len(trans_list) or int(choice) < 1:
                            print("Digite um dos números mostrados!")
                        else:
                            break
                    
                    for i, trans in enumerate(trans_list):
                        if i == (int(choice)-1):
                            print("-" * 30)
                            print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                                        ))
                            print("-" * 30)
                    
                        else:
                            new_trans.append(trans)

                    while True:
                        confimation = input("Essa é a transação que você deseja editar[S/N]? ").strip().upper()
                        if quit(confimation):
                            return
                        if not confimation:
                            print("O campo não pode ficar vazio!")
                        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                            print("Digite somente letras!")
                        elif not (confimation == "S" or confimation == "N"):
                            print("Digite uma das opções dadas(S/N)")
                        else:
                            break
                    if confimation == "S":
                        break
                    elif confimation == "N":
                        continue


            new_type = type_verf()
            if quit(new_type):
                return
            new_value = value_verf(input("Digite o novo valor: "))
            if quit(new_value):
                return
            if new_type == "Receita":
                new_category = categorize_rev()
                if quit(new_category):
                    return
            elif new_type == "Despesa":
                new_category = categorize_exp()
                if quit(new_category):
                    return
            new_description = input("Digite a nova descrição: ")
            if quit(new_description):
                return
            new_date = date_verf(input("Digite a nova data: "))#datetime.datetime.fromisoformat(input("Digite a nova data(YYYY-MM-DD): "))
            if quit(new_date):
                return
            trans = Transaction(new_type,new_value,new_category,new_description,new_date)
            new_trans.append(trans.to_dict())
            
            new_db(DB_PATH, new_trans)

        elif type == "2":
            while True:
                trans_exist = False
                year_exist = False
                new_trans = []
                trans_list = []
                choice_year = year_verf(input("Digite o ano que você quer ver os meses: ").strip())
                if quit(choice_year):
                    return
                choice_mon = month_verf(input("Digite o mês que você quer ver: ").lstrip("0"))
                if quit(choice_mon):
                    return
                
                print("-" * 30)
                print("")
                for trans in transactions:
                    year = datetime.datetime.fromisoformat(trans["date"]).year
                    if str(choice_year) == str(year):
                        year_exist = True
                        month = datetime.datetime.fromisoformat(trans["date"]).month
                        if str(choice_mon) == str(month):
                            trans_exist = True
                            trans_list.append(trans)
                            print(f"[{len(trans_list)}] ", end="")
                            print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                                            ))  
                            print("") 
                        else:
                            new_trans.append(trans)
                    else:
                        new_trans.append(trans)

                if not year_exist:
                    print("Nenhuma transação encontrada!\n")

                else:
                    if not trans_exist:
                        print("Nenhuma transação encontrada!\n")

                print("-" * 30)
                if not trans_exist:
                    continue

                if not year_exist:
                    continue


                if trans_exist == True:
                    while True:  
                        choice = input("Qual o número da transação que deseja editar: ").strip()
                        if quit(choice):
                            return
                        if not choice:
                            print("O campo não pode ficar vazio!")
                        elif not re.fullmatch(r"[0-9]+", choice):
                            print("Digite somente números naturais!")
                        elif int(choice) > len(trans_list) or int(choice) < 1:
                            print("Digite um dos números mostrados!")
                        else:
                            break
                    
                    for i, trans in enumerate(trans_list):
                        if i == (int(choice)-1):
                            print("-" * 30)
                            print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                                        ))
                            print("-" * 30)

                        else:
                            new_trans.append(trans)

                    while True:
                        confimation = input("Essa é a transação que você deseja editar[S/N]? ").strip().upper()
                        if quit(confimation):
                            return
                        if not confimation:
                            print("O campo não pode ficar vazio!")
                        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                            print("Digite somente letras!")
                        elif not (confimation == "S" or confimation == "N"):
                            print("Digite uma das opções dadas(S/N)")
                        else:
                            break
                    if confimation == "S":
                        break
                    elif confimation == "N":
                        continue


            new_type = type_verf()
            if quit(new_type):
                return
            new_value = value_verf(input("Digite o novo valor: "))
            if quit(new_value):
                return
            if new_type == "Receita":
                new_category = categorize_rev()
                if quit(new_category):
                    return
            elif new_type == "Despesa":
                new_category = categorize_exp()
                if quit(new_category):
                    return
            new_description = input("Digite a nova descrição: ")
            if quit(new_description):
                return
            new_date = date_verf(input("Digite a nova data: "))#datetime.datetime.fromisoformat(input("Digite a nova data(YYYY-MM-DD): "))
            if quit(new_date):
                return
            trans = Transaction(new_type,new_value,new_category,new_description,new_date)
            new_trans.append(trans.to_dict())
              
            
            new_db(DB_PATH, new_trans)

        elif type == "3":
            while True:
                trans_exist = False
                trans_list = []
                new_trans = []
                choice_year = year_verf(input("Digite o ano que você quer ver as transações: ").strip())
                print("-" * 30)
                print("")
                for trans in transactions:
                    year = datetime.datetime.fromisoformat(trans["date"]).year
                    if str(choice_year) == str(year):
                        trans_list.append(trans)
                        trans_exist = True
                        print(f"[{len(trans_list)}] ", end="")
                        print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                                        ))  
                        print("") 

                    else:
                        new_trans.append(trans)
                
                if not trans_exist:
                    print("Nenhuma transação encontrada!\n")
                print("-" * 30)
                if not trans_exist:
                    continue


                if trans_exist == True:
                        while True:  
                            choice = input("Qual o número da transação que deseja editar: ").strip()
                            if quit(choice):
                                return
                            if not choice:
                                print("O campo não pode ficar vazio!")
                            elif not re.fullmatch(r"[0-9]+", choice):
                                print("Digite somente números naturais!")
                            elif int(choice) > len(trans_list) or int(choice) < 1:
                                print("Digite um dos números mostrados!")
                            else:
                                break
                        
                        for i, trans in enumerate(trans_list):
                            if i == (int(choice)-1):
                                print("-" * 30)
                                print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                                            ))
                                print("-" * 30)
                            else:
                                new_trans.append(trans)
                        
                        while True:
                            confimation = input("Essa é a transação que você deseja editar[S/N]? ").strip().upper()
                            if quit(confimation):
                                return
                            if not confimation:
                                print("O campo não pode ficar vazio!")
                            elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                                print("Digite somente letras!")
                            elif not (confimation == "S" or confimation == "N"):
                                print("Digite uma das opções dadas(S/N)")
                            else:
                                break
                        if confimation == "S":
                            break
                        elif confimation == "N":
                            continue


            new_type = type_verf()
            if quit(new_type):
                return
            new_value = value_verf(input("Digite o novo valor: "))
            if quit(new_value):
                return
            if new_type == "Receita":
                new_category = categorize_rev()
                if quit(new_category):
                    return
            elif new_type == "Despesa":
                new_category = categorize_exp()
                if quit(new_category):
                    return
            new_description = input("Digite a nova descrição: ")
            if quit(new_description):
                return
            new_date = date_verf(input("Digite a nova data: "))#datetime.datetime.fromisoformat(input("Digite a nova data(YYYY-MM-DD): "))
            if quit(new_date):
                return
            trans = Transaction(new_type,new_value,new_category,new_description,new_date)
            new_trans.append(trans.to_dict())  
            
            new_db(DB_PATH, new_trans)

def deleteall():
    transactions = db_confirm()
    if transactions == None:
        return
    
    while True:
        confirm = input("Tem certeza que deseja deletar TODAS os transações [S]/[N]?").strip().upper()
        if quit(confirm):
            return
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
       
def find_trans():
    transactions = db_confirm()
    if transactions is None:
        return
    cat_list = []
    trans_exist = False
    year_exist = False
    while True:
        choice = input("Como você deseja procurar sua transação? [1]Valor [2]Categoria [3]Data\nDigite: ")
        if quit(choice):
            return
        if not choice:
            print("O campo não pode ficar vazio")
        elif not re.fullmatch(r"[0-9]+", choice):
            print("Digite somente números naturais!")
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
                print("Digite somente números naturais!")
            elif (choice != "1") and (choice != "2"):
                print("Digite uma das opções dadas(1/2)!")
            else:
                break
        if option == "1":
            while True:
                value = value_verf(input("Digite o valor que queira procurar: "))
                if quit(value):
                    return
                print("-" * 30)
                print("")
                for trans in transactions:
                    if trans["value"] == value:
                        trans_exist = True
                        print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                                                )) 
                        print("")
                if not trans_exist:
                    print("Nenhuma transação encontrada!\n")
                print("-" * 30)  
                if trans_exist:
                    break

        elif option == "2":  
            while True:
                higher = value_verf_float(input("O valor é maior que: "))
                if quit(higher):
                    return
                lower = value_verf_float(input("O valor é menor que: "))
                if quit(lower):
                    return
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
                                trans["description"],
                                trans["date"]
                                                )) 
                        print("")

                if not trans_exist:
                    print("Nenhuma transação encontrada!\n")
                print("-" * 30)  
                if trans_exist:
                    break

    elif choice == "2": #tem forma melhor de organizar/separar despesa e receita? aperfeicoar organizacao (cronologicamente)
        while True:
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
                if quit(choice):
                    return
                if not choice:
                    print("O campo não pode ficar vazio")
                elif not re.fullmatch(r"[0-9]+", choice):
                    print("Digite somente números naturais!")
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
                                                trans["description"],
                                                trans["date"]
                                                            ))  
                                        print("") 
                    
            if not trans_exist:
                print("Nenhuma transação encontrada!\n")
            print("-" * 30)
            if trans_exist:
                break
            
    elif choice == "3":
        while True:
            option = input("Pesquisar por: [1]Dia/Mês/Ano [2]Periodo personalizado\nDigite: ").strip()
            if not choice:
                print("O campo não pode ficar vazio")
            elif not re.fullmatch(r"[0-9]+", option):
                print("Digite somente números naturais!")
            elif (option != "1") and (option != "2"):
                print("Digite uma das opções dadas!")
            else:
                break
        if option == "1":
            while True:
                type = input("[1]Dia [2]Mês [3]Ano\nDigite: ").strip()
                if quit(type):
                    return
                if not choice:
                    print("O campo não pode ficar vazio")
                elif not re.fullmatch(r"[0-9]+", type):
                    print("Digite somente números naturais!")
                elif (type != "1") and (type != "2") and (type != "3"):
                    print("Digite uma das opções dadas!")
                else:
                    break
            if type == "1":
                while True:
                    day = date_verf(input("Digite o dia específico que quer procurar(YYYY-MM-DD): "))
                    if quit(day):
                        return
                    print("-" * 30)
                    print("")
                    for trans in transactions:
                        if trans["date"] == day:
                            trans_exist = True
                            print(Transaction(
                                    trans["type"],
                                    trans["value"],
                                    trans["category"],
                                    trans["description"],
                                    trans["date"]
                                                ))  
                            print("") 
                    if not trans_exist:
                        print("Nenhuma transação encontrada!\n")
                    print("-" * 30)
                    if trans_exist:
                        break

            elif type == "2":
                while True:
                    choice_year = year_verf(input("Digite o ano que você quer ver os meses: ").strip())
                    choice_mon = month_verf(input("Digite o mês que você quer ver: ").lstrip("0"))
                    
                    print("-" * 30)
                    print("")
                    for trans in transactions:
                        year = datetime.datetime.fromisoformat(trans["date"]).year
                        if str(choice_year) == str(year):
                            year_exist = True
                            month = datetime.datetime.fromisoformat(trans["date"]).month
                            if str(choice_mon) == (str(month)):
                                trans_exist = True
                                print(Transaction(
                                    trans["type"],
                                    trans["value"],
                                    trans["category"],
                                    trans["description"],
                                    trans["date"]
                                                ))  
                                print("") 

                    if not year_exist:
                        print("Nenhuma transação encontrada!\n")

                    else:
                        if not trans_exist:
                            print("Nenhuma transação encontrada!\n")
                    print("-" * 30)
                    if trans_exist:
                        break
            elif type == "3":
                while True:
                    choice_year = year_verf(input("Digite o ano que você quer ver as transações: ").strip())
                    print("-" * 30)
                    print("")
                    for trans in transactions:
                            year = datetime.datetime.fromisoformat(trans["date"]).year
                            if str(choice_year) == str(year):
                                trans_exist = True
                                print(Transaction(
                                    trans["type"],
                                    trans["value"],
                                    trans["category"],
                                    trans["description"],
                                    trans["date"]
                                                ))  
                                print("") 
                    if not trans_exist:
                        print("Nenhuma transação encontrada!\n")
                    print("-" * 30)
                    if trans_exist:
                        break

