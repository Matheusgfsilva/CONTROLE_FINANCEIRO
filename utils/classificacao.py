from utils.arquivos import db_cat_rev,db_cat_exp, new_db, db_confirm
from utils.verifiers import quit
import re
from utils.ui import HEADER, RULE, ASK, OK, ERROR, WARN, INFO
from utils.verifiers import _cancelled

# Helpers de normalização e checagem de duplicidade de nomes de categoria
import re as _re
EXP_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/cat_exp.json"
REV_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/cat_rev.json"
DB_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/financeiro.json"

def _normalize_cat_name(s: str) -> str:
    # Colapsa espaços, tira espaços extras e mantém seu padrão visual (capitalize)
    s = _re.sub(r"\s+", " ", str(s).strip())
    return s.capitalize()

def _exists_casefold(seq, name: str, except_name: str | None = None) -> bool:
    target = _normalize_cat_name(name)
    exc = _normalize_cat_name(except_name) if except_name else None
    for item in seq:
        norm = _normalize_cat_name(item)
        if exc and norm == exc:  # ignora o próprio nome quando estiver editando
            continue
        if norm.casefold() == target.casefold():
            return True
    return False

def categorize_rev():
    #LISTA DE CATEGORIAS
    categories = db_cat_rev()
    if categories is None:
        return
    HEADER("CATEGORIAS DE RECEITA")
    for i, category in enumerate(categories, 1):
        INFO(f"[{i}] {category}")
    RULE()

    # ESCOLHA DE CATEGORIAS (robusta)
    while True:
        choice = ASK("DIGITE O NÚMERO DA CATEGORIA:")
        if quit(choice):
            return choice
        if not choice:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            continue
        if not re.fullmatch(r"[0-9]+", choice):
            ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
            continue
        idx = int(choice)
        if not (1 <= idx <= len(categories)):
            ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
            continue
        return categories[idx - 1]
        
