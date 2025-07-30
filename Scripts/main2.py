from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

GameScene = []
MainMenuScene = []
Scenes = [GameScene]

def switch_scene(target: list):
    for scene in Scenes:
        if scene == target:
            continue
        
        for element in scene:
            element.disable()
    
    for element in target:
        element.enable()

b = Button("Test", on_click=lambda: switch_scene(GameScene))
ground = Entity(model='plane', collider='box', scale=64, texture='brick', texture_scale=(4,4), parent=GameScene)
TestDummy = Entity(model="cube", collider="mesh", scale=(1, 2, 1), color=color.red, position=(0, 1, 0), parent=GameScene)
CoordinateText = Text('(100, 64, 100)', color=color.blue, world_scale=2, origin=(-1, -3))

class Player:
    def __init__(self, GameScene):
        self.player = FirstPersonController(y=2)
        self.player.cursor.disable()
        self.player.parent = GameScene

    def get_position(self) -> Vec3:
        return self.player.position

    def distance_from(self, entity: Entity) -> float:
        xp, yp, zp = self.get_position()
        xe, ye, ze = entity.get_position()
        dx, dy, dz = xp - xe, yp - ye, zp - ze

        distance2D = ((dx ** 2) + (dz ** 2)) ** 0.5
        distance = ((distance2D ** 2) + (dy ** 2)) ** 0.5

        return distance

    def on_update(self):
        print(self.distance_from(TestDummy))

player = Player(GameScene)

def update():
    # if held_keys['d']:
    #     CoordinateText.x_setter(CoordinateText.x_getter() + 0.01*time.dt)
    # elif held_keys['a']:
    #     CoordinateText.x_setter(CoordinateText.x_getter() - 0.01*time.dt)
    # if held_keys['w']:
    #     CoordinateText.y_setter(CoordinateText.y_getter() + 0.01*time.dt)
    # elif held_keys['s']:
    #     CoordinateText.y_setter(CoordinateText.y_getter() - 0.01*time.dt)

    # x, y, z = player.get_position()
    # x, y, z = int(x), int(y), int(z)

    # CoordinateText.text = str((x, y, z))
    # player.on_update()
    pass

Sky()
app.run()
