from pygame import *
import time as t

SC_WIDTH = 700
SC_HEIGHTS = 500
init()
window = display.set_mode((SC_WIDTH, SC_HEIGHTS))
background = transform.scale(image.load('back.jpg'),(SC_WIDTH, SC_HEIGHTS))
death_sc = transform.scale(image.load('dead.jpg'),(SC_WIDTH, SC_HEIGHTS))
win_sc = transform.scale(image.load('god.jpg'),(SC_WIDTH, SC_HEIGHTS))
window.blit(background,(0, 0))

f1 = font.SysFont('PC_CGA', 50)
clock = time.Clock()
FPS = 60

class Player(sprite.Sprite):
    def __init__(self, x, y, Xhitbox, Yhitbox, img='h.jpg'):
        super().__init__()
        
        mage = image.load(img)
        self.Xhitbox = Xhitbox
        self.Yhitbox = Yhitbox
        self.image = transform.scale(mage, (self.Xhitbox, self.Yhitbox))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0
        self.walls = None
        self.end = None

        self.enemies = sprite.Group()
        self.live = True
        self.level = 0

    def tp_to(self, x ,y):
        self.change_x = 0
        self.change_y = 0
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.change_x
        if sprite.spritecollide(self, self.enemies, False):
            self.live = False
        wall_hit_list = sprite.spritecollide(self, self.walls, False)
        for wall in wall_hit_list:
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        self.rect.y += self.change_y
        wall_hit_list = sprite.spritecollide(self, self.walls, False)
        for wall in wall_hit_list:
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

        if sprite.spritecollide(self, self.end, False):
            self.live = 'W'

            



class Wall(sprite.Sprite):
    def __init__(self, Xhitbox, Yhitbox, x, y, img='wall.png'):
        super().__init__()
        mage = image.load(img)
        self.Xhitbox = Xhitbox
        self.Yhitbox = Yhitbox
        self.image = transform.scale(mage, (self.Xhitbox, self.Yhitbox))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Maze:
    def __init__(self):
        self.M = 15
        self.N = 11
        self.maze =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                      1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,
                      1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,
                      1,0,1,0,1,0,0,1,0,1,0,0,0,0,1,
                      1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,
                      1,0,1,1,1,1,1,1,0,1,0,0,0,0,1,
                      1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,
                      1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,
                      1,2,2,2,2,2,2,2,2,1,0,0,0,0,1,
                      1,1,1,1,1,1,1,1,1,1,0,0,0,2,1,
                      0,0,0,0,0,0,0,0,0,0,1,1,1,1,1]

    def maze_draw(self, display_surf, image_surf1, image_surf2):
        bx = 0
        by = 0
        for i in range(0,self.M*self.N):
            if self.maze[bx + (by*self.M) ] == 1:
                display_surf.blit(image_surf1, (bx * 50, by * 50))
                
            elif self.maze[bx + (by*self.M) ] == 2:
                display_surf.blit(image_surf2, (bx * 50, by * 50))
      
            bx = bx + 1
            if bx > self.M-1:
                bx = 0 
                by = by + 1

    def maze_col(self):
        bx = 0
        by = 0
        wall_list = list()
        end_list = list()
        for i in range(0,self.M*self.N):
            if self.maze[bx + (by*self.M) ] == 1:
                wall_list.append(Wall(50, 50, bx * 50, by * 50))
            elif self.maze[bx + (by*self.M) ] == 2:
                end_list.append(Wall(50, 50, bx * 50, by * 50))
        
            bx = bx + 1
            if bx > self.M-1:
                bx = 0 
                by = by + 1
        return wall_list, end_list

class End(sprite.Sprite):
    def __init__(self, Xhitbox, Yhitbox, x, y, img='ending.jpg'):
        super().__init__()
        mage = image.load(img)
        self.Xhitbox = Xhitbox
        self.Yhitbox = Yhitbox
        self.image = transform.scale(mage, (self.Xhitbox, self.Yhitbox))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(sprite.Sprite):
    def __init__(self, x, y, Xhitbox, Yhitbox, stop, img='b.jpg'):
        super().__init__()
        mage = image.load(img)
        self.Xhitbox = Xhitbox
        self.Yhitbox = Yhitbox
        self.image = transform.scale(mage, (self.Xhitbox, self.Yhitbox))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start = x
        self.stop = x + stop
        self.direction = 1

    def update(self, h):
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        elif self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1
        self.rect.x += self.direction * h

all_sprite_list = sprite.Group()
enemy_sprite_list = sprite.Group()
maze = Maze()
wall = Wall(50, 50, 0, 0)
end = End(50, 50, 0, 0)
enemy1 = Enemy(250, 105, 40, 40, 160)
enemy2 = Enemy(50, 405, 40, 40, 360)
enemy3 = Enemy(500, 155, 40, 40, 160)
enemy4 = Enemy(500, 255, 40, 40, 160)
enemy5 = Enemy(500, 355, 40, 40, 160)

enemy_sprite_list.add(enemy1, enemy2, enemy3, enemy4, enemy5)

player = Player(50, 50, 40, 40)
all_sprite_list.add(player)

player.enemies = [enemy1, enemy2, enemy3, enemy4, enemy5]
wall_list, end_list = maze.maze_col()
player.walls = wall_list
player.end = end_list

#start = t.time()

game = True
h = 1
#att = 1
while game:
    window.blit(background,(0, 0))
    keys_pressed = key.get_pressed()


    while player.live == False:
        window.blit(death_sc,(0, 0))

        text2 = f1.render('press space to retry', True, (200, 0, 0))
        window.blit(text2, (185, 310))
        for e in event.get():
            if e.type == QUIT:
                player.live = True
                game = False

            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    h = 1
                    #att += 1
                    player.tp_to(50, 50)
                    player.live = True

        display.update()
        clock.tick(FPS)

    while player.live == 'W':
        window.blit(win_sc,(0, 0))

        text1 = f1.render('speed increased to ' + str(h+1), True, (255, 255, 255))
        window.blit(text1, (185, 290))
        text2 = f1.render('press space to continue', True, (255, 255, 255))
        window.blit(text2, (165, 330))
        #text2 = f1.render('attempt - ' + str(att), True, (255, 255, 255))
        #window.blit(text2, (275, 140))

        #tt = t.time() - start
        #text3 = f1.render('time - ' + str(tt), True, (255, 255, 255))
        #window.blit(text3, (185, 180))

        for e in event.get():
            if e.type == QUIT:
                player.live = True
                game = False

            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    h += 1
                    start = t.time()
                    player.tp_to(50, 50)
                    player.live = True
        display.update()



    for ez in event.get():
        if ez.type == QUIT:
            game = False
        elif ez.type == KEYDOWN:
            if ez.key == K_a:
                player.change_x += -10       
            if ez.key == K_d:
                player.change_x += 10   
            if ez.key == K_w:
                player.change_y += -10   
            if ez.key == K_s:
                player.change_y += 10 

        elif ez.type == KEYUP:
            if ez.key == K_a:
                player.change_x = 0       
            elif ez.key == K_d:
                player.change_x = 0   
            elif ez.key == K_w:
                player.change_y = 0   
            elif ez.key == K_s:
                player.change_y = 0

    maze.maze_draw(window, wall.image, end.image)
    enemy_sprite_list.update(h)
    enemy_sprite_list.draw(window)
    all_sprite_list.update()
    all_sprite_list.draw(window)
    display.update()
    clock.tick(FPS)




















