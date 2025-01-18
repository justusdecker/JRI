
from pygame import display, NOFRAME,event,QUIT,KEYDOWN,key,K_LCTRL,MOUSEWHEEL
from win32gui import GetWindowLong, SetLayeredWindowAttributes , SetWindowPos , SetWindowLong
from win32con import GWL_EXSTYLE , WS_EX_LAYERED , LWA_COLORKEY
from win32api import RGB
from bin.settings import SETTINGS
from time import time
class Application:
    def __init__(self,size: tuple | list = SETTINGS._getWindowSize(),avs=True,con=False,mov=False) -> None:
        """
        Creates an Window Instance:
            avs: creates awesomeViewStuff like: transparent Bg
            con: controls the events if true: events will disappear
            mov: switch between topless and normal
        """
        self.crashed = False
        self.keyboardInputs = {
            'delete': False,
            'currentKeys': [],
            'strg': False,
            'alt': False,
            'copy': False,
            'paste': False,
            'enter': False
        }
        self.keyboardInputsDefault = {
            'delete': False,
            'currentKeys': [],
            'strg': False,
            'alt': False,
            'copy': False,
            'paste': False,
            'enter': False
        }
        if mov:
            
            self.window = display.set_mode(
                size,
                display=1
            )

        else:
            
            self.window = display.set_mode(
                size,
                NOFRAME,
                display=1
            )
        self.isAlive = True
        if avs: 
            self.awesomeViewStuff()
        self.scrollX = 0
        self.scrollY = 0
        self.con = con
        self.deltaTime = 0
        self.quitJob = None
    def run(self):
        """
        Runs until is not alive
        """
        while self.isAlive:
            t = time()
            self.update()
            self.deltaTime = time() - t
            
    def update(self):
        """
        updates every frame
        """
        
        display.update()
        self.keyboardInputs['currentKeys'].clear()
        self.keyboardInputs['strg'] = False
        self.keyboardInputs['delete'] = False
        self.keyboardInputs['copy'] = False
        self.keyboardInputs['paste'] = False
        self.scrollX = 0
        self.scrollY = 0
        for ev in event.get():
            if ev.type == MOUSEWHEEL:
                self.scrollX,self.scrollY = ev.x,ev.y
            if ev.type == QUIT:
                self.isAlive = False
                if self.quitJob is not None:
                    self.quitJob()
            if ev.type == KEYDOWN:
                self.keyboardInputs['strg'] = key.get_pressed()[K_LCTRL]
                self.keyboardInputs['enter'] = ev.key == 13
                
                if ev.key == 8 and ev.key != 13:
                    self.keyboardInputs['delete'] = True
                elif ev.key == 99 and self.keyboardInputs['strg']:
                    self.keyboardInputs['copy'] = True
                elif ev.key == 118 and self.keyboardInputs['strg']:
                    self.keyboardInputs['paste'] = True
                elif str(ev.unicode).isascii() and ev.key != 13:
                    self.keyboardInputs['currentKeys'].append(ev.unicode)
                    
                elif ev.key == 228 or ev.key == 246 or ev.key == 252:
                    self.keyboardInputs['currentKeys'].append(ev.unicode)



    def render(self,surf,pos):
        """
        draws an Object to Main Surface
        """
        self.window.blit(
            surf,
            pos
            )
    def awesomeViewStuff(self):
        """
        Sets Background Invisible
        Move Window to Monitor 2 and sets the xy coords to 0,0
        """
        hwnd = display.get_wm_info()["window"]
        SetWindowLong(
            hwnd, 
            GWL_EXSTYLE, 
            GetWindowLong(
                hwnd, 
                GWL_EXSTYLE
                ) | WS_EX_LAYERED)

        SetLayeredWindowAttributes(
            hwnd, 
            RGB(0, 255, 0), 
            0, 
            LWA_COLORKEY)
        SetWindowPos(
            display.get_wm_info()['window'], 
            -1, 
            0, 
            0, 
            0, 
            0, 
            1
            )