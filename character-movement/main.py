"""Smooth Movement in pygame"""

#Imports
import pygame, sys
import global_var as Glob

#pygame initialization
pygame.init()
clock = pygame.time.Clock()

def get_font(size):
    return pygame.font.Font("freesansbold.ttf", size)

#Debug Class
class Debug():
    def log(self, flag):

        if flag:
            
            pygame.draw.rect(Glob.screen, (255,255,255), player.rect, int(1*Glob.MULT))

            sprint = Glob.Player_speed > Glob.Player_default_speed
            keys_pressed = pygame.key.get_pressed()

            key = ""

            if player.getUpPress():
                key = "up"
            elif player.getDownPress():
                key = "down"
            elif player.getLeftPress():
                key = "left"
            elif player.getRightPress():
                key = "right"
            
            FPS_TEXT = get_font(8*int(Glob.MULT)).render("FPS: "+str(int(clock.get_fps())), True, "white")
            FPS_RECT = FPS_TEXT.get_rect(center=(Glob.screen_width-40*Glob.MULT, 20*Glob.MULT))

            DROP_TEXT = get_font(5*int(Glob.MULT)).render("DROP "+str(100-int(clock.get_fps()*100/Glob.FPS))+"%", True, "red")
            DROP_RECT = DROP_TEXT.get_rect(center=(Glob.screen_width-95*Glob.MULT, 20*Glob.MULT))

            KEY_TEXT = get_font(10*int(Glob.MULT)).render(key, True, "blue")
            KEY_RECT = KEY_TEXT.get_rect(center=(Glob.screen_width-140*Glob.MULT, 20*Glob.MULT))


            Glob.screen.blit(KEY_TEXT, KEY_RECT)

            if int(clock.get_fps()) <= (Glob.FPS-(Glob.FPS/20)):
                #print("Gli fps sono scesi: "+str(clock.get_fps()))
                Glob.screen.blit(DROP_TEXT, DROP_RECT)
                

            Glob.screen.blit(FPS_TEXT, FPS_RECT)

            if keys_pressed[pygame.K_o]:
                Glob.Moff -= 1

            if keys_pressed[pygame.K_p]:
                Glob.Moff += 1

            RUN_TEXT = get_font(8*int(Glob.MULT)).render("V-A: "+str(round(Glob.Player_speed, 1)), True, "white")
            RUN_RECT = RUN_TEXT.get_rect(center=(40*Glob.MULT, 20*Glob.MULT))

            Glob.screen.blit(RUN_TEXT, RUN_RECT)

            POS_TEXT = get_font(8*int(Glob.MULT)).render("x/y: "+str(int(player.getPositionX()-cam.getPositionX()))+" | "+str(int(player.getPositionY()-cam.getPositionY())), True, "white")
            POS_RECT = POS_TEXT.get_rect(center=(200*Glob.MULT, 20*Glob.MULT))

            Glob.screen.blit(POS_TEXT, POS_RECT)

