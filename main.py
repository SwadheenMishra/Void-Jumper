from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from Scripts import sound

app = Ursina(title="Look at the screen not here!")
window.basic_shaders = True

GameScene1 = []
GameScene2 = []
GameScene3 = []
GameScene4 = []
MainMenuScene1 = []

currentScene = MainMenuScene1
scenes = [MainMenuScene1, GameScene1, GameScene2, GameScene3, GameScene4]

platforms = []
portalList = []
MovingPlatFormsList = []
textureChangeCoolDown = 0.5
TimeWhenTextureChanged = time.time()


GunItem = Entity()

class utils:
    def distance_between(self, entity1: Entity, entity2: Entity):
        xp, yp, zp = entity1.position
        xe, ye, ze = entity2.position
        dx, dy, dz = xp - xe, yp - ye, zp - ze

        distance2D = ((dx ** 2) + (dz ** 2)) ** 0.5
        distance = ((distance2D ** 2) + (dy ** 2)) ** 0.5

        return distance
    
    def set_scene(self, target: list, allScenes: list):
        global currentScene

        for scene in allScenes:
            if scene == target:
                continue

            for element in scene:
                element.disable()

        for element in target:
            element.enable()
        
        # Disable player if not in the current scene
        if target in [GameScene1, GameScene2, GameScene3, GameScene4]:
            player.enable()
        else:
            player.disable()
        
        currentScene = target


class Player:
    def __init__(self):
        self.player = FirstPersonController(collider="box")
        self.player.jump_height = 3
        self.HasGun = False
        self.currentDialog = 0
        # self.player.cursor.disable()
        # self.player.cursor = Entity(parent=camera.ui, model='sphere', color=color.black, scale=.0008, rotation_z=45)

    def get_position(self) -> Vec3:
        return self.player.position

    def set_position(self, pos: Vec3) -> None:
        self.player.position = pos

    def enable(self):
        self.player.enable()

    def disable(self):
        self.player.disable()

    def kill(self):
        self.disable()

    def equip_gun(self):
        self.HasGun = True
        GunHandItem = Entity(
        model="Models/mp5_submachine_gun.glb",
        parent=camera,                          
        position=Vec3(0.5, -0.3, 0.9),          
        rotation=Vec3(5, 180, 0),              
        scale=1.5                      
        )


class MovingPlatform:
    def __init__(self, yStart: int, xStart: int, xEnd: int, zStart: int, zEnd: int, speed: int|float):
        pos = Vec3(xStart, yStart, zStart)
        self.Entity = Entity(model="cube", scale=Vec3(3.5, 0.1, 2.5), position=pos, collider="box")
        self.xStart = xStart
        self.xEnd = xEnd
        self.zStart = zStart
        self.zEnd = zEnd
        self.TargetPos = [self.xEnd, self.zEnd]
        self.speed = speed

    def calculate_move_vector(self, current, target):
        x, z = 0, 0

        deltaX, deltaZ = abs(target[0] - current[0]), abs(target[1] - current[1])

        if deltaX >= 0.02:
            if target[0] > current[0]:
                x = 1
            elif target[0] < current[0]:
                x = -1

        if deltaZ >= 0.02:
            if target[1] > current[1]:
                z = 1
            elif target[1] < current[1]:
                z = -1

        return [x, z]
    
    def disable(self):
        self.Entity.disable()
    
    def update(self):
        vec = self.calculate_move_vector([self.Entity.x_getter(), self.Entity.z_getter()], self.TargetPos)

        if vec == [0, 0]:
            if self.TargetPos == [self.xEnd, self.zEnd]:
                self.TargetPos = [self.xStart, self.zStart]
            else:
                self.TargetPos = [self.xEnd, self.zEnd]

        self.Entity.set_position(self.Entity.get_position() + (Vec3(vec[0], 0, vec[1]) * time.dt * self.speed))

def create_platform(pos: Vec3):
    return Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=pos, collider="box")

player = Player()
util = utils()
ground = Entity()

def main_menu():
    WelcomeText = Text('Welcome to Void Jumper!', color=color.blue, origin=(0, -6.5), world_scale=50)
    
    def play():
        util.set_scene(GameScene1, scenes)
        game_scene1()

    PlayBtn = Button(
        text='Play',
        scale=(0.4, 0.2),  # Width and height
        origin=(0,-0.9),
        on_click=play,
        text_size=3.5
    )

    QuitBtn = Button(
        text="Quit",
        scale=(0.4, 0.2),  # Width and height
        origin=(0,0.9),
        on_click=lambda: print("test quit"),
        text_size=3.5
    )


    MainMenuScene1.append(WelcomeText)
    MainMenuScene1.append(PlayBtn)
    MainMenuScene1.append(QuitBtn)


