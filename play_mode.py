from pico2d import *
import game_framework
import title_mode
from deliveryman import DeliveryMan
from employee_bg import EmployeeBG
import game_world

deliveryman = None
running = True

def handle_events():
    global running, deliveryman
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            deliveryman.handle_event(event)


def init():
    global deliveryman, running

    running = True
    employeeBG = EmployeeBG()
    game_world.add_object(employeeBG, 0)

    deliveryman = DeliveryMan()
    game_world.add_object(deliveryman, 1)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    pass

def pause():
    pass

def resume():
    pass


