from utils.arquivos import db_cat

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



