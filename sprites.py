import pygame as pg
from settings import *
import random
import math
vec = pg.math.Vector2
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # initlise all variables adn sprite properties
        # look and group
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = player_image1_left
        self.image.set_colorkey(WHITE)
        #other
        self.rect = self.image.get_rect()
        self.vel=vec(0,0)
        self.pos=vec(x,y)*tilesize
        self.moveable=False
        #gun attributes
        self.gunwait=0
        self.gunammo=[0,20,0]#temp
        self.gunchosen=1
        self.changewait=0
        self.direction='left'
        self.skinwait=0
        self.health=100

    def move(self):
        #movemnt for the charater
        keys = pg.key.get_pressed()# gets keys currently pressed
        if self.moveable:
            
            if keys[pg.K_w]:# W key
                self.vel.y+=-playerjump

        self.vel.x=0    
        if keys[pg.K_a]:#A key
            self.vel.x = -playerspeed
            self.direction='left'
        if keys[pg.K_d]:#D key
            self.vel.x = playerspeed
            self.direction='right'

        self.vel.y+=gravity*self.game.dt# apply gravity
        self.moveable=False# cant move again

        
        


    def update(self):
        self.shoot() #call the shoot function
        self.move()   # call the movemnt function   
        self.pos += self.vel * self.game.dt# update pos
        self.rect.x = self.pos.x# update hitbox in x axis
        self.collision('x')# check for collisions in x axis
        self.rect.y = self.pos.y#update hitbox in y axis
        self.collision('y')#check for collision in y axis
        self.collision('a')#check for collisions with ammo boxes
        self.collision('b')
        if self.health<0:
            self.game.playing=False
        if self.direction=='left' and self.game.skin==0:
            self.image=player_image1_left
        elif self.direction=='right' and self.game.skin==0:
            self.image=player_image1_right
        elif self.direction=='left' and self.game.skin==1:
            self.image=player_image2_left
        elif self.direction=='right' and self.game.skin==1:
            self.image=player_image2_right
            

    def shoot(self):
        #changes gun selected
        keys = pg.key.get_pressed()
        #decriments it
        if self.gunammo != [0,0,0,0]:
            if keys[pg.K_q] and self.changewait>0.2:
                if self.gunchosen>0:
                    self.gunchosen+=-1
                else:
                    self.gunchosen=len(self.gunammo)-1
                #does untill it finds a unlocked gun
                while self.gunammo[self.gunchosen]==0:
                    if self.gunchosen>0:
                        self.gunchosen+=-1
                    else:
                        self.gunchosen=len(self.gunammo)-1
                self.changewait=0
            #incriments it 
            if keys[pg.K_e] and self.changewait>0.2:
                if self.gunchosen<len(self.gunammo)-1:
                    self.gunchosen+=1
                else:
                    self.gunchosen=0
                #does untill it finds a unlocked gun
                while self.gunammo[self.gunchosen]==0:
                    if self.gunchosen<len(self.gunammo)-1:
                        self.gunchosen+=1
                    else:
                        self.gunchosen=0
                self.changewait=0
        #shoots that gun
        mousedown= pg.mouse.get_pressed()
        print(mousedown)
        if mousedown[0]==True:#checks if the let mouse button is down
            mousepos=pg.mouse.get_pos()# gets the mouse positon on the screen 
            temp=[]
            for item in mousepos:
                temp.append(item)# changes tuple to array
            mousepos=temp
            mousepos[0]=mousepos[0]-self.game.camera.x# gets real positon
            mousepos[1]=mousepos[1]-self.game.camera.y
            #shoots the correct gun
            if self.gunchosen ==0 and self.gunammo[0]>0:
                self.shotgun(mousepos)               
            if self.gunchosen ==1 and self.gunammo[1]>0:
                self.pistol(mousepos)
            if self.gunchosen ==2 and self.gunammo[2]>0:
                self.gatling(mousepos)

                

                
        self.gunwait+=self.game.dt
        self.changewait+=self.game.dt

    def collision(self,side):
        if side == 'x':# if checking x
            self.hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if self.hits:# if hit a wall
                if self.vel.x > 0:# and going right
                    self.pos.x = self.hits[0].rect.left - self.rect.width
                if self.vel.x < 0:# adn going left
                    self.pos.x = self.hits[0].rect.right
                self.vel.x = 0# dont move
                self.rect.x = self.pos.x# reset position
        if side == 'y':# if checking y
            self.hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if self.hits:# if hit a wall
                if self.vel.y > 0:# and going down
                    self.pos.y = self.hits[0].rect.top - self.rect.height
                    self.moveable=True# can move as touching a surface
                if self.vel.y < 0:#if going up
                    self.pos.y = self.hits[0].rect.bottom
                    
                self.vel.y = 0#dont move up or down
                self.rect.y = self.pos.y# reset position

        if side =='a':
            for n in range (0,3):
                self.hits = pg.sprite.spritecollide(self, self.game.ammo[n], True)
                if self.hits:
                    self.gunammo[n]+=100
        if side =='b':
            self.hits = pg.sprite.spritecollide(self, self.game.bullets, True)
            if self.hits:
                self.health+=-30*len(self.hits)
            


                    
    def shotgun(self,mousepos):
        #shoots three bullets in a cone 
        if self.gunwait>0.3:
            bullet(self.game,vec(self.rect.center),mousepos,1200,0)
            bullet(self.game,vec(self.rect.center),mousepos,1200,0.125)
            bullet(self.game,vec(self.rect.center),mousepos,1200,-0.125)
            self.gunwait=0
            self.gunammo[0]+=-1

    def pistol(self,mousepos):
        #shoots one bullet
        if self.gunwait>0.3:
            bullet(self.game,vec(self.rect.center),mousepos,1000,0)
            self.gunwait=0
            self.gunammo[1]+=-1

    def gatling(self,mousepos):
        #shoots one bullet with a slight random angle to mimic inaccuracy
        if self.gunwait>0.05:
            bullet(self.game,vec(self.rect.center),mousepos,1000,random.randrange(-500,500,1)/10000)
            self.gunwait=0
            self.gunammo[2]+=-1
            
            


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # initlise wall looks and group
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = wallimage

        # initilise position and hitbox
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize

class bullet(pg.sprite.Sprite):
    def __init__(self,game,start,end,speed,angle):
        # initilistes bullets look
        self.groups=game.all_sprites,game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image=pg.Surface((10,10))
        self.image.fill(GREEN)
        # movement parameters
        self.rect=self.image.get_rect()
        # vector math
        self.pos=vec(start)
        self.vel=vec(end-start)
        self.unitvector=self.vel/math.sqrt( self.vel.x**2 + self.vel.y**2 )
        #finds the angle of the bullet being shot and adds the angle differance
        if self.unitvector[0]>0:
            newangle=math.atan(self.unitvector[1]/self.unitvector[0])+angle
        elif self.unitvector[0]<0:
            newangle=math.pi+math.atan(self.unitvector[1]/self.unitvector[0])+angle
        elif self.unitvector[0]==0 and self.unitvector[1]>0:
            newagle=(math.pi/2)+angle
        else:
            newangle=((3*math.pi)/2)+angle
        #refinds the unitvector
        self.unitvector[0]=math.cos(newangle)
        self.unitvector[1]=math.sin(newangle)
        self.vel=self.unitvector*speed       
        self.pos=self.pos+self.unitvector*((self.game.player.rect.width/2)+15)

    def update(self):
        #changes the position of the bullet each frame 
        self.pos+=self.vel*self.game.dt
        self.rect.centerx=self.pos.x
        self.rect.centery=self.pos.y
        #self.vel.y+=gravity*self.game.dt*-0.25
        #checks for collisions 
        self.collision()
    def collision(self):
        # kills itsself if collsided with a wall.
        hits=pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            pg.sprite.Sprite.kill(self)