#Cam Class
class Cam():
    def __init__(self):

        #indico il giocatore impostato
        self.setPositionX(0) 
        self.setPositionY(0)

        self.image = pygame.image.load("assets/BackgroundCam.png").convert()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.image = pygame.transform.scale(self.image,((self.width*Glob.MULT*2), (self.height*Glob.MULT*2)))


    def setPositionX(self, x):
        self.x = x

    def setPositionY(self, y):
        self.y = y

    def getPositionX(self):
        return self.x

    def getPositionY(self):
        return self.y

        
    def update(self, visibility):
        Glob.screen.blit(self.image, (self.x, self.y))

        offset = (4 * Glob.Moff * Glob.MULT, 2.25 * Glob.Moff * Glob.MULT)

        a =  player.getPositionX() >= Glob.screen_width - offset[0] - player.width
        b =  player.getPositionX() <= offset[0]

        c =  player.getPositionY() >= Glob.screen_height - offset[1] - player.height
        d =  player.getPositionY() <= offset[1]

        a1 = player.getRightPress()
        b1 = player.getLeftPress()

        c1 = player.getDownPress()
        d1 = player.getUpPress()

        ln = player.Last_keyPressed=="Null"

        if a and ln and not (player.getLeftPress() or player.getRightPress()):
            player.x -= Glob.Player_default_speed

        if b and ln and not (player.getLeftPress() or player.getRightPress()):
            player.x += Glob.Player_default_speed

        if c and ln and not (player.getUpPress() or player.getDownPress()):
            player.y -= Glob.Player_default_speed

        if d and ln and not (player.getUpPress() or player.getDownPress()):
            player.y += Glob.Player_default_speed

        if a and a1 or ln and a:
            player.setPositionX(player.getPositionX()-player.getVelocitaX())
            self.x -= player.getVelocitaX()
            print("Cam-destra")
    

        if b and b1 or ln and b:
            player.setPositionX(player.getPositionX()-player.getVelocitaX())
            self.x += -player.getVelocitaX()
            print("Cam-sinistra")


        if c and c1 or ln and c:
            player.setPositionY(player.getPositionY()-player.getVelocitaY())
            self.y -= player.getVelocitaY()
            print("Cam-basso")
    

        if d and d1 or ln and d:
            player.setPositionY(player.getPositionY()-player.getVelocitaY())
            self.y += -player.getVelocitaY()
            print("Cam-alto")
        
        if visibility:

            Player_hitbox = [ 0 * Glob.MULT /Glob.Player_proportion, 0 * Glob.MULT /Glob.Player_proportion, player.width * Glob.MULT /Glob.Player_proportion, player.height * Glob.MULT /Glob.Player_proportion]
            #Player_hitbox = player.rect

            Offset_rect = pygame.Rect(offset[0] + Player_hitbox[0], offset[1] + Player_hitbox[1], Glob.screen_width - offset[0]*2 - Player_hitbox[0]*2, Glob.screen_height - offset[1]*2 - Player_hitbox[1]*2)
            pygame.draw.rect(Glob.screen, (255,255,255), Offset_rect, int(Glob.MULT))
        
        #print("Posizione x: "+str(player.getPositionX())+" | Posizione y: "+str(player.getPositionY())+" | VelocitàX: "+str(player.getVelocitaX()))

