from utils.transacoes import revenue, expense, edit_trans, deleteone, deleteall, find_trans, random
from utils.relatorios import balance
from utils.classificacao import edit_cat


while True:
    print("\n========= CONTROLE FINANCEIRO =========")
    print("Saldo: ", end=""), balance()
    print("[0] GERAR TRANSAÇÕES ALEATÓRIAS")
    print("\n[1] RECEITA")
    print("[2] DESPESA") 
    print("[3] RELATÓRIO")
    print("[4] EDITAR TRANSAÇÃO")
    print("[5] LISTAR TRANSAÇÃO")
    print("[6] DELETAR UMA TRANSAÇÃO")
    print("[7] DELETAR TODAS TRANSAÇÕES")
    print("[8] EDITAR CATEGORIAS")
    print("[9] SAIR")
    print("(sempre digite \"-1\" para interromper um processo)\n")
    choice = input("Digite: ").strip()

    if choice == "0":
        random()
    elif choice == "1":
        revenue()
    elif choice == "2":
        expense()
    elif choice == "3":
        print("3")
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
        print("OBRIGADO PELA PREFERÊNCIA!")
        break
    elif not choice:
        print("O campo não pode ficar vazio")
    else:
        print("Digite um carctere válido!")