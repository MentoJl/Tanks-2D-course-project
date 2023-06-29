import pygame
from tank import Tank
from tank import Bullet_Direction
from field import Field
from tkinter import *


class Display:
    screen = None
    clock = None
    bg = None
    wall_size = None
    Width = None
    Full_Width = None
    Height = None

    class Button(pygame.sprite.Sprite):
        sizeX = None
        sizeY = None
        img = None
        position = None

        def __init__(self, img, sizeX, sizeY,  position):
            self.sizeX = sizeX
            self.sizeY = sizeY
            self.img = img
            self.position = position
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(img)
            self.image = pygame.transform.scale(self.image, (sizeX, sizeY))
            self.rect = self.image.get_rect(center=position)

        def scale(self, sizeX, sizeY):
            self.image = pygame.image.load(self.img)
            self.image = pygame.transform.scale(self.image, (sizeX, sizeY))
            self.rect = self.image.get_rect(center=self.position)

        def update(self, screen): screen.blit(self.image, self.rect)

    def game_process(self, gamefield, info):
        FPS = 60
        tank = Tank(self.wall_size, [float(self.wall_size) / 2 + self.wall_size, float(self.wall_size) / 2 + self.wall_size],
                    0, Bullet_Direction.Right, [pygame.image.load("./icon/Tank/tank_00.png"),
            pygame.image.load("./icon/Tank/tank_01.png")])
        tank2 = Tank(self.wall_size, [self.Width - self.wall_size - (self.wall_size/2), self.Height - self.wall_size - (self.wall_size/2)],
                    180, Bullet_Direction.Left, [pygame.image.load("./icon/Tank/tank_10.png"),
            pygame.image.load("./icon/Tank/tank_11.png")])
        field = Field(self.wall_size, gamefield)
        game_stop = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((0, 0, 0))
            field.display(self.screen, self.wall_size)
            tank.keysf([pygame.K_w, pygame.K_s, pygame.K_a,
                       pygame.K_d, pygame.K_LSHIFT])
            tank.tank_info_display(self.screen, (self.monitor_width * 51.125) // 100, (self.monitor_width * 2.604) // 100,
                                   self.monitor_width, 1, info) # Display tank info
            tank.display(self.screen, field, tank2, self.monitor_width)
            tank2.keysf([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT,
                        pygame.K_RIGHT, pygame.K_RSHIFT])
            tank2.tank_info_display(self.screen, (self.monitor_width * 51.125) // 100, self.Height - (self.monitor_width * 23.437) // 100,
                                    self.monitor_width, 2, False) # Display tank2 info
            tank2.display(self.screen, field, tank, self.monitor_width)
            if tank.hp <=0 or tank2.hp <= 0:
                game_stop += 1
                if game_stop >= 100: # Game end
                    surf = pygame.Surface((self.Full_Width, self.Height)) 
                    surf.fill((0, 0, 0)) 
                    surf.set_alpha(70)
                    self.screen.blit(surf,(0,0))
                    print(self.Height)
                    if tank2.hp <= 0:
                        self.screen.blit(self.image_win1,((self.Width * 23.437) // 100,0))
                    elif tank.hp <= 0:
                         self.screen.blit(self.image_win2,((self.Width * 23.437) // 100,0))
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pressed = pygame.mouse.get_pressed()
                    if mouse_pos[0] >= self.back_button.rect.x and mouse_pos[0] <= (self.back_button.rect.x + self.back_button.sizeX) \
                       and mouse_pos[1] >= self.back_button.rect.y and mouse_pos[1] <= (self.back_button.rect.y + self.back_button.sizeY):
                        self.back_button.scale((self.Width * 27.083) // 100, (self.Width * 6.25) // 100)
                        if mouse_pressed[0] == True:
                            break
                    self.back_button.update(self.screen)
                    self.back_button.scale((self.Width * 26.041) // 100, (self.Width * 5.208) // 100)
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.time.delay(200)
        return True

    def levels_menu(self):
        FPS = 60
        pygame.time.delay(200)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pos[0] >= self.lvl_button_1.rect.x and mouse_pos[0] <= (self.lvl_button_1.rect.x + self.lvl_button_1.sizeX) \
                and mouse_pos[1] >= self.lvl_button_1.rect.y and mouse_pos[1] <= (self.lvl_button_1.rect.y + self.lvl_button_1.sizeY):
                self.lvl_button_1.scale((self.Width * 27.083) // 100, (self.Width * 6.25) // 100)
                if mouse_pressed[0] == True:
                   if self.game_process(
                ['################',
                 '#   #          #',            
                 '### # #  ####  #',
                 '#@#   #        #',
                 '# # #######  # #',
                 '# #       #  * #',
                 '#   ##### #  # #',
                 '### $#         #',
                 '#   ## ###     #',
                 '# ###  #$  #####',
                 '#   # ###     @#',
                 '# #   #@### ####',
                 '# # # #        #',
                 '# # # ##### ## #',
                 '#@#*#          #',
                 '################'], False):
                        return
            elif mouse_pos[0] >= self.lvl_button_2.rect.x and mouse_pos[0] <= (self.lvl_button_2.rect.x + self.lvl_button_2.sizeX) \
                and mouse_pos[1] >= self.lvl_button_2.rect.y and mouse_pos[1] <= (self.lvl_button_2.rect.y + self.lvl_button_2.sizeY):
                self.lvl_button_2.scale((self.Width * 27.083) // 100, (self.Width * 6.25) // 100)
                if mouse_pressed[0] == True:
                    if self.game_process(
                ['################',
                 '#              #',            
                 '#        #     #',
                 '# ####  ##$### #',
                 '#          ### #',
                 '## ###  #  ### #',
                 '#@ #@#  #      #',
                 '#  # #         #',
                 '#      * ## # @#',
                 '#  ##     # ####',
                 '# ###  #  #   @#',
                 '#  ##  #  # #  #',
                 '#           ## #',
                 '#  ###$# #  #  #',
                 '#           #  #',
                 '################'], True):
                        return
            self.lvl_button_1.update(self.screen)
            self.lvl_button_1.scale((self.Width * 26.041) // 100, (self.Width * 5.208) // 100)
            self.lvl_button_2.update(self.screen)
            self.lvl_button_2.scale((self.Width * 26.041) // 100, (self.Width * 5.208) // 100)
            pygame.display.update()
            self.clock.tick(FPS)

    def menu(self):
        FPS = 60
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pos[0] >= self.lvl_button.rect.x and mouse_pos[0] <= (self.lvl_button.rect.x + self.lvl_button.sizeX) \
                and mouse_pos[1] >= self.lvl_button.rect.y and mouse_pos[1] <= (self.lvl_button.rect.y + self.lvl_button.sizeY):
                self.lvl_button.scale(260,60)
                if mouse_pressed[0] == True:
                    self.levels_menu()
            self.lvl_button.update(self.screen)
            self.lvl_button.scale(250,50)
            pygame.display.update()
            self.clock.tick(FPS)

    def main(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.Full_Width, self.Height), vsync=1)
        pygame.display.set_caption("Tanks 2D")
        pygame.display.set_icon(pygame.image.load("./icon/main/caption.png"))
        self.menu()

    def __init__(self):
        root = Tk()
        self.monitor_width = root.winfo_screenwidth()
        self.clock = pygame.time.Clock()
        self.wall_size = (self.monitor_width * 3.125) // 100
        self.Width = self.wall_size * 16
        self.Full_Width = self.wall_size * 21
        self.Height = self.wall_size * 16
        self.image_win1 = pygame.image.load("./icon/menu/win1.png")
        self.image_win2 = pygame.image.load("./icon/menu/win2.png")
        self.image_win1 = pygame.transform.scale(self.image_win1, ((self.Width * 52.083) // 100, (self.Width * 15.625) // 100))
        self.image_win2 = pygame.transform.scale(self.image_win2, ((self.Width * 52.083) // 100, (self.Width * 15.625) // 100))
        self.bg = pygame.image.load("./icon/main/bg.jpg")
        self.bg = pygame.transform.scale(
            self.bg, (self.Full_Width, self.Height+5))
        self.lvl_button = self.Button(
            "./icon/menu/lvl_button.png", (self.Width * 26.041) // 100, (self.Width * 5.208) // 100, \
                 (self.Full_Width/2, self.Height/2))
        self.lvl_button_1 = self.Button(
            "./icon/menu/lvl_button1.png", (self.Width * 26.041) // 100, (self.Width * 5.208) // 100, \
                 (self.Full_Width/2, self.Height/2))
        self.lvl_button_2 = self.Button(
            "./icon/menu/lvl_button2.png", (self.Width * 26.041) // 100, (self.Width * 5.208) // 100, \
                 (self.Full_Width/2, self.Height/2+100))
        self.back_button = self.Button(
            "./icon/menu/back_button.png", (self.Width * 26.041) // 100, (self.Width * 5.208) // 100, \
                 (self.Width/2, self.Height/2+100))

tanks2D = Display()
tanks2D.main()