from utils.arquivos import db_confirm
from utils.ui import OK, ERROR, WARN, HEADER, RULE, ASK
import json
import os
from datetime import datetime
from collections import defaultdict
from rich.table import Table, Column
from rich.console import Console
from utils.verifiers import _cancelled

import math

console = Console()

# Largura fixa suficiente para moedas como R$1.234.567,89 sem truncar
COL_WIDTH = 14

def _compute_page_capacity(console_width: int) -> int:
    """Calcula quantas colunas de categorias cabem por tabela.
    Mantém 4 colunas fixas (Ano/Mês, Receitas, Despesas, Saldo) e usa o restante
    como capacidade total para colunas de categorias (receita + despesa misturadas).
    """
    margin = 8
    fixed_cols = 4
    per_col = COL_WIDTH + 1  # margem para separadores
    available = max(0, console_width - margin - fixed_cols * per_col)
    total_cat_cols = max(1, available // per_col)  # pelo menos 1
    return total_cat_cols

def _parse_value(value_str):
    # Remove currency symbol and format to float
    value_str = str(value_str)
    value_str = value_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(value_str)
    except ValueError:
        return 0.0

def _format_value(value_float):
    # Format float to Brazilian currency format R$X.XXX,XX
    formatted = f"R${value_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted

def _load_categories(filename):
    # Resolve from project root (this file is in utils/)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, filename)
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return list(dict.fromkeys(data))
            elif isinstance(data, dict):
                return list(dict.fromkeys(list(data.keys())))
    except Exception:
        return []
    return []

def balance():
    balance = 0
    transactions = db_confirm()
    if transactions is None:
        return
    for transaction in transactions:
        float_value = str(transaction["value"])
        float_value = float(float_value.replace("R$", "").replace(".","").replace(",","."))
        
        if transaction["type"] == "Receita":
            balance += float_value
        elif transaction["type"] == "Despesa":
            balance -= float_value
        
    balance = f"R${float(balance):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    HEADER("SALDO ATUAL")
    OK(balance)

def relatory():
    transactions = db_confirm()
    if transactions is None:
        ERROR("Nenhuma transação encontrada.")
        return

    # Load categories
    cat_rev = _load_categories("cat_rev.json")
    cat_exp = _load_categories("cat_exp.json")

    # Preferir apenas um "Outros": manter o de despesas e remover de receitas se duplicado
    if "Outros" in cat_rev and "Outros" in cat_exp:
        cat_rev = [c for c in cat_rev if c != "Outros"]

    # Aggregate data by year and month
    # Structure: data[year][month][type][category] = sum_value
    data = defaultdict(lambda: defaultdict(lambda: {"Receita": defaultdict(float), "Despesa": defaultdict(float)}))

    # Also keep track of totals per year and month
    totals_year = defaultdict(lambda: {"Receita": 0.0, "Despesa": 0.0})
    totals_month = defaultdict(lambda: defaultdict(lambda: {"Receita": 0.0, "Despesa": 0.0}))

    for tr in transactions:
        date_str = tr.get("date", "")
        # Datas podem vir como YYYY-MM-DD (ISO) ou DD/MM/YYYY (BR)
        date_obj = None
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                date_obj = datetime.strptime(date_str, fmt)
                break
            except Exception:
                pass
        if date_obj is None:
            continue
        year = date_obj.year
        month = date_obj.month
        ttype = tr.get("type", "")
        category = tr.get("category", "")
        value = _parse_value(tr.get("value", 0))

        if ttype not in ("Receita", "Despesa"):
            continue

        data[year][month][ttype][category] += value
        totals_year[year][ttype] += value
        totals_month[year][month][ttype] += value

    # Totais anuais por categoria (para filtrar e ordenar colunas)
    cat_tot_rev = defaultdict(float)
    cat_tot_exp = defaultdict(float)
    for y in data:
        for m in data[y]:
            for c, v in data[y][m]["Receita"].items():
                cat_tot_rev[c] += v
            for c, v in data[y][m]["Despesa"].items():
                cat_tot_exp[c] += v

    # Mantém apenas categorias com algum valor (>0) e ordena desc
    rev_sorted_all = [c for c in cat_rev if cat_tot_rev.get(c, 0.0) > 0]
    exp_sorted_all = [c for c in cat_exp if cat_tot_exp.get(c, 0.0) > 0]
    rev_sorted_all.sort(key=lambda c: cat_tot_rev[c], reverse=True)
    exp_sorted_all.sort(key=lambda c: cat_tot_exp[c], reverse=True)

    # Sort years descending
    years_sorted = sorted(data.keys(), reverse=True)

    def _show_month_detail(ano_int) -> bool:
        """Exibe o detalhamento mensal para o ano informado.
        Retorna True se o usuário cancelar (-1) para encerrar o relatório por completo; False para voltar à visão anual.
        """
        HEADER(f"DETALHAMENTO DO ANO {ano_int}")
        now = datetime.now()
        max_month = 12 if ano_int != now.year else now.month

        # Totais por categoria apenas no ano escolhido (para filtrar e ordenar)
        cat_tot_rev_y = defaultdict(float)
        cat_tot_exp_y = defaultdict(float)
        for m in range(1, max_month+1):
            for c, v in data[ano_int][m]["Receita"].items():
                cat_tot_rev_y[c] += v
            for c, v in data[ano_int][m]["Despesa"].items():
                cat_tot_exp_y[c] += v

        rev_sorted_y = [c for c in cat_rev if cat_tot_rev_y.get(c, 0.0) > 0]
        exp_sorted_y = [c for c in cat_exp if cat_tot_exp_y.get(c, 0.0) > 0]
        rev_sorted_y.sort(key=lambda c: cat_tot_rev_y[c], reverse=True)
        exp_sorted_y.sort(key=lambda c: cat_tot_exp_y[c], reverse=True)

        # Paginação por categorias no detalhe mensal
        cap = _compute_page_capacity(console.size.width)
        combined = [("rev", c) for c in rev_sorted_y] + [("exp", c) for c in exp_sorted_y]
        pages = max(1, math.ceil(len(combined) / cap))

        # Saldo do ano
        saldo_acum_month = 0.0
        for m in range(1, max_month+1):
            r = totals_month[ano_int][m]["Receita"]
            d = totals_month[ano_int][m]["Despesa"]
            saldo_acum_month += (r - d)

        page = 0
        while True:
            start = page * cap
            end = (page + 1) * cap
            cols = combined[start:end]

            table_month = Table(show_lines=True, title=f"Resumo por Mês - {ano_int} (página {page+1}/{pages})")
            table_month.add_column("Mês", style="bold", justify="center")
            table_month.add_column("Receitas (R$)", justify="right", style="green")
            table_month.add_column("Despesas (R$)", justify="right", style="red")
            table_month.add_column("Saldo (R$)", justify="right", style="bold")

            for kind, cat in cols:
                style = "green" if kind == "rev" else "red"
                table_month.add_column(cat, justify="right", style=style, no_wrap=True, overflow="crop", width=COL_WIDTH)

            for m in range(1, max_month+1):
                r = totals_month[ano_int][m]["Receita"]
                d = totals_month[ano_int][m]["Despesa"]
                s = r - d
                row = [f"{m:02d}", _format_value(r), _format_value(d), _format_value(s)]
                for kind, cat in cols:
                    val = data[ano_int][m]["Receita" if kind == "rev" else "Despesa"].get(cat, 0.0)
                    row.append(_format_value(val) if val != 0 else _format_value(0.0))
                table_month.add_row(*row)

            row = ["Saldo do ano", "", "", _format_value(saldo_acum_month)]
            row.extend([""] * len(cols))
            table_month.add_row(*row)

            console.print(table_month)

            # Navegação do detalhe mensal, com opção de voltar
            if pages > 1:
                nav = ASK("[P] Próxima | [A] Anterior | [V] Voltar | número da página | -1 sair: ").strip()
            else:
                nav = ASK("[V] Voltar | -1 sair: ").strip()
            if _cancelled(nav):
                return True  # encerrar relatório
            if not nav or nav.lower() == "p":
                page = (page + 1) % pages
            elif nav.lower() == "a":
                page = (page - 1) % pages
            elif nav.lower() == "v":
                break  # voltar para visão anual
            elif nav.isdigit():
                num = int(nav)
                if 1 <= num <= pages:
                    page = num - 1
                else:
                    WARN("NÚMERO DE PÁGINA INVÁLIDO!")
            else:
                WARN("COMANDO INVÁLIDO!")

        RULE()
        OK(f"SALDO DO ANO {ano_int}: {_format_value(saldo_acum_month)}")
        RULE()
        return False  # voltar para visão anual

    # Annual summary table (paginada por categorias)
    HEADER("RELATÓRIO ANUAL")
    cap = _compute_page_capacity(console.size.width)
    # lista combinada com tipo para manter cor correta
    combined = [("rev", c) for c in rev_sorted_all] + [("exp", c) for c in exp_sorted_all]
    pages = max(1, math.ceil(len(combined) / cap))
    saldo_acumulado = 0.0
    for year in years_sorted:
        tot_r = totals_year[year]["Receita"]
        tot_d = totals_year[year]["Despesa"]
        saldo = tot_r - tot_d
        saldo_acumulado += saldo
    page = 0
    while True:
        # Seleciona fatia combinada de categorias para a página atual
        start = page * cap
        end = (page + 1) * cap
        cols = combined[start:end]

        table = Table(show_lines=True, title=f"Resumo por Ano (página {page+1}/{pages})")
        table.add_column("Ano", justify="center", style="bold")
        table.add_column("Receitas (R$)", justify="right", style="green")
        table.add_column("Despesas (R$)", justify="right", style="red")
        table.add_column("Saldo (R$)", justify="right", style="bold")

        for kind, cat in cols:
            style = "green" if kind == "rev" else "red"
            table.add_column(cat, justify="right", style=style, no_wrap=True, overflow="crop", width=COL_WIDTH)

        for year in years_sorted:
            tot_r = totals_year[year]["Receita"]
            tot_d = totals_year[year]["Despesa"]
            saldo = tot_r - tot_d
            row = [str(year), _format_value(tot_r), _format_value(tot_d), _format_value(saldo)]
            # valores por categoria para as colunas desta página
            for kind, cat in cols:
                val = 0.0
                for m in data[year]:
                    val += data[year][m]["Receita" if kind == "rev" else "Despesa"].get(cat, 0.0)
                row.append(_format_value(val) if val != 0 else _format_value(0.0))
            table.add_row(*row)

        # Linha de saldo acumulado (visível em todas as páginas)
        row = ["Saldo acumulado", "", "", _format_value(saldo_acumulado)]
        row.extend([""] * len(cols))
        table.add_row(*row)

        console.print(table)

        # Navegação entre páginas
        if pages > 1:
            nav = ASK("[P] Próxima | [A] Anterior | ANO (YYYY) para detalhar | número da página | -1 sair: ").strip()
        else:
            nav = ASK("ANO (YYYY) para detalhar | -1 sair: ").strip()
        if _cancelled(nav):
            return
        if not nav or nav.lower() == "p":  # Próxima
            page = (page + 1) % pages
        elif nav.lower() == "a":  # Anterior
            page = (page - 1) % pages
        elif nav.isdigit() and len(nav) == 4 and int(nav) in years_sorted:  # detalhar ano direto
            ano_int = int(nav)
            should_quit = _show_month_detail(ano_int)
            if should_quit:
                return
            # após voltar do detalhe, continua na visão anual
        elif nav.isdigit():
            num = int(nav)
            if 1 <= num <= pages:
                page = num - 1
            else:
                WARN("NÚMERO DE PÁGINA INVÁLIDO!")
        else:
            WARN("COMANDO INVÁLIDO!")
