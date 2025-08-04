from utils.arquivos import db_cat_rev,db_cat_exp, new_db
import re
EXP_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/cat_exp.json"
REV_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/cat_rev.json"

def categorize_rev():
    #LISTA DE CATEGORIAS
    categories = db_cat_rev()
    if categories is None:
        return
    
    for i, category in enumerate(categories, 1):
        print(f"[{i}] {category}")

    #ESCOLHA DE CATEGORIAS  
    choice = str(input("Digite: ")).strip()
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
    for i, category in enumerate(categories):
        if choice == str(i+1):
            return(category)

def edit_cat():
    categories_rev = db_cat_rev()
    if categories_rev is None:
        return
    categories_exp = db_cat_exp()
    if categories_exp is None:
        return

    edited_cat = []
    while True:
        choice = input("Você deseja DELETAR(1) ou CRIAR(2) uma categoria: ").strip()
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
            if not choice:
                print("O campo não pode ficar vazio!")
            elif not re.fullmatch(r"[1-9]+", choice):
                print("Digite somente números!")
            elif choice != "1" and choice != "2":
                print("Escolha entre o número 1 e 2!")
            else:
                break

        if trans_type == "1":
            for i, category in enumerate(categories_rev, 1):
                print(f"[{i}] {category}")

            del_cat = input("Digite a categoria que quer deletar: ")
            for i, category in enumerate(categories_rev):
                if del_cat != str(i+1):
                    edited_cat.append(category)
                    print(edited_cat)
            new_db(REV_PATH, edited_cat)
            return
        
        if trans_type == "2":
            for i, category in enumerate(categories_exp, 1):
                print(f"[{i}] {category}")

            del_cat = input("Digite a categoria que quer deletar: ")
            for i, category in enumerate(categories_exp):
                if del_cat != str(i+1):
                    edited_cat.append(category)
            new_db(EXP_PATH, edited_cat)
            return

    elif choice == "2":
        print("2")
        
    


