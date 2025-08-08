import re
import datetime
def value_verf(val):
    while True:
        if val == "-1":
            return val
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
        if val == "-1":
            return val
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

def month_verf(mon):
    while True:
        if mon == "-1":
            return mon
        if not mon:
            print("O campo não pode ficar vazio!")
        elif not re.fullmatch(r"[0-9]+", mon):
            print("Digite somente números naturais!")
        elif not (int(mon) >= 1 and int(mon) <= 12 and int(mon) > 0):
            print("Digite um número que corresponda á um mês!")
        else:
            return mon
        mon = input("Digite o mês que a transação foi feita(1=janeiro...): ").strip() 

def year_verf(year):
    while True:
        if year == "-1":
            return year
        if not year:
            print("O campo não pode ficar vazio!")
        elif not re.fullmatch(r"\d{4}", year):
            print("Digite um ano com 4 dígitos!")
        else:
            try:
                ano = int(year)
                if ano < 1 or ano > datetime.date.today().year:
                    print("Ano inválido! Deve ser entre 0001 e o ano atual.")
                else:
                    # retorna um objeto date com 1º de janeiro do ano escolhido
                    return str(datetime.date(ano, 1, 1).isoformat()).replace("-01-01", "").lstrip("0")  # "YYYY-01-01"
            except ValueError:
                print("Erro ao processar o ano.")

        year = input("Digite o ano (YYYY): ").strip()

def type_verf():
    while True:
        type = input("Digite o novo tipo de transação(Receita/Despesa): ").capitalize().strip()
        if type == "-1":
            return type
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
        if date == "-1":
            return date
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
                    
                elif not (1 <= mes <= 12):
                    print("Mês inválido. Deve estar entre 1 e 12.")
                else:
                    new_date = datetime.date(ano, mes, dia)
                if new_date > datetime.date.today():
                    print("A data não pode estar no futuro.")
                else:
                    return(new_date.isoformat())
            except ValueError as e:
                print(f"Data inválida")
        date = input("Data(YYYY-MM-DD): ")

def quit(any):
    if any == "-1":
        print("\nOPERAÇÃO CANCELADA!")
        return True
    return False