def create_portal(pos: Vec3) -> list[Entity, Entity]:
    portal = []
    portalPortal = Entity(model="cube", scale=Vec3(2, 3.5, 0.3), position=pos, collider="box", color=color.black)
    portalPortal.alpha_setter(0.6)
    portalFrame = Entity(model="cube", scale=Vec3(1.8, 3, 0.28), position=Vec3(pos.x_getter(), pos.y_getter(), pos.z_getter() - 0.1), color=color.blue, collider="box")
    portalFrame.alpha_setter(0.5)
    portal.append(portalFrame)
    portal.append(portalPortal)
    
    return portal


def graple(hookshot_target: Button):
    if util.distance_between(player.player, hookshot_target) > 17:
        return
    
    player.player.animate_position(hookshot_target.position, duration=.5, curve=curve.linear)


def game_scene1():
    global platforms, portalList, GunItem

    platforms = []
    ground = Entity(model='plane', collider='box', scale=64, color=color.black50, texture_scale=(10,10), Collider="box")
    spawn = Entity(model='cube', scale=Vec3(2, 0.5, 2), position=Vec3(0, 0, 0), collider="box", texture="brick")

    portalList = create_portal(Vec3(0, 6.75, 16.5))
    portalFrame, portal =  portalList

    for i in range(1, 6):
        platform = Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=Vec3(0, i, i * 3), collider="box")
        platforms.append(platform)
        GameScene1.append(platform)

    GunItem = Entity(
    model="Models/mp5_submachine_gun.glb",  
    position=Vec3(5, 1, 0),          
    rotation=Vec3(5, 180, 0),              
    scale=1.7,
    collider="box"                      
    )

    sound.play_dialog1()

    GameScene1.append(player)
    GameScene1.append(ground)
    GameScene1.append(spawn)
    GameScene1.append(portalFrame)
    GameScene1.append(portal)
    GameScene1.append(GunItem)


def set_lava_scale(TextureScale: float | int) -> None:
    ground.texture_offset_setter(TextureScale)

def game_scene2():
    global platforms, portalList, ground

    player.set_position((0, 0, 0))

    platforms = []
    lava = Entity(model='plane', collider='box', scale=640, color=color.red)
    lava.alpha_setter(.55)
    ground = Entity(model='plane', collider='box', scale=640, texture="grass", texture_scale=(3.5,3.5), Collider="box")
    ground.position_setter((lava.position_getter().x_getter(), lava.position_getter().y_getter() - 0.25, lava.position_getter().z_getter()))
    spawn = Entity(model='cube', scale=Vec3(2, 0.5, 2), position=Vec3(0, 0, 0), collider="box", texture="brick")

    portalList = create_portal(Vec3(0, 11.75, 33.5))
    portalFrame, portal = portalList

    platform = Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=Vec3(0, 10, 32), collider="box")
    platforms.append(platform)
    GameScene2.append(platform)

    platform = Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=Vec3(0, 10, 29), collider="box")
    platforms.append(platform)
    GameScene2.append(platform)

    for i in range(1, 4):
        platform = Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=Vec3(0, i, i*3), collider="box")
        platforms.append(platform)
        GameScene2.append(platform)
    
    for j in range(1, 4)[::-1]:
        platform = Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=Vec3(0, j, i*3 + (4 - j) * 3), collider="box")
        platforms.append(platform)
        GameScene2.append(platform)


    hookshot_target = Button(parent=scene, model='sphere', color=color.cyan, position=(0,14,25), scale=0.6)
    hookshot_target.on_click = lambda: graple(hookshot_target)


    sound.play_dialog2()

    GameScene2.append(player)
    GameScene2.append(lava)
    GameScene2.append(spawn)
    GameScene2.append(portalFrame)
    GameScene2.append(portal)
    GameScene2.append(hookshot_target)
    GameScene2.append(ground)

