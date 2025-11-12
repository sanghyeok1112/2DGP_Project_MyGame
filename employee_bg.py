from pico2d import load_image

class EmployeeBG:
    def __init__(self):
        self.image = load_image('employeeBG.png')

    def draw(self):
        self.image.draw(400, 300, 800, 600)

    def update(self):
        pass