#Player Class
class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

        #indicazione grandezza (statica)
        self.width = 16*Glob.MULT
        self.height = 16*Glob.MULT

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = "Red"

        #indicazione velocità (dinamica)
        self.setVelocitaX(0)
        self.setVelocitaY(0)

        #pulsanti cliccati si/no
        self.setLeftPress(False)
        self.setRightPress(False)
        self.setUpPress(False)
        self.setDownPress(False)
        self.speed = Glob.Player_speed

        self.Last_keyPressed = "Null"

        #hitbox del player
        self.setHitbox()
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    def update(self):
        #indicazione velocità (dinamica)
        self.setVelocitaX(0)
        self.setVelocitaY(0)
        if self.getLeftPress() and not self.getRightPress():
            self.setVelocitaX(-Glob.Player_speed)
        if self.getRightPress() and not self.getLeftPress():
            self.setVelocitaX(Glob.Player_speed)
        if self.getUpPress() and not self.getDownPress():
            self.setVelocitaY(-Glob.Player_speed)
        if self.getDownPress() and not self.getUpPress():
            self.setVelocitaY(Glob.Player_speed)
        
        self.setPositionX(self.getPositionX()+self.getVelocitaX())
        self.setPositionY(self.getPositionY()+self.getVelocitaY())

        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        self.setHitbox()
        self.rect = pygame.Rect(self.hitbox) # indico la hitbox (mesh) del Player

    def HasCollision(self, object):
    
        def Confronta(value):   # Creo una funziona dato che la utilizzo piu' volte e se gli passo "x" fa una cosa mentre se gli passo "y" ne fa un'altra
            
            #self.finish()    # ogni volta che collido stoppo l'animazione del player

            if value=="x":  # confronto il valore passato

                if self.x >= object.x:  # confronto se la posizione del player delle x è maggiore o uguale della posizione delle x dell'oggetto di cui ho collisione
                    self.x += Glob.Player_speed    # ogni volta che collido vado a settare la posizione del player indietro grazie alla sua velocità
                    self.setLeftPress(False)    # ogni volta che collido dal lato sinistro non posso riandare a ricliccare il pulsante destro
                    return True # ritorno un valore perchè dopo lo vado ad utilizzare
                elif self.x <= object.x:
                    self.x -= Glob.Player_speed    # ogni volta che collido vado a settare la posizione del player indietro grazie alla sua velocità
                    self.setRightPress(False)    # ogni volta che collido dal lato destro non posso riandare a ricliccare il pulsante sinistro
                    return False # ritorno un valore perchè dopo lo vado ad utilizzare

            if value=="y":  # confronto il valore passato

                if self.y >= object.y:  # confronto se la posizione del player delle y è maggiore o uguale della posizione delle y dell'oggetto di cui ho collisione
                    self.y += Glob.Player_speed    # ogni volta che collido vado a settare la posizione del player indietro grazie alla sua velocità
                    self.setUpPress(False)    # ogni volta che collido dal lato basso non posso riandare a ricliccare il pulsante alto
                    return True # ritorno un valore perchè dopo lo vado ad utilizzare
                elif self.y <= object.y:
                    self.y -= Glob.Player_speed    # ogni volta che collido vado a settare la posizione del player indietro grazie alla sua velocità
                    self.setDownPress(False)    # ogni volta che collido dal lato alto non posso riandare a ricliccare il pulsante basso
                    return False # ritorno un valore perchè dopo lo vado ad utilizzare
            

        if self.rect.colliderect(object):   # Metodo di pygame che confronta se due rettangoli collidono

            # Setto diverse variabili per non ripeterli nei confronti
            w = (self.Last_keyPressed == "Up")
            a = (self.Last_keyPressed == "Left")
            
            s = (self.Last_keyPressed == "Down")
            d = (self.Last_keyPressed == "Right")

            
            a1 = (self.getRightPress() and w or self.getLeftPress() and w)
            b1 =  (self.getLeftPress() and s or self.getRightPress() and s)

            c1 =  (self.getUpPress() and a or self.getDownPress() and a)
            d1 =  (self.getUpPress() and d or self.getDownPress() and d)

            # print("\n\nSinistro o Destro and Sù: ",str(a1))
            # print("Sinistro o Destro and Giù: ",str(b1))
            # print("Alto o Basso and Sinistra: ",str(c1))
            # print("Alto o Basso and Destra: ",str(d1))

            # print("\nup: "+str(self.getUpPress())+" |down: "+str(self.getDownPress())+" |left: "+str(self.getLeftPress())+" |right: "+str(self.getRightPress())+"\n")
            
            if self.Last_keyPressed != "Null":  # Confronto se il giocatore è fermo o si sta muovendo

                if (a1 or b1) and (not c1 and not d1):  # se è stato premuto il pulsante destro/sinistro e NON quello alto o basso mentre si ha una collisione allora:

                    Confronta("x")  # richiamo la funzione

                    if Confronta("x"):  # se la funzione mi ritorna True allora:
                        self.setLeftPress(False)
                    else:  # se la funzione mi ritorna False allora:
                        self.setRightPress(False)

                    self.Last_keyPressed = "Null"   # Variabile usata per non dare errori dato che l'ultimo pulsante cliccato sono l'insieme di due in contemporanea

                    
                if (c1 or d1) and (not a1 and not b1):  # se è stato premuto il pulsante alto/basso e NON con quello sinistro o destro mentre si ha una collisione allora:

                    Confronta("y")  # richiamo la funzione

                    if Confronta("y"):  # se la funzione mi ritorna True allora:
                        self.setUpPress(False)
                    else:  # se la funzione mi ritorna False allora:
                        self.setDownPress(False)

                    self.Last_keyPressed = "Null"   # Variabile usata per non dare errori dato che l'ultimo pulsante cliccato sono l'insieme di due in contemporanea
                    

                if (self.getRightPress() or self.getLeftPress() or a or d) and (not w and not s):   # Qua altri confronti con unicamente con un pulante a volta cliccato sinistra/destra
                    Confronta("x")
                
                if (self.getUpPress() or self.getDownPress() or w or s) and (not d and not a):   # Qua altri confronti con unicamente con un pulante a volta cliccato alto/basso
                    Confronta("y")
            else:
                Confronta("y")
                Confronta("x")
                #self.setAllkeys(None)