class Ammo(pg.sprite.Sprite):
    def __init__(self, game, x, y,types):
        # initlise wall looks and group
        self.groups = game.all_sprites, game.ammo[types]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = ammoimage[types]

        # initilise position and hitbox
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
'''
Enemy
Enemy

'''

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y,temp):
        # initlise all variables adn sprite properties
        # look and group
        self.groups = game.all_sprites,game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = enemy_image_left
        self.image.set_colorkey(WHITE)
        #other
        self.rect = self.image.get_rect()
        self.vel=vec(0,0)
        self.pos=vec(x,y)*tilesize
        self.moveable=False
        #gun attributes
        self.gunwait=0
        #temp
        self.gunchosen=temp
        self.lrwait=random.randint(-1,1)
        self.firstwait=0
        self.health=100


    def move(self):
        pass
        #movemnt for the charater
       
        self.vel.x=0
        if self.lrwait>0.2:
            self.vel.x=playerspeed#makes it move right
            self.lrwait+=-self.game.dt#adds the time since last frame
            self.image=enemy_image_right#sets it image to the right on
            
        elif self.lrwait<-0.2:
            self.vel.x=-playerspeed#makes it go left
            self.lrwait+=self.game.dt
            self.image=enemy_image_left#sets it to left image
        else:
            self.lrwait=random.randint(-1,1)#waits a new random time
            
        self.vel.y+=gravity*self.game.dt# apply gravity
        self.moveable=False# cant move again

    def update(self):
        self.shoot() #call the shoot function
        self.move()   # call the movemnt function   
        self.pos += self.vel * self.game.dt# update pos
        self.rect.x = self.pos.x# update hitbox in x axis
        self.collision('x')# check for collisions in x axis
        self.rect.y = self.pos.y#update hitbox in y axis
        self.collision('y')#check for collision in y axis      
        self.collision('b')
        
        if self.health<0:
            pg.sprite.Sprite.kill(self)
    def shoot(self):
        #shoots that gun
        
        b=[0,0]
        b[0]=self.game.player.rect.centerx
        b[1]=self.game.player.rect.centery
        if cansee(self,b,self.game.walls,self.game)and self.firstwait>1:
            
            mousepos=b
            if (math.sqrt(((b[0]-self.rect.centerx)**2)+((b[1]-self.rect.centery)**2)))<900 :
                if self.gunchosen ==0 :
                    self.shotgun(mousepos)               
                if self.gunchosen ==1 :
                    self.pistol(mousepos)

        if  self.firstwait>1 and (not(cansee(self,b,self.game.walls,self.game))):
            self.firstwait=0
        self.gunwait+=self.game.dt       
        self.firstwait+=self.game.dt

        
    def collision(self,side):
        if side == 'x':# if checking x
            self.hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if self.hits:# if hit a wall
                if self.vel.x > 0:# and going right
                    self.pos.x = self.hits[0].rect.left - self.rect.width
                if self.vel.x < 0:# adn going left
                    self.pos.x = self.hits[0].rect.right
                self.vel.x = 0# dont move
                self.rect.x = self.pos.x# reset position
        if side == 'y':# if checking y
            self.hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if self.hits:# if hit a wall
                if self.vel.y > 0:# and going down
                    self.pos.y = self.hits[0].rect.top - self.rect.height
                    self.moveable=True# can move as touching a surface
                if self.vel.y < 0:#if going up
                    self.pos.y = self.hits[0].rect.bottom
                    
                self.vel.y = 0#dont move up or down
                self.rect.y = self.pos.y# reset position
        if side =='b':
            self.hits = pg.sprite.spritecollide(self, self.game.bullets, True)
            if self.hits:
                self.health+=-30*(len(self.hits))
                
                    
    def shotgun(self,mousepos):
        #shoots three bullets in a cone 
        if self.gunwait>0.3:
            bullet(self.game,vec(self.rect.center),mousepos,1200,0)
            bullet(self.game,vec(self.rect.center),mousepos,1200,0.125)
            bullet(self.game,vec(self.rect.center),mousepos,1200,-0.125)
            self.gunwait=0

    def pistol(self,mousepos):
        #shoots one bullet
        if self.gunwait>0.3:
            bullet(self.game,vec(self.rect.center),mousepos,1000,0)
            self.gunwait=0          




