import pygame, sys

FPS = 30
clock = pygame.time.Clock()

screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Delay")

class Delay():
    def __init__(self, sec, event):
        self.__min = 0
        self.__max = sec * FPS
        self.__increment = 1
        self.__function = event
        self.__flag = True

    #print(self.min, self.max, self.increment, self.function)

    def Start(self):
        if self.__flag:
            self.__min += self.__increment

            if int(self.__min) == self.__max:
                self.__function()
                self.__flag = False

        #print(int(self.__min))

    def ReStart(self):
        if not self.__flag:
            self.__min = 0
            self.__flag = True

        #print(int(self.__min))

    def Infinite(self):
        self.ReStart()
        self.Start()

    def ActualState(self):
        print("| Current Second: %d | Max Seconds: %d | Function: %s |" %(self.__min/FPS, self.__max/FPS, self.__function))


class Delay1():
    def __init__(self, sec):
        self.__min = 0
        self.__max = sec * FPS
        self.__increment = 1
        self.__flag = True

    #print(self.min, self.max, self.increment, self.function)

    def Start(self):
        if self.__flag:
            self.__min += self.__increment

            if int(self.__min) == self.__max:
                self.__flag = False
                return True

        return False

        #print(int(self.__min))

    def ReStart(self):
        if not self.__flag:
            self.__min = 0
            self.__flag = True

        #print(int(self.__min))

    def Infinite(self):
        self.ReStart()
        self.Start()

    def ActualState(self):
        print("| Current Second: %d | Max Seconds: %d | Function: %s |" %(self.__min/FPS, self.__max/FPS, self.__function))

var = 0

def miaFunzione():
    global var
    var += 1
    print(var)

delay = Delay(sec = 3, event = miaFunzione)

def main():
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        screen.fill((12,24,36))

        delay.Infinite()
        #delay.ActualState()

        testo = pygame.font.Font("freesansbold.ttf", 102).render(str(var), True, "White")

        screen.blit(testo, (screen_width/2 - testo.get_width()/2, screen_height/2 - testo.get_height()/2))

        #delay.ActualState()

        clock.tick(FPS)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    main()