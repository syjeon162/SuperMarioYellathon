import pygame
import random
import sys, time

# Modified from http://programarcadegames.com/python_examples/show_file.php?file=platform_scroller.py

FPS = int(input("Enter desired framerate (30, 60, or 120): "))

# Colors
BLACK = (0, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    # From Stackoverflow, Google "pygame draw background image"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 30
        self.height = 40
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/oimr_right.png').convert_alpha(),
            (self.width, self.height)), 0)
        self.facing = "right"
        self.walking = False
        self.rect = self.image.get_rect() 
        self.change_x = 0
        self.change_y = 0
        self.level = None
 
    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        if self.change_x < 0:
            self.walking = True
            self.facing = "left"
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/oimr_left_walk.png').convert_alpha(),
                (self.width+5, self.height)), 0)
        elif self.change_x > 0:
            self.walking = True
            self.facing = "right"
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/oimr_right_walk.png').convert_alpha(),
                (self.width+5, self.height)), 0)
        else:
            self.walking = False
            if self.facing == "right":
                self.image = pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load('images/oimr_right.png').convert_alpha(),
                    (self.width, self.height)), 0)
            else:
                self.image = pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load('images/oimr_left.png').convert_alpha(),
                    (self.width, self.height)), 0)
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.image = pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load('images/oimr_right.png').convert_alpha(),
                    (self.width, self.height)), 0)
        self.rect.y += self.change_y
        if self.change_y != 0:
            if self.facing == "right":
                self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/oimr_right_air.png').convert_alpha(),
                (self.width+5, self.height)), 0)
            else:
                self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/oimr_left_air.png').convert_alpha(),
                (self.width+5, self.height)), 0)
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
            if self.walking:
                if self.facing == "right":
                    self.image = pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load(
                        'images/oimr_right_walk.png').convert_alpha(),
                    (self.width+5, self.height)), 0)
                else:
                    self.image = pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load(
                        'images/oimr_left_walk.png').convert_alpha(),
                    (self.width+5, self.height)), 0)
            else:
                if self.facing == "right":
                    self.image = pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load('images/oimr_right.png').convert_alpha(),
                    (self.width, self.height)), 0)
                else:
                    self.image = pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load('images/oimr_left.png').convert_alpha(),
                    (self.width, self.height)), 0)
 
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom+10 >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        self.change_x = -4
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/oimr_left_walk.png').convert_alpha(),
            (self.width+5, self.height)), 0)

    def go_right(self, audio):
        self.change_x = audio.curSpeed
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/oimr_right_walk.png').convert_alpha(),
            (self.width+5, self.height)), 0)

    def stop(self):
        self.change_x = 0
 
 
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.image.load("images/brick.png")
        self.rect = self.image.get_rect()
 

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.world_shift = 0
 
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        BackGround = Background('images/background.png', [0,0])
        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
        self.world_shift += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
 

class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        for platform in Game.rectList:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            self.enemy_list.add(block)

class Projectile(pygame.sprite.Sprite):

    projectileList = []
    projGroup = pygame.sprite.Group()


    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.vx, self.vy = vx, vy
        width, height = 20,60
        self.message = ''
        self.radius = random.randint(10,20)
        self.image = pygame.image.load("images/arrow.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        Projectile.projGroup.add(self)
        Projectile.projectileList.append(self)

    def update(self):
        self.rect.y += self.vy

    def shift_projectile(self, shift_x):
        self.rect.x += shift_x

    def distance(x0,y0,x1,y1):
        return ((x0-x1)**2 + (y0-y1)**2)**0.5

    def collide(player):
        if pygame.sprite.spritecollideany(player, Projectile.projGroup):
            Game.gameOver = True
            player.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/oimr_ded.png').convert_alpha(),
            (player.width+10, player.height)), 0)

class Game(object):
    rectList = []
    gameStart = False
    gameOver = False

def createRects(Game,x,y):
    x += random.randint(50,500)
    y = SCREEN_HEIGHT - random.randint(50,100)
    width = random.randint(100,500)
    height = SCREEN_HEIGHT-y
    Game.rectList.append([width,height,x,y])
    return (x,y,width,height)

