class Product:
    quantity:int
    price_id:str
    name:str

    def __init__(self, name, price_id, quantity):
        self.name = name
        self.price_id = price_id
        self.quantity = quantity