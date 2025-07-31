from utils.arquivos import db_confirm

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
    print(balance)

print("OI")