def drawGameOver(screen, audio):
    if Game.gameOver == True:
        text = pygame.font.Font(None, 40).render("Game Over", True, (0,0,0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
            screen.get_height() //2 - text.get_height() * 2))
        text2 = pygame.font.Font(None, 30).render("Score:%d"%audio.timePassed, True, (0,0,0))
        screen.blit(text2, (screen.get_width() // 2 - text2.get_width() // 2,
            screen.get_height() //2 - text2.get_height()*.9))
        text3 = pygame.font.Font(None, 30).render("Press R to restart", True, (0,0,0))
        screen.blit(text3, (screen.get_width() // 2 - text3.get_width() // 2,
            screen.get_height() //2 + text3.get_height() * 1.2))

def main(a):
    pygame.init()

    def initaudio(audio, a):
        audio.posX = 0
        audio.constantSpeed = 5
        audio.curSpeed = audio.constantSpeed
        audio.targetSpeed = audio.constantSpeed
        audio.acc = 1
        audio.timePassed = 0
        audio.font = pygame.font.Font(None, 30)
        audio.message = ""
        audio.threshold = 66
        audio.sensitivity = 1
        audio.timeIncrement = 0.05
        audio.timePassed = 0
        audio.maxSpeed = 20

    def update(audio):
        audio.timePassed += audio.timeIncrement
        audio.message = ("Pitch = %d, Speed = %d, Target Speed = %d, Acceleration = %d, timePassed = %d"
            %(int(a.value), audio.curSpeed, audio.targetSpeed, audio.acc, audio.timePassed))
        audio.posX += audio.curSpeed*audio.timeIncrement

        if 0 < audio.curSpeed + audio.acc*audio.timeIncrement < audio.maxSpeed:
            audio.curSpeed += audio.acc*audio.timeIncrement

        if a.value == 0: audio.targetSpeed = audio.constantSpeed
        else:
            if a.value > audio.threshold: sign = 1
            else: sign = -1
            audio.targetSpeed = abs(a.value - audio.threshold)**0.5*sign*1.3 + audio.constantSpeed
        audio.acc = (audio.targetSpeed - audio.curSpeed) * audio.sensitivity

    def redrawAll(audio, screen):
        text = audio.font.render(audio.message, True, (0,0,0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                            screen.get_height() - text.get_height() * 2))

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Side-scrolling Platformer")

    class Struct(object): pass
    audio = Struct()
    initaudio(audio, a)
    
    class Struct(object): pass
    data = Struct()
    def init(data):
        data.player = Player()
        data.startX,data.startY = 50,50
        data.count = 0
        while data.startX < 20000:
            if data.count%10 == 0:
                data.startX,data.startY,data.width,data.height = createRects(Game,data.startX,data.startY)
        # Create all the levels
        data.level_list = [Level_01(data.player)]
        data.current_level = data.level_list[0]
        data.active_sprite_list = pygame.sprite.Group()
        data.player.level = data.current_level
        data.player.rect.x = 0
        data.player.rect.y = SCREEN_HEIGHT - data.player.rect.height
        data.active_sprite_list.add(data.player)
        # Loop until the user clicks the close button.
        data.done = False
        # Used to manage how fast the screen updates
        data.clock = pygame.time.Clock()
        data.counter = 0
    init(data)

    # -------- Main Program Loop -----------
    while not data.done:
        while not data.done:
            Projectile.collide(data.player)
            for event in pygame.event.get():
                num = random.randint(0,10)
                if num < 10 and not Game.gameOver:
                    x_pos = random.randint(SCREEN_WIDTH//2 +200, SCREEN_WIDTH*3//2)
                    y_vel = random.randint(5,10)
                    Projectile(x_pos,0,0,y_vel)
                if event.type == pygame.QUIT:
                    data.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and not Game.gameOver:
                            data.player.jump()
                    if event.key == pygame.K_r:
                        init(data)
                        initaudio(audio, a)
                        Game.rectList = []
                        Projectile.projectileList = []
                        Game.gameOver = False
            if not Game.gameOver:
                update(audio)
                data.player.go_right(audio)
            data.counter += 1
            
            # Update
            if not Game.gameOver:
                data.active_sprite_list.update()
                data.current_level.update()
                Projectile.projGroup.update()

            # Shift
            if data.player.rect.right >= 400:
                diff = data.player.rect.right - 400
                data.player.rect.right = 400
                data.current_level.shift_world(-diff)
                for projectile in Projectile.projGroup.sprites():
                    projectile.shift_projectile(-diff)

            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            data.current_level.draw(screen)
            Projectile.projGroup.draw(screen)
            drawGameOver(screen, audio)
            data.active_sprite_list.draw(screen)
            redrawAll(audio, screen)
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            
            # Limit to 60 frames per second
            data.clock.tick(60)
                # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
 
    pygame.quit()
 
if __name__ == "__main__":
    main()