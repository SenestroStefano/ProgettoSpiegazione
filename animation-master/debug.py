#Importo i vari file e classi necessarie
import myanimation

# Importo le variabili Globali
import global_var as Glob


class Debug():
    def log(self, flag):

        if flag:

            key = ""

            if myanimation.player.getUpPress():
                key = "↑"
            elif myanimation.player.getDownPress():
                key = "↓"
            elif myanimation.player.getLeftPress():
                key = "←"
            elif myanimation.player.getRightPress():
                key = "→"
            
            FPS_TEXT = myanimation.get_font(8*int(Glob.MULT)).render("FPS: "+str(int(myanimation.clock.get_fps())), True, "white")
            FPS_RECT = FPS_TEXT.get_rect(center=(Glob.screen_width-40*Glob.MULT, 20*Glob.MULT))

            DROP_TEXT = myanimation.get_font(5*int(Glob.MULT)).render("DROP "+str(100-int(myanimation.clock.get_fps()*100/Glob.FPS))+"%", True, "red")
            DROP_RECT = DROP_TEXT.get_rect(center=(Glob.screen_width-95*Glob.MULT, 20*Glob.MULT))

            KEY_TEXT = myanimation.get_font(10*int(Glob.MULT)).render(key, True, "blue")
            KEY_RECT = KEY_TEXT.get_rect(center=(Glob.screen_width-140*Glob.MULT, 20*Glob.MULT))


            Glob.screen.blit(KEY_TEXT, KEY_RECT)

            if int(myanimation.clock.get_fps()) <= (Glob.FPS-(Glob.FPS/20)):
                #print("Gli fps sono scesi: "+str(clock.get_fps()))
                Glob.screen.blit(DROP_TEXT, DROP_RECT)
                

            Glob.screen.blit(FPS_TEXT, FPS_RECT)
        