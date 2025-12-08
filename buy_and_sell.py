import items

    # 구매 함수
def buy_item(item_name, quantity):
    item = next((it for it in items.CATALOG if it.name == item_name), None)
    if item is None:
        return False, "아이템이 존재하지 않습니다."

    total_price = item.current_price * quantity
    if items.player_inventory.get_money() < total_price:
        return False, "소지금이 부족합니다."

    current_qty = items.player_inventory.get_quantity(item_name)
    if current_qty + quantity > item.max_quantity:
        return False, "최대 수량을 초과합니다."

    # 구매 처리
    items.player_inventory.own_money -= total_price
    items.player_inventory.add_item(item_name, quantity)
    return True, "구매 성공!"

    # 판매 함수
def sell_item(item_name, quantity):
    item = next((it for it in items.CATALOG if it.name == item_name), None)
    if item is None:
        return False, "아이템이 존재하지 않습니다."

    current_qty = items.player_inventory.get_quantity(item_name)
    if current_qty < quantity:
        return False, "판매할 아이템 수량이 부족합니다."

    total_price = item.current_price * quantity

    # 판매 처리
    items.player_inventory.own_money += total_price
    items.player_inventory.remove_item(item_name, quantity)
    return True, "판매 성공!"

    # 변동성 반영 가격 조정
def adjust_item_prices():
    import random
    for item in items.CATALOG:
        volatility = item.Volatility
        if volatility > 0:
            change_percent = random.uniform(-volatility, volatility)
            new_price = int(item.current_price * (1 + change_percent))
            # 가격이 최소/최대 범위를 벗어나지 않도록 조정
            if item.min_price > 0:
                new_price = max(new_price, item.min_price)
            if item.max_price > 0:
                new_price = min(new_price, item.max_price)
            item.set_price(new_price)