# ---------- self.set() ----------

    def setPositionX(self, x):
        self.x = x

    def setPositionY(self, y):
        self.y = y

    def setVelocitaX(self, x):
        self.__velX = x

    def setVelocitaY(self, y):
        self.__velY = y

    def setRightPress(self, r):
        self.__right_pressed = r

    def setLeftPress(self, l):
        self.__left_pressed = l

    def setUpPress(self, u):
        self.__up_pressed = u

    def setDownPress(self, d):
        self.__down_pressed = d

    def setAllkeys(self, v):
        
        if (v != True and v != False):
            return

        self.setUpPress(v)
        self.setDownPress(v)
        self.setLeftPress(v)
        self.setRightPress(v)

    def setHitbox(self):
        #self.hitbox = (self.x + 15 * Glob.MULT /Glob.Player_proportion, self.y + 17 * Glob.MULT /Glob.Player_proportion, 24* Glob.MULT /Glob.Player_proportion, 43 * Glob.MULT /Glob.Player_proportion)
        self.hitbox = (self.rect)

# ---------- self.get() ----------

    def getPositionX(self):
        return self.x

    def getPositionY(self):
        return self.y

    def getVelocitaX(self):
        return self.__velX

    def getVelocitaY(self):
        return self.__velY

    def getRightPress(self):
        return self.__right_pressed

    def getLeftPress(self):
        return self.__left_pressed

    def getUpPress(self):
        return self.__up_pressed

    def getDownPress(self):
        return self.__down_pressed

#Player Initialization
def inizializza():
    global player, cam, console
    player = Player(Glob.screen_width/2, Glob.screen_height/2)
    cam = Cam()
    console = Debug()


def render(lista, color, var, hitbox):
        x = 0
        y = 0
        tiles_risoluzione = 32 * Glob.MULT
        collisione = pygame.Rect(x + cam.getPositionX(), y + cam.getPositionY(), tiles_risoluzione, tiles_risoluzione)

        for valore_y in range(len(lista)):

            x = 0
            for valore_x in range(len(lista[valore_y])):
                condition = lista[valore_y][valore_x] == var

                if condition:
                    collisione = pygame.Rect(x + cam.getPositionX(), y + cam.getPositionY(), tiles_risoluzione, tiles_risoluzione)
                    pygame.draw.rect(Glob.screen, color, collisione)
                    #print("\n- Render | Oggetto a schermo!", object)
                    
                    if hitbox != None:
                        #print("- Render | Collisione Oggetto Impostata!", collisione,"\n")
                        player.HasCollision(collisione)

                if Glob.Debug:
                    pygame.draw.rect(Glob.screen, (255,0,0), collisione, 1)

                x += tiles_risoluzione

            y += tiles_risoluzione


lista_oggetti = [

    [1, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 1]
]

def disegna():
    #Draw
    Glob.screen.fill((12, 24, 36))
    cam.update(Glob.Cam_visible)
    #print(cam.getPositionX(), cam.getPositionY())
    player.draw(Glob.screen)

    render(lista = lista_oggetti, color = "Blue", var = 1, hitbox = None)
    render(lista = lista_oggetti, color = "Yellow", var = 0, hitbox = True)

    # obstacle = pygame.Rect((cam.getPositionX()+60*Glob.MULT),(cam.getPositionY()+140*Glob.MULT), 20*Glob.MULT, 10*Glob.MULT)

    # pygame.draw.rect(Glob.screen, (0,100,255), obstacle)
    # player.HasCollision(obstacle)

    #update
    player.update()

def main():
    #Main Loop
    inizializza()
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.setLeftPress(True)
                    player.Last_keyPressed = "Left"
                if event.key == pygame.K_RIGHT:
                    player.setRightPress(True)
                    player.Last_keyPressed = "Right"
                if event.key == pygame.K_UP:
                    player.setUpPress(True)
                    player.Last_keyPressed = "Up"
                if event.key == pygame.K_DOWN:
                    player.setDownPress(True)
                    player.Last_keyPressed = "Down"
            if event.type == pygame.KEYUP:
                player.Last_keyPressed = "Null"
                if event.key == pygame.K_LEFT:
                    player.setLeftPress(False)
                if event.key == pygame.K_RIGHT:
                    player.setRightPress(False)
                if event.key == pygame.K_UP:
                    player.setUpPress(False)
                if event.key == pygame.K_DOWN:
                    player.setDownPress(False)
            
        disegna()

        console.log(Glob.Debug)
        pygame.display.flip()
        clock.tick(Glob.FPS)


if __name__ == "__main__":
    main()