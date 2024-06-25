from backports import configparser
import kartet
import pygame

ferdiglevel1 = 0
ferdiglevel2 = 0
ferdiglevel3 = 0
ferdiglevel4 = 0

class Level(object):
    def load_file(self, filename="Level1.py"):
        """Loader filen"""
        self.map = []
        self.key = {}
        parser = configparser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

    def get_tile(self, x, y):
        """Henter ruten du spør om"""
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, name):
        """Sjekker om ruten har hva enn du vil sjekke"""
        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')
    
    def change_tile(self, x, y, tile_type):
        """Skifter en rute til en annen"""
        rowlist = list(self.map[y])
        rowlist[x] = tile_type
        self.map[y] = ''.join(rowlist)
        
    def count_tiles(self, name):
        """Teller antall ruter"""
        num_tiles = 0
        for x in range(self.width):
            for y in range(self.height):
                if (self.get_tile(x,y).get('name') == name):
                    num_tiles += 1
        return num_tiles

    def is_blocking(self, x, y):
        """Blokker dette stedet bevegelse?"""
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')
    
    def is_red(self, x, y):
        """Er det en rød knapp her?"""
        return self.get_bool(x, y, 'redpress')
    
    def cannot_enter(self, x, y):
        """Er det en portal her?"""
        return self.get_bool(x, y, 'cannotenter')
    
    def pressbutton(self, x, y):
        """klikker på knapp"""
        self.change_tile(x, y, 'z')
    
    def portalchange(self, x, y):
        """portal aktiveres"""
        self.change_tile(x,y,'p')
    
    def vingchange(self, x, y):
        """vinger blir plukket opp"""
        self.change_tile(x,y,'.')
    
    def is_ving(self, x, y):
        """Er dette vinger?"""
        return self.get_bool(x, y, 'plukk')
        
    def find_portalx(self, name='portalblocked'):
        """Finner x-koordinatene til portalen"""
        for x in range(self.width):
            for y in range(self.height):
                if (level.cannot_enter(x,y) == True):
                    x_verdi = x
        return x_verdi
    
    def find_portaly(self):
        """Finner y-koordinatene til portalen"""
        for x in range(self.width):
            for y in range(self.height):
                if (level.cannot_enter(x,y) == True):
                    y_verdi = y
        return y_verdi
    
    def portal(self, x, y):
        """Er det en aktiv portal her?"""
        return self.get_bool(x, y, 'canenter')
    
    def render(self):
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width*rute, self.height*rute))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 0, 0
                    tile_image = tiles[tile[0]][tile[1]]
                    image.blit(tile_image,(map_x*rute, map_y*rute))
        return image, overlays
    
