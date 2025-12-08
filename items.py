from time import sleep


# 목표금액 상수 추가
GOAL_MONEY = 1000000

# 아이템 클래스
class Item:
    def __init__(self, name, base_price, max_quantity, icon=None, max_price=0, min_price=0, Volatility =0.0):
        self.name = name
        self.base_price = base_price
        self.max_quantity = max_quantity
        self.current_price = base_price
        self.icon = icon  # 파일명
        self.max_price = max_price
        self.min_price = min_price
        self.Volatility = Volatility

    def set_price(self, price):
        self.current_price = price


class PlayerInventory:
    def __init__(self):
        # 아이템 이름을 키로, 값은 수량으로 저장
        self.items = {}
        self.own_money = 100000  # 초기 자금

    def add_item(self, item_name, quantity):
        cur = self.items.get(item_name, 0)
        self.items[item_name] = cur + quantity

    def remove_item(self, item_name, quantity):
        cur = self.items.get(item_name, 0)
        new_q = max(cur - quantity, 0)
        if new_q == 0 and item_name in self.items:
            del self.items[item_name]
        else:
            self.items[item_name] = new_q

    def set_quantity(self, item_name, quantity):
        if quantity <= 0:
            if item_name in self.items:
                del self.items[item_name]
        else:
            self.items[item_name] = quantity

    def get_quantity(self, item_name):
        return self.items.get(item_name, 0)

    def get_money(self):
        return self.own_money

    # 게임승리 소지금 설정 (버그 수정: 원치않는 덮어쓰기 제거)
    def set_money(self, amount):
        self.own_money = amount


# 카탈로그: item.1 ~ item.6에 해당하는 아이템 정의
CATALOG = [
    Item('수저', 7500, 10, icon='item.1.png', max_price = 5000, min_price = 1000, Volatility = 0.1),
    Item('휴지', 5000, 10, icon='item.2.png', max_price = 5000, min_price = 5000, Volatility = 0.05),
    Item('옷', 5000, 10, icon='item.3.png', max_price = 99000, min_price = 1000, Volatility = 0.2),
    Item('모자', 5000, 10, icon='item.4.png', max_price = 99000, min_price = 1000, Volatility = 0.15),
    Item('의자', 75000, 10, icon='item.5.png', max_price = 100000, min_price = 50000, Volatility = 0.25),
    Item('돌하르방', 100000, 10, icon='item.6.png', max_price = 5000000, min_price = 100, Volatility = 0.3),
]

# 플레이어 인벤토리 싱글턴 인스턴스
player_inventory = PlayerInventory()
# 초기 수량 0으로 세팅(명시적)
for it in CATALOG:
    player_inventory.set_quantity(it.name, 0)

# 헬퍼 함수
def get_catalog():
    return CATALOG

def get_item_by_index(idx):
    if 0 <= idx < len(CATALOG):
        return CATALOG[idx]
    return None

def get_price(item_name):
    for it in CATALOG:
        if it.name == item_name:
            return it.current_price
    return None

def set_price(item_name, price):
    for it in CATALOG:
        if it.name == item_name:
            it.set_price(price)
            return True
    return False

def get_quantity(item_name):
    return player_inventory.get_quantity(item_name)

def set_quantity(item_name, quantity):
    player_inventory.set_quantity(item_name, quantity)
    return True

# 현재 소지 금액을 반환하는 헬퍼
def get_money():
    return player_inventory.get_money()

def set_money(amount):
    player_inventory.set_money(amount)

# 목표금액 조회 함수
def get_goal():
    return GOAL_MONEY