def game_scene3():
    global platforms, portalList, ground, MovingPlatFormsList

    for MP in MovingPlatFormsList:
        MP.disable()

    MovingPlatFormsList.append(MovingPlatform(13, -5, 5, 1, 1, 1))
    MovingPlatFormsList.append(MovingPlatform(13, 5, -5, 5.5, 5.5, 1))
    MovingPlatFormsList.append(MovingPlatform(13, -5, 5, 10, 10, 1))

    player.set_position((0, 0, 0))

    platforms = []
    lava = Entity(model='plane', collider='box', scale=640, color=color.red)
    lava.alpha_setter(.55)
    ground = Entity(model='plane', collider='box', scale=640, texture="grass", texture_scale=(3.5,3.5), Collider="box")
    ground.position_setter((lava.position_getter().x_getter(), lava.position_getter().y_getter() - 0.25, lava.position_getter().z_getter()))
    spawn = Entity(model='cube', scale=Vec3(2, 0.5, 2), position=Vec3(0, 0, 0), collider="box", texture="brick")

    portalList = create_portal(Vec3(0, 14.5, 12))
    portalFrame, PortalPortal = portalList

    for i in range(1, 4):
        platform = Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=Vec3(0, i, i * 3), collider="box")
        platforms.append(platform)
        GameScene3.append(platform)

    for j in range(1, 4):
        platform = Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=Vec3(j * 3, i + j, i * 3), collider="box")
        platforms.append(platform)
        GameScene3.append(platform)
    
    for k in range(1, 5):
        platform = Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=Vec3(j * 3, i + j + k, i * 3 - k * 3), collider="box")
        platforms.append(platform)
        GameScene3.append(platform)
    
    for m in range(1, 4):
        platform = Entity(model="cube", scale=Vec3(1.5, 0.1, 1.5), position=Vec3(j * 3 - m * 3, i + j + k + m, i * 3 - k * 3), collider="box")
        platforms.append(platform)
        GameScene3.append(platform)

    

    sound.play_dialog3()

    GameScene3.append(player)
    GameScene3.append(spawn)
    GameScene3.append(lava)
    GameScene3.append(ground)
    GameScene3.append(PortalPortal)
    GameScene3.append(portalFrame)

def game_scene4():
    global platforms, portalList, ground, MovingPlatFormsList

    for MP in MovingPlatFormsList:
        MP.disable()

    player.set_position((0, 0, 0))

    platforms = []
    lava = Entity(model='plane', collider='box', scale=640, color=color.red)
    lava.alpha_setter(.55)
    ground = Entity(model='plane', collider='box', scale=640, texture="grass", texture_scale=(3.5,3.5), Collider="box")
    ground.position_setter((lava.position_getter().x_getter(), lava.position_getter().y_getter() - 0.25, lava.position_getter().z_getter()))
    spawn = Entity(model='cube', scale=Vec3(2, 0.5, 2), position=Vec3(0, 0, 0), collider="box", texture="brick")


    sound.play_dialog4()

    GameScene4.append(player)
    GameScene4.append(lava)
    GameScene4.append(ground)
    GameScene4.append(spawn)

def main():
    main_menu()
    util.set_scene(MainMenuScene1, scenes)

def update():
    global TimeWhenTextureChanged

    if currentScene == GameScene1:
        for platform in platforms:
            if platform.intersects(player.player).hit:
                platform.color = color.white50
            else:
                platform.color = color.green
        
        if portalList[1].intersects(player.player).hit or portalList[0].intersects(player.player).hit:
            game_scene2()
            util.set_scene(GameScene2, scenes)


    if currentScene == GameScene2:
        for platform in platforms:
            if platform.intersects(player.player).hit:
                platform.color = color.white50
            else:
                platform.color = color.green
        
        if portalList[1].intersects(player.player).hit or portalList[0].intersects(player.player).hit:
            util.set_scene(GameScene3, scenes)
            game_scene3()

        if time.time() - TimeWhenTextureChanged >= textureChangeCoolDown:
            randomScale = (3 + random.random()) * 10
            set_lava_scale((randomScale, randomScale))
            TimeWhenTextureChanged = time.time()
    
    if currentScene == GameScene3:
        for platform in platforms:
            if platform.intersects(player.player).hit:
                platform.color = color.white50
            else:
                platform.color = color.green

        if portalList[1].intersects(player.player).hit or portalList[0].intersects(player.player).hit:
            util.set_scene(GameScene4, scenes)
            game_scene4()

        if time.time() - TimeWhenTextureChanged >= textureChangeCoolDown:
            randomScale = (3 + random.random()) * 10
            set_lava_scale((randomScale, randomScale))
            TimeWhenTextureChanged = time.time()
    
    if currentScene == GameScene4:
        if time.time() - TimeWhenTextureChanged >= textureChangeCoolDown:
            randomScale = (3 + random.random()) * 10
            set_lava_scale((randomScale, randomScale))
            TimeWhenTextureChanged = time.time()

    for movingPlatform in MovingPlatFormsList:
        movingPlatform.update()

        if movingPlatform.Entity.intersects(player.player).hit:
            movingPlatform.Entity.color = color.white50
        else:
            movingPlatform.Entity.color = color.blue


main()
Sky()
app.run()
