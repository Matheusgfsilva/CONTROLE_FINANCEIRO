class Transaction:
    def __init__(self, type, value, category, description, date):
        self.type = type
        self.value = value
        self.category = category
        self.description = description
        self.date = date

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }
    
    def __str__(self):
        return (
            f"Tipo: {self.type}\n"
            f"Valor: {self.value}\n"
            f"Categoria: {self.category}\n"
            f"Descrição: {self.description}\n"
            f"Data: {self.date}"
        )