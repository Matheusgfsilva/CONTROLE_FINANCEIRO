from utils.arquivos import db_cat_rev,db_cat_exp, new_db, db_confirm
from utils.verifiers import quit
import re
EXP_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/cat_exp.json"
REV_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/cat_rev.json"
DB_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/financeiro.json"

def categorize_rev():
    #LISTA DE CATEGORIAS
    categories = db_cat_rev()
    if categories is None:
        return
    
    for i, category in enumerate(categories, 1):
        print(f"[{i}] {category}")

    #ESCOLHA DE CATEGORIAS  
    choice = str(input("Digite: ")).strip()
    if choice == "-1":
        return choice
    for i, category in enumerate(categories):
        if choice == str(i+1):
            return(category)
        
def categorize_exp():
    #LISTA DE CATEGORIAS
    categories = db_cat_exp()
    if categories is None:
        return
    
    for i, category in enumerate(categories, 1):
        print(f"[{i}] {category}")

    #ESCOLHA DE CATEGORIAS  
    choice = str(input("Digite: ")).strip()
    if choice == "-1":
            return choice
    for i, category in enumerate(categories):
        if choice == str(i+1):
            return(category)

def edit_cat():
    categories_rev_Wother = db_cat_rev()
    if categories_rev_Wother is None:
        return
    categories_rev = []
    for category in categories_rev_Wother:
        if category != "Outros":
            categories_rev.append(category)

    
    categories_exp_Wother = db_cat_exp()
    if categories_exp_Wother is None:
        return
    categories_exp = []
    for category in categories_exp_Wother:
        if category != "Outros":
            categories_exp.append(category)
        

    transactions = db_confirm()
    if transactions is None:
        return

    edited_cat = []
    while True:
        choice = input("Você deseja DELETAR(1) ou CRIAR(2) uma categoria: ").strip()
        if quit(choice):
            return
        if not choice:
            print("O campo não pode ficar vazio!")
        elif not re.fullmatch(r"[1-9]+", choice):
            print("Digite somente números!")
        elif choice != "1" and choice != "2":
            print("Escolha entre o número 1 e 2!")
        else:
            break
    if choice == "1":
        while True:
            trans_type = input("Você quer deletar uma categoria de RECEITA(1) ou DESPESA(2): ").strip()
            if quit(trans_type):
                return
            if not trans_type:
                print("O campo não pode ficar vazio!")
            elif not re.fullmatch(r"[1-9]+", trans_type):
                print("Digite somente números!")
            elif trans_type != "1" and trans_type != "2":
                print("Escolha entre o número 1 e 2!")
            else:
                break
    

        if trans_type == "1":
            while True:
                replay = False
                confirm = False
                edited_cat = []
                new_trans = []
                for i, category in enumerate(categories_rev, 1):
                    print(f"[{i}] {category}")
                while True:
                    del_cat = input("Digite o número da categoria que quer deletar: ")
                    if quit(del_cat):
                        return
                    if not choice:
                        print("O campo não pode ficar vazio!")
                    elif not re.fullmatch(r"[0-9]+", del_cat):
                        print("Digite somente números naturais!")
                    elif int(del_cat) > len(categories_rev) or int(del_cat) < 1:
                        print("Digite um dos números mostrados!")
                    else:
                        break
                for i, category in enumerate(categories_rev):
                    if replay:
                        continue

                    if del_cat == str(i+1):
                        for trans in transactions:
                            if replay:
                                continue
                            if trans["category"] == category:
                                final_cat = category
                                while True:
                                    choice = input("Existem transações com essa categoria, deseja apagar mesmo assim[S/N]? ").strip().upper()
                                    if quit(choice):
                                        return
                                    if not choice:
                                        print("O campo não pode ficar vazio!")
                                    elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", choice):
                                        print("Digite somente letras!")
                                    elif not (choice == "S" or choice == "N"):
                                        print("Digite uma das opções dadas(S/N)")
                                    else:
                                        break
                                if choice == "N":
                                    replay = True
                                    continue
                                if choice == "S":
                                    confirm = True
                                    for trans in transactions:
                                        if trans["category"] == category:  
                                            trans["category"] = "Outros" 
                                            new_trans.append(trans)
                                        else:
                                            new_trans.append(trans)
                                                                    
                    else:
                        edited_cat.append(category)
                if confirm:
                    print(f"A categoria \"{final_cat}\" foi deletada!(Foi substituida por \"Outros\" nas transações que usavam-a)")
                    edited_cat.append("Outros")
                    new_db(REV_PATH, edited_cat)
                    new_db(DB_PATH, new_trans)
                    return
        
        elif trans_type == "2":
            while True:
                replay = False
                confirm = False
                edited_cat = []
                new_trans = []
                for i, category in enumerate(categories_exp, 1):
                    print(f"[{i}] {category}")
                while True:
                    del_cat = input("Digite o número da categoria que quer deletar: ")
                    if quit(del_cat):
                        return
                    if not choice:
                        print("O campo não pode ficar vazio!")
                    elif not re.fullmatch(r"[0-9]+", del_cat):
                        print("Digite somente números naturais!")
                    elif int(del_cat) > len(categories_exp) or int(del_cat) < 1:
                        print("Digite um dos números mostrados!")
                    else:
                        break
                for i, category in enumerate(categories_exp):
                    if replay:
                        continue

                    if del_cat == str(i+1):
                        for trans in transactions:
                            if replay:
                                continue
                            if trans["category"] == category:
                                final_cat = category
                                while True:
                                    choice = input("Existem transações com essa categoria, deseja apagar mesmo assim[S/N]? ").strip().upper()
                                    if quit(choice):
                                        return
                                    if not choice:
                                        print("O campo não pode ficar vazio!")
                                    elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", choice):
                                        print("Digite somente letras!")
                                    elif not (choice == "S" or choice == "N"):
                                        print("Digite uma das opções dadas(S/N)")
                                    else:
                                        break
                                if choice == "N":
                                    replay = True
                                    continue
                                if choice == "S":
                                    confirm = True
                                    for trans in transactions:
                                        if trans["category"] == category:  
                                            trans["category"] = "Outros" 
                                            new_trans.append(trans)
                                        else:
                                            new_trans.append(trans)
                                                                    
                    else:
                        edited_cat.append(category)
                if confirm:
                    print(f"A categoria \"{final_cat}\" foi deletada!(Foi substituida por \"Outros\" nas transações que usavam-a)")
                    edited_cat.append("Outros")
                    new_db(EXP_PATH, edited_cat)
                    new_db(DB_PATH, new_trans)
                    return
        else:
            print("Digite uma das opções(1 ou 2)!")

    elif choice == "2":
        while True:
            trans_type = input("Você quer adicionar uma categoria de RECEITA(1) ou DESPESA(2): ").strip()
            if quit(trans_type):
                return
            if not trans_type:
                print("O campo não pode ficar vazio!")
            elif not re.fullmatch(r"[1-9]+", trans_type):
                print("Digite somente números!")
            elif trans_type != "1" and trans_type != "2":
                print("Escolha entre o número 1 e 2!")
            else:
                break
        if trans_type == "1":
            for category in categories_rev:
                edited_cat.append(category)
            while True:
                new_cat = input("Digite o nome da nova categoria que você deseja: ").strip()
                if quit(new_cat):
                    return
                if not new_cat:
                    print("O campo não pode ficar vazio!")
                elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", new_cat):
                    print("Digite somente letras!")
                else:
                    break 
            edited_cat.append(new_cat)
            new_db(REV_PATH,edited_cat)
            
        elif trans_type == "2":
            for category in categories_exp:
                edited_cat.append(category)
            while True:
                new_cat = input("Digite o nome da nova categoria que você deseja: ").strip()
                if quit(new_cat):
                    return
                if not new_cat:
                    print("O campo não pode ficar vazio!")
                elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", new_cat):
                    print("Digite somente letras!")
                else:
                    break 
            edited_cat.append(new_cat)
            new_db(EXP_PATH,edited_cat)
    

    