def categorize_exp():
    #LISTA DE CATEGORIAS
    categories = db_cat_exp()
    if categories is None:
        return
    HEADER("CATEGORIAS DE DESPESA")
    for i, category in enumerate(categories, 1):
        INFO(f"[{i}] {category}")
    RULE()

    # ESCOLHA DE CATEGORIAS (robusta)
    while True:
        choice = ASK("DIGITE O NÚMERO DA CATEGORIA:")
        if quit(choice):
            return choice
        if not choice:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            continue
        if not re.fullmatch(r"[0-9]+", choice):
            ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
            continue
        idx = int(choice)
        if not (1 <= idx <= len(categories)):
            ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
            continue
        return categories[idx - 1]

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

    HEADER("EDITAR CATEGORIAS")
    RULE()
    edited_cat = []
    while True:
        choice = ASK("VOCÊ DESEJA EDITAR(1), DELETAR(2) OU CRIAR(3) UMA CATEGORIA:")
        if _cancelled(choice):
            return
        if not choice:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        elif not re.fullmatch(r"[1-9]+", choice):
            ERROR("DIGITE SOMENTE NÚMEROS!")
        elif choice != "1" and choice != "2" and choice != "3":
            ERROR("ESCOLHA ENTRE 1, 2 E 3!")
        else:
            break

    if choice == "1":
        while True:
            trans_type = ASK("VOCÊ QUER EDITAR UMA CATEGORIA DE RECEITA(1) OU DESPESA(2):")
            if _cancelled(trans_type):
                return
            if not trans_type:
                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            elif not re.fullmatch(r"[1-9]+", trans_type):
                ERROR("DIGITE SOMENTE NÚMEROS!")
            elif trans_type != "1" and trans_type != "2":
                ERROR("ESCOLHA ENTRE 1 E 2!")
            else:
                break
    
        if trans_type == "1":
            while True:
                replay = False
                confirm = False
                edited_cat = []
                new_trans = []
                for i, category in enumerate(categories_rev, 1):
                    INFO(f"[{i}] {category}")
                RULE()
                while True:
                    del_cat = ASK("DIGITE O NÚMERO DA CATEGORIA QUE QUER EDITAR:")
                    if _cancelled(del_cat):
                        return
                    if not del_cat:
                        ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                    elif not re.fullmatch(r"[0-9]+", del_cat):
                        ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                    elif int(del_cat) > len(categories_rev) or int(del_cat) < 1:
                        ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                    else:
                        break
                for i, category in enumerate(categories_rev):
                    if replay:
                        continue
                    if del_cat == str(i+1):
                        while True:
                            new_cat = ASK("DIGITE O NOME DA NOVA CATEGORIA QUE VOCÊ DESEJA:")
                            if _cancelled(new_cat):
                                return
                            if not new_cat:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                                continue
                            if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", new_cat):
                                ERROR("DIGITE SOMENTE LETRAS!")
                                continue
                            new_cat = _normalize_cat_name(new_cat)
                            if _exists_casefold(categories_rev, new_cat, except_name=category):
                                ERROR("JÁ EXISTE UMA CATEGORIA COM ESSE NOME!")
                                continue
                            break
                        edited_cat.append(new_cat)

                        final_cat = category
                        has_links = any(t["category"] == category for t in transactions)
                        if has_links:
                            while True:
                                choice = ASK("EXISTEM TRANSAÇÕES COM ESSA CATEGORIA, DESEJA EDITAR MESMO ASSIM [S/N]?").upper()
                                if _cancelled(choice):
                                    return
                                if not choice:
                                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                                elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", choice):
                                    ERROR("DIGITE SOMENTE LETRAS!")
                                elif not (choice == "S" or choice == "N"):
                                    ERROR("DIGITE UMA DAS OPÇÕES DADAS (S/N)!")
                                else:
                                    break
                            if choice == "N":
                                replay = True
                                continue
                            confirm = True
                        else:
                            confirm = True

                        if confirm:
                            for t in transactions:
                                if t["category"] == category:
                                    t["category"] = new_cat
                                new_trans.append(t)
                    else:
                        edited_cat.append(category)
                if confirm:
                    OK(f"A CATEGORIA '{final_cat}' FOI EDITADA (SUBSTITUÍDA POR '{new_cat}' NAS TRANSAÇÕES RELACIONADAS)")
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
                    INFO(f"[{i}] {category}")
                RULE()
                while True:
                    del_cat = ASK("DIGITE O NÚMERO DA CATEGORIA QUE QUER EDITAR:")
                    if _cancelled(del_cat):
                        return
                    if not del_cat:
                        ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                    elif not re.fullmatch(r"[0-9]+", del_cat):
                        ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                    elif int(del_cat) > len(categories_exp) or int(del_cat) < 1:
                        ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                    else:
                        break
                for i, category in enumerate(categories_exp):
                    if replay:
                        continue
                    if del_cat == str(i+1):
                        while True:
                            new_cat = ASK("DIGITE O NOME DA NOVA CATEGORIA QUE VOCÊ DESEJA:")
                            if _cancelled(new_cat):
                                return
                            if not new_cat:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                                continue
                            if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", new_cat):
                                ERROR("DIGITE SOMENTE LETRAS!")
                                continue
                            new_cat = _normalize_cat_name(new_cat)
                            if _exists_casefold(categories_exp, new_cat, except_name=category):
                                ERROR("JÁ EXISTE UMA CATEGORIA COM ESSE NOME!")
                                continue
                            break
                        edited_cat.append(new_cat)

                        final_cat = category
                        has_links = any(t["category"] == category for t in transactions)
                        if has_links:
                            while True:
                                choice = ASK("EXISTEM TRANSAÇÕES COM ESSA CATEGORIA, DESEJA EDITAR MESMO ASSIM [S/N]?").upper()
                                if _cancelled(choice):
                                    return
                                if not choice:
                                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                                elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", choice):
                                    ERROR("DIGITE SOMENTE LETRAS!")
                                elif not (choice == "S" or choice == "N"):
                                    ERROR("DIGITE UMA DAS OPÇÕES DADAS (S/N)!")
                                else:
                                    break
                            if choice == "N":
                                replay = True
                                continue
                            confirm = True
                        else:
                            confirm = True

                        if confirm:
                            for t in transactions:
                                if t["category"] == category:
                                    t["category"] = new_cat
                                new_trans.append(t)
                    else:
                        edited_cat.append(category)
                if confirm:
                    OK(f"A CATEGORIA '{final_cat}' FOI EDITADA (SUBSTITUÍDA POR '{new_cat}' NAS TRANSAÇÕES RELACIONADAS)")
                    edited_cat.append("Outros")
                    new_db(EXP_PATH, edited_cat)
                    new_db(DB_PATH, new_trans)
                    return
                
    if choice == "2":
        while True:
            trans_type = ASK("VOCÊ QUER DELETAR UMA CATEGORIA DE RECEITA(1) OU DESPESA(2):")
            if _cancelled(trans_type):
                return
            if not trans_type:
                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            elif not re.fullmatch(r"[1-9]+", trans_type):
                ERROR("DIGITE SOMENTE NÚMEROS!")
            elif trans_type != "1" and trans_type != "2":
                ERROR("ESCOLHA ENTRE 1 E 2!")
            else:
                break
    
        if trans_type == "1":
            while True:
                replay = False
                confirm = False
                edited_cat = []
                new_trans = []
                for i, category in enumerate(categories_rev, 1):
                    INFO(f"[{i}] {category}")
                RULE()
                while True:
                    del_cat = ASK("DIGITE O NÚMERO DA CATEGORIA QUE QUER DELETAR:")
                    if _cancelled(del_cat):
                        return
                    if not del_cat:
                        ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                    elif not re.fullmatch(r"[0-9]+", del_cat):
                        ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                    elif int(del_cat) > len(categories_rev) or int(del_cat) < 1:
                        ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                    else:
                        break
                for i, category in enumerate(categories_rev):
                    if replay:
                        continue
                    if del_cat == str(i+1):
                        final_cat = category
                        has_links = any(t["category"] == category for t in transactions)
                        if has_links:
                            while True:
                                choice = ASK("EXISTEM TRANSAÇÕES COM ESSA CATEGORIA, DESEJA APAGAR MESMO ASSIM [S/N]?").upper()
                                if _cancelled(choice):
                                    return
                                if not choice:
                                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                                elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", choice):
                                    ERROR("DIGITE SOMENTE LETRAS!")
                                elif not (choice == "S" or choice == "N"):
                                    ERROR("DIGITE UMA DAS OPÇÕES DADAS (S/N)!")
                                else:
                                    break
                            if choice == "N":
                                replay = True
                                continue
                            confirm = True
                        else:
                            confirm = True

                        if confirm:
                            for t in transactions:
                                if t["category"] == category:
                                    t["category"] = "Outros"
                                new_trans.append(t)
                    else:
                        edited_cat.append(category)
                if confirm:
                    OK(f"A CATEGORIA '{final_cat}' FOI DELETADA (SUBSTITUÍDA POR 'Outros' NAS TRANSAÇÕES RELACIONADAS)")
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
                    INFO(f"[{i}] {category}")
                RULE()
                while True:
                    del_cat = ASK("DIGITE O NÚMERO DA CATEGORIA QUE QUER DELETAR:")
                    if _cancelled(del_cat):
                        return
                    if not del_cat:
                        ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                    elif not re.fullmatch(r"[0-9]+", del_cat):
                        ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                    elif int(del_cat) > len(categories_exp) or int(del_cat) < 1:
                        ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                    else:
                        break
                for i, category in enumerate(categories_exp):
                    if replay:
                        continue
                    if del_cat == str(i+1):
                        final_cat = category
                        has_links = any(t["category"] == category for t in transactions)
                        if has_links:
                            while True:
                                choice = ASK("EXISTEM TRANSAÇÕES COM ESSA CATEGORIA, DESEJA APAGAR MESMO ASSIM [S/N]?").upper()
                                if _cancelled(choice):
                                    return
                                if not choice:
                                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                                elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", choice):
                                    ERROR("DIGITE SOMENTE LETRAS!")
                                elif not (choice == "S" or choice == "N"):
                                    ERROR("DIGITE UMA DAS OPÇÕES DADAS (S/N)!")
                                else:
                                    break
                            if choice == "N":
                                replay = True
                                continue
                            confirm = True
                        else:
                            confirm = True

                        if confirm:
                            for t in transactions:
                                if t["category"] == category:
                                    t["category"] = "Outros"
                                new_trans.append(t)
                    else:
                        edited_cat.append(category)
                if confirm:
                    OK(f"A CATEGORIA '{final_cat}' FOI DELETADA (SUBSTITUÍDA POR 'Outros' NAS TRANSAÇÕES RELACIONADAS)")
                    edited_cat.append("Outros")
                    new_db(EXP_PATH, edited_cat)
                    new_db(DB_PATH, new_trans)
                    return       

    elif choice == "3":
        while True:
            trans_type = ASK("VOCÊ QUER ADICIONAR UMA CATEGORIA DE RECEITA(1) OU DESPESA(2):")
            if _cancelled(trans_type):
                return
            if not trans_type:
                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            elif not re.fullmatch(r"[1-9]+", trans_type):
                ERROR("DIGITE SOMENTE NÚMEROS!")
            elif trans_type != "1" and trans_type != "2":
                ERROR("ESCOLHA ENTRE 1 E 2!")
            else:
                break
        if trans_type == "1":
            for category in categories_rev:
                edited_cat.append(category)
            while True:
                new_cat = ASK("DIGITE O NOME DA NOVA CATEGORIA QUE VOCÊ DESEJA:")
                if _cancelled(new_cat):
                    return
                if not new_cat:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                    continue
                if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", new_cat):
                    ERROR("DIGITE SOMENTE LETRAS!")
                    continue
                new_cat = _normalize_cat_name(new_cat)
                if _exists_casefold(edited_cat, new_cat):
                    ERROR("JÁ EXISTE UMA CATEGORIA COM ESSE NOME!")
                    continue
                break 
            edited_cat.append(new_cat)
            if "Outros" not in edited_cat:
                edited_cat.append("Outros")
            new_db(REV_PATH, edited_cat)
            
        elif trans_type == "2":
            for category in categories_exp:
                edited_cat.append(category)
            while True:
                new_cat = ASK("DIGITE O NOME DA NOVA CATEGORIA QUE VOCÊ DESEJA:")
                if _cancelled(new_cat):
                    return
                if not new_cat:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                    continue
                if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", new_cat):
                    ERROR("DIGITE SOMENTE LETRAS!")
                    continue
                new_cat = _normalize_cat_name(new_cat)
                if _exists_casefold(edited_cat, new_cat):
                    ERROR("JÁ EXISTE UMA CATEGORIA COM ESSE NOME!")
                    continue
                break 
            edited_cat.append(new_cat)
            if "Outros" not in edited_cat:
                edited_cat.append("Outros")
            new_db(EXP_PATH, edited_cat)
    

    