if __name__ == "__main__":
    done = False
    
    #startposisjonen i level 1
    xpos = 16
    ypos = 9

    rute = 48
    x_lengde = 30
    y_lengde = 15

    fps = 15
    teller = 0

    engang = 1
    
    level = Level()
    level.load_file('Level1.py')

    klikk = 0
    pygame.init()
    pygame.mixer.init()
    
    #musikk
    pygame.mixer.music.load('musikk.wav')
    pygame.mixer.music.play(-1)
    
    clock = pygame.time.Clock()
    pygame.display.set_caption("katteklikkeren")
    retning = 1 #starter mot høyre
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                done = True
            elif event.type == pygame.locals.KEYDOWN:
                klikk = event.key
                
        screen = pygame.display.set_mode((rute*x_lengde, rute*y_lengde))

        MAP_CACHE = kartet.TileCache(rute, rute)

        if klikk == pygame.K_a and level.is_blocking(xpos-1,ypos) != True:
            xpos -= 1
            klikk = 0
            retning = 0 #0 er venstre
        if klikk == pygame.K_d and level.is_blocking(xpos+1,ypos) != True:
            xpos += 1
            klikk = 0
            retning = 1 #1 er høyre
        if klikk == pygame.K_s and level.is_blocking(xpos,ypos+1) != True:
            ypos += 1
            klikk = 0
        if klikk == pygame.K_w and level.is_blocking(xpos,ypos-1) != True:
            ypos -= 1
            klikk = 0
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_UP] and level.is_blocking(xpos,ypos-1) != True:
            ypos -= 1
        if keys[pygame.K_DOWN] and level.is_blocking(xpos,ypos+1) != True:
            ypos += 1
        if keys[pygame.K_LEFT] and level.is_blocking(xpos-1,ypos) != True:
            xpos -= 1
            retning = 0 #0 er venstre
        if keys[pygame.K_RIGHT] and level.is_blocking(xpos+1,ypos) != True:
            xpos += 1
            retning = 1 #1 er høyre
        
        if level.is_red(xpos,ypos) == True:
            level.pressbutton(xpos, ypos)
            
        if level.count_tiles('redbutton') == 0:
            if engang == 1:
                xportal = level.find_portalx()
                yportal = level.find_portaly()
                level.portalchange(xportal,yportal)
            if engang == 1:
                pygame.mixer.Sound.play(pygame.mixer.Sound("portal.wav"))
                engang = 0
            if level.portal(xpos,ypos) == True:
                done = True
                ferdiglevel1 = 1
        
        background, overlay_dict = level.render()
        overlays = pygame.sprite.RenderUpdates()
        for (x, y), image in overlay_dict.items():
            overlay = pygame.sprite.Sprite(overlays)
            overlay.image = image
            overlay.rect = image.get_rect().move(x * rute, y * rute - rute)
            
        screen.blit(background, (0, 0))
        overlays.draw(screen)

        if retning == 0:
            img = pygame.image.load('venstrekatt.png')
            img.convert()
            screen.blit(img,(rute*xpos,rute*ypos))
        else:
            img = pygame.image.load('høyrekatt.png')
            img.convert()
            screen.blit(img,(rute*xpos,rute*ypos))
        
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    
###############################################################################

if __name__ == "__main__" and ferdiglevel1 == 1:
    done = False
    
    #startposisjonen i level 2
    xpos = 21
    ypos = 14
    
    rute = 48
    x_lengde = 31
    y_lengde = 15
    engang = 1

    
    fps = 15
    teller = 0
    
    level = Level()
    level.load_file('Level2.py')

    klikk = 0
    pygame.init()
    pygame.mixer.init()
    
    #musikk
    pygame.mixer.music.load('pirat.wav')
    pygame.mixer.music.play(-1)
    
    clock = pygame.time.Clock()
    pygame.display.set_caption("katteklikkeren")
    retning = 1 #starter mot høyre
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                done = True
            elif event.type == pygame.locals.KEYDOWN:
                klikk = event.key
                
        screen = pygame.display.set_mode((rute*x_lengde, rute*y_lengde))

        MAP_CACHE = kartet.TileCache(rute, rute)

        if klikk == pygame.K_a and level.is_blocking(xpos-1,ypos) != True:
            xpos -= 1
            klikk = 0
            retning = 0 #0 er venstre
        if klikk == pygame.K_d and level.is_blocking(xpos+1,ypos) != True:
            xpos += 1
            klikk = 0
            retning = 1 #1 er høyre
        if klikk == pygame.K_s and level.is_blocking(xpos,ypos+1) != True:
            ypos += 1
            klikk = 0
        if klikk == pygame.K_w and level.is_blocking(xpos,ypos-1) != True:
            ypos -= 1
            klikk = 0
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_UP] and level.is_blocking(xpos,ypos-1) != True:
            ypos -= 1
        if keys[pygame.K_DOWN] and level.is_blocking(xpos,ypos+1) != True:
            ypos += 1
        if keys[pygame.K_LEFT] and level.is_blocking(xpos-1,ypos) != True:
            xpos -= 1
            retning = 0 #0 er venstre
        if keys[pygame.K_RIGHT] and level.is_blocking(xpos+1,ypos) != True:
            xpos += 1
            retning = 1 #1 er høyre
        
        if level.is_red(xpos-16,ypos) == True:
            level.pressbutton(xpos-16, ypos)
            
        if level.count_tiles('redbutton') == 0:
            if engang == 1:
                xportal = level.find_portalx()
                yportal = level.find_portaly()
                level.portalchange(xportal,yportal)
            if engang == 1:
                pygame.mixer.Sound.play(pygame.mixer.Sound("portal.wav"))
                engang = 0
            if level.portal(xpos,ypos) == True:
                done = True
                ferdiglevel2 = 1

        background, overlay_dict = level.render()
        overlays = pygame.sprite.RenderUpdates()
        for (x, y), image in overlay_dict.items():
            overlay = pygame.sprite.Sprite(overlays)
            overlay.image = image
            overlay.rect = image.get_rect().move(x * rute, y * rute - rute)
            
        screen.blit(background, (0, 0))
        overlays.draw(screen)
        
        if retning == 0:
            img = pygame.image.load('venstrepirat.png')
            img.convert()
            screen.blit(img,(rute*xpos,rute*ypos))
        elif retning == 1:
            img = pygame.image.load('høyrepirat.png')
            img.convert()
            screen.blit(img,(rute*xpos,rute*ypos))
        
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    
###############################################################################

