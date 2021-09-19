def showmenu(self):
        global level
        self.screen.fill(BGCOLOR)
        pg.draw.rect(self.screen,BLACK,(50,300,100,100))
        pg.draw.rect(self.screen,BLACK,(200,300,100,100))
        pg.draw.rect(self.screen,BLACK,(350,300,100,100))
        pg.draw.rect(self.screen,GREEN,(50,450,100,100))
        pg.draw.rect(self.screen,GREEN,(200,450,100,100))
        pg.draw.rect(self.screen,GREEN,(350,450,100,100))
        pg.draw.rect(self.screen,BLACK,(50,600,100,100))
        pg.draw.rect(self.screen,BLACK,(200,600,100,100))
        pg.draw.rect(self.screen,BLACK,(350,600,100,100))
        mousepos=pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]==1:
            if mousepos[0]>50 and mousepos[0]<150:
                if mousepos[1]>300 and mousepos[1]<400:
                    level=1
                    self.playing=True
                if mousepos[1]>450 and mousepos[1]<550:
                    level=4
                    self.playing=True
                if mousepos[1]>600 and mousepos[1]<700:
                    level=7
                    self.playing=True
            if mousepos[0]>200 and mousepos[0]<300:
                if mousepos[1]>300 and mousepos[1]<400:
                    level=2
                    self.playing=True
                if mousepos[1]>450 and mousepos[1]<550:
                    level=5
                    self.playing=True
                if mousepos[1]>600 and mousepos[1]<700:
                    level=8
                    self.playing=True
            if mousepos[0]>350 and mousepos[0]<450:
                if mousepos[1]>300 and mousepos[1]<400:
                    level=3
                    self.playing=True
                if mousepos[1]>450 and mousepos[1]<550:
                    level=6
                    self.playing=True
                if mousepos[1]>600 and mousepos[1]<700:
                    level=9
                    self.playing=True
