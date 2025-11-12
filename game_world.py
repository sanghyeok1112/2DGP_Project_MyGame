world = [[], []]

def update():
    for layer in world:
        for o in layer:
            if hasattr(o, 'update'):
                try:
                    o.update()
                except Exception:
                    # 개별 객체의 업데이트 오류가 전체 루프를 중단하지 않도록 안전 처리
                    pass

def render():
    for layer in world:
        for o in layer:
            if hasattr(o, 'draw'):
                try:
                    o.draw()
                except Exception:
                    pass

# render의 별칭으로 draw를 추가하면 호출하는 쪽에서 이름이 달라도 동작함
def draw():
    render()

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    raise ValueError('Trying to remove non-existing object')