from utils.classificacao import categorize_rev, categorize_exp
from utils.arquivos import db_add, db_confirm, new_db
from utils.verifiers import quit, _cancelled, value_verf, month_verf, type_verf, date_verf, value_verf_float, year_verf
from utils.trans_class import Transaction
import datetime
import re
import json
from utils.ui import HEADER, RULE, ASK, OK, ERROR, WARN, INFO, trans_table

def _list_with_table(trans_list):
    if trans_list:
        trans_table(trans_list)
    else:
        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")


# Helper para escolher categoria sem duplicar aviso de cancelamento
# Retorna None se o usuário cancelar (-1)
def pick_category(kind: str):
    cat = categorize_rev() if kind == "Receita" else categorize_exp()
    if cat == "-1":
        WARN("OPERAÇÃO CANCELADA!")
        return None
    return cat

DB_PATH = "/Users/matheusgomes/Documents/CONTROLE_FINANCEIRO/financeiro.json"

def revenue():
    type = "Receita"
    raw = ASK("VALOR:")
    if _cancelled(raw):
        return
    value = value_verf(raw)
    if value == "-1":
        WARN("OPERAÇÃO CANCELADA!")
        return

    category = pick_category("Receita")
    if category is None:
        return

    description = ASK("DESCRIÇÃO:")
    if _cancelled(description):
        return

    date = datetime.date.today().isoformat()
    db_add(type, value, category, description, date)
    
def expense():
    type = "Despesa"
    raw = ASK("VALOR:")
    if _cancelled(raw):
        return
    value = value_verf(raw)
    if value == "-1":
        WARN("OPERAÇÃO CANCELADA!")
        return

    category = pick_category("Despesa")
    if category is None:
        return

    description = ASK("DESCRIÇÃO:").capitalize()
    if _cancelled(description):
        return
    
    date = datetime.date.today().isoformat()

    db_add(type, value, category, description, date)

