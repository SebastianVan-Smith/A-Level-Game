# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 16:11:30 2019

@author: sebastian
"""

import pygame as pg
import sys
from settings import *
from sprites import *
from showmenu import *
from loadlevel import *
from menu import *
from os import path

class Game:
    def __init__(self,level):
        global skin
        #initilise the game window and the clock the game runs on
        pg.init()
        self.screen = pg.display.set_mode((width, height),pg.FULLSCREEN)
        pg.display.set_caption(gamename)
        self.clock = pg.time.Clock()
        self.load_data(level)
        self.level=1
        self.skin=skin
    def load_data(self,level):
        game_folder = path.dirname(__file__)
        chosenlevel=path.join(game_folder, 'level'+str(level)+'.txt')
        self.map = loadlevel(chosenlevel)
        
    def new(self):
        # initialize all groups and do all the setup for a new game
        self.score=0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets=pg.sprite.Group()
        self.enemies=pg.sprite.Group()
        self.ammo=[]
        for n in range(0,4):
            self.ammo.append(pg.sprite.Group())
        
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 's':
                    Ammo(self, col, row,0)
                if tile == 'p':
                    Ammo(self, col, row,1)
                if tile == 'g':
                    Ammo(self, col, row,2)
                if tile == 'E':
                    Enemy(self, col, row,0)
                if tile == 'e':
                    Enemy(self, col, row,1)
        self.camera = camera(self.map.width, self.map.height)
    
    def run(self):
        # game update loop 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(fps) / 1000
            self.events()
            self.update()
            self.draw()
        while self.playing==False:
            
            self.events()
            self.showmenu()
    def quit(self):
        #used to quit the game
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop

        self.all_sprites.update()
        if len(self.enemies)>0:
            self.score+=self.dt


        
        self.camera.update(self.player)
   
    def draw(self):
        #draws all the sprites on the screen
        #as well as filling in the background colour
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image,self.camera.apply(sprite))
        self.text()
        pg.display.flip()
        
        
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing==True:
                        self.playing=False
                    elif self.playing==False:
                        self.playing=True
               
    def showmenu(self):
        global level
        global skin
        showmenu2(self)
        level=self.level
        skin=self.skin
        pg.display.flip()

        
    def text(self):
        #disapleys what gun is being shown
        if self.player.gunchosen==0:
            text = menunumberfont.render('Shotgun', True, RED, None)
        if self.player.gunchosen==1:
            text = menunumberfont.render('Pistol', True, RED, None)
        if self.player.gunchosen==2:
            text = menunumberfont.render('Gatling Gun', True, RED, None)
        if self.player.gunchosen==3:
            text = menunumberfont.render('Sniper', True, RED, None)
        textRect = text.get_rect()
        textRect.center = (width/2,40)
        self.screen.blit(text, textRect)
        # displays the ammo in the gun that is selected
        if self.player.gunchosen==0:
            text = menunumberfont.render(str(self.player.gunammo[0]), True, RED, None)
        if self.player.gunchosen==1:
            text = menunumberfont.render(str(self.player.gunammo[1]), True, RED, None)
        if self.player.gunchosen==2:
            text = menunumberfont.render(str(self.player.gunammo[2]), True, RED, None)
        if self.player.gunchosen==3:
            text = menunumberfont.render(str(self.player.gunammo[3]), True, RED, None)
        textRect = text.get_rect()
        textRect.midright = (1900,40)
        self.screen.blit(text, textRect)
        text = menunumberfont.render(str(self.player.health), True, RED, None)
        textRect = text.get_rect()
        textRect.midleft = (20,40)
        self.screen.blit(text, textRect)

        text = menunumberfont.render(str(math.trunc(self.score)), True, RED, None)
        textRect = text.get_rect()
        textRect.midright = (1900,1040)
        self.screen.blit(text, textRect)

        text = menunumberfont.render(str(level), True, RED, None)
        textRect = text.get_rect()
        textRect.midleft = (20,1040)
        self.screen.blit(text, textRect)

        if len(self.enemies)==0:
            text = menunumberfont.render('Yay!  Your score was: '+str(math.trunc(self.score)), True, RED, None)
            textRect = text.get_rect()
            textRect.center = (width/2,height/2)
            self.screen.blit(text, textRect)
# create the game object
global level
global skin
skin=1
level=1
while True:

    g=Game(level)
    
    g.playing=True
        
    g.new()
    g.run()

