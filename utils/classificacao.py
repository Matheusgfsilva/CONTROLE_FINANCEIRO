from utils.arquivos import db_cat
import re

def categorize_rev():
    #LISTA DE CATEGORIAS
    categories = db_cat()
    if categories is None:
        return
    
    default = categories["padrao_receita"]
    new_cat = categories["nova_receita"]
    edit = categories["editar"]
    all_cat = default + new_cat + edit
    for i, category in enumerate(all_cat, 1):
        print(f"[{i}] {category}")

    #ESCOLHA DE CATEGORIAS  
    choice = str(input("Digite: ")).strip()
    for i, category in enumerate(all_cat):
        if int(choice) == len(all_cat):
            print("editando visse")
        elif choice == str(i+1):
            return(category)
        

def categorize_exp():
    #LISTA DE CATEGORIAS
    categories = db_cat()
    if categories is None:
        return
    
    default = categories["padrao_despesa"]
    new_cat = categories["nova_despesa"]
    edit = categories["editar"]
    all_cat = default + new_cat + edit
    for i, category in enumerate(all_cat, 1):
        print(f"[{i}] {category}")

    #ESCOLHA DE CATEGORIAS  
    choice = str(input("Digite: ")).strip()
    for i, category in enumerate(all_cat):
        if int(choice) == len(all_cat):
            print("editando visse")
        elif choice == str(i+1):
            return(category)

def edit_cat():
    categories = db_cat()
    if categories is None:
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
            default = categories["padrao_receita"]
            new_cat = categories["nova_receita"]
            all_cat = default + new_cat
            for i, category in enumerate(all_cat, 1):
                print(f"[{i}] {category}")

            del_cat = input("Digite a categoria que quer deletar: ")
            for i, category in enumerate(all_cat):
                if del_cat != str(i+1):
                    edited_cat.append(category)

        if trans_type == "2":
            default = categories["padrao_despesa"]
            new_cat = categories["nova_despesa"]
            all_cat = default + new_cat
            for i, category in enumerate(all_cat, 1):
                print(f"[{i}] {category}")

            del_cat = input("Digite a categoria que quer deletar: ")
            for i, category in enumerate(all_cat):
                if del_cat != str(i+1):
                    edited_cat.append(category)


    elif choice == "2":
        print("2")
        
    


