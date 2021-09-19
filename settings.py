import pygame as pg
import os
pg.init() 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOR = DARKGREY
#player
playerspeed=300
playerjump=1000
wait=10
scale=1
gravity=2000
tilesize=64
height=1080*scale#1080
width=1920*scale#1920
gamename='my game'
fps=60
colour=[(255, 50, 50),(255, 0, 100),(255, 100, 0),(255, 0, 255)]
font = pg.font.Font('freesansbold.ttf', 32) 
menunumberfont = pg.font.Font('freesansbold.ttf', 64)
gamefolder=os.path.dirname(__file__)
imgfolder=os.path.join(gamefolder,'img')
player_image1_left=pg.image.load(os.path.join(imgfolder, 'player_left.png'))
player_image1_right=pg.image.load(os.path.join(imgfolder, 'player_right.png'))
wallimage=pg.image.load(os.path.join(imgfolder, 'tile2dirty.png'))
enemy_image_left=pg.image.load(os.path.join(imgfolder, 'enemy_left.png'))
enemy_image_right=pg.image.load(os.path.join(imgfolder, 'enemy_right.png'))
player_image2_left=pg.image.load(os.path.join(imgfolder, 'player_left2.png'))
player_image2_right=pg.image.load(os.path.join(imgfolder, 'player_right2.png'))
player_image1_menu=pg.image.load(os.path.join(imgfolder, 'player_left_big.png'))
player_image2_menu=pg.image.load(os.path.join(imgfolder, 'player_left2_big.png'))
ammoimage=[pg.image.load(os.path.join(imgfolder, 'extra_damage.png')),pg.image.load(os.path.join(imgfolder, 'extra_damage2.png')),pg.image.load(os.path.join(imgfolder, 'extra_damage3.png'))]
