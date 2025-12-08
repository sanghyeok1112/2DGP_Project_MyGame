from pico2d import *
import game_framework
import items
import title_mode
from deliveryman import DeliveryMan
from background import EmployeeMap, RoadMap1, RoadMap2, RoadMap3, RoadMap4, RoadMap5, RoadMap6, RoadMap7, MapManager
import background
import game_world
import item_mode
import buy_and_sell  # 가격 변동 적용을 위해 추가


deliveryman = None
running = True

# UI 팝업 관련 전역
ui_image = None
ui_visible = False

# 가격 변동 관련 전역
price_update_interval = 5.0  # 초 단위
last_price_update = 0.0

# 목표달성 로그 플래그
_goal_logged = False

def handle_events():
    global running, deliveryman, ui_visible
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return

        # ESC: UI가 열려 있으면 닫고, 아니면 타이틀로
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            if ui_visible:
                ui_visible = False
                continue
            else:
                game_framework.change_mode(title_mode)
                return

        # UI 토글: 'e' 키 -> item_mode를 푸시하여 별도 모드로 연다
        if event.type == SDL_KEYDOWN and event.key == SDLK_e:
            # 현재 UI가 플레이 모드의 오버레이로 열려있다면 닫고, 아니면 item_mode를 푸시
            if ui_visible:
                ui_visible = False
            else:
                game_framework.push_mode(item_mode)
            continue

        # UI가 열려 있으면 다른 입력은 무시
        if ui_visible:
            continue

        # UI가 닫혀 있으면 기존 입력을 플레이어에게 전달
        if deliveryman:
            deliveryman.handle_event(event)


def init():
    global deliveryman, running, ui_image, ui_visible, last_price_update

    running = True
    # 맵 인스턴스 생성(이미지 로드는 지연)
    maps = [
        EmployeeMap(),
        RoadMap1(),
        RoadMap2(),
        RoadMap3(),
        RoadMap4(),
        RoadMap5(),
        RoadMap6(),
        RoadMap7()
    ]

    # 첫 맵 크기로 캔버스를 재설정: 현재는 로고/타이틀에서 이미 캔버스가 열려 있으므로
    # 닫고 다시 열어야 안전하게 크기를 변경할 수 있음
    try:
        from pico2d import close_canvas, open_canvas
        # 닫고 다시 열기
        close_canvas()
        first_w = maps[0].get_width()
        first_h = maps[0].get_height()
        open_canvas(first_w, first_h)
    except Exception:
        # 실패해도 계속 진행(기존 캔버스 사용)
        pass

    # 캔버스가 열린 후 이미지 로드
    for m in maps:
        # ensure load will run after canvas is available
        try:
            m.load()
        except Exception:
            pass

    map_manager = MapManager(maps)
    game_world.add_object(map_manager, 0)

    deliveryman = DeliveryMan()
    game_world.add_object(deliveryman, 1)

    game_world.add_collision_pair('deliveryman:background', deliveryman, map_manager)

    # UI 이미지 로드
    try:
        ui_image = load_image('UI_default.png')
    except Exception:
        ui_image = None
    ui_visible = False

    # 가격 갱신 타이머 초기화
    try:
        last_price_update = get_time()
    except Exception:
        last_price_update = 0.0

    # 목표달성 테스트
    #items.set_money(items.get_goal() + 1)

def update():
    global last_price_update
    # UI가 열려 있으면 게임 상태 업데이트(이동/충돌)은 정지
    if ui_visible:
        return
    game_world.update()
    game_world.handle_collision()

    # 주기적으로 가격 변동 적용
    try:
        if get_time() - last_price_update >= price_update_interval:
            try:
                buy_and_sell.adjust_item_prices()
            except Exception:
                pass
            last_price_update = get_time()
    except Exception:
        pass

def draw():
    global _goal_logged
    clear_canvas()
    game_world.render()

    # UI 팝업이 보이면 오버레이로 중앙에 그림
    if ui_visible and ui_image is not None:
        try:
            w = get_canvas_width()
            h = get_canvas_height()
            ui_image.draw(w // 2, h // 2)
        except Exception:
            pass

    # 목표달성 텍스트를 최상위 오버레이로 표시 (background._safe_draw_text 사용)
    try:
        money = items.get_money()
        goal = items.get_goal()
        # 디버그 출력: 현재 소지/목표 값
        try:
            print(f"DEBUG: money={money}, goal={goal}, _goal_logged={_goal_logged}")
        except Exception:
            pass
        if money >= goal:
            w = get_canvas_width()
            h = get_canvas_height()
            # background 모듈의 안전한 폰트/폴백 함수 사용하여 중앙 정렬로 그림
            try:
                print('DEBUG: attempting to draw goal text via background._safe_draw_text')
                background._safe_draw_text(None, 0, h // 2 - 10, '목표금액 달성!', (0, 0, 0), center=True, size=40)
                background._safe_draw_text(None, 0, h // 2, '목표금액 달성!', (255, 220, 0), center=True, size=40)
                if not _goal_logged:
                    try:
                        print('INFO: 목표 달성 텍스트 그리기 시도됨')
                    except Exception:
                        pass
                    _goal_logged = True
            except Exception as e:
                try:
                    print('ERROR: 목표달성 그리기 실패:', e)
                except Exception:
                    pass
                # 최후 폴백: pico2d.draw_string가 있다면 사용
                if hasattr(_pico2d, 'draw_string'):
                    _pico2d.draw_string(int(w//2 - len('목표금액 달성!')*6), int(h//2), '목표금액 달성!')
    except Exception:
        pass

    update_canvas()

def finish():
    global ui_image
    try:
        del ui_image
    except Exception:
        pass

def pause():
    pass

def resume():
    pass