engang = 1
xpos = 0
ypos = 14

rute = 48
x_lengde = 31
y_lengde = 15

knappx = []
knappy = []
vingx = []
vingy = []
portalx = []
portaly = []

pygame.init()
#musikk

pygame.mixer.init()
pygame.mixer.music.load('tetris.wav')
pygame.mixer.music.play(-1)

fps = 15

level = Level()
level.load_file('Level3bakke.py')
engangving = 1

donelvl3 = False

while __name__ == "__main__" and ferdiglevel2 == 1 and donelvl3 == False:
    
    if __name__ == "__main__" and ferdiglevel2 == 1:
        done = False
    
        level = Level()
        level.load_file('Level3bakke.py')
    
        klikk = 0
        
        clock = pygame.time.Clock()
        pygame.display.set_caption("katteklikkeren")
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    donelvl3 = True
                    done = True
                elif event.type == pygame.locals.KEYDOWN:
                    klikk = event.key
                    
            screen = pygame.display.set_mode((rute*x_lengde, rute*y_lengde))
    
            MAP_CACHE = kartet.TileCache(rute, rute)
    
            if klikk == pygame.K_a and level.is_blocking(xpos-1,ypos) != True:
                xpos -= 1
                klikk = 0
                retning = 0 #0 er venstre
            if klikk == pygame.K_d and level.is_blocking(xpos+1,ypos) != True:
                xpos += 1
                klikk = 0
                retning = 1 #1 er høyre
            if klikk == pygame.K_s and level.is_blocking(xpos,ypos+1) != True:
                ypos += 1
                klikk = 0
            if klikk == pygame.K_w and level.is_blocking(xpos,ypos-1) != True:
                ypos -= 1
                klikk = 0
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_UP] and level.is_blocking(xpos,ypos-1) != True:
                ypos -= 1
            if keys[pygame.K_DOWN] and level.is_blocking(xpos,ypos+1) != True:
                ypos += 1
            if keys[pygame.K_LEFT] and level.is_blocking(xpos-1,ypos) != True:
                xpos -= 1
                retning = 0 #0 er venstre
            if keys[pygame.K_RIGHT] and level.is_blocking(xpos+1,ypos) != True:
                xpos += 1
                retning = 1 #1 er høyre
            if klikk == pygame.K_e and engangving == 0:
                level = Level()
                level.load_file('Level3himmel.py')
                if level.is_blocking(xpos,ypos) != True:
                    done = True
                level = Level()
                level.load_file('Level3bakke.py')
            
            for i in range(len(knappx)):
                level.pressbutton(knappx[i], knappy[i])
            if engang == 0:
                level.portalchange(portalx[0], portaly[0])
            if engangving == 0:
                level.vingchange(vingx[0], vingy[0])
            
            
            if level.is_red(xpos,ypos) == True:
                level.pressbutton(xpos, ypos)
                knappx.append(xpos)
                knappy.append(ypos)
            
            if level.count_tiles('redbutton') == 0:
                if engang == 1:
                    if level.count_tiles('exitblocked') >= 1:
                        xportal = level.find_portalx()
                        yportal = level.find_portaly()
                        level.portalchange(xportal,yportal)
                        portalx.append(xportal)
                        portaly.append(yportal)
                if engang == 1:
                    pygame.mixer.Sound.play(pygame.mixer.Sound("portal.wav"))
                    engang = 0
                if level.portal(xpos,ypos) == True:
                    done = True
                    donelvl3 = True
                    ferdiglevel3 = 1
                    
            if level.is_ving(xpos,ypos) == True:
                level.vingchange(xpos, ypos)
                if engangving == 1:
                    pygame.mixer.Sound.play(pygame.mixer.Sound("knapp.wav"))
                    engangving = 0
                    vingx.append(xpos)
                    vingy.append(ypos)
    
            background, overlay_dict = level.render()
            overlays = pygame.sprite.RenderUpdates()
            for (x, y), image in overlay_dict.items():
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * rute, y * rute - rute)
                
            screen.blit(background, (0, 0))
            overlays.draw(screen)
            
            if retning == 0:
                if engangving == 0:
                    img = pygame.image.load('venstrefly.png')
                    img.convert()
                    screen.blit(img,(rute*xpos,rute*ypos))
                else:
                    img = pygame.image.load('venstrekatt.png')
                    img.convert()
                    screen.blit(img,(rute*xpos,rute*ypos))
            elif retning == 1:
                if engangving == 0:
                    img = pygame.image.load('høyrefly.png')
                    img.convert()
                    screen.blit(img,(rute*xpos,rute*ypos))
                else:
                    img = pygame.image.load('høyrekatt.png')
                    img.convert()
                    screen.blit(img,(rute*xpos,rute*ypos))
            
            pygame.display.flip()
            clock.tick(fps)

    ###########################################################################

    if __name__ == "__main__" and ferdiglevel2 == 1 and donelvl3 == False:
        done = False
        rute = 48
        x_lengde = 31
        y_lengde = 15    
        
        fps = 15
        
        level = Level()
        level.load_file('Level3himmel.py')
    
        klikk = 0
        
        clock = pygame.time.Clock()
        pygame.display.set_caption("katteklikkeren")
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    donelvl3 = True
                    done = True
                elif event.type == pygame.locals.KEYDOWN:
                    klikk = event.key
                    
            screen = pygame.display.set_mode((rute*x_lengde, rute*y_lengde))
    
            MAP_CACHE = kartet.TileCache(rute, rute)
    
            if klikk == pygame.K_a and level.is_blocking(xpos-1,ypos) != True:
                xpos -= 1
                klikk = 0
                retning = 0 #0 er venstre
            if klikk == pygame.K_d and level.is_blocking(xpos+1,ypos) != True:
                xpos += 1
                klikk = 0
                retning = 1 #1 er høyre
            if klikk == pygame.K_s and level.is_blocking(xpos,ypos+1) != True:
                ypos += 1
                klikk = 0
            if klikk == pygame.K_w and level.is_blocking(xpos,ypos-1) != True:
                ypos -= 1
                klikk = 0
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_UP] and level.is_blocking(xpos,ypos-1) != True:
                ypos -= 1
            if keys[pygame.K_DOWN] and level.is_blocking(xpos,ypos+1) != True:
                ypos += 1
            if keys[pygame.K_LEFT] and level.is_blocking(xpos-1,ypos) != True:
                xpos -= 1
                retning = 0 #0 er venstre
            if keys[pygame.K_RIGHT] and level.is_blocking(xpos+1,ypos) != True:
                xpos += 1
                retning = 1 #1 er høyre
            if klikk == pygame.K_e and engangving == 0:
                level = Level()
                level.load_file('Level3bakke.py')
                if level.is_blocking(xpos,ypos) != True:
                    done = True
                level = Level()
                level.load_file('Level3himmel.py')
                
            background, overlay_dict = level.render()
            overlays = pygame.sprite.RenderUpdates()
            for (x, y), image in overlay_dict.items():
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * rute, y * rute - rute)
                
            screen.blit(background, (0, 0))
            overlays.draw(screen)
            
            if retning == 0:
                img = pygame.image.load('venstrefly.png')
                img.convert()
                screen.blit(img,(rute*xpos,rute*ypos))
            elif retning == 1:
                img = pygame.image.load('høyrefly.png')
                img.convert()
                screen.blit(img,(rute*xpos,rute*ypos))
            
            pygame.display.flip()
            clock.tick(fps)
    
pygame.quit()

###############################################################################

engang = 1
xpos = 0
ypos = 0

rute = 48
x_lengde = 31
y_lengde = 15

knappx = []
knappy = []
vingx = []
vingy = []
portalx = []
portaly = []

pygame.init()
#musikk

pygame.mixer.init()
pygame.mixer.music.load('sandstorm.wav')
pygame.mixer.music.play(-1)

fps = 15
engangving = 0

level = Level()
level.load_file('Level4bakke.py')

donelvl4 = False

while __name__ == "__main__" and ferdiglevel3 == 1 and donelvl4 == False:
    
    if __name__ == "__main__" and ferdiglevel3 == 1:
        done = False
    
        level = Level()
        level.load_file('Level4bakke.py')
    
        klikk = 0
        
        clock = pygame.time.Clock()
        pygame.display.set_caption("katteklikkeren")
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    donelvl4 = True
                    done = True
                elif event.type == pygame.locals.KEYDOWN:
                    klikk = event.key
                    
            screen = pygame.display.set_mode((rute*x_lengde, rute*y_lengde))
    
            MAP_CACHE = kartet.TileCache(rute, rute)
    
            if klikk == pygame.K_a and level.is_blocking(xpos-1,ypos) != True:
                xpos -= 1
                klikk = 0
                retning = 0 #0 er venstre
            if klikk == pygame.K_d and level.is_blocking(xpos+1,ypos) != True:
                xpos += 1
                klikk = 0
                retning = 1 #1 er høyre
            if klikk == pygame.K_s and level.is_blocking(xpos,ypos+1) != True:
                ypos += 1
                klikk = 0
            if klikk == pygame.K_w and level.is_blocking(xpos,ypos-1) != True:
                ypos -= 1
                klikk = 0
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_UP] and level.is_blocking(xpos,ypos-1) != True:
                ypos -= 1
            if keys[pygame.K_DOWN] and level.is_blocking(xpos,ypos+1) != True:
                ypos += 1
            if keys[pygame.K_LEFT] and level.is_blocking(xpos-1,ypos) != True:
                xpos -= 1
                retning = 0 #0 er venstre
            if keys[pygame.K_RIGHT] and level.is_blocking(xpos+1,ypos) != True:
                xpos += 1
                retning = 1 #1 er høyre
            if klikk == pygame.K_e and engangving == 0:
                level = Level()
                level.load_file('Level4himmel.py')
                if level.is_blocking(xpos,ypos) != True:
                    done = True
                level = Level()
                level.load_file('Level4bakke.py')
            
            for i in range(len(knappx)):
                level.pressbutton(knappx[i], knappy[i])
            if engang == 0:
                level.portalchange(portalx[0], portaly[0])
            
            if level.is_red(xpos,ypos) == True:
                level.pressbutton(xpos, ypos)
                knappx.append(xpos)
                knappy.append(ypos)
            
            if level.count_tiles('redbutton') == 0:
                if engang == 1:
                    if level.count_tiles('exitblocked') >= 1:
                        xportal = level.find_portalx()
                        yportal = level.find_portaly()
                        level.portalchange(xportal,yportal)
                        portalx.append(xportal)
                        portaly.append(yportal)
                if engang == 1:
                    pygame.mixer.Sound.play(pygame.mixer.Sound("portal.wav"))
                    engang = 0
                if level.portal(xpos,ypos) == True:
                    done = True
                    donelvl4 = True
                    ferdiglevel4 = 1
    
            background, overlay_dict = level.render()
            overlays = pygame.sprite.RenderUpdates()
            for (x, y), image in overlay_dict.items():
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * rute, y * rute - rute)
                
            screen.blit(background, (0, 0))
            overlays.draw(screen)
            
            if retning == 0:
                img = pygame.image.load('venstrefly.png')
                img.convert()
                screen.blit(img,(rute*xpos,rute*ypos))
            elif retning == 1:
                img = pygame.image.load('høyrefly.png')
                img.convert()
                screen.blit(img,(rute*xpos,rute*ypos))
            
            pygame.display.flip()
            clock.tick(fps)

    ###########################################################################
    
    if __name__ == "__main__" and ferdiglevel3 == 1 and donelvl4 == False:
        done = False
        rute = 48
        x_lengde = 31
        y_lengde = 15    
        
        fps = 15
        
        level = Level()
        level.load_file('Level4himmel.py')
    
        klikk = 0
        
        clock = pygame.time.Clock()
        pygame.display.set_caption("katteklikkeren")
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    donelvl4 = True
                    done = True
                elif event.type == pygame.locals.KEYDOWN:
                    klikk = event.key
                    
            screen = pygame.display.set_mode((rute*x_lengde, rute*y_lengde))
    
            MAP_CACHE = kartet.TileCache(rute, rute)
    
            if klikk == pygame.K_a and level.is_blocking(xpos-1,ypos) != True:
                xpos -= 1
                klikk = 0
                retning = 0 #0 er venstre
            if klikk == pygame.K_d and level.is_blocking(xpos+1,ypos) != True:
                xpos += 1
                klikk = 0
                retning = 1 #1 er høyre
            if klikk == pygame.K_s and level.is_blocking(xpos,ypos+1) != True:
                ypos += 1
                klikk = 0
            if klikk == pygame.K_w and level.is_blocking(xpos,ypos-1) != True:
                ypos -= 1
                klikk = 0
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_UP] and level.is_blocking(xpos,ypos-1) != True:
                ypos -= 1
            if keys[pygame.K_DOWN] and level.is_blocking(xpos,ypos+1) != True:
                ypos += 1
            if keys[pygame.K_LEFT] and level.is_blocking(xpos-1,ypos) != True:
                xpos -= 1
                retning = 0 #0 er venstre
            if keys[pygame.K_RIGHT] and level.is_blocking(xpos+1,ypos) != True:
                xpos += 1
                retning = 1 #1 er høyre
            if klikk == pygame.K_e and engangving == 0:
                level = Level()
                level.load_file('Level4bakke.py')
                if level.is_blocking(xpos,ypos) != True:
                    done = True
                level = Level()
                level.load_file('Level4himmel.py')
                
            background, overlay_dict = level.render()
            overlays = pygame.sprite.RenderUpdates()
            for (x, y), image in overlay_dict.items():
                overlay = pygame.sprite.Sprite(overlays)
                overlay.image = image
                overlay.rect = image.get_rect().move(x * rute, y * rute - rute)
                
            screen.blit(background, (0, 0))
            overlays.draw(screen)
            
            if retning == 0:
                img = pygame.image.load('venstrefly.png')
                img.convert()
                screen.blit(img,(rute*xpos,rute*ypos))
            elif retning == 1:
                img = pygame.image.load('høyrefly.png')
                img.convert()
                screen.blit(img,(rute*xpos,rute*ypos))
            
            pygame.display.flip()
            clock.tick(fps)
    
pygame.quit()

if __name__ == "__main__" and ferdiglevel4 == 1:
    fps = 15
    done = False
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('bday.wav')
    pygame.mixer.music.play(-1)
    
    bilde = pygame.image.load("vinn.png")
    x = bilde.get_width()
    y = bilde.get_height()
    
    screen = pygame.display.set_mode((x, y))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Du vant!")
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                done = True

        screen.blit(bilde,(0,0))
        
        font = pygame.font.SysFont('Calibri', 25, True, False)
        if ferdiglevel1 == 1 and ferdiglevel2 == 1 and ferdiglevel3 == 1 and ferdiglevel4 == 1:
            tekst = font.render("Du vant!", True, (0,0,255))
        
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
