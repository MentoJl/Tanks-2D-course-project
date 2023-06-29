import pygame
from field import Field
from enum import Enum


class Bullet_Direction(Enum):
    Up = 1
    Down = 2
    Right = 3
    Left = 4

class Bullet_Sprite(pygame.sprite.Sprite):

    direction = None

    def __init__(self, width, height, start, direction): # Initialization bullet direction
        self.direction = direction
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "./icon/Tank/bullet.png")
        self.image = pygame.transform.scale(
            self.image, (width, height))
        match(self.direction):
            case Bullet_Direction.Down:
                self.image = pygame.transform.rotate(self.image, 180)
            case Bullet_Direction.Right:
                self.image = pygame.transform.rotate(self.image, 270)
            case Bullet_Direction.Left:
                self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=start)

    def update(self, step): # Bullet moving
        match(self.direction):
            case Bullet_Direction.Up:
                self.rect.y -= (step * 3)
            case Bullet_Direction.Down:
                self.rect.y += (step * 3)
            case Bullet_Direction.Right:
                self.rect.x += (step * 3)
            case Bullet_Direction.Left:
                self.rect.x -= (step * 3)

class Tank_Sprite(pygame.sprite.Sprite):

    anim = 0
    anim_time = 0

    def __init__(self, tank_position, tank_size, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets[0]
        self.image = pygame.transform.scale(self.image, (tank_size, tank_size))
        self.rect = self.image.get_rect(center=tank_position)

    def rotate_img(self, assets, tank_size, rotate): # Set tank direction 
        if self.anim_time >=5:
            self.anim += 1
            self.anim_time = 0
        if self.anim >= len(assets.tank_assets):
            self.anim = 0
        self.image = assets.tank_assets[self.anim]
        self.image = pygame.transform.scale(self.image, (tank_size, tank_size))
        self.image = pygame.transform.rotate(self.image, rotate)
        self.anim_time += 1

class Tank(pygame.sprite.Sprite):

    class Assets(pygame.sprite.Sprite):
        tank_assets = None

        def __init__(self, tank_assets):
            self.tank_assets = tank_assets
        
        def change_img(self, asset):
            self.tank_assets = asset

    keys = {"Up": None, 
    "Down": None,
    "Left": None,
    "Right": None,
    "Shoot": None}
    direction = Bullet_Direction.Right
    bullets = None 
    tank_size = None 
    tank = None
    mega_shoot = False
    time = 100 # Shoot CD
    hp = int(100)
    shells = 10
    damage = None

    def __init__(self, wall_size, tank_position, tank_rotate, bullet_direction, tank_assets):
        self.assets = self.Assets(tank_assets)
        self.tank_size = wall_size - 10
        self.damage = 25
        self.mega = False
        self.bullets = pygame.sprite.Group()
        self.tank = Tank_Sprite(tank_position, self.tank_size, self.assets.tank_assets)
        self.tank.rotate_img(self.assets, self.tank_size, tank_rotate)
        self.rotate = tank_rotate
        self.direction = bullet_direction

    def tank_info_display(self, screen, x, y, width, player_number, info): # Tank info
        font = pygame.font.SysFont("Nimbus Sans", int(width * 1.875 // 100))
        text = font.render(f"Player {player_number}", 1, (255,255,255))
        screen.blit(text, (x, y)); y += (width * 3.125 // 100)
        text = font.render(f"HP: {self.hp}", 1, (255,50,50))
        screen.blit(text, (x, y)); y += (width * 2.083 // 100)
        text = font.render(f"Bullets: {self.shells}", 1, (50,50,255))
        screen.blit(text, (x, y)); y += (width * 3.125 // 100)
        text = font.render(f"Controls:", 1, (255,255,255))
        screen.blit(text, (x, y))
        for key in self.keys:
            text = font.render(f"{key}: {pygame.key.name(self.keys[key])}", 1, (50,255,50))
            y += (width * 2.083 // 100)
            screen.blit(text, (x, y))
        if info:
            font = pygame.font.SysFont("Nimbus Sans", int(width * 1.3 // 100))
            text = font.render(f"Map created by Yakysevich", 1, (255,255,255))
            screen.blit(text, (width // 2, 0))
        

    def keysf(self, interaction): # Keys iteraction
        count = 0
        for i in self.keys:
            self.keys[i] = interaction[count]
            count += 1

    def touchable(self, enemy_tank, ammunation, health_point, mega):
        if pygame.sprite.spritecollide(enemy_tank.tank, self.bullets, False):
            if self.mega_shoot:
                enemy_tank.hp -= self.damage * 2
            else:
                enemy_tank.hp -= self.damage
            if enemy_tank.hp < 0:
                enemy_tank.hp = 0
        if self.hp <= 0:
            self.assets.change_img([pygame.image.load("./icon/Tank/destroyeed_tank.png")])
            self.tank.rotate_img(self.assets, self.tank_size, self.rotate)
        if pygame.sprite.spritecollide(self.tank, ammunation, True):
            self.shells += 5
        if pygame.sprite.spritecollide(self.tank, health_point, True):
            self.hp += 50
        if pygame.sprite.spritecollide(self.tank, mega, True):
            self.mega = True

    def display(self, screen, field, enemy_tank, width): # Display sprites
        if self.hp > 0:
            self.movement(field.walls, enemy_tank.tank, width)
        if self.bullets:
            self.bullets.update(2)
            self.bullets.draw(screen)
        screen.blit(self.tank.image, self.tank.rect)
        self.touchable(enemy_tank, field.ammunation, field.health_Points, field.mega)
        field.walls.update(screen, enemy_tank.tank, self.bullets, self.mega_shoot)

    def movement(self, walls, enemy_tank, width): # Tank iteraction
        step = 2
        key = pygame.key.get_pressed()

        if key[self.keys["Down"]]: # Reaction to pressing key to moving DOWN
            self.tank.rect.y += step
            if pygame.sprite.spritecollide(self.tank, walls, False) or self.tank.rect.colliderect(enemy_tank):
                self.tank.rect.y -= step
            self.rotate = 270
            self.tank.rotate_img(self.assets, self.tank_size, self.rotate)
            self.direction = Bullet_Direction.Down

        elif key[self.keys["Up"]]: # Reaction to pressing key to moving UP
            self.tank.rect.y -= step
            if pygame.sprite.spritecollide(self.tank, walls, False) or self.tank.rect.colliderect(enemy_tank):
                self.tank.rect.y += step
            self.rotate = 90
            self.tank.rotate_img(self.assets, self.tank_size, self.rotate)
            self.direction = Bullet_Direction.Up

        elif key[self.keys["Left"]]: # Reaction to pressing key to moving LEFT
            self.tank.rect.x -= step
            if pygame.sprite.spritecollide(self.tank, walls, False) or self.tank.rect.colliderect(enemy_tank):
                self.tank.rect.x += step
            self.rotate = 180
            self.tank.rotate_img(self.assets, self.tank_size, self.rotate)
            self.direction = Bullet_Direction.Left

        elif key[self.keys["Right"]]: # Reaction to pressing key to moving RIGHT
            self.tank.rect.x += step
            if pygame.sprite.spritecollide(self.tank, walls, False) or self.tank.rect.colliderect(enemy_tank):
                self.tank.rect.x -= step
            self.rotate = 0
            self.tank.rotate_img(self.assets, self.tank_size, self.rotate)
            self.direction = Bullet_Direction.Right

        if key[self.keys["Shoot"]] and self.time >= 100 and self.shells > 0: # Reaction to pressing key to SHOOTING
            self.bullets.add(Bullet_Sprite(
                (width * 0.416 // 100), (width * 1.302 // 100), self.tank.rect.center, self.direction))
            if not self.mega and self.mega_shoot:
                self.mega_shoot = False
            if self.mega and not self.mega_shoot:
                self.mega_shoot = True
            if self.mega:
                self.mega = False
            self.time = 0
            self.shells -= 1
        self.time += 1 