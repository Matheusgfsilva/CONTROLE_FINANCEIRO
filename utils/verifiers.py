import re
import datetime
def value_verf(val):
    while True:
        val = str(val).replace(",", ".").strip()

        # Verifica se há mais de um ponto
        if val.count(".") > 1:
            print("Número inválido: não use mais de um ponto decimal.")
        elif not val:
            print("O campo não pode ficar vazio!")
        else:
            try:
                numero = float(val)
                if numero <= 0:
                    print("Digite um número positivo!")
                else:
                    new_val = f"R${numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    return new_val
            except ValueError:
                print("Digite um valor numérico válido!")

        val = input("Valor: ")

def value_verf_float(val):
    while True:
        val = str(val).replace(",", ".").strip()

        # Verifica se há mais de um ponto
        if val.count(".") > 1:
            print("Número inválido: não use mais de um ponto decimal.")
        elif not val:
            print("O campo não pode ficar vazio!")
        else:
            try:
                numero = float(val)
                if numero < 0:
                    print("Digite um número positivo!")
                else:
                    return float(val)
            except ValueError:
                print("Digite um valor numérico válido!")

        val = input("Valor: ")

def month_verf():
    while True:
        mon = input("Digite o mês que a transação foi feita(1=janeiro...): ").strip() 
        if not mon:
            print("O campo não pode ficar vazio!")
        elif not re.fullmatch(r"[0-9]+", mon):
            print("Digite somente números inteiros!")
        elif not (int(mon) >= 1 and int(mon) <= 12 and int(mon) > 0):
            print("Digite um número que corresponda á um mês!")
        else:
            return mon
     
def type_verf():
    while True:
        type = input("Digite o novo tipo de transação(Receita/Despesa): ").capitalize().strip()
        if not type:
            print("O campo não pode ficar vazio!")
        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", type):
            print("Digite somente letras!")
        elif not (type == "Receita" or type == "Despesa"):
            print("Digite uma das opções dadas(Receira/Despesa)")
        else:
            return type
     
def date_verf(date):
    while True:
        print("Data: ")
        if not date:
            print("O campo não pode ficar vazio!")
        elif not re.fullmatch(r"[0-9 /-]+", date):
            print("Digite somente carateres válidos!")
        else:
            try:
                date = re.sub(r"[ /]", "-", date)
                ano, mes, dia = map(int, date.split("-"))
                if not (1 <= dia <= 31):
                    print("Dia inválido. Deve estar entre 1 e 31.")
                    continue
                elif not (1 <= mes <= 12):
                    print("Mês inválido. Deve estar entre 1 e 12.")
                    continue
                new_date = datetime.date(ano, mes, dia)
                if new_date > datetime.date.today():
                    print("A data não pode estar no futuro.")
                    continue
                return(new_date.isoformat())
            except ValueError as e:
                print(f"Data inválida")
