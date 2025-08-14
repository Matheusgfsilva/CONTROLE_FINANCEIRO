import re
import datetime
from utils.ui import ERROR, WARN, OK, ASK


def quit(value: str) -> bool:
    """Retorna True se o usuário digitou -1. Não exibe mensagens."""
    return str(value).strip() == "-1"

def _cancelled(value) -> bool:
    """Retorna True se o usuário digitou -1 e exibe um aviso padronizado."""
    if quit(value):
        WARN("OPERAÇÃO CANCELADA!")
        return True
    return False


def value_verf(val):
    """Valida valor monetário e retorna string formatada em BR: R$1.234,56.
    Aceita vírgula ou ponto como separador decimal. Usa -1 para cancelar.
    """
    while True:
        # leitura e cancelamento
        val = str(val).strip()
        if quit(val):
            return val

        # normaliza separador decimal
        s = val.replace(",", ".")
        if not s:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        elif s.count(".") > 1:
            ERROR("NÚMERO INVÁLIDO: NÃO USE MAIS DE UM PONTO DECIMAL.")
        else:
            try:
                numero = float(s)
                if numero <= 0:
                    ERROR("DIGITE UM NÚMERO POSITIVO!")
                else:
                    # formata BR: R$1.234,56
                    new_val = f"R${numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    return new_val
            except ValueError:
                ERROR("DIGITE UM VALOR NUMÉRICO VÁLIDO!")

        val = ASK("VALOR:")


def value_verf_float(val):
    """Valida valor numérico e retorna float positivo. Usa -1 para cancelar."""
    while True:
        val = str(val).strip()
        if quit(val):
            return val

        s = val.replace(",", ".")
        if not s:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        elif s.count(".") > 1:
            ERROR("NÚMERO INVÁLIDO: NÃO USE MAIS DE UM PONTO DECIMAL.")
        else:
            try:
                numero = float(s)
                if numero < 0:
                    ERROR("DIGITE UM NÚMERO POSITIVO!")
                else:
                    return numero
            except ValueError:
                ERROR("DIGITE UM VALOR NUMÉRICO VÁLIDO!")

        val = ASK("VALOR (NÚMERO):")


def month_verf(mon):
    """Valida mês (1–12). Retorna string zero-padded (01..12). Usa -1 para cancelar."""
    while True:
        mon = str(mon).strip()
        if quit(mon):
            return mon

        if not mon:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        elif not mon.isdigit():
            ERROR("DIGITE SOMENTE NÚMEROS NATURAIS!")
        else:
            m = int(mon)
            if not (1 <= m <= 12):
                ERROR("DIGITE UM NÚMERO QUE CORRESPONDA A UM MÊS (1–12)!")
            else:
                return str(m).zfill(2)

        mon = ASK("DIGITE O MÊS (1–12):")


def year_verf(year):
    """Valida ano (1–4 dígitos) e retorna string zero-padded (0001..YYYY). Não aceita futuro."""
    while True:
        year = str(year).strip()
        if quit(year):
            return year

        if not year:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        elif not re.fullmatch(r"\d{1,4}", year):
            ERROR("DIGITE UM ANO VÁLIDO (ATÉ 4 DÍGITOS)!")
        else:
            try:
                ano = int(year)
                ano_atual = datetime.date.today().year
                if ano < 1 or ano > ano_atual:
                    ERROR("ANO INVÁLIDO! DEVE SER ENTRE 0001 E O ANO ATUAL.")
                else:
                    return str(ano).zfill(4)
            except ValueError:
                ERROR("ERRO AO PROCESSAR O ANO.")

        year = ASK("DIGITE O ANO (YYYY):")


def type_verf():
    """Valida tipo de transação e retorna 'Receita' ou 'Despesa'. Usa -1 para cancelar."""
    while True:
        t = ASK("TIPO [1] RECEITA / [2] DESPESA:").capitalize()
        if quit(t):
            return t

        if not t:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
        elif not re.fullmatch(r"[A-Za-zÀ-ÿ\s12]+", t):
            ERROR("DIGITE SOMENTE LETRAS OU AS OPÇÕES 1/2!")
        else:
            if t in ("1", "Receita"):
                return "Receita"
            if t in ("2", "Despesa"):
                return "Despesa"
            ERROR("DIGITE UMA DAS OPÇÕES DADAS (1/2) OU OS NOMES RECEITA/DESPESA!")


def date_verf(date):
    """Valida data, aceita separadores espaço/barra/hífen e retorna ISO YYYY-MM-DD. Usa -1 para cancelar."""
    while True:
        date = str(date).strip()
        if quit(date):
            return date

        if not date:
            ERROR("O CAMPO NÃO PODE FICAR VAZIO!")
            date = ASK("DATA (YYYY-MM-DD):")
            continue

        # normaliza separadores (espaço ou barra -> hífen)
        s = re.sub(r"[ /]", "-", date)
        if not re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", s):
            ERROR("FORMATO INVÁLIDO! USE YYYY-MM-DD.")
            date = ASK("DATA (YYYY-MM-DD):")
            continue

        try:
            ano, mes, dia = map(int, s.split("-"))
            if not (1 <= mes <= 12):
                ERROR("MÊS INVÁLIDO! DEVE SER ENTRE 1 E 12.")
                date = ASK("DATA (YYYY-MM-DD):")
                continue
            if not (1 <= dia <= 31):
                ERROR("DIA INVÁLIDO! DEVE SER ENTRE 1 E 31.")
                date = ASK("DATA (YYYY-MM-DD):")
                continue

            new_date = datetime.date(ano, mes, dia)
            if new_date > datetime.date.today():
                ERROR("A DATA NÃO PODE ESTAR NO FUTURO.")
            else:
                return new_date.isoformat()
        except ValueError:
            ERROR("DATA INVÁLIDA!")

        date = ASK("DATA (YYYY-MM-DD):")