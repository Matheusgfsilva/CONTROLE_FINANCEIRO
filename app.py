from utils.transacoes import revenue, expense, edit_trans, deleteone, deleteall, find_trans, random
from utils.relatorios import balance, relatory
from utils.classificacao import edit_cat
from utils.ui import HEADER, RULE, ASK, OK, ERROR, WARN, INFO

while True:
    HEADER("CONTROLE FINANCEIRO")
    balance()
    RULE()
    INFO("[0] GERAR TRANSAÇÕES ALEATÓRIAS")
    INFO("[1] RECEITA")
    INFO("[2] DESPESA")
    INFO("[3] RELATÓRIO")
    INFO("[4] EDITAR TRANSAÇÃO")
    INFO("[5] LISTAR TRANSAÇÃO")
    INFO("[6] DELETAR UMA TRANSAÇÃO")
    INFO("[7] DELETAR TODAS TRANSAÇÕES")
    INFO("[8] EDITAR CATEGORIAS")
    INFO("[9] SAIR")
    INFO("(SEMPRE DIGITE \"-1\" PARA INTERROMPER UM PROCESSO)")
    RULE()

    choice = ASK("DIGITE A OPÇÃO:")

    if choice == "0":
        random()
    elif choice == "1":
        revenue()
    elif choice == "2":
        expense()
    elif choice == "3":
        relatory()
    elif choice == "4":
        edit_trans()
    elif choice == "5":
        find_trans()
    elif choice == "6":
        deleteone()
    elif choice == "7":
        deleteall()
    elif choice == "8":
        edit_cat()
    elif choice == "9":
        OK("OBRIGADO PELA PREFERÊNCIA!")
        break
    elif not choice:
        ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
    else:
        ERROR("DIGITE UM CARACTERE VÁLIDO!")