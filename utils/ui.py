from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

console = Console()

# ===== mensagens (MAIÚSCULAS como você pediu) =====
def ERROR(msg: str):
    console.print(Panel(msg, title="ERRO", border_style="red"))
    console.print()  # espaço após erro

def OK(msg: str):
    console.print(f"[bold green]✓ {msg}[/]")
    console.print()

def WARN(msg: str):
    console.print(f"[yellow]⚠ {msg}[/]")
    console.print()

def INFO(msg: str = ""):
    console.print(msg)

def HEADER(title: str):
    console.print(Panel(f"[bold]{title}[/]", border_style="blue"))

def RULE(text: str = ""):
    console.print(Rule(text))

def ASK(prompt: str) -> str:
    # Devolve string já stripada
    return console.input(f"[cyan]{prompt}[/] ").strip()

# ===== componentes =====
def trans_table(rows):
    """rows: lista de dicts com chaves: type, value, category, description, date"""
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", justify="right", width=3)
    table.add_column("TIPO")
    table.add_column("VALOR", justify="right")
    table.add_column("CATEGORIA")
    table.add_column("DESCRIÇÃO")
    table.add_column("DATA", justify="center", width=12)

    for i, t in enumerate(rows, start=1):
        table.add_row(
            str(i),
            str(t.get("type", "")),
            str(t.get("value", "")),
            str(t.get("category", "")),
            str(t.get("description", "")),
            str(t.get("date", "")),
        )
    console.print(table)
    console.print()