def edit_trans():  # aprofundar depois quando tiver beckup de cada dia, e separar melhor por mesv
    transactions = db_confirm()
    if transactions is None:
        return
    HEADER("EDITAR TRANSAÇÃO")
    
    while True:
        choice = ASK("COMO VOCÊ DESEJA PROCURAR SUA TRANSAÇÃO? [1]VALOR [2]CATEGORIA [3]DATA")
        if _cancelled(choice):
            return
        if not choice:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        elif not re.fullmatch(r"[0-9]+", choice):
            ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
        elif (choice != "1") and (choice != "2") and (choice != "3"):
            ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
        else:
            break
    if choice == "1":
            while True:
                option = ASK("PESQUISAR POR: [1]VALOR [2]INTERVALO")
                if _cancelled(option):
                    return
                if not option:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                elif not re.fullmatch(r"[0-9]+", option):
                    ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                elif (option != "1") and (option != "2"):
                    ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                else:
                    break
            if option == "1":
                while True:
                    trans_list = []
                    trans_exist = False
                    new_trans = []
                    raw = ASK("DIGITE O VALOR QUE QUEIRA PROCURAR:")
                    if _cancelled(raw):
                        return
                    value = value_verf(raw)
                    if value == "-1":
                        WARN("OPERAÇÃO CANCELADA!")
                        return
                    RULE()
                    print("")
                    for trans in transactions:
                        if trans["value"] == value:
                            trans_exist = True
                            trans_list.append(trans)
                        else:
                            new_trans.append(trans)

                    _list_with_table(trans_list)
                    if not trans_exist:
                        continue

                    if trans_exist == True:
                        while True:  
                            choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA EDITAR:")
                            if _cancelled(choice):
                                return
                            if not choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(choice) > len(trans_list) or int(choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                        
                        for i, trans in enumerate(trans_list):
                            if i == (int(choice)-1):
                                RULE()
                                print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                                            ))
                                RULE()
                        
                            else:
                                new_trans.append(trans)

                        while True:
                            confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA EDITAR [S/N]?").upper()
                            if _cancelled(confimation):
                                return
                            if not confimation:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                                ERROR("DIGITE SOMENTE LETRAS!")
                            elif not (confimation == "S" or confimation == "N"):
                                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                            else:
                                break
                        if confimation == "S":
                            break
                        elif confimation == "N":
                            continue


                new_type = type_verf()
                if new_type in ("-1", None, ""):
                    WARN("OPERAÇÃO CANCELADA!")
                    return

                raw_nv = ASK("DIGITE O NOVO VALOR:")
                if _cancelled(raw_nv):
                    return
                new_value = value_verf(raw_nv)
                if new_value == "-1":
                    WARN("OPERAÇÃO CANCELADA!")
                    return

                new_category = pick_category(new_type)
                if new_category is None:
                    return

                new_description = ASK("DIGITE A NOVA DESCRIÇÃO:")
                if _cancelled(new_description):
                    return

                raw_nd = ASK("DIGITE A NOVA DATA:")
                if _cancelled(raw_nd):
                    return
                new_date = date_verf(raw_nd)
                trans = Transaction(new_type, new_value, new_category, new_description, new_date)
                new_trans.append(trans.to_dict())
                
                new_db(DB_PATH, new_trans)

            elif option == "2":  
                while True:
                    trans_list = []
                    trans_exist = False
                    new_trans = []
                    raw_h = ASK("O VALOR É MAIOR QUE:")
                    if _cancelled(raw_h):
                        return
                    higher = value_verf_float(raw_h)
                    if higher == "-1":
                        WARN("OPERAÇÃO CANCELADA!")
                        return
                    raw_l = ASK("O VALOR É MENOR QUE:")
                    if _cancelled(raw_l):
                        return
                    lower = value_verf_float(raw_l)
                    if lower == "-1":
                        WARN("OPERAÇÃO CANCELADA!")
                        return
                    
                    if lower < higher:
                        lower, higher = higher, lower

                    if higher == lower:
                        ERROR("DIGITE VALORES DIFERENTES!")
                        continue
                    RULE()  
                    print("")
                    for trans in transactions:
                        val = float(str(trans["value"]).replace("R$", "").replace(".", "").replace(",", ".").strip())
                        if (val > higher) and (val < lower):
                            trans_exist = True
                            trans_list.append(trans)
                        else:
                            new_trans.append(trans)

                    _list_with_table(trans_list)
                    if not trans_exist:
                        continue
                
                    if trans_exist == True:
                        while True:  
                            choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA EDITAR:")
                            if _cancelled(choice):
                                return
                            if not choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(choice) > len(trans_list) or int(choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                        
                        for i, trans in enumerate(trans_list):
                            if i == (int(choice)-1):
                                RULE()
                                print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                                            ))
                                RULE()
                        
                            else:
                                new_trans.append(trans)

                        while True:
                            confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA EDITAR [S/N]?").upper()
                            if _cancelled(confimation):
                                return
                            if not confimation:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                                ERROR("DIGITE SOMENTE LETRAS!")
                            elif not (confimation == "S" or confimation == "N"):
                                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                            else:
                                break
                        if confimation == "S":
                            break
                        elif confimation == "N":
                            continue


                new_type = type_verf()
                if new_type in ("-1", None, ""):
                    WARN("OPERAÇÃO CANCELADA!")
                    return

                raw_nv = ASK("DIGITE O NOVO VALOR:")
                if _cancelled(raw_nv):
                    return
                new_value = value_verf(raw_nv)
                if new_value == "-1":
                    WARN("OPERAÇÃO CANCELADA!")
                    return

                new_category = pick_category(new_type)
                if new_category is None:
                    return

                new_description = ASK("DIGITE A NOVA DESCRIÇÃO:")
                if _cancelled(new_description):
                    return

                raw_nd = ASK("DIGITE A NOVA DATA:")
                if _cancelled(raw_nd):
                    return
                new_date = date_verf(raw_nd)
                trans = Transaction(new_type,new_value,new_category,new_description,new_date)
                new_trans.append(trans.to_dict())
                
                new_db(DB_PATH, new_trans)

    elif choice == "2":
        while True:
            cat_list = []
            trans_list = []
            new_trans = []
            trans_exist = False
            # Listar categorias únicas de Receita e Despesa
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
                choice_cat = ASK("DE QUAL CATEGORIA VOCÊ QUER EDITAR AS TRANSAÇÕES:")
                if _cancelled(choice_cat):
                    return
                if not choice_cat:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                elif not re.fullmatch(r"[0-9]+", choice_cat):
                    ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                elif (int(choice_cat) > len(cat_list)) or (int(choice_cat) <= 0):
                    ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                else:
                    break
            RULE()
            print("")
            for i, cat in enumerate(cat_list):
                if i == (int(choice_cat)-1):
                    for trans in transactions:
                        if trans["category"] == cat:
                            trans_list.append(trans)
                            trans_exist = True
                        else:
                            new_trans.append(trans)
            _list_with_table(trans_list)
            RULE()
            if not trans_exist:
                continue
            if trans_exist:
                while True:
                    idx_choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA EDITAR:")
                    if _cancelled(idx_choice):
                        return
                    if not idx_choice:
                        ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                    elif not re.fullmatch(r"[0-9]+", idx_choice):
                        ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                    elif int(idx_choice) > len(trans_list) or int(idx_choice) < 1:
                        ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                    else:
                        break
                for i, trans in enumerate(trans_list):
                    if i == (int(idx_choice)-1):
                        RULE()
                        print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                        ))
                        RULE()
                    else:
                        new_trans.append(trans)
                while True:
                    confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA EDITAR [S/N]?").upper()
                    if _cancelled(confimation):
                        return
                    if not confimation:
                        ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                    elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                        ERROR("DIGITE SOMENTE LETRAS!")
                    elif not (confimation == "S" or confimation == "N"):
                        ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                    else:
                        break
                if confimation == "S":
                    break
                elif confimation == "N":
                    continue
        new_type = type_verf()
        if new_type in ("-1", None, ""):
            WARN("OPERAÇÃO CANCELADA!")
            return

        raw_nv = ASK("DIGITE O NOVO VALOR:")
        if _cancelled(raw_nv):
            return
        new_value = value_verf(raw_nv)
        if new_value == "-1":
            WARN("OPERAÇÃO CANCELADA!")
            return

        new_category = pick_category(new_type)
        if new_category is None:
            return

        new_description = ASK("DIGITE A NOVA DESCRIÇÃO:")
        if _cancelled(new_description):
            return

        raw_nd = ASK("DIGITE A NOVA DATA:")
        if _cancelled(raw_nd):
            return
        new_date = date_verf(raw_nd)
        trans = Transaction(new_type, new_value, new_category, new_description, new_date)
        new_trans.append(trans.to_dict())
        new_db(DB_PATH, new_trans)
                 
    elif choice == "3":
        while True:
            option = ASK("PESQUISAR POR: [1]DIA/MÊS/ANO [2]PERÍODO PERSONALIZADO")
            if _cancelled(option):
                return
            if not option:
                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            elif not re.fullmatch(r"[0-9]+", option):
                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
            elif (option != "1") and (option != "2"):
                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
            else:
                break
        if option == "1":
            while True:
                type = ASK("[1]DIA [2]MÊS [3]ANO")
                if _cancelled(type):
                    return
                if not type:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                elif not re.fullmatch(r"[0-9]+", type):
                    ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                elif (type != "1") and (type != "2") and (type != "3"):
                    ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                else:
                    break
            if type == "1":
                go_edit = False
                while True:
                    trans_exist = False
                    trans_list = []
                    new_trans = []
                    raw_day = ASK("DIGITE O DIA ESPECÍFICO QUE QUER PROCURAR (YYYY-MM-DD):")
                    if _cancelled(raw_day):
                        return
                    day = date_verf(raw_day)
                    RULE()
                    print("")
                    for trans in transactions:
                        if trans["date"] == day:
                            trans_list.append(trans)
                            trans_exist = True
                        else:
                            new_trans.append(trans)
                    _list_with_table(trans_list)
                    RULE()
                    if not trans_exist:
                        continue
                    if trans_exist:
                        while True:
                            idx_choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA EDITAR:")
                            if _cancelled(idx_choice):
                                return
                            if not idx_choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", idx_choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(idx_choice) > len(trans_list) or int(idx_choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                        for i, trans in enumerate(trans_list):
                            if i == (int(idx_choice)-1):
                                RULE()
                                print(Transaction(
                                    trans["type"],
                                    trans["value"],
                                    trans["category"],
                                    trans["description"],
                                    trans["date"]
                                ))
                                RULE()
                            else:
                                new_trans.append(trans)
                        while True:
                            confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA EDITAR [S/N]?").upper()
                            if _cancelled(confimation):
                                return
                            if not confimation:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                                ERROR("DIGITE SOMENTE LETRAS!")
                            elif not (confimation == "S" or confimation == "N"):
                                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                            else:
                                break
                        if confimation == "S":
                            go_edit = True
                            break
                        elif confimation == "N":
                            continue
                if not go_edit:
                    return
                new_type = type_verf()
                if new_type in ("-1", None, ""):
                    WARN("OPERAÇÃO CANCELADA!")
                    return

                raw_nv = ASK("DIGITE O NOVO VALOR:")
                if _cancelled(raw_nv):
                    return
                new_value = value_verf(raw_nv)
                if new_value == "-1":
                    WARN("OPERAÇÃO CANCELADA!")
                    return

                new_category = pick_category(new_type)
                if new_category is None:
                    return

                new_description = ASK("DIGITE A NOVA DESCRIÇÃO:")
                if _cancelled(new_description):
                    return

                raw_nd = ASK("DIGITE A NOVA DATA:")
                if _cancelled(raw_nd):
                    return
                new_date = date_verf(raw_nd)
                trans = Transaction(new_type, new_value, new_category, new_description, new_date)
                new_trans.append(trans.to_dict())
                new_db(DB_PATH, new_trans)
            elif type == "2":
                go_edit = False
                while True:
                    trans_exist = False
                    year_exist = False
                    new_trans = []
                    trans_list = []
                    raw_y = ASK("DIGITE O ANO QUE VOCÊ QUER VER OS MESES:")
                    if _cancelled(raw_y):
                        return
                    choice_year = year_verf(raw_y)
                    raw_m = ASK("DIGITE O MÊS QUE VOCÊ QUER VER:")
                    if _cancelled(raw_m):
                        return
                    choice_mon = (month_verf(raw_m)).lstrip("0")
                    RULE()
                    print("")
                    for trans in transactions:
                        year = datetime.datetime.fromisoformat(trans["date"]).year
                        if str(choice_year) == str(year):
                            year_exist = True
                            month = datetime.datetime.fromisoformat(trans["date"]).month
                            if str(choice_mon) == str(month):
                                trans_exist = True
                                trans_list.append(trans)
                            else:
                                new_trans.append(trans)
                        else:
                            new_trans.append(trans)
                    _list_with_table(trans_list)
                    if not year_exist:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                    elif not trans_exist:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                    RULE()
                    if not trans_exist or not year_exist:
                        continue
                    if trans_exist:
                        while True:
                            idx_choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA EDITAR:")
                            if _cancelled(idx_choice):
                                return
                            if not idx_choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", idx_choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(idx_choice) > len(trans_list) or int(idx_choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                        for i, trans in enumerate(trans_list):
                            if i == (int(idx_choice)-1):
                                RULE()
                                print(Transaction(
                                    trans["type"],
                                    trans["value"],
                                    trans["category"],
                                    trans["description"],
                                    trans["date"]
                                ))
                                RULE()
                            else:
                                new_trans.append(trans)
                        while True:
                            confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA EDITAR [S/N]?").upper()
                            if _cancelled(confimation):
                                return
                            if not confimation:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                                ERROR("DIGITE SOMENTE LETRAS!")
                            elif not (confimation == "S" or confimation == "N"):
                                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                            else:
                                break
                        if confimation == "S":
                            go_edit = True
                            break
                        elif confimation == "N":
                            continue
                if not go_edit:
                    return
                new_type = type_verf()
                if new_type in ("-1", None, ""):
                    WARN("OPERAÇÃO CANCELADA!")
                    return

                raw_nv = ASK("DIGITE O NOVO VALOR:")
                if _cancelled(raw_nv):
                    return
                new_value = value_verf(raw_nv)

                new_category = pick_category(new_type)
                if new_category is None:
                    return

                new_description = ASK("DIGITE A NOVA DESCRIÇÃO:")
                if _cancelled(new_description):
                    return

                raw_nd = ASK("DIGITE A NOVA DATA:")
                if _cancelled(raw_nd):
                    return
                new_date = date_verf(raw_nd)
                trans = Transaction(new_type, new_value, new_category, new_description, new_date)
                new_trans.append(trans.to_dict())
                new_db(DB_PATH, new_trans)
            elif type == "3":
                go_edit = False
                while True:
                    trans_exist = False
                    trans_list = []
                    new_trans = []
                    raw_y2 = ASK("DIGITE O ANO QUE VOCÊ QUER VER AS TRANSAÇÕES:")
                    if _cancelled(raw_y2):
                        return
                    choice_year = year_verf(raw_y2)
                    RULE()
                    print("")
                    for trans in transactions:
                        year = datetime.datetime.fromisoformat(trans["date"]).year
                        if str(choice_year) == str(year):
                            trans_list.append(trans)
                            trans_exist = True
                        else:
                            new_trans.append(trans)
                    _list_with_table(trans_list)
                    RULE()
                    if not trans_exist:
                        continue
                    if trans_exist:
                        while True:
                            idx_choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA EDITAR:")
                            if _cancelled(idx_choice):
                                return
                            if not idx_choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", idx_choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(idx_choice) > len(trans_list) or int(idx_choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                        for i, trans in enumerate(trans_list):
                            if i == (int(idx_choice)-1):
                                RULE()
                                print(Transaction(
                                    trans["type"],
                                    trans["value"],
                                    trans["category"],
                                    trans["description"],
                                    trans["date"]
                                ))
                                RULE()
                            else:
                                new_trans.append(trans)
                        while True:
                            confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA EDITAR [S/N]?").upper()
                            if _cancelled(confimation):
                                return
                            if not confimation:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                                ERROR("DIGITE SOMENTE LETRAS!")
                            elif not (confimation == "S" or confimation == "N"):
                                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                            else:
                                break
                        if confimation == "S":
                            go_edit = True
                            break
                        elif confimation == "N":
                            continue
                if not go_edit:
                    return
                new_type = type_verf()
                if new_type in ("-1", None, ""):
                    WARN("OPERAÇÃO CANCELADA!")
                    return

                raw_nv = ASK("DIGITE O NOVO VALOR:")
                if _cancelled(raw_nv):
                    return
                new_value = value_verf(raw_nv)

                new_category = pick_category(new_type)
                if new_category is None:
                    return

                new_description = ASK("DIGITE A NOVA DESCRIÇÃO:")
                if _cancelled(new_description):
                    return

                raw_nd = ASK("DIGITE A NOVA DATA:")
                if _cancelled(raw_nd):
                    return
                new_date = date_verf(raw_nd)
                trans = Transaction(new_type, new_value, new_category, new_description, new_date)
                new_trans.append(trans.to_dict())
                new_db(DB_PATH, new_trans)

        elif option == "2":
            while True:
                trans_exist = False
                trans_list = []
                new_trans = []
                # Perguntas do intervalo personalizado
                raw_si = ASK("DIGITE A DATA INICIAL (YYYY-MM-DD):")
                if _cancelled(raw_si):
                    return
                start_iso = date_verf(raw_si)
                raw_ei = ASK("DIGITE A DATA FINAL (YYYY-MM-DD):")
                if _cancelled(raw_ei):
                    return
                end_iso = date_verf(raw_ei)

                # Converte para date para validar ordem e normalizar
                start_date = datetime.date.fromisoformat(start_iso)
                end_date = datetime.date.fromisoformat(end_iso)

                # Normaliza caso o usuário tenha invertido
                if end_date < start_date:
                    start_date, end_date = end_date, start_date
                
                RULE()
                for trans in transactions:
                    if start_date <= datetime.date.fromisoformat(trans["date"]) <= end_date:
                        trans_list.append(trans)
                        trans_exist = True
                    else:
                        new_trans.append(trans)

                _list_with_table(trans_list)
                RULE()

                if not trans_exist:
                    continue
                
                if trans_exist == True:
                    while True:  
                        choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA EDITAR:")
                        if _cancelled(choice):
                            return
                        if not choice:
                            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                        elif not re.fullmatch(r"[0-9]+", choice):
                            ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                        elif int(choice) > len(trans_list) or int(choice) < 1:
                            ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                        else:
                            break
                    
                    for i, trans in enumerate(trans_list):
                        if i == (int(choice)-1):
                            RULE()
                            print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                            ))
                            RULE()
                        else:
                            new_trans.append(trans)

                    while True:
                        confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA EDITAR [S/N]?").upper()
                        if _cancelled(confimation):
                            return
                        if not confimation:
                            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                            ERROR("DIGITE SOMENTE LETRAS!")
                        elif not (confimation == "S" or confimation == "N"):
                            ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                        else:
                            break
                    if confimation == "S":
                        break
                    elif confimation == "N":
                        continue


            new_type = type_verf()
            if new_type in ("-1", None, ""):
                WARN("OPERAÇÃO CANCELADA!")
                return
            raw_nv = ASK("DIGITE O NOVO VALOR:")
            if _cancelled(raw_nv):
                return
            new_value = value_verf(raw_nv)

            new_category = pick_category(new_type)
            if new_category is None:
                return

            new_description = ASK("DIGITE A NOVA DESCRIÇÃO:")
            if _cancelled(new_description):
                return

            raw_nd = ASK("DIGITE A NOVA DATA:")
            if _cancelled(raw_nd):
                return
            new_date = date_verf(raw_nd)
            trans = Transaction(new_type, new_value, new_category, new_description, new_date)
            new_trans.append(trans.to_dict())
            
            new_db(DB_PATH, new_trans)           

