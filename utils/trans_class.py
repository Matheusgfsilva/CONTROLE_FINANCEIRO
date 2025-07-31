class Transaction:
    def __init__(self, type, value, category, discription, date):
        self.type = type
        self.value = value
        self.category = category
        self.discription = discription
        self.date = date

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "category": self.category,
            "discription": self.discription,
            "date": self.date
        }
    
    def __str__(self):
        return (
            f"Tipo: {self.type}\n"
            f"Valor: {self.value}\n"
            f"Categoria: {self.category}\n"
            f"Descrição: {self.discription}\n"
            f"Data: {self.date}"
        )