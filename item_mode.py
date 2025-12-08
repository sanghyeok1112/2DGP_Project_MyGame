from pico2d import *
import os
import game_framework
import game_world
import buy_and_sell
import items
from items import get_catalog, get_price, get_quantity

ui_image = None
item_images = []
font = None

# UI 상태
selected_index = 0
quantity = 1
message = ''
message_time = 0.0


def init():
    global ui_image, item_images, font, selected_index, quantity, message, message_time
    selected_index = 0
    quantity = 1
    message = ''
    message_time = 0.0

    try:
        ui_image = load_image('UI_default.png')
    except Exception:
        ui_image = None

    # item.1.png ~ item.6.png 로드 (개별 실패 무시)
    item_images = []
    for i in range(1, 7):
        fname = f'item.{i}.png'
        try:
            exists = os.path.exists(fname)
            img = load_image(fname) if exists else None
        except Exception:
            img = None
            exists = os.path.exists(fname)
        item_images.append(img)
        try:
            print(f'item_mode: load {fname} exists={exists} loaded={img is not None}')
        except Exception:
            pass

    # 폰트 로드: 프로젝트 TTF 우선, 없으면 시스템 폰트 또는 draw_string 폴백
    font = None
    try:
        if os.path.exists('NanumGothic.ttf'):
            font = load_font('NanumGothic.ttf', 14)
        else:
            win_malgun = r'C:\Windows\Fonts\malgun.ttf'
            win_nanumm = r'C:\Windows\Fonts\NanumGothic.ttf'
            if os.path.exists(win_nanumm):
                font = load_font(win_nanumm, 14)
            elif os.path.exists(win_malgun):
                font = load_font(win_malgun, 14)
            else:
                try:
                    font = load_font(None, 14)
                except Exception:
                    font = None
    except Exception:
        try:
            font = load_font(None, 12)
        except Exception:
            font = None

    # 디버그: 캔버스 크기와 카탈로그 정보 출력
    try:
        w = get_canvas_width()
        h = get_canvas_height()
        print(f'item_mode.init: canvas {w}x{h}, catalog_len={len(get_catalog())}')
    except Exception:
        try:
            print(f'item_mode.init: canvas unknown, catalog_len={len(get_catalog())}')
        except Exception:
            pass


def handle_events():
    global selected_index, quantity, message, message_time
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE or event.key == SDLK_e:
                game_framework.pop_mode()
                return

            # 선택 좌우 이동
            if event.key == SDLK_LEFT:
                selected_index = (selected_index - 1) % 6
                continue
            if event.key == SDLK_RIGHT:
                selected_index = (selected_index + 1) % 6
                continue

            # 수량 조절(위/아래)
            if event.key == SDLK_UP:
                quantity = min(99, quantity + 1)
                continue
            if event.key == SDLK_DOWN:
                quantity = max(1, quantity - 1)
                continue

            # 구매(B) / 판매(S)
            if event.key == SDLK_b:
                item_obj = items.get_item_by_index(selected_index)
                if item_obj:
                    ok, msg = buy_and_sell.buy_item(item_obj.name, quantity)
                    message = msg
                    message_time = get_time()
                continue
            if event.key == SDLK_s:
                item_obj = items.get_item_by_index(selected_index)
                if item_obj:
                    ok, msg = buy_and_sell.sell_item(item_obj.name, quantity)
                    message = msg
                    message_time = get_time()
                continue


def update():
    # 메시지 자동 소멸
    global message, message_time
    try:
        if message and get_time() - message_time > 2.5:
            message = ''
    except Exception:
        pass


def _safe_draw_text(f, x, y, text):
    try:
        if f:
            try:
                f.draw(int(x), int(y), str(text))
                return
            except Exception:
                try:
                    f.draw(int(x), int(y), str(text), (255, 255, 255))
                    return
                except Exception:
                    pass
        # 폰트가 없거나 위 호출이 실패하면 draw_string 사용 시도
        try:
            draw_string(int(x), int(y), str(text))
            return
        except Exception:
            return
    except Exception:
        return


def draw():
    clear_canvas()
    try:
        game_world.render()
    except Exception:
        pass

    try:
        w = get_canvas_width()
        h = get_canvas_height()
        cx = w // 2
        cy = h // 2
    except Exception:
        cx = 400
        cy = 300

    if ui_image is not None:
        try:
            ui_image.draw(cx, cy, 420, 320)
        except Exception:
            pass

    # 아이콘과 텍스트
    try:
        cols = 3
        rows = 2
        icon_w, icon_h = 64, 64
        spacing_x = 70
        spacing_y = 60

        total_w = cols * icon_w + (cols - 1) * spacing_x
        total_h = rows * icon_h + (rows - 1) * spacing_y

        start_x = (cx - total_w // 2 + icon_w // 2)
        start_y = (cy + total_h // 2 - icon_h // 2) + 50

        catalog = get_catalog()

        idx = 0
        sel_x = sel_y = None
        for r in range(rows):
            y = start_y - r * (icon_h + spacing_y)
            for c in range(cols):
                x = start_x + c * (icon_w + spacing_x)
                # 아이콘 그리기
                if idx < len(item_images) and item_images[idx] is not None:
                    try:
                        item_images[idx].draw(x, y, icon_w, icon_h)
                    except Exception:
                        pass

                # 선택 위치 저장
                if idx == selected_index:
                    sel_x, sel_y = x, y

                # 아이템 텍스트(이름, 가격, 수량) 그리기
                if idx < len(catalog):
                    try:
                        item = catalog[idx]
                        name = item.name
                        price = get_price(name)
                        qty = get_quantity(name)

                        text_center_x = x
                        text_name_y = y - icon_h // 2 - 8
                        text_price_y = text_name_y - 16
                        text_qty_y = text_price_y - 16

                        def draw_centered_text(f, cxp, cyp, text):
                            w_text = len(text) * 6
                            px = int(cxp - w_text // 2)
                            _safe_draw_text(f, px + 1, cyp - 1, text)
                            _safe_draw_text(f, px, cyp, text)

                        draw_centered_text(font, text_center_x, text_name_y, name)
                        draw_centered_text(font, text_center_x, text_price_y, f'가격: {price}')
                        draw_centered_text(font, text_center_x, text_qty_y, f'소지: {qty}')
                    except Exception:
                        pass

                idx += 1

        # 선택된 아이템 강조 표시
        if sel_x is not None and sel_y is not None:
            try:
                left = sel_x - icon_w // 2
                right = sel_x + icon_w // 2
                bottom = sel_y - icon_h // 2
                top = sel_y + icon_h // 2
                draw_rectangle(left, bottom, right, top)
                _safe_draw_text(font, cx - 160, cy - 120, f'선택: {selected_index + 1} / 수량: {quantity} (↑↓ 변경)')
                _safe_draw_text(font, cx - 160, cy - 140, 'B:구매  S:판매  E:종료')
            except Exception:
                pass

        # 메시지 표시
        if message:
            try:
                _safe_draw_text(font, cx - 60, cy - 180, message)
            except Exception:
                pass

    except Exception:
        pass

    update_canvas()


def pause():
    pass


def resume():
    pass


def finish():
    global ui_image, item_images
    try:
        del ui_image
    except Exception:
        pass
    try:
        for img in item_images:
            del img
    except Exception:
        pass
    item_images = []