def deleteone():
    transactions = db_confirm()
    if transactions is None:
        return
    HEADER("DELETAR UMA TRANSAÇÃO")
 

    while True:
        choice = ASK("COMO VOCÊ DESEJA PROCURAR SUA TRANSAÇÃO? [1]VALOR [2]CATEGORIA [3]DATA")
        if _cancelled(choice):
            return
        if not choice:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        elif not re.fullmatch(r"[0-9]+", choice):
            ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
        elif (choice != "1") and (choice != "2") and (choice != "3"):
            ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
        else:
            break
    if choice == "1":
            while True:
                option = ASK("PESQUISAR POR: [1]VALOR [2]INTERVALO")
                if _cancelled(option):
                    return
                if not option:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                elif not re.fullmatch(r"[0-9]+", option):
                    ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                elif (option != "1") and (option != "2"):
                    ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                else:
                    break
            if option == "1":
                while True:
                    trans_list = []
                    trans_exist = False
                    new_trans = []
                    raw = ASK("DIGITE O VALOR QUE QUEIRA PROCURAR:")
                    if _cancelled(raw):
                        return
                    value = value_verf(raw)
                    if value == "-1":
                        WARN("OPERAÇÃO CANCELADA!")
                        return
                    RULE()
                    print("")
                    for trans in transactions:
                        if trans["value"] == value:
                            trans_exist = True
                            trans_list.append(trans)
                        else:
                            new_trans.append(trans)

                    _list_with_table(trans_list)
                    if not trans_exist:
                        continue
                
                    if trans_exist == True:
                        while True:  
                            choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA DELETAR:")
                            if _cancelled(choice):
                                return
                            if not choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(choice) > len(trans_list) or int(choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                
                    for i, trans in enumerate(trans_list):
                        if i == (int(choice)-1):
                            RULE()
                            print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                                        ))
                            RULE()
                    
                        else:
                            new_trans.append(trans)

                    while True:
                        confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA DELETAR [S/N]?").upper()
                        if _cancelled(confimation):
                            return
                        if not confimation:
                            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                            ERROR("DIGITE SOMENTE LETRAS!")
                        elif not (confimation == "S" or confimation == "N"):
                            ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                        else:
                            break
                    if confimation == "S":
                        new_db(DB_PATH, new_trans)
                        OK("TRANSAÇÃO DELETADA!")
                        return
                    elif confimation == "N":
                        continue
                    
            elif option == "2":  
                while True:
                    trans_list = []
                    trans_exist = False
                    new_trans = []
                    raw_h = ASK("O VALOR É MAIOR QUE:")
                    if _cancelled(raw_h):
                        return
                    higher = value_verf_float(raw_h)
                    if higher == "-1":
                        WARN("OPERAÇÃO CANCELADA!")
                        return
                    raw_l = ASK("O VALOR É MENOR QUE:")
                    if _cancelled(raw_l):
                        return
                    lower = value_verf_float(raw_l)
                    if lower == "-1":
                        WARN("OPERAÇÃO CANCELADA!")
                        return
                    
                    if lower < higher:
                        lower, higher = higher, lower

                    if higher == lower:
                        ERROR("DIGITE VALORES DIFERENTES!")
                        continue
                    RULE()
                    print("")
                    for trans in transactions:
                        val = float(str(trans["value"]).replace("R$", "").replace(".", "").replace(",", ".").strip())
                        if (val > higher) and (val < lower):
                            trans_exist = True
                            trans_list.append(trans)
                        else:
                            new_trans.append(trans)

                    _list_with_table(trans_list)
                    if not trans_exist:
                        continue
                
                    if trans_exist == True:
                        while True:  
                            choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA DELETAR:")
                            if _cancelled(choice):
                                return
                            if not choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(choice) > len(trans_list) or int(choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                    
                    for i, trans in enumerate(trans_list):
                        if i == (int(choice)-1):
                            RULE()
                            print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                                        ))
                            RULE()
                        else:
                            new_trans.append(trans)

                    while True:
                        confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA DELETAR [S/N]?").upper()
                        if _cancelled(confimation):
                            return
                        if not confimation:
                            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                            ERROR("DIGITE SOMENTE LETRAS!")
                        elif not (confimation == "S" or confimation == "N"):
                            ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                        else:
                            break
                    if confimation == "S":
                        OK("TRANSAÇÃO DELETADA!")
                        new_db(DB_PATH, new_trans)
                        return
                    elif confimation == "N":
                        continue

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
                choice = ASK("DE QUAL CATEGORIA VOCÊ QUER DELETAR AS TRANSAÇÕES:")
                if _cancelled(choice):
                    return
                if not choice:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                elif not re.fullmatch(r"[0-9]+", choice):
                    ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                elif (int(choice) > len(cat_list)) or (int(choice) <= 0):
                    ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                else:
                    break   
            RULE()
            print("")
            for i, cat in enumerate(cat_list):
                if i == (int(choice)-1):
                    for trans in transactions:
                        if trans["category"] == cat:
                            trans_list.append(trans)
                            trans_exist = True
                        else:
                            new_trans.append(trans)

            _list_with_table(trans_list)
            RULE()
            if trans_exist == True:
                    while True:  
                        choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA DELETAR:")
                        if _cancelled(choice):
                            return
                        if not choice:
                            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                        elif not re.fullmatch(r"[0-9]+", choice):
                            ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                        elif int(choice) > len(trans_list) or int(choice) < 1:
                            ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                        else:
                            break
                    
                    for i, trans in enumerate(trans_list):
                        if i == (int(choice)-1):
                            RULE()
                            print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                                        ))
                            RULE()

                        else:
                            new_trans.append(trans)
                    
                    while True:
                        confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA DELETAR [S/N]?").upper()
                        if _cancelled(confimation):
                            return
                        if not confimation:
                            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                            ERROR("DIGITE SOMENTE LETRAS!")
                        elif not (confimation == "S" or confimation == "N"):
                            ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                        else:
                            break
                    if confimation == "S":
                        OK("TRANSAÇÃO DELETADA!")
                        new_db(DB_PATH, new_trans)
                        return
                    elif confimation == "N":
                        continue
                 
    elif choice == "3":
        while True:
            option = ASK("PESQUISAR POR: [1]DIA/MÊS/ANO [2]PERÍODO PERSONALIZADO")
            if _cancelled(option):
                return
            if not option:
                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            elif not re.fullmatch(r"[0-9]+", option):
                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
            elif (option != "1") and (option != "2"):
                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
            else:
                break
        if option == "1":
            while True:
                type = ASK("[1]DIA [2]MÊS [3]ANO")
                if _cancelled(type):
                    return
                if not type:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                elif not re.fullmatch(r"[0-9]+", type):
                    ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                elif (type != "1") and (type != "2") and (type != "3"):
                    ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                else:
                    break
            if type == "1":
                while True:
                    trans_exist = False
                    trans_list = []
                    new_trans = []
                    raw_day = ASK("DIGITE O DIA ESPECÍFICO QUE QUER PROCURAR (YYYY-MM-DD):")
                    if _cancelled(raw_day):
                        return
                    day = date_verf(raw_day)
                    RULE()
                    for trans in transactions:
                        if trans["date"] == day:
                            trans_list.append(trans)
                            trans_exist = True
                        else:
                            new_trans.append(trans)
                    _list_with_table(trans_list)
                    RULE()
                    if not trans_exist:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                        continue
                    if trans_exist == True:
                        while True:  
                            choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA DELETAR:")
                            if _cancelled(choice):
                                return
                            if not choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(choice) > len(trans_list) or int(choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                        for i, trans in enumerate(trans_list):
                            if i == (int(choice)-1):
                                RULE()
                                print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                                            ))
                                RULE()
                            else:
                                new_trans.append(trans)
                        while True:
                            confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA DELETAR [S/N]?").upper()
                            if _cancelled(confimation):
                                return
                            if not confimation:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                                ERROR("DIGITE SOMENTE LETRAS!")
                            elif not (confimation == "S" or confimation == "N"):
                                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                            else:
                                break
                        if confimation == "S":
                            OK("TRANSAÇÃO DELETADA!")
                            new_db(DB_PATH, new_trans)
                            return
                        elif confimation == "N":
                            continue

            elif type == "2":
                while True:
                    trans_exist = False
                    year_exist = False
                    new_trans = []
                    trans_list = []
                    raw_y = ASK("DIGITE O ANO QUE VOCÊ QUER VER OS MESES:")
                    if _cancelled(raw_y):
                        return
                    choice_year = year_verf(raw_y)
                    raw_m = ASK("DIGITE O MÊS QUE VOCÊ QUER VER:")
                    if _cancelled(raw_m):
                        return
                    choice_mon = (month_verf(raw_m)).lstrip("0")
                    RULE()
                    rows = []
                    for trans in transactions:
                        year = datetime.datetime.fromisoformat(trans["date"]).year
                        if str(choice_year) == str(year):
                            year_exist = True
                            month = datetime.datetime.fromisoformat(trans["date"]).month
                            if str(choice_mon) == str(month):
                                trans_exist = True
                                rows.append(trans)
                            else:
                                new_trans.append(trans)
                        else:
                            new_trans.append(trans)
                    if year_exist and rows:
                        trans_table(rows)
                        trans_list = rows
                    if not year_exist:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                        continue
                    elif not trans_exist:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                        continue
                    if trans_exist == True:
                        while True:  
                            choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA DELETAR:")
                            if _cancelled(choice):
                                return
                            if not choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(choice) > len(trans_list) or int(choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                        for i, trans in enumerate(trans_list):
                            if i == (int(choice)-1):
                                RULE()
                                print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                                            ))
                                RULE()
                            else:
                                new_trans.append(trans)
                        while True:
                            confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA DELETAR [S/N]?").upper()
                            if _cancelled(confimation):
                                return
                            if not confimation:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                                ERROR("DIGITE SOMENTE LETRAS!")
                            elif not (confimation == "S" or confimation == "N"):
                                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                            else:
                                break
                        if confimation == "S":
                            OK("TRANSAÇÃO DELETADA!")
                            new_db(DB_PATH, new_trans)
                            return
                        elif confimation == "N":
                            continue

            elif type == "3":
                while True:
                    trans_exist = False
                    trans_list = []
                    new_trans = []
                    raw_y2 = ASK("DIGITE O ANO QUE VOCÊ QUER VER AS TRANSAÇÕES:")
                    if _cancelled(raw_y2):
                        return
                    choice_year = year_verf(raw_y2)
                    RULE()
                    for trans in transactions:
                        year = datetime.datetime.fromisoformat(trans["date"]).year
                        if str(choice_year) == str(year):
                            trans_list.append(trans)
                            trans_exist = True
                        else:
                            new_trans.append(trans)
                    _list_with_table(trans_list)
                    RULE()
                    if not trans_exist:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                        continue
                    if trans_exist == True:
                        while True:  
                            choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA DELETAR:")
                            if _cancelled(choice):
                                return
                            if not choice:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[0-9]+", choice):
                                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                            elif int(choice) > len(trans_list) or int(choice) < 1:
                                ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                            else:
                                break
                        for i, trans in enumerate(trans_list):
                            if i == (int(choice)-1):
                                RULE()
                                print(Transaction(
                                trans["type"],
                                trans["value"],
                                trans["category"],
                                trans["description"],
                                trans["date"]
                                            ))
                                RULE()
                            else:
                                new_trans.append(trans)
                        while True:
                            confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA DELETAR [S/N]?").upper()
                            if _cancelled(confimation):
                                return
                            if not confimation:
                                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                            elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                                ERROR("DIGITE SOMENTE LETRAS!")
                            elif not (confimation == "S" or confimation == "N"):
                                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                            else:
                                break
                        if confimation == "S":
                            OK("TRANSAÇÃO DELETADA!")
                            new_db(DB_PATH, new_trans)
                            return
                        elif confimation == "N":
                            continue

        elif option == "2":
            while True:
                trans_exist = False
                trans_list = []
                new_trans = []
                # Perguntas do intervalo personalizado
                raw_si = ASK("DIGITE A DATA INICIAL (YYYY-MM-DD):")
                if _cancelled(raw_si):
                    return
                start_iso = date_verf(raw_si)
                raw_ei = ASK("DIGITE A DATA FINAL (YYYY-MM-DD):")
                if _cancelled(raw_ei):
                    return
                end_iso = date_verf(raw_ei)

                # Converte para date para validar ordem e normalizar
                start_date = datetime.date.fromisoformat(start_iso)
                end_date = datetime.date.fromisoformat(end_iso)

                # Normaliza caso o usuário tenha invertido
                if end_date < start_date:
                    start_date, end_date = end_date, start_date
                
                RULE()
                for trans in transactions:
                    if (end_date >= datetime.date.fromisoformat(trans["date"]) >= start_date):
                        trans_list.append(trans)
                        trans_exist = True
                    else:
                        new_trans.append(trans)
                _list_with_table(trans_list)
                RULE()
                if not trans_exist:
                    WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                    continue
                if trans_exist == True:
                    while True:  
                        choice = ASK("QUAL O NÚMERO DA TRANSAÇÃO QUE DESEJA DELETAR:")
                        if _cancelled(choice):
                            return
                        if not choice:
                            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                        elif not re.fullmatch(r"[0-9]+", choice):
                            ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                        elif int(choice) > len(trans_list) or int(choice) < 1:
                            ERROR("DIGITE UM DOS NÚMEROS MOSTRADOS!")
                        else:
                            break
                    for i, trans in enumerate(trans_list):
                        if i == (int(choice)-1):
                            RULE()
                            print(Transaction(
                            trans["type"],
                            trans["value"],
                            trans["category"],
                            trans["description"],
                            trans["date"]
                                        ))
                            RULE()
                        else:
                            new_trans.append(trans)
                    while True:
                        confimation = ASK("ESSA É A TRANSAÇÃO QUE VOCÊ DESEJA DELETAR [S/N]?").upper()
                        if _cancelled(confimation):
                            return
                        if not confimation:
                            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", confimation):
                            ERROR("DIGITE SOMENTE LETRAS!")
                        elif not (confimation == "S" or confimation == "N"):
                            ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                        else:
                            break
                    if confimation == "S":
                        OK("TRANSAÇÃO DELETADA!")
                        new_db(DB_PATH, new_trans)
                        return
                    elif confimation == "N":
                        continue