#7 hours
def cansee(shooter,target,obstacles,self):
    #gets the vctor between the player and the mosue
    vector=target-vec(shooter.rect.center)
    #
    found=False
    obstacles_list = [rectangle.rect for rectangle in obstacles]
    temp=[]
    # calculates which of the vlaues are the larger and smaller
    smallerx=min(shooter.rect.centerx,target[0])
    largerx=max(shooter.rect.centerx,target[0])
    smallery=min(shooter.rect.centery,target[1])
    largery=max(shooter.rect.centery,target[1])
    #CALCULATES THE GARDIENT OF THE VECTOR BETWEEN THE PLAYER AND THE MOUSE
    try:
        vecgrad=vector[1]/vector[0]
    except:
        if vector[1]>0:
            vecgrad=9999
        else:
            vecgrad=-9999
    # calculates the intersection of the y axis of that vectors line
    vecc=shooter.rect.centery-(vecgrad*shooter.rect.centerx)
    #itterates through all obstacles and sees if any could collide with the vector
    for n in range (0,len(obstacles_list)-1):
        if obstacles_list[n].x > smallerx-63 and obstacles_list[n].x <largerx:
            if obstacles_list[n].y >smallery-63 and obstacles_list[n].y < largery:
                if obstacles_list[n].x != shooter.rect.centerx and obstacles_list[n].y != shooter.rect.centery:
                    temp.append(obstacles_list[n])

                    # if they are and arent the player then add them to the temp list
    #:)   this code desides what quadrent it is in, thisis the top left and bottom right         
    if (vector[0]>32 and vector[1]<-32 )or( vector[0]<-32 and vector[1]>32):
        #sets the second line gradient 
        templinegrad=1

        #itterates through all the walls that are in the square the vecotr is the diagonal of
        #adn then calculates the interection of their diagonal and the vector

        for n in range(0,len(temp)) :
            #found is for optimisation i dont want it continue searching if its found to be true
            if found==False:
                templinec=(temp[n].centery-temp[n].centerx)
                intersectx=(vecc-templinec)/(templinegrad-vecgrad)
                
                #checks if the intersection is in range
                if intersectx>smallerx and intersectx<largerx:
                    intersecty=(intersectx*vecgrad)+vecc
                    #checks if it is then wall segment
                    if intersecty>temp[n].midtop[1] and intersecty<temp[n].midbottom[1]:
                        return(False)
                        found=True
        #if it doesnt find any then return true
        return(True)
    #bottom right and top left the rest is the same so look above
    elif (vector[0]<-32 and vector[1]<-32)or (vector[0]>32 and vector[1]>32):
        templinegrad=-1
        for n in range(0,len(temp)) :
            if found==False:
                templinec=(temp[n].centery+temp[n].centerx)
                intersectx=(vecc-templinec)/(templinegrad-vecgrad)
                
                
                if intersectx>smallerx and intersectx<largerx:
                    intersecty=(intersectx*vecgrad)+vecc

                    if intersecty>temp[n].midtop[1] and intersecty<temp[n].midbottom[1]:
                        return(False)
                        found=True
        return(True)
    #above     
    elif (target[0]-shooter.rect.centerx)<=32 and vector[1]<0 and (target[0]-shooter.rect.centerx)>=-32:
        templinegrad=0        
        for n in range(0,len(temp)) :
            if found==False:
                templinec=(temp[n].midbottom[1])
                intersectx=(vecc-templinec)/(-vecgrad)                
            
                if intersectx>smallerx and intersectx<largerx:
                    intersecty=(intersectx*vecgrad)+vecc
                    if intersecty>=temp[n].midtop[1] and intersecty<=temp[n].midbottom[1]:
                        return(False)
                        found=True
        return(True)
    #below
    elif (target[0]-shooter.rect.centerx)<=32 and vector[1]>0 and (target[0]-shooter.rect.centerx)>=-32:
        templinegrad=0

        for n in range(0,len(temp)):         
            templinec=(temp[n].midtop[1])

            intersectx=(vecc-templinec)/(-vecgrad)                

            if intersectx>smallerx and intersectx<largerx:
                intersecty=(intersectx*vecgrad)+vecc
                
                if intersecty>=temp[n].midtop[1] and intersecty<=temp[n].midbottom[1]:
                    return(False)
        return(True)
    #right
    elif (target[1]-shooter.rect.centery)<=32 and vector[0]>0 and (target[1]-shooter.rect.centery)>=-32:       
        for n in range(0,len(temp)):         
            x=(temp[n].x)
            intersecty= (x*vecgrad)+vecc                            
            if intersecty>=temp[n].midtop[1] and intersecty<=temp[n].midbottom[1]:
                return(False)
        return(True)
    #left
    elif (target[1]-shooter.rect.centery)<=32 and vector[0]<0 and (target[1]-shooter.rect.centery)>=-32:       
        for n in range(0,len(temp)):         
            x=(temp[n].midright[0])
            intersecty= (x*vecgrad)+vecc                            
            if intersecty>=temp[n].midtop[1] and intersecty<=temp[n].midbottom[1]:
                return(False)
        return(True)
       




