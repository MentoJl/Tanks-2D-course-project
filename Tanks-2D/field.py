import pygame


class Assets:
    explosion_imgs = [pygame.image.load("./icon/Explosions/Explosion_1.png"),\
                pygame.image.load("./icon/Explosions/Explosion_2.png"),\
                pygame.image.load("./icon/Explosions/Explosion_3.png"),\
                pygame.image.load("./icon/Explosions/Explosion_4.png"),\
                pygame.image.load("./icon/Explosions/Explosion_5.png"),\
                pygame.image.load("./icon/Explosions/Explosion_6.png"),\
                pygame.image.load("./icon/Explosions/Explosion_7.png")]
    mega_explosion_imgs = [pygame.image.load("./icon/Mega_Explosion/001.png"),\
                pygame.image.load("./icon/Mega_Explosion/002.png"),\
                pygame.image.load("./icon/Mega_Explosion/003.png"),\
                pygame.image.load("./icon/Mega_Explosion/004.png"),\
                pygame.image.load("./icon/Mega_Explosion/005.png"),\
                pygame.image.load("./icon/Mega_Explosion/006.png"),\
                pygame.image.load("./icon/Mega_Explosion/007.png"),\
                pygame.image.load("./icon/Mega_Explosion/008.png"),\
                pygame.image.load("./icon/Mega_Explosion/009.png"),\
                pygame.image.load("./icon/Mega_Explosion/010.png"),\
                pygame.image.load("./icon/Mega_Explosion/011.png"),\
                pygame.image.load("./icon/Mega_Explosion/012.png"),\
                pygame.image.load("./icon/Mega_Explosion/013.png"),\
                pygame.image.load("./icon/Mega_Explosion/014.png"),\
                pygame.image.load("./icon/Mega_Explosion/015.png")]
    mega_imgs = [pygame.image.load("./icon/Mega/001.png"),\
                pygame.image.load("./icon/Mega/002.png"),\
                pygame.image.load("./icon/Mega/003.png"),\
                pygame.image.load("./icon/Mega/004.png"),\
                pygame.image.load("./icon/Mega/005.png"),\
                pygame.image.load("./icon/Mega/006.png"),\
                pygame.image.load("./icon/Mega/007.png"),\
                pygame.image.load("./icon/Mega/008.png"),\
                pygame.image.load("./icon/Mega/009.png"),\
                pygame.image.load("./icon/Mega/010.png"),\
                pygame.image.load("./icon/Mega/011.png"),\
                pygame.image.load("./icon/Mega/012.png"),\
                pygame.image.load("./icon/Mega/013.png"),\
                pygame.image.load("./icon/Mega/014.png"),\
                pygame.image.load("./icon/Mega/015.png"),\
                pygame.image.load("./icon/Mega/016.png")]
    wall_img = pygame.image.load("./icon/Field/wall.png")
    bullet_box_img = pygame.image.load("./icon/Field/bullet_box.png")
    grass_img = pygame.image.load("./icon/Field/grass.png")
    health_point_imgs = [pygame.image.load("./icon/Heart/001.png"),
    pygame.image.load("./icon/Heart/002.png"),
    pygame.image.load("./icon/Heart/003.png"),
    pygame.image.load("./icon/Heart/004.png"),
    pygame.image.load("./icon/Heart/005.png")]

class Wall_Sprite(pygame.sprite.Sprite):

    exlposion_progress = False
    anim = 0
    anim_time = 0
    mega = False

    def __init__(self, wall_size, i, j):
        pygame.sprite.Sprite.__init__(self)
        self.image = Assets.wall_img
        self.explosion_size = wall_size
        self.image = pygame.transform.scale(self.image, (wall_size, wall_size))
        self.rect = self.image.get_rect(topleft = (j * wall_size, i * wall_size))

    def update(self, screen, enemy_tank, bullets, mega): # Collision check & Display explosion
        if pygame.sprite.spritecollide(self, bullets, False):
            self.hit = pygame.sprite.spritecollide(self, bullets, True)
            self.exlposion_progress = True
            self.mega = mega
            
        elif pygame.sprite.spritecollide(enemy_tank, bullets, False):
            self.hit = pygame.sprite.spritecollide(enemy_tank, bullets, True)
            self.exlposion_progress = True
            self.mega = mega

        if self.exlposion_progress: #Display explosion
            asset = Assets() # Explosion img
            if self.mega:
                explosion_imgs = asset.mega_explosion_imgs
                anim_FPS = 3
                size = self.explosion_size * 3
            else:
                explosion_imgs = asset.explosion_imgs
                anim_FPS = 10
                size = self.explosion_size
            self.anim_time += 1
            explosion_imgs[self.anim] = pygame.transform.scale(explosion_imgs[self.anim], (size, size))
            rect = explosion_imgs[self.anim].get_rect(center = self.hit[0].rect.center)
            screen.blit(explosion_imgs[self.anim], rect)
            if self.anim_time >= anim_FPS:
                self.anim += 1
                self.anim_time = 0
            if self.anim >= len(explosion_imgs):
                self.anim = 0
                self.exlposion_progress = False

