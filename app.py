from utils.transacoes import revenue, expense, edit_trans, deleteall
from utils.relatorios import balance
from utils.classificacao import edit_cat

while True:
    print("\n========= CONTROLE FINANCEIRO =========")
    print("Saldo atual: ", end=""), balance()
    print("\n[1] RECEITA")
    print("[2] DESPESA")
    print("[3] RELATÓRIO")
    print("[4] EDITAR TRANSAÇÃO")
    print("[5] PROCURAR TRANSAÇÃO")
    print("[6] DELETAR TODAS TRANSAÇÕES")
    print("[7] EDITAR CATEGORIAS")
    choice = input("Digite: ").strip()

    if choice == "1":
        revenue()
    elif choice == "2":
        expense()
    elif choice == "3":
        print("3")
    elif choice == "4":
        edit_trans()
    elif choice == "5":
        print("5")
    elif choice == "6":
        deleteall()
    elif choice == "7":
        edit_cat()
    elif not choice:
        print("O campo não pode ficar vazio")
    else:
        print("Digite um carctere válido!")