def deleteall():
    transactions = db_confirm()
    if transactions == None:
        return
    
    while True:
        confirm = ASK("TEM CERTEZA QUE DESEJA DELETAR TODAS AS TRANSAÇÕES [S]/[N]?").upper()
        if _cancelled(confirm):
            return
        if confirm == "S":
            trans_empty = []
            new_db(DB_PATH, trans_empty)
            OK("TRANSAÇÕES DELETADAS!")
            break
        elif confirm == "N":
            WARN("NENHUMA TRANSAÇÃO DELETADA!")
            break
        elif not confirm:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        else:
            ERROR("DIGITE UM CARACTERE VÁLIDO!")
       
def find_trans():
    transactions = db_confirm()
    if transactions is None:
        return
    HEADER("BUSCAR TRANSAÇÕES")
    cat_list = []
    trans_exist = False
    year_exist = False
    while True:
        choice = ASK("COMO VOCÊ DESEJA PROCURAR SUA TRANSAÇÃO? [1]VALOR [2]CATEGORIA [3]DATA")
        if _cancelled(choice):
            return
        if not choice:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        elif not re.fullmatch(r"[0-9]+", choice):
            ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
        elif (choice != "1") and (choice != "2") and (choice != "3"):
            ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
        else:
            break
    if choice == "1":
        while True:
            option = ASK("PESQUISAR POR: [1]VALOR [2]INTERVALO")
            if _cancelled(option):
                return
            if not option:
                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            elif not re.fullmatch(r"[0-9]+", option):
                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
            elif (option != "1") and (option != "2"):
                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
            else:
                break
        if option == "1":
            while True:
                trans_list = []
                trans_exist = False
                raw = ASK("DIGITE O VALOR QUE QUEIRA PROCURAR:")
                if _cancelled(raw):
                    return
                value = value_verf(raw)
                if value == "-1":
                    WARN("OPERAÇÃO CANCELADA!")
                    return
                RULE()
                print("")
                for trans in transactions:
                    if trans["value"] == value:
                        trans_exist = True
                trans_table([t for t in transactions if t["value"] == value])
                if not trans_exist:
                    WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                RULE()
                if trans_exist:
                    break

        elif option == "2":  
            while True:
                trans_list = []
                trans_exist = False
                raw_h = ASK("O VALOR É MAIOR QUE:")
                if _cancelled(raw_h):
                    return
                higher = value_verf_float(raw_h)
                if higher == "-1":
                    WARN("OPERAÇÃO CANCELADA!")
                    return
                raw_l = ASK("O VALOR É MENOR QUE:")
                if _cancelled(raw_l):
                    return
                lower = value_verf_float(raw_l)
                if lower == "-1":
                    WARN("OPERAÇÃO CANCELADA!")
                    return
                RULE()
                print("")
                for trans in transactions:
                    val = float(str(trans["value"]).replace("R$", "").replace(".", "").replace(",", ".").strip())
                    if (val > higher) and (val < lower):
                        trans_exist = True
                rows = [t for t in transactions if float(str(t["value"]).replace("R$", "").replace(".", "").replace(",", ".").strip()) > higher and float(str(t["value"]).replace("R$", "").replace(".", "").replace(",", ".").strip()) < lower]
                if rows:
                    trans_table(rows)
                if not trans_exist:
                    WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                RULE()
                if trans_exist:
                    break

    elif choice == "2": #tem forma melhor de organizar/separar despesa e receita? aperfeicoar organizacao (cronologicamente)
        while True:
            trans_list = []
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
                choice = ASK("DE QUAL CATEGORIA VOCÊ QUER VER AS TRANSAÇÕES:")
                if _cancelled(choice):
                    return
                if not choice:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                elif not re.fullmatch(r"[0-9]+", choice):
                    ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                elif (int(choice) > len(cat_list)) or (int(choice) <= 0):
                    ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                else:
                    break   
            RULE()
            print("")
            for i, cat in enumerate(cat_list):
                if i == (int(choice)-1):
                    rows = [t for t in transactions if t["category"] == cat]
                    trans_exist = bool(rows)
                    if rows:
                        trans_table(rows)
            if not trans_exist:
                WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
            RULE()
            if trans_exist:
                break
            
    elif choice == "3":
        while True:
            option = ASK("PESQUISAR POR: [1]DIA/MÊS/ANO [2]PERÍODO PERSONALIZADO")
            if _cancelled(option):
                return
            if not option:
                ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            elif not re.fullmatch(r"[0-9]+", option):
                ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
            elif (option != "1") and (option != "2"):
                ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
            else:
                break
        if option == "1":
            while True:
                type = ASK("[1]DIA [2]MÊS [3]ANO")
                if _cancelled(type):
                    return
                if not type:
                    ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
                elif not re.fullmatch(r"[0-9]+", type):
                    ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
                elif (type != "1") and (type != "2") and (type != "3"):
                    ERROR("DIGITE UMA DAS OPÇÕES DADAS!")
                else:
                    break
            if type == "1":
                while True:
                    raw_day = ASK("DIGITE O DIA ESPECÍFICO QUE QUER PROCURAR (YYYY-MM-DD):")
                    if _cancelled(raw_day):
                        return
                    day = date_verf(raw_day)
                    RULE()
                    rows = [t for t in transactions if t["date"] == day]
                    if rows:
                        trans_table(rows)
                        break
                    else:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                        RULE()
                        continue
            elif type == "2":
                while True:
                    year_exist = False
                    raw_y = ASK("DIGITE O ANO QUE VOCÊ QUER VER OS MESES:")
                    if _cancelled(raw_y):
                        return
                    choice_year = year_verf(raw_y)
                    raw_m = ASK("DIGITE O MÊS QUE VOCÊ QUER VER:")
                    if _cancelled(raw_m):
                        return
                    choice_mon = (month_verf(raw_m)).lstrip("0")
                    RULE()
                    rows = []
                    for trans in transactions:
                        year = datetime.datetime.fromisoformat(trans["date"]).year
                        if str(choice_year) == str(year):
                            year_exist = True
                            month = datetime.datetime.fromisoformat(trans["date"]).month
                            if str(choice_mon) == (str(month)):
                                rows.append(trans)
                    if not year_exist:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                    elif not rows:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                    else:
                        trans_table(rows)
                        break
                    RULE()
                    continue
            elif type == "3":
                while True:
                    raw_y2 = ASK("DIGITE O ANO QUE VOCÊ QUER VER AS TRANSAÇÕES:")
                    if _cancelled(raw_y2):
                        return
                    choice_year = year_verf(raw_y2)
                    RULE()
                    rows = []
                    for trans in transactions:
                        year = datetime.datetime.fromisoformat(trans["date"]).year
                        if str(choice_year) == str(year):
                            rows.append(trans)
                    if rows:
                        trans_table(rows)
                        break
                    else:
                        WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                        RULE()
                        continue
        elif option == "2":
            while True:
                trans_list = []
                raw_si = ASK("DIGITE A DATA INICIAL (YYYY-MM-DD):")
                if _cancelled(raw_si):
                    return
                start_iso = date_verf(raw_si)
                raw_ei = ASK("DIGITE A DATA FINAL (YYYY-MM-DD):")
                if _cancelled(raw_ei):
                    return
                end_iso = date_verf(raw_ei)
                start_date = datetime.date.fromisoformat(start_iso)
                end_date = datetime.date.fromisoformat(end_iso)
                if end_date < start_date:
                    start_date, end_date = end_date, start_date
                RULE()
                for trans in transactions:
                    if (end_date >= datetime.date.fromisoformat(trans["date"]) >= start_date):
                        trans_list.append(trans)
                if trans_list:
                    trans_table(trans_list)
                    break
                else:
                    WARN("NENHUMA TRANSAÇÃO ENCONTRADA!")
                    RULE()
                    continue
           