class Bullet_Box_Sprite(pygame.sprite.Sprite):
    def __init__(self, wall_size, i, j):
        pygame.sprite.Sprite.__init__(self)
        self.image = Assets.bullet_box_img # Bullet img
        self.image = pygame.transform.scale(self.image, (wall_size-10, wall_size-10))
        self.rect = self.image.get_rect(center = ((j * wall_size) + (wall_size / 2), (i * wall_size) + (wall_size / 2)))

class Health_Point_Sprite(pygame.sprite.Sprite):

    size = None
    anim = 0
    anim_time = 0
    anim_FPS = 30
    x = None
    y = None

    def __init__(self, wall_size, i, j):
        pygame.sprite.Sprite.__init__(self)
        self.size = wall_size - 15
        self.x = (j * wall_size) + (wall_size / 2)
        self.y = (i * wall_size) + (wall_size / 2)
        
    def update(self, screen):
        self.image = Assets.health_point_imgs[self.anim] # Health point img
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.anim_time += 1
        screen.blit(self.image, self.rect)
        if self.anim_time >= self.anim_FPS:
            self.anim += 1
            self.anim_time = 0
        if self.anim >= len(Assets.health_point_imgs):
            self.anim = 0
            self.exlposion_progress = False

class Mega_Sprite(pygame.sprite.Sprite):

    size = None
    anim = 0
    anim_time = 0
    anim_FPS = 5
    x = None
    y = None

    def __init__(self, wall_size, i, j):
        pygame.sprite.Sprite.__init__(self)
        self.size = wall_size - 15
        self.x = (j * wall_size) + (wall_size / 2)
        self.y = (i * wall_size) + (wall_size / 2)
        
    def update(self, screen):
        self.image = Assets.mega_imgs[self.anim] # Mega img
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.anim_time += 1
        screen.blit(self.image, self.rect)
        if self.anim_time >= self.anim_FPS:
            self.anim += 1
            self.anim_time = 0
        if self.anim >= len(Assets.mega_imgs):
            self.anim = 0
            self.exlposion_progress = False
                
class Field(pygame.sprite.Sprite):
    screen = None
    walls = None
    ammunation = None
    health_Points = None
    mega = None

    gamefield = None # Gamefield

    def __init__(self, wall_size, gamefield):
        pygame.sprite.Sprite.__init__(self)



        self.walls = pygame.sprite.Group()




        self.ammunation = pygame.sprite.Group()
        self.health_Points = pygame.sprite.Group()
        self.mega = pygame.sprite.Group()
        self.gamefield = gamefield
        for i in range(0, len(self.gamefield)):
            for j in range(0, len(self.gamefield[i])):
                if self.gamefield[i][j] == "#":
                    self.walls.add(Wall_Sprite(wall_size, i, j))
                elif self.gamefield[i][j] == "@":
                    self.ammunation.add(Bullet_Box_Sprite(wall_size, i, j))
                elif self.gamefield[i][j] == "$":
                    self.health_Points.add(Health_Point_Sprite(wall_size, i, j))
                elif self.gamefield[i][j] == "*":
                    self.mega.add(Mega_Sprite(wall_size, i, j))
        self.grass = Assets.grass_img # Grass img

    def display(self, screen, wall_size): # Display gamefield
        pygame.sprite.Sprite.__init__(self)
        self.grass = pygame.transform.scale(self.grass, (wall_size, wall_size))
        for i in range(0, len(self.gamefield)):
            for j in range(0, len(self.gamefield[i])):
                self.rect = self.grass.get_rect(topleft = (j * wall_size, i * wall_size))
                screen.blit(self.grass, self.rect)
        self.walls.draw(screen)
        if self.ammunation:
            self.ammunation.draw(screen)
        if self.health_Points:
            self.health_Points.update(screen)
        if self.mega:
            self.mega.update(screen)