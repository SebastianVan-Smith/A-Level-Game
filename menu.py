from settings import *
def showmenu2(self):
    global level
    #puts the background colour
    self.screen.fill(BGCOLOR)
    #splits the screen into two shades
    pg.draw.rect(self.screen,(20,20,20),(0,0,960,1080))
    #480 405
    #240 165
    #720 645
    #creates level numbers and boxes
    pg.draw.rect(self.screen,GREEN,(165,325,150,150))
    textbox(self,1,240,400,menunumberfont)
    pg.draw.rect(self.screen,GREEN,(405,325,150,150))
    textbox(self,2,480,400,menunumberfont)
    pg.draw.rect(self.screen,GREEN,(645,325,150,150))
    textbox(self,3,720,400,menunumberfont)
    pg.draw.rect(self.screen,GREEN,(165,575,150,150))
    textbox(self,4,240,650,menunumberfont)
    pg.draw.rect(self.screen,GREEN,(405,575,150,150))
    textbox(self,5,480,650,menunumberfont)
    pg.draw.rect(self.screen,GREEN,(645,575,150,150))
    textbox(self,6,720,650,menunumberfont)
    pg.draw.rect(self.screen,GREEN,(165,825,150,150))
    textbox(self,7,240,900,menunumberfont)
    pg.draw.rect(self.screen,GREEN,(405,825,150,150))
    textbox(self,8,480,900,menunumberfont)
    pg.draw.rect(self.screen,GREEN,(645,825,150,150))
    textbox(self,9,720,900,menunumberfont)
    
    #are they pressing any of those buttons and if so what one
    mousepos=pg.mouse.get_pos()
    if pg.mouse.get_pressed()[0]==1:
        if mousepos[0]>165 and mousepos[0]<315:
            if mousepos[1]>325 and mousepos[1]<475:
                self.level=1
                self.playing=True
            elif mousepos[1]>575 and mousepos[1]<725:
                self.level=4
                self.playing=True
            elif mousepos[1]>825 and mousepos[1]<975:
                self.level=7
                self.playing=True
        elif mousepos[0]>405 and mousepos[0]<555:
            if mousepos[1]>325 and mousepos[1]<475:
                self.level=2
                self.playing=True
            elif mousepos[1]>575 and mousepos[1]<725:
                self.level=5
                self.playing=True
            elif mousepos[1]>825 and mousepos[1]<975:
                self.level=8
                self.playing=True
        elif mousepos[0]>645 and mousepos[0]<795:
            if mousepos[1]>325 and mousepos[1]<475:
                self.level=3
                self.playing=True
            elif mousepos[1]>575 and mousepos[1]<725:
                self.level=6
                self.playing=True
            elif mousepos[1]>825 and mousepos[1]<975:
                self.level=9
                self.playing=True
    # does the hedding for each side
    textbox(self,'Level Select',480,150,menunumberfont)
    textbox(self,'Skin Select',1440,150,menunumberfont)
    #changesa dn shoes the skin
    if self.skin==0:
        image=player_image1_menu
    else:
        image=player_image2_menu
        

    rect=image.get_rect()
    self.screen.blit(image,(1440-(rect.width/2),300))
    # makes then  next skin box and sees if its been hit
    pg.draw.rect(self.screen,BLACK,(1140,825,600,150))
    textbox(self,'Next Skin',1440,900,menunumberfont)
    if pg.mouse.get_pressed()[0]==1 and self.player.skinwait>0.8:
        if mousepos[0]>1140 and mousepos[0]<1740:
            if mousepos[1]>825 and mousepos[1]<975:
                nextskin(self)
                self.player.skinwait=0
    self.player.skinwait+=self.dt

    
def textbox(self,text,x,y,font):
    # draws some text
    text = font.render(str(text), True, RED, None)
    textRect = text.get_rect()
    textRect.center = (x,y)
    self.screen.blit(text, textRect)

def nextskin(self):
    #goes to the next skin
    if self.skin<1:
        self.skin+=1
    else:
        self.skin=0
    print(self.skin)



