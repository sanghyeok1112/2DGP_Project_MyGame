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

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

collision_pairs = {}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def handle_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
