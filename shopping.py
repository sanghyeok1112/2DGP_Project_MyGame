class Item:
    def __init__(self):
        self.name = name                    #아이템 이름
        self.base_price = base_price        #아이템 기본 가격
        self.max_quantity = max_quantity    #아이템 최대 수량

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item, quantity):
        if item.name in self.items:
            if self.items[item.name] + quantity <= item.max_quantity:
                self.items[item.name] += quantity
            else:
                print(f"{item.max_quantity} 이상 {item.name}를 구매할 수 없습니다.")
        if item.name in self.items:
            self.items[item.name]['quantity'] += quantity
        else:
            self.items[item.name] = {'item': item, 'quantity': quantity}
            return True

    def remove_item(self, item, quantity):
        if item.name in self.items:
            if self.items[item.name] >= quantity:
                self.items[item.name] -= quantity
                if self.items[item.name] == 0:
                    del self.items[item.name]
            else:
                print(f"Not enough {item.name} to remove.")
        else:
            print(f"{item.name} not found in inventory.")

