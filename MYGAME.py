# This file was created by: Daniel Barandica
# Sources: http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/

# import libs
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
# import settings 
import os
from settings import *
from sprites import *
import math

vec = pg.math.Vector2

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")
snd_folder = os.path.join(game_folder, 'sounds')


# create game class in order to pass properties to the sprites file
class Game:
    def __init__(self):
        # init game window etc.
        pg.init()
        pg.mixer.init()
        # makes display of screen and game
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("my game")
        self.clock = pg.time.Clock()
        self.running = True


    def new(self):
        # starting a new game
        # create group for sprites
        # defines score
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_ice = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()

        # instantiate classes
        self.player = Player(self)

        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        for m in range(0,5):
            # help generate 5 "mobs" in map
            m = Mob(randint(0,WIDTH), randint(0,math.floor(HEIGHT/2)),20,20,"normal")
            # mobs get their own sprite, class
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        for _ in range(0, 3):
            # generate 3 random "powerups" for player in map
            powerup = powerup(randint(0, WIDTH), randint(0, math.floor(HEIGHT / 2)), 20, 20, "normal")
            # gives powerup own class
            self.all_sprites.add(powerup)
            self.all_powerups.add(powerup)

        self.run()



    def run(self):
        # game checks for updates as game progresses
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    

    def events(self):
        # check for closed window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()



    def update(self):
        # game learns when the character hits a mob
        self.all_sprites.update()
        if self.player.vel.y > 0:
            mhits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if mhits:
                print('this collision happened in main')
                self.score -= 1
            phits = pg.sprite.spritecollide(self.player, self.all_powerups, False)
            if phits:
                print('this collision happened in main')
                self.score += 1
                # if player score becomes 0, start again with 5 points
            if self.score == 0:
                self.player.pos = vec(WIDTH/2, HEIGHT/2)
                self.score = 5
            self.all_sprites.update()

        # allows player to move from left to right side of screen using edges, not just disappear
        if self.player.pos.x<0:
            self.player.pos.x = WIDTH
        if self.player.pos.x>WIDTH:
            self.player.pos.x=0

                    

    def draw(self):
        self.screen.fill(RED)
        self.draw_text("MYGAME", 30, WHITE, WIDTH/4, HEIGHT/2)
        self.all_sprites.draw(self.screen)

       
        pg.display.flip()
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('Comic Sans')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)

# instantiate the game class...
g = Game()

# kick off the game loop
while g.running:
    g.new()

pg.quit()