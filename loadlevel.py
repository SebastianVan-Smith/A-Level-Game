# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 18:40:45 2019

@author: sebastian
"""
import pygame as pg
from settings import *

class loadlevel:
    def __init__(self,filename):
        self.data=[]
        with open(filename,'rt') as file:
            for line in file:
                
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * tilesize
        self.height = self.tileheight * tilesize


class camera:
    def __init__(self,width,height):
        self.camera=pg.Rect(0,0,width,height)
        self.width=width
        self.height=height
        self.x=0
        self.y=0
    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def update(self,target):
        self.x=-target.rect.centerx +int(width/2)
        self.y=-target.rect.centery +int(height/2)
        self.x=min(0,self.x)
        self.y=min(0,self.y)
        self.x=max(width-self.width,self.x)
        self.y=max(height-self.height,self.y)

        self.camera = pg.Rect(self.x, self.y, self.width, self.height)
