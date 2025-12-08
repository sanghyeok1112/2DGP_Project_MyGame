from pico2d import *
from state_machine import StateMachine
import game_framework


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class DeliveryMan:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0

        self.IDLE = Idle(self)
        self.WALKING = Walking(self)
        self.SLEEP = Sleep(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP: {space_down: self.IDLE,
                             right_down: self.WALKING, left_down: self.WALKING,
                             right_up: self.WALKING, left_up: self.WALKING},

                self.IDLE: {space_down: self.IDLE, time_out: self.SLEEP,
                            right_down: self.WALKING, left_down: self.WALKING,
                            right_up: self.WALKING, left_up: self.WALKING},

                self.WALKING: {space_down: self.WALKING,
                               left_up: self.IDLE, right_up: self.IDLE,
                               left_down: self.WALKING, right_down: self.WALKING}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        # 디버깅용 바운딩 박스
        # draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def handle_collision(self, group, other):
        # 충돌 처리: 배달원의 맵이동, x좌표 변환
        if group == 'deliveryman:background':
            # other는 MapManager 또는 BaseMap 인스턴스일 수 있으므로 직접 속성 접근 금지
            left, _, right, _ = other.get_bb()
            # 왼쪽 끝 충돌 → 위치 보정
            if self.x < left + 10:
                self.x = left + 60
            # 오른쪽 끝 충돌 → 위치 보정
            elif self.x > right - 10:
                self.x = right - 60

class Idle:
    def __init__(self, deliveryman):
        self.deliveryman = deliveryman
        self.image = [load_image(f'DeliveryMan_{i}.png') for i in range(21, 25)]
        self.frame_count = len(self.image)

    def enter(self, e):
        self.deliveryman.dir = 0
        self.deliveryman.frame = 0
        self.deliveryman.wait_time = get_time()
        pass

    def exit(self, e):
        pass

    def do(self):
        self.deliveryman.frame = (self.deliveryman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - self.deliveryman.wait_time > 2:
            self.deliveryman.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        frame = int(self.deliveryman.frame)
        if self.deliveryman.face_dir == 1:
            self.image[frame].composite_draw((int(self.deliveryman.frame)) * 0, '', self.deliveryman.x, self.deliveryman.y, 25, 150)
        elif self.deliveryman.face_dir == -1:
            self.image[frame].composite_draw((int(self.deliveryman.frame)) * 0, 'h', self.deliveryman.x, self.deliveryman.y, 25, 150)


class Walking:
    def __init__(self, deliveryman):
        self.deliveryman = deliveryman
        self.image = [load_image(f'DeliveryMan_{i}.png') for i in range(13, 21)]

    def enter(self, e):
        self.deliveryman.frame = 0
        if right_down(e) or left_up(e):
            self.deliveryman.dir = self.deliveryman.face_dir = 1
        elif left_down(e) or right_up(e):
            self.deliveryman.dir = self.deliveryman.face_dir = -1
        else:
            self.deliveryman.dir = self.deliveryman.face_dir

    def exit(self, e):
        self.deliveryman.dir = 0

    def do(self):
        self.deliveryman.frame = (self.deliveryman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.deliveryman.x += self.deliveryman.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        frame = int(self.deliveryman.frame)
        if self.deliveryman.face_dir == 1:
            self.image[frame].composite_draw((int(self.deliveryman.frame)) * 0, 'h', self.deliveryman.x, self.deliveryman.y, 50, 150)
        elif self.deliveryman.face_dir == -1:
            self.image[frame].composite_draw((int(self.deliveryman.frame)) * 0, '', self.deliveryman.x, self.deliveryman.y, 50, 150)


class Sleep:
    def __init__(self, deliveryman):
        self.deliveryman = deliveryman
        self.image = [load_image(f'DeliveryMan_{i}.png') for i in range(21, 25)]

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.deliveryman.frame = (self.deliveryman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(self):
        frame = int(self.deliveryman.frame)
        if self.deliveryman.face_dir == 1:
            self.image[frame].composite_draw(-3.141592 / 2, '', self.deliveryman.x - 25,self.deliveryman.y - 25, 25, 150)
        elif self.deliveryman.face_dir == -1:
            self.image[frame].composite_draw(3.141592/2, 'h', self.deliveryman.x + 25, self.deliveryman.y - 25, 25, 150)