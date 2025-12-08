from pico2d import *
import game_framework
import play_mode
import os

image = None
_image_file = 'BGRoad_BGSheet_1.png'
font = None

def init():
    global image, font
    # 먼저 이미지 파일의 크기를 얻기 위해 임시로 로드
    temp = None
    try:
        temp = load_image(_image_file)
        img_w = getattr(temp, 'w', None) or getattr(temp, 'width', None) or 800
        img_h = getattr(temp, 'h', None) or getattr(temp, 'height', None) or 600
    except Exception:
        temp = None
        img_w, img_h = 800, 600

    # 현재 캔버스 크기와 다르면 안전하게 닫고 다시 엽니다
    try:
        from pico2d import get_canvas_width, get_canvas_height, close_canvas, open_canvas
        try:
            cw = get_canvas_width()
            ch = get_canvas_height()
        except Exception:
            cw = None
            ch = None
        if cw != img_w or ch != img_h:
            try:
                close_canvas()
            except Exception:
                pass
            try:
                open_canvas(img_w, img_h)
            except Exception:
                # 실패하면 기본 캔버스를 사용
                pass
    except Exception:
        pass

    # 캔버스가 열려난 이후에 이미지를 다시 로드하여 안전하게 사용
    try:
        image = load_image(_image_file)
    except Exception:
        # 로드 실패 시 임시 이미지를 사용하거나 None
        image = temp

    # 폰트 로드: 프로젝트 TTF 우선, 없으면 시스템 폰트 또는 draw_string 폴백
    try:
        if os.path.exists('NanumGothic.ttf'):
            font = load_font('NanumGothic.ttf', 20)
        else:
            win_malgun = r'C:\Windows\Fonts\malgun.ttf'
            win_nanumm = r'C:\Windows\Fonts\NanumGothic.ttf'
            if os.path.exists(win_nanumm):
                font = load_font(win_nanumm, 20)
            elif os.path.exists(win_malgun):
                font = load_font(win_malgun, 20)
            else:
                try:
                    font = load_font(None, 20)
                except Exception:
                    font = None
    except Exception:
        font = None


def finish():
    global image, font
    try:
        del image
    except Exception:
        pass
    try:
        del font
    except Exception:
        pass

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)


def _draw_centered_text(text, y_offset=None, color=(255,255,255)):
    """텍스트를 캔버스 가로 중앙, y_offset이 None이면 수직 중앙에 그림"""
    try:
        w = get_canvas_width()
        h = get_canvas_height()
        # 기본 y는 캔버스의 수직 중앙
        if y_offset is None:
            y = h // 2
        else:
            y = y_offset

        # 폰트가 있으면 대략적인 너비로 중앙 정렬
        if font:
            text_w = len(str(text)) * 10
            font.draw(int(w//2 - text_w//2), int(y), str(text), color)
        else:
            text_w = len(str(text)) * 6
            draw_string(int(w//2 - text_w//2), int(y), str(text))
    except Exception:
        try:
            draw_string(10, 10, str(text))
        except Exception:
            pass


def draw():
    clear_canvas()
    try:
        if image:
            w = get_canvas_width()
            h = get_canvas_height()
            image.draw(w // 2, h // 2)
    except Exception:
        try:
            image.draw(400, 300)
        except Exception:
            pass

    # 중앙에 안내 텍스트 그리기 (수직 중앙)
    try:
        _draw_centered_text('스페이스: 시작  /  ESC: 종료', None, (255, 220, 0))
    except Exception:
        pass

    update_canvas()

def update(): pass

def pause(): pass

def resume(): pass