def random():
    # 1. Definir a lista de transações fornecida pelo usuário
    transactions = [
     {
          "type": "Receita",
          "value": "R$1.400,00",
          "category": "Salário",
          "description": "Mesada",
          "date": "2025-08-11"
     },
     {
          "type": "Receita",
          "value": "R$50,00",
          "category": "Dividendos",
          "description": "investimentos",
          "date": "2025-08-10"
     },
     {
          "type": "Receita",
          "value": "R$20,00",
          "category": "Empréstimo",
          "description": "peguei emprestado com ferreira",
          "date": "2024-12-15"
     },
     {
          "type": "Receita",
          "value": "R$90,00",
          "category": "Outros",
          "description": "tigrinho",
          "date": "2023-07-01"
     },
     {
          "type": "Receita",
          "value": "R$700,00",
          "category": "Salário",
          "description": "parte do salário",
          "date": "2024-02-28"
     },
     {
          "type": "Receita",
          "value": "R$40,00",
          "category": "Dividendos",
          "description": "renda passiva",
          "date": "2023-11-05"
     },
     {
          "type": "Receita",
          "value": "R$120,00",
          "category": "Outros",
          "description": "venda usada",
          "date": "2025-01-20"
     },
     {
          "type": "Receita",
          "value": "R$80,00",
          "category": "Dividendos",
          "description": "rendimentos",
          "date": "2024-08-11"
     },
     {
          "type": "Despesa",
          "value": "R$120,00",
          "category": "Lazer",
          "description": "Cinema",
          "date": "2025-08-11"
     },
     {
          "type": "Despesa",
          "value": "R$200,00",
          "category": "Alimentação",
          "description": "Mercado do mês",
          "date": "2025-08-10"
     },
     {
          "type": "Despesa",
          "value": "R$45,00",
          "category": "Transporte",
          "description": "Ônibus/cartão",
          "date": "2024-12-16"
     },
     {
          "type": "Despesa",
          "value": "R$250,00",
          "category": "Saúde",
          "description": "Consulta",
          "date": "2023-07-02"
     },
     {
          "type": "Despesa",
          "value": "R$40,00",
          "category": "Célula",
          "description": "Lanche do grupo",
          "date": "2024-03-01"
     },
     {
          "type": "Despesa",
          "value": "R$220,00",
          "category": "Alimentação",
          "description": "Restaurante",
          "date": "2024-02-28"
     },
     {
          "type": "Despesa",
          "value": "R$90,00",
          "category": "Transporte",
          "description": "Combustível",
          "date": "2023-11-06"
     },
     {
          "type": "Despesa",
          "value": "R$150,00",
          "category": "Lazer",
          "description": "Passeio",
          "date": "2025-01-21"
     },
     {
          "type": "Despesa",
          "value": "R$37,00",
          "category": "Alimentação",
          "description": "Hamburguer",
          "date": "2025-08-09"
     },
     {
          "type": "Despesa",
          "value": "R$13,75",
          "category": "Transporte",
          "description": "Uber",
          "date": "2025-08-08"
     },
     {
          "type": "Despesa",
          "value": "R$70,00",
          "category": "Saúde",
          "description": "Remédios",
          "date": "2024-12-20"
     },
     {
          "type": "Despesa",
          "value": "R$584,25",
          "category": "Outros",
          "description": "Ajuste de despesas",
          "date": "2023-10-10"
     }
]

    # 4. Salvar tudo novamente usando new_db(DB_PATH, lista_atualizada)
    new_db(DB_PATH, transactions)
    # 5. Imprimir uma mensagem confirmando a geração
    OK("TRANSAÇÕES DE EXEMPLO GERADAS E SALVAS EM financeiro.json")