from pico2d import load_image, get_canvas_width, get_canvas_height, draw_rectangle, get_time, load_font
import items
import pico2d as _pico2d

HAS_DRAW_STRING = hasattr(_pico2d, 'draw_string')

# 폰트 폴백 캐시
_fallback_fonts = {}

# 폰트 폴백 래퍼: draw_string 대신 load_font(None,size)로 그리도록 변경
class _FontFallback:
    def __init__(self, size=16):
        try:
            self.f = load_font(None, size)
        except Exception:
            self.f = None

    def draw(self, x, y, text, color=None):
        try:
            if self.f:
                # pico2d load_font의 draw 시 색상 인수를 허용하므로 전달
                self.f.draw(int(x), int(y), str(text), color)
        except Exception:
            pass


def _safe_draw_text(fobj, x, y, text, color=(255, 220, 0), center=False, size=16):
    """폰트 오브젝트가 있으면 사용, 없으면 load_font(None,size)로 폰트를 로드하여 그림. center=True이면 x를 중앙 기준으로 처리."""
    try:
        s = str(text)
        if center:
            try:
                w = get_canvas_width()
            except Exception:
                w = 800
            # 대략 문자 너비 계산
            approx_w = len(s) * (10 if fobj else 8)
            x = int(w // 2 - approx_w // 2)

        # 우선 전달받은 폰트 사용
        if fobj:
            try:
                fobj.draw(int(x), int(y), s, color)
                return
            except Exception:
                pass

        # 폰트 없으면 캐시에서 불러오거나 새로 로드
        font = _fallback_fonts.get(size)
        if font is None:
            try:
                font = load_font(None, size)
            except Exception:
                font = None
            if font is None:
                # 최후 폴백: _FontFallback
                font = _FontFallback(size)
            _fallback_fonts[size] = font

        try:
            font.draw(int(x), int(y), s, color)
            return
        except Exception:
            pass

    except Exception:
        pass


backgrounds = [
    'employeeBG.png',
    'BGRoad_BGSheet_1.png',
    'BGRoad_BGSheet_2.png',
    'BGRoad_BGSheet_3.png',
    'BGRoad_BGSheet_4.png',
    'BGRoad_BGSheet_5.png',
    'BGRoad_BGSheet_6.png',
    'BGRoad_BGSheet_7.png'
]


class BaseMap:
    def __init__(self, file_name, target_w=384*3, target_h=111*3):
        # 이미지 로드는 캔버스가 열린 이후에 수행하도록 지연
        self.file_name = file_name
        self.image = None
        self.target_w = target_w
        self.target_h = target_h
        self.offset_x = 0
        self.offset_y = 0

    def load(self):
        if self.image is not None:
            return
        try:
            self.image = load_image(self.file_name)
        except Exception as e:
            raise IOError(f"이미지 로드 실패: {self.file_name}") from e

    def draw(self, canvas_w=None, canvas_h=None):
        if self.image is None:
            self.load()

        if canvas_w is None:
            canvas_w = get_canvas_width()
        if canvas_h is None:
            canvas_h = get_canvas_height()
        cx = canvas_w // 2 + self.offset_x
        cy = canvas_h // 2 + self.offset_y
        self.image.draw(cx, cy, self.target_w, self.target_h)
        # 디버깅용 바운딩 박스
        #draw_rectangle(*self.get_bb())

        # 왼쪽 상단에 소지금액 표시 (items.get_money() 사용)
        try:
            money = items.get_money()
            amount = items.get_goal()
            # 화면 좌측 상단 여백 10px
            # 지연하여 폰트 로드: 모듈 전역 _money_font 사용, TTF 우선
            global _money_font
            try:
                _money_font
            except NameError:
                _money_font = None

            if _money_font is None:
                try:
                    # 우선 프로젝트 TTF 시도
                    import os
                    if os.path.exists('NanumGothic.ttf'):
                        _money_font = load_font('NanumGothic.ttf', 16)
                    else:
                        # Windows 기본 한글 폰트 시도
                        win_malgun = r'C:\Windows\Fonts\malgun.ttf'
                        win_nanumm = r'C:\Windows\Fonts\NanumGothic.ttf'
                        if os.path.exists(win_nanumm):
                            _money_font = load_font(win_nanumm, 16)
                        elif os.path.exists(win_malgun):
                            _money_font = load_font(win_malgun, 16)
                        else:
                            # 시스템 기본 폰트 시도
                            _money_font = load_font(None, 16)
                except Exception:
                    _money_font = None

                # 디버깅: 폰트 로드 상태 출력(콘솔)
                try:
                    print(f"_money_font loaded: {_money_font is not None}")
                except Exception:
                    pass

            # 텍스트 그리기 (항상 _safe_draw_text 사용)
            text_x = 10
            text_y = canvas_h - 24
            _safe_draw_text(_money_font, text_x + 1, text_y - 1, f'소지금액: {money}', (0, 0, 0), size=16)
            _safe_draw_text(_money_font, text_x, text_y, f'소지금액: {money}', (255, 220, 0), size=16)
            # 목표금액을 소지금 아래에 출력
            _safe_draw_text(_money_font, text_x + 1, text_y - 20 - 1, f'목표금액: {amount}', (0, 0, 0), size=16)
            _safe_draw_text(_money_font, text_x, text_y - 20, f'목표금액: {amount}', (255, 220, 0), size=16)

            # 소지금액이 목표금액보다 높으면 목표달성 텍스트를 중앙에 그림
            if money >= amount:
                try:
                    # 중앙에 텍스트: 그림자(검정, 아래로 1px) + 메인 텍스트(녹색)
                    y_center = canvas_h // 2
                    _safe_draw_text(_money_font, 0, y_center - 2, '목표금액 달성!', (0, 0, 0), center=True, size=36)
                    _safe_draw_text(_money_font, 0, y_center + 0, '목표금액 달성!', (0, 255, 0), center=True, size=36)
                except Exception:
                    pass

        except Exception:
            pass


    def get_bb(self):
        canvas_w = get_canvas_width()
        canvas_h = get_canvas_height()
        cx = canvas_w // 2 + self.offset_x
        cy = canvas_h // 2 + self.offset_y
        left = cx - self.target_w // 2
        bottom = cy - self.target_h // 2
        right = cx + self.target_w // 2
        top = cy + self.target_h // 2
        return left, bottom, right, top

    def get_width(self):
        return self.target_w

    def get_height(self):
        return self.target_h


# MapManager 클래스로 올바르게 정의
class MapManager:
    def __init__(self, maps):
        # maps: BaseMap 인스턴스 리스트
        self.maps = maps
        self.index = 0
        self.last_change_time = 0.0
        # 최소 쿨다운(초)
        self.change_cooldown = 0.15

    def draw(self):
        self.maps[self.index].draw()

    def update(self):
        pass

    def get_bb(self):
        return self.maps[self.index].get_bb()

    @property
    def map_index(self):
        return self.index

    @map_index.setter
    def map_index(self, v):
        self.index = max(0, min(int(v), len(self.maps) - 1))

    def change_map(self, next_index):
        # change_map은 map_index 프로퍼티를 통해 변경
        old = self.index
        self.map_index = next_index
        new = self.index
        if old != new:
            try:
                fname = self.maps[self.index].file_name
            except Exception:
                fname = '<unknown>'
            print(f'Map changed: {old} -> {new} ({fname})')
            self.last_change_time = get_time()

    def handle_collision(self, group, other):
        if group != 'deliveryman:background':
            return

        # 쿨다운 동안 충돌 무시
        if get_time() - self.last_change_time < self.change_cooldown:
            return

        # 현재 맵의 바운딩
        left, _, right, _ = self.get_bb()
        # other가 플레이어라면 get_bb가 있어야 함
        if not hasattr(other, 'get_bb'):
            return
        ol, ob, orr, ot = other.get_bb()

        # 플레이어의 엣지(오른쪽/왼쪽)를 기준으로 판정
        thresh = 30

        # 플레이어의 오른쪽이 맵 오른쪽 경계 근처를 넘으면 다음 맵으로
        if orr >= right - thresh:
            old_index = self.index
            self.change_map(self.index + 1)
            if hasattr(other, 'x'):
                # 새 맵의 왼쪽 내부로 안전하게 배치 (진입 방향: 오른쪽 -> 새 맵 왼쪽)
                new_left, _, new_right, _ = self.get_bb()
                other.x = new_left + 100
            return

        # 플레이어의 왼쪽이 맵 왼쪽 경계 근처를 넘으면 이전 맵으로
        if ol <= left + thresh:
            old_index = self.index
            self.change_map(self.index - 1)
            if hasattr(other, 'x'):
                # 새 맵(이전 맵)의 오른쪽 내부로 안전하게 배치 (진입 방향: 왼쪽 -> 새 맵 오른쪽)
                new_left, _, new_right, _ = self.get_bb()
                other.x = new_right - 100
            return


# 각 맵을 개별 클래스로 정의 (BaseMap 상속, 필요 시 커스터마이징 가능)
class EmployeeMap(BaseMap):
    def __init__(self):
        super().__init__('employeeBG.png')


class RoadMap1(BaseMap):
    def __init__(self):
        super().__init__('BGRoad_BGSheet_1.png')


class RoadMap2(BaseMap):
    def __init__(self):
        super().__init__('BGRoad_BGSheet_2.png')


class RoadMap3(BaseMap):
    def __init__(self):
        super().__init__('BGRoad_BGSheet_3.png')


class RoadMap4(BaseMap):
    def __init__(self):
        super().__init__('BGRoad_BGSheet_4.png')


class RoadMap5(BaseMap):
    def __init__(self):
        super().__init__('BGRoad_BGSheet_5.png')


class RoadMap6(BaseMap):
    def __init__(self):
        super().__init__('BGRoad_BGSheet_6.png')


class RoadMap7(BaseMap):
    def __init__(self):
        super().__init__('BGRoad_BGSheet_7.png')