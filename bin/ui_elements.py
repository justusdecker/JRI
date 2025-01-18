import pygame as pg
from bin.settings import SETTINGS
from bin.dataManagement import DM
import calendar
from random import random,randint
from math import sin
from datetime import datetime
import numpy
from time import time
from moviepy.video.io.VideoFileClip import VideoFileClip
from bin.fx.audio import AudioWaveOnlyWvi
from threading import Thread
from bin.log import LOG
from bin.debugFunctions import debugExecutionTimeCheck
from bin.fx.image import TupleImage
from bin.images import WOBBLE,LOADING_CONE
#?
#?
#!      UI creating AREA
#?
#?

def UnpackManager(arg:str,kwargs,default = None):
    if arg in kwargs:
        return kwargs[arg]
    else:
        return default
    
def ImageSaver(imgl:list):
    for idx,img in enumerate(imgl):
        pg.image.save(img,f'{idx}_test.png')

class FONT:
    def __init__(self) -> None:
        pg.font.init()
        self.font = pg.font.SysFont('bahnschrift',13)
    def draw(self,
             text: str = '',
             aa: bool = True,
             color: tuple | list | pg.Color = pg.Color('#454545'),
             size: int = 13):
        self.font.set_point_size(size)

        return self.font.render(text,aa,color)
    
FONTDRAW = FONT()
def getTopCenter(size,dest):
    x,y = size[0]//2,0
    w,h = dest[0]//2,0
    return x - w, y - h
def getCenter(size,dest):
    x,y = size[0]//2,size[1]//2
    w,h = dest[0]//2,dest[1]//2
    return x - w, y - h

TEXT_COLOR = pg.Color('#a6a6a6')
HIGHLIGHT_TEXT_COLOR = pg.Color('#d2d2d2')
PRESSED_TEXT_COLOR = pg.Color('#ffffff')

DEFAULT_BACKGROUND_COLOR = pg.Color('#242424')
MEDIUM_BACKGROUND_COLOR = pg.Color('#484848')

class UXButton:
    def __init__(self,
                 **options) -> None:
        
        self.size = UnpackManager('size',options,(64,24))
        self.borderRadius = UnpackManager('borderRadius',options,15)
        
        
        self.normalTextColor = UnpackManager('normal_text_color',options,TEXT_COLOR)
        self.hoveredTextColor = UnpackManager('hovered_text_color',options,HIGHLIGHT_TEXT_COLOR)
        self.pressedTextColor = UnpackManager('pressed_text_color',options,PRESSED_TEXT_COLOR)
        
        self.normalColor = UnpackManager('normal_color',options,DEFAULT_BACKGROUND_COLOR)
        self.hoveredColor = UnpackManager('hovered_color',options,DEFAULT_BACKGROUND_COLOR)
        self.pressedColor = UnpackManager('pressed_color',options,DEFAULT_BACKGROUND_COLOR)
        
        self.text = UnpackManager('text',options,'')
        self.draw()
    def getAllImages(self):
        return self.normalImage,self.hoveredImage,self.pressedImage 
    def draw(self):
        self.normalImage , self.hoveredImage , self.pressedImage = self.gen(
            [
                (self.normalTextColor,self.normalColor),
                (self.hoveredTextColor,self.hoveredColor),
                (self.pressedTextColor,self.pressedColor)
            ]
        )
        
    def gen(self,array:list=[]):
        _ret = []
        for textColor,backgroundColor in array:
            SURF = pg.Surface(self.size,pg.SRCALPHA)
            pg.draw.rect(
                SURF,
                backgroundColor,
                (
                    0,
                    0,
                    *self.size
                    ),
                border_radius = self.borderRadius
            )
            
            img = FONTDRAW.draw(
                self.text,
                color=textColor
                )
            
            SURF.blit(
                img,
                getCenter(
                    self.size,
                    img.get_size()
                    )
                )
            _ret.append(SURF)
        return _ret

class UXSwitch:
    def __init__(self,
                 **options) -> None:
        
        self.size = UnpackManager('size',options,(24,24))
        self.borderRadius = UnpackManager('borderRadius',options,6)
        self.bg =  UnpackManager('bg_color',options,MEDIUM_BACKGROUND_COLOR)
        self.normalColor = UnpackManager('normal_color',options,TEXT_COLOR)
        self.hoveredColor = UnpackManager('hovered_color',options,HIGHLIGHT_TEXT_COLOR)
        self.pressedColor = UnpackManager('pressed_color',options,PRESSED_TEXT_COLOR)
        
        #On: Pressed
        #on: Hove
        #on normal
        #off pressed
        #off hove
        #off normal
        
        self.normalOffImage,self.hoveredOffImage, self.pressedOffImage,self.normalOnImage,self.hoveredOnImage, self.pressedOnImage = self.draw()
    def draw(self):
        return self.gen([
            (self.normalColor,False),
            (self.hoveredColor,False),
            (self.pressedColor,False),
            (self.normalColor,True),
            (self.hoveredColor,True),
            (self.pressedColor,True),
        ])
    def gen(self,array:list=[]):
        _ret = []
        
        
        
        for foregroundColor,state in array:
            SURF = pg.Surface(self.size,pg.SRCALPHA)
            pg.draw.rect(
                    SURF,
                    self.bg,
                    (
                        0,
                        0,
                        *self.size
                        ),
                    border_radius = self.borderRadius
                )
            if state:
                pg.draw.rect(
                    SURF,
                    foregroundColor,
                    (
                        2,
                        2,
                        20,
                        20
                        ),
                    border_radius = self.borderRadius
                )
                
            
            
            _ret.append(SURF)
        return _ret

class UXLabel:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(128,24))
        self.borderRadius = UnpackManager('borderRadius',options,15)
        self.textColor = UnpackManager('text_color',options,TEXT_COLOR)
        self.backgroundColor = UnpackManager('background_color',options,DEFAULT_BACKGROUND_COLOR)
        self.text = UnpackManager('text',options,'')
        self.anchor = UnpackManager('anchor',options,'center')
        self.surface = self.gen()
        
    def gen(self):

        SURF = pg.Surface(self.size,pg.SRCALPHA)
        pg.draw.rect(
            SURF,
            self.backgroundColor,
            (
                0,
                0,
                *self.size
                ),
            border_radius = self.borderRadius
        )
        
        img = FONTDRAW.draw(
            self.text,
            color=self.textColor
            )
        match self.anchor:
            case 'center':
                SURF.blit(
                    img,
                    getCenter(
                        self.size,
                        img.get_size()
                        )
                    )
            case 'top_center':
                SURF.blit(
                    img,
                    getTopCenter(
                        self.size,
                        img.get_size()
                        )
                    )
        
        return SURF

class UXWindow:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(128,256))
        self.borderRadius = UnpackManager('borderRadius',options,15)
        self.textColor = UnpackManager('text_color',options,TEXT_COLOR)
        self.barColor = UnpackManager('bar_color',options,MEDIUM_BACKGROUND_COLOR)
        self.bgColor = UnpackManager('bg_color',options,DEFAULT_BACKGROUND_COLOR)
        self.text = UnpackManager('text',options,'')
        self.surface = self.gen()
        #! Draw Top
        #! Draw Bottom
        #? _[]X in the next versions?
        #* This Element is needed for Node Building
    def gen(self):
        SURF = pg.Surface(self.size,pg.SRCALPHA)
        pg.draw.rect(
            SURF,
            self.bgColor,
            (
                0,
                0,
                *self.size
                ),
            border_radius = self.borderRadius
        )
        pg.draw.rect(
            SURF,
            self.barColor,
            (
                0,
                0,
                self.size[0],
                24
                ),
            border_top_left_radius = self.borderRadius,
            border_top_right_radius = self.borderRadius
        )
        
        img = FONTDRAW.draw(
            self.text,
            color=self.textColor
            )
        
        SURF.blit(
            img,
            getCenter(
                (self.size[0],24),
                img.get_size()
                )
            )
        
        return SURF

class UXLoadingBar:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(512,24))
        self.borderRadius = UnpackManager('borderRadius',options,15)
        self.barColor = UnpackManager('bar_color',options,MEDIUM_BACKGROUND_COLOR)
        self.bgColor = UnpackManager('bg_color',options,DEFAULT_BACKGROUND_COLOR)
        self.bg,self.bar = self.gen([self.bgColor,self.barColor])
        self.currentProgress = 0
        self.currentProgressImage = self.bg.copy()
    def getCurrentProgress(self,percent:float):
        if percent != self.currentProgress:
            self.currentProgress = percent
            SURF:pg.Surface = self.bg.copy()
            max = self.bg.get_width()
            SURF.blit(self.bar,(0,0),area=(0,0,int(percent * max),self.bg.get_height()))
            self.currentProgressImage = SURF
            return SURF
        return self.currentProgressImage
    def gen(self,array:list):
        _surfaces = []
        for color in array:
            
            SURF = pg.Surface(self.size,pg.SRCALPHA)
            pg.draw.rect(
                SURF,
                color,
                (
                    0,
                    0,
                    *self.size
                    ),
                border_radius = self.borderRadius
            )
        
            _surfaces.append(SURF)
        return _surfaces

class UXBubbleText:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(1280,720))
        self.borderRadius = UnpackManager('borderRadius',options,15)
        CUTOUT = pg.Surface(self.size,pg.SRCALPHA)
        CUTOUT.fill((0,255,0))
        pg.draw.rect(CUTOUT,
                     (0,0,0,0),
                     (0,
                      0,
                      *self.size
                      ),
                        border_radius=self.borderRadius
                        )
        self.CUTOUT = CUTOUT

class UXLoadingCone:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(384,216))
        """
        calculate Alpha based on distance to the last pixel before out of surface
        """
        self.baseImage = TupleImage(LOADING_CONE).surf

        self.gen()
    @debugExecutionTimeCheck
    def gen(self):
        self.animationFrames = [pg.transform.rotate(self.baseImage,i) for i in range(0,360,90)]
        pass
class UXBackgroundWobble:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(384,216))
        """
        calculate Alpha based on distance to the last pixel before out of surface
        """
        self.gen()
    @debugExecutionTimeCheck
    def gen(self) -> None:
        self.element = TupleImage(WOBBLE).surf
            #self.element.blit(pg.transform.rotate(circle,x),(50,50))
        
        
    def getRgb(self,pixel):
        return pixel.r,pixel.g,pixel.b,pixel.a

class UXVideo:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(384,216))
        self.borderRadius = UnpackManager('borderRadius',options,15)
        CUTOUT = pg.Surface(self.size,pg.SRCALPHA)
        BACKGROUND = pg.Surface(self.size)
        CUTOUT.fill((0,255,0))
        pg.draw.rect(CUTOUT,
                     (0,0,0,0),
                     (0,
                      0,
                      *self.size
                      ),
                        border_radius=self.borderRadius
                        )
        self.CUTOUT = CUTOUT

class UXWaveForm:
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(256,64))
        self.wv = UnpackManager('wv',options,[])
        CUTOUT = pg.Surface(self.size,pg.SRCALPHA)
        BACKGROUND = pg.Surface(self.size)
        CUTOUT.fill((0,255,0))
        pg.draw.rect(CUTOUT,
                     (0,0,0,0),
                     (0,
                      0,
                      *self.size
                      ),
                        border_radius=15
                        )
        self.CUTOUT = CUTOUT
    def gen(self):
        surf = pg.Surface(self.size)
        surf.fill(pg.Color('#242424'))
        if self.wv.__len__() == 0:
            return surf
        for i in range(self.size[0]):
            idx = (((self.wv.__len__()- 1) // self.size[0]) ) * i
            if self.wv[idx] > 0.2:
                self.wv[idx] = self.wv[idx] * .5
                pg.draw.line(surf,pg.Color('#960f0f'),(i,0),(i,self.size[1]))
            else:
                pg.draw.line(surf,pg.Color('#969696'),(i,0),(i,self.size[1]))
            pg.draw.line(surf,pg.Color('#484848'),(i,0),(i,self.wv[idx] * 500 if self.wv[idx] > 0 else 1 / self.size[1]))
        surf = pg.transform.flip(surf,False,True)
        surf.blit(self.CUTOUT,(0,0))
        surf.set_colorkey((0,255,0))
        return surf

#ImageSaver([UXLoadingBar().getCurrentProgress(50)])
#input('passed')

class UXToolTip: #Todo
    def __init__(self,**options) -> None:
        self.size = UnpackManager('size',options,(128,24))
        self.borderRadius = UnpackManager('borderRadius',options,6)
        self.textColor = UnpackManager('text_color',options,TEXT_COLOR)
        self.backgroundColor = UnpackManager('background_color',options,DEFAULT_BACKGROUND_COLOR)
        self.text = UnpackManager('text',options,'')
        self.surface = self.gen()
        
    def gen(self):

        SURF = pg.Surface(self.size,pg.SRCALPHA)
        pg.draw.rect(
            SURF,
            self.backgroundColor,
            (
                0,
                0,
                *self.size
                ),
            border_radius = self.borderRadius
        )
        
        img = FONTDRAW.draw(
            self.text,
            color=self.textColor
            )
        
        SURF.blit(
            img,
            getCenter(
                self.size,
                img.get_size()
                )
            )
        for x in range(SURF.get_width()):
            for y in range(SURF.get_height()):
                cur = SURF.get_at()
                cur[-1] -= 128
                SURF.set_at((x,y),cur)
        return SURF

class UIElement: pass

class UICounter:
    def __init__(self):
        self.count = {}
        self.all = 0
    def addElement(self,key):
        self.all += 1
        
        if key in self.count:
            self.count[key] += 1
        else:
            self.count[key] = 1
            
        LOG.nlog(1,'created UIE of Type: $ | e: $',[key,self.count[key]])
    def remElement(self,key):
        if key in self.count:
            self.count[key] -= 1
        LOG.nlog(1,'removed UIE of Type: $ | e: $',[key,self.count[key]])
            
UIC = UICounter()
class UIID:
    def __init__(self) -> None:
        self.id = 0
    def add(self):
        self.id += 1
        return self.id - 1
    
UIIDCOUNT = UIID()
class UIManager: #
    def __init__(self) -> None:
        self.queue = {}
        UIC.addElement('uiManager')
    def addToQueue(self,object,layer):
        if not layer in self.queue:
            self.queue[layer] = []
        
        self.queue[layer].append(object)
        
        LOG.nlog(1,'$ added to queue on layer $',[object.elementId,layer])
    def removeFromQueue(self,id):
        for layer in self.queue:
            for idx,obj in enumerate(self.queue[layer]):
                if obj.elementId == id:
                    self.queue[layer].pop(idx)
                    LOG.nlog(1,'$ removed from queue  $',[obj.id,layer])
                    

        
        
    def renderQueue(self,
                    app,
                    groups:list | tuple = ('default',),
                    ignoreList=[]):
        #+ Only One button is clickable
        _updates = []
        for layer in self.queue.keys():
            if layer in ignoreList: continue
            for object in self.queue[layer]:

                if object.group.groupName in groups:
                        
                    _updates.append(object)
                    if object.visible:
                        app.window.blit(object.getImage(),object.getAbsPosition())
        _updates.reverse()
        for object in _updates:
            object.update() 
            if object.thisFramePressed:
                break
            #! Check Frame is checked

UIM = UIManager()

class UIGroup:
    def __init__(self,
                 groupName):
        self.groupName = groupName
        UIC.addElement('uiGroup')
UIDefaultGroup = UIGroup('default')
class UIElement:
    def __init__(self,
                 rect: pg.Rect,
                 **kwargs) -> None:
        """
        The Default UI Element:
        Arguments:
            rect    : pygame.Rect = (pos,dest)
            kwargs:
                layer   :   int         =   0
                visible :   bool        =   True
                canvas  :   None        =   None    [CURRENTLY NOT USED!]
                anchor  :   str         =   'top_left'  [BETA: NOT USED IN EVERY FUNCTION]
                name    :   str         =   ''
                ? Makes finding much easier
                parent  :   UIElement   = None
                group   :UIGroup        = UIDefaultGroup
        """
        self.rect = rect.copy()
        
        UIC.addElement('uiElement')
        self.pos = rect.x,rect.y
        self.dest = rect.w,rect.h
        
        self.group = UnpackManager('group',kwargs,UIDefaultGroup)
        
        self.elementId = UIIDCOUNT.add()
        self.elementName = kwargs['name'] if 'name' in kwargs else ''
        
        self.setLayer(kwargs['layer'] if 'layer' in kwargs else 0)
        
        self.setVisibility(kwargs['visible'] if 'visible' in kwargs else True)
        
        self.setCanvas(kwargs['canvas'] if 'canvas' in kwargs else None)
        
        self.setAnchor(kwargs['anchor'] if 'anchor' in kwargs else 'top_left')
        
        self.setParent(kwargs['parent'] if 'parent' in kwargs else None)
        
        UIM.addToQueue(self,self.layer)
        
        #Clickable Stuff
        self.isHovered = False
        self.isPressed = False
        self.stop = False
        self.thisFrameHovered = False
        self.thisFrameUnHovered = False
        self.thisFramePressed = False
        self.thisFrameUnPressed = False
        self.lastFrameHover = False
        
    def check(self,absPos,dest):
        #! Defines thisFrame Values
        self.thisFrameHovered = False
        self.thisFrameUnHovered = False
        self.thisFramePressed = False
        self.thisFrameUnPressed = False
        click = pg.mouse.get_pressed()[0]
        
        if not self.stop:
            
            x,y,w,h = absPos[0],absPos[1],dest[0],dest[1]
            g,l = pg.mouse.get_pos()
            
            if g > x and l > y and g < x + w and l < y + h: #? Check Hovering
                self.isHovered = True
                if not self.lastFrameHover:
                    self.thisFrameHovered = True
                    self.lastFrameHover = True
            else:
                self.isHovered = False
                if self.lastFrameHover:
                    self.lastFrameHover = False
                    self.thisFrameUnHovered = True
            
            if not self.isHovered and click:# ? Check not over!
                self.stop = True
                return

            if not click and self.isPressed:    # ? Check Unpress Condition
                self.isPressed = False
                self.thisFrameUnPressed = True

            if self.isHovered and click and not self.isPressed:    # ? Check Pressed Condition
                self.isPressed = True
                self.thisFramePressed = True
            
        if not click: # ? Reset Blocking!
            self.stop = False     
    def kill(self):
        UIM.removeFromQueue(self.elementId)
        del self
    def update(self):
        if self.visible:
            return self.check(self.getAbsPosition(),self.dest)
    
    def getImage(self):
        if not hasattr(self,'surface'):
            self.surface = pg.Surface((1,1))
        return self.surface
    
    def getAbsPosition(self):
        x,y = self.getParentOffsets()
        match self.anchor: #? Manipulates the offset by a certain value
            case 'center':
                if self.parent is None:
                    return self.pos[0] + (self.dest[0] *.5),self.pos[1] + (self.dest[1] *.5)
                else:
                    return x + (self.parent.dest[0] *.5) - (self.dest[0] *.5) + self.pos[0],y  + (self.parent.dest[1] *.5) - (self.dest[1] *.5)+ self.pos[1]
            case 'top_left':
                if self.parent is None:
                    return self.pos
                else:
                    return x + self.pos[0],y + self.pos[1]
    
    def getPosition(self) -> list:
        return self.pos
    
    def getDest(self) -> list:
        return self.dest
    
    def getLayer(self) -> int:
        return self.layer
    
    def getParentOffsets(self) -> list:
        xOffset,yOffset = 0,0
        parent = self.parent
        
        while parent is not None:
            xOffset += parent.pos[0]
            yOffset += parent.pos[1]
            parent = parent.parent
            
        return xOffset,yOffset
    
    def getAllParents(self) -> list[UIElement]:
        parents = []
        parent = self.parent
        while parent is not None:
            parents.append(parent)
            parent = parent.parent
            
        return parents
    
    def getParent(self) -> UIElement:
        return self.parent
    
    def setLayer(self,layer:int) -> None:
        self.layer: int = layer
    
    def setParent(self,parent: UIElement) -> None:
        self.parent: UIElement = parent
    
    def setAnchor(self,position:str) -> None:
        self.anchor: str = position
        
    def setImage(self,surface:pg.Surface) -> None:
        self.surface: pg.Surface = surface
        
    def setCanvas(self,value:pg.Rect) -> None:
        self.canvas: pg.Rect = value
        
    def setVisibility(self,value:bool) -> None:
        self.visible: bool = value

FONTBTE = pg.font.SysFont('bahnschrift',1)
class BubbleTextElement:
    def __init__(self,text,size,uie) -> None:
        UIC.addElement('uiBTE')
        
        self.offset = random()
        self.text = text
        self.size = size if size < 20 else 20
        #print(size)
        
        self.preRenderedSizes = {}
        self.currentSize = -1
        self.moveX = randint(-255,255) * .1
        self.moveY = randint(-255,255) * .1
        self.fadeOut = False
        self.fadeIn = True
        self.fade = 0
        self.dead = False
        self.uiElement = uie
        self.position = [randint(0,self.uiElement.surface.get_width()),randint(0,self.uiElement.surface.get_height())]
    def gen(self,t):
        size = int((self.size)*(2*abs(sin(t+self.offset))+1))
        self.currentSize = size
        if str(size) not in self.preRenderedSizes:
            
            FONTBTE.set_point_size(size)
        #print([int(255 * self.color) % 255 for x in range(3)])
            self.surface = FONTBTE.render(self.text,True,[int(255 * self.color) if 255 * self.color <= 255 else 255 for x in range(3)])
            self.preRenderedSizes[str(size)] = self.surface

        #self.surface = scale(self.surface,(int(self.surface.get_width()*size),int(self.surface.get_height()*size)))
    def update(self,app):
        flip = False
        while self.position[0]+(self.preRenderedSizes[str(self.currentSize)].get_width()//2) > self.uiElement.surface.get_width():
            self.position[0] -= 1
            flip = True
        while self.position[1]+(self.preRenderedSizes[str(self.currentSize)].get_height()//2) > self.uiElement.surface.get_height():
            self.position[1] -= 1
            flip = True
        
        while self.position[0]-(self.preRenderedSizes[str(self.currentSize)].get_width()//2) < 0:
            self.position[0] += 1
            flip = True
        while self.position[1]-(self.preRenderedSizes[str(self.currentSize)].get_height()//2) < 0:
            self.position[1] += 1
            flip = True
        if flip:
            self.moveX = self.moveX * -1
            self.moveY = self.moveY * -1
            #self.position[1] = abs(self.position[1]+(self.preRenderedSizes[str(self.currentSize)].get_height()//2))
        
        self.position[0] += self.moveX * app.deltaTime
        self.position[1] += self.moveY * app.deltaTime
        
        #Text FadeOut
        if randint(0,50) == 1:
            if not self.fadeOut:
                self.fadeIn = True
            if not self.fadeIn:
                self.fadeOut = True
        if self.fade <= 0 and randint(0,100) == 1:
            self.dead = True
            self.fadeOut = False
            self.fadeIn = False
        if self.dead and randint(0,100) == 1:
            self.dead = False
            self.fadeIn = True
        if self.fadeIn:
            self.fade += app.deltaTime * randint(0,100)
            if self.fade > 255:
                self.fade = 255
        if self.fadeOut:
            self.fade -= app.deltaTime * randint(0,100)
        if self.preRenderedSizes[str(self.currentSize)].get_alpha() != self.fade:
            
            self.preRenderedSizes[str(self.currentSize)].set_alpha(self.fade)
        return self.preRenderedSizes[str(self.currentSize)],(int((self.position[0])-(self.preRenderedSizes[str(self.currentSize)].get_width()//2)),int((self.position[1])-(self.preRenderedSizes[str(self.currentSize)].get_height()//2)))


class UIAudioWave(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs) -> None:
        super().__init__(rect, **kwargs)
        UIC.addElement('uiAudioWave')
        
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
        """self.UX = UXWaveForm(
            **UnpackManager(
                'ux',
                kwargs,
                {}
                )
            )"""
        if 'slider' in kwargs:
            self.slider = kwargs['slider']
        else:
            raise Exception('No Slider given')
        self.adaptor = []
        #self.slider = UISliderLR(pg.Rect(0,rect.h,rect.w,24),group=self.group,parent=self,layer=self.layer)

        self.fileNameLabel = UILabel(
            pg.Rect(0,rect.h-24,512,24),
            group=self.group,
            parent=self,
            layer=self.layer+1,
            ux={
                'size':(512,24),
                'text': ''
                },
            )
        
        self.loadedLabel = UILabel(
            pg.Rect(512,rect.h-24,48,24),
            group=self.group,
            parent=self,
            layer=self.layer+1,
            ux={
                'size':(48,24),
                'text': ''
                },
            )

        self.setImage(pg.Surface((rect.w,rect.h)))
        self.surface.fill((0,0,0))
        self.audioVisualizer: AudioWaveOnlyWvi = None
        # Normal Size 1232 x 200
        super().__init__(rect,**kwargs)
        #self.setImage(self.UX.gen())
        self.zoom = 0
        self.start = 0
        self.heightZoom = .3
        self.waveZoom = 1
        self.start_id = 0
        self.thread = None
    def setAudio(self,filePath):
        self.audioVisualizer = AudioWaveOnlyWvi(filePath)

    def calculateStartPosition(self):
        for element in self.adaptor:
            if self.waveZoom != element.waveZoom:
                element.waveZoom = self.waveZoom
                element.zoom = self.zoom
                #element.calculateStartPosition()
        #remove slider
        self.surface.fill((0,0,0))
        
        if self.audioVisualizer is not None:
            LENGTH_AUDIO = self.audioVisualizer.data.__len__()
            ACTUAL_ZOOM = self.waveZoom*1232
            MAX = LENGTH_AUDIO - ACTUAL_ZOOM #! Das ist die Maximallänge die erreicht werden darf
            DELENGTH = (MAX / 1232) * (1 / self.waveZoom)
            DEL = (DELENGTH*1232*self.waveZoom)

            ABS = (DEL - (MAX*self.waveZoom))*self.slider.sliderPercent
            

            start_id = ABS


            _data,ids = self.audioVisualizer.get(int(start_id),self.waveZoom)
            
            
            
            hSize = (self.dest[1] // 2) * self.heightZoom
            
            _copySurface = self.surface.copy()
            #! 0 Bg light grey fg black
            #! Over x Values are light red and bg black
            for index,height in enumerate(_data):
                pg.draw.line(_copySurface,(128,128,128),(index,0),(index,(hSize * height)))

            self.surface.blit(pg.transform.flip(_copySurface,False,True),(0,-(self.dest[1]//2)))
            self.surface.blit(_copySurface,(0,self.dest[1]//2))
            self.loadedLabel.UX.text = str(int((len(self.audioVisualizer.hashMap)/len(self.audioVisualizer.data))*100)) + '%'
            self.loadedLabel.setImage(self.loadedLabel.UX.gen())
    def calculateZoom(self):
        if self.isHovered and pg.key.get_pressed()[pg.K_LCTRL]:
            self.heightZoom += self.app.scrollY*.02
        elif self.isHovered:
            self.zoom = self.zoom + (self.app.scrollY)
            match self.zoom:#More Levels
                case 0:
                    _zoom = 1
                case 1:
                    _zoom = 0.75
                case 2:
                    _zoom = 0.5
                case 3:
                    _zoom = 0.25
                case 4:
                    _zoom = 0.125
                case 5:
                    _zoom = 0.0625
            if self.zoom > 5:
                _zoom = 0.0625
                self.zoom = 5
            if self.zoom < 0:
                _zoom = 1
                self.zoom = 0
            self.waveZoom = _zoom
            
    def update(self):
        self.calculateZoom()
        self.calculateStartPosition()
        #if self.audioVisualizer is not None:
            #self.audioVisualizer.get(self.start,self.zoom)
        #self.surface.fill((0,0,0))
        
        
        return super().update()

class UIBubbleText(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs) -> None:
        super().__init__(rect, **kwargs)
        UIC.addElement('uiBubbleText')
        self.setImage(pg.Surface((rect.w,rect.h)))
        self.data = UnpackManager('data',kwargs,{'NOTHING':1})
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
        self.UX = UXBubbleText(
            **UnpackManager(
                'ux',
                kwargs,
                {}
                )
            )
        self.generateBubbleElementsLow()
        
        #self.setImage(self.UX.normalImage)
    def generateBubbleElementsHigh(self):
        self.bubbles = []
        self.highestNum = 0
        for word in self.data.keys():
            if self.data[word] > self.highestNum:
                self.highestNum = self.data[word]
            self.bubbles.append(BubbleTextElement(word,self.data[word],self))
        t = time()
        self.lastTime = time()
        for bubble in self.bubbles:
            bubble.color = bubble.size / self.highestNum
            bubble.gen(0)
    def generateBubbleElementsLow(self):
        if self.data.__len__() == 0:
            self.data = {'NOTHING':1}
        self.bubbles = []
        self.lowestNum = 0
        for word in self.data.keys():
            if self.data[word] > self.lowestNum:
                self.lowestNum = self.data[word]
            
            if randint(0,3) == 2 or self.bubbles.__len__() == 0:
                self.bubbles.append(BubbleTextElement(word,20-(self.data[word]%20),self))
        t = time()
        self.lastTime = time()
        for bubble in self.bubbles:
            bubble.color = bubble.size / self.lowestNum
            bubble.gen(0)
    def update(self):
        #display.set_caption(f'{int(1 / self.deltaTime) if self.deltaTime != 0 else 0}')
        t = time()
        self.surface.fill(pg.Color('#121212'))
        for bubble in self.bubbles:
            bubble.gen(t)
            _surf,_pos = bubble.update(self.app)
            self.surface.blit(_surf,_pos)
        self.surface.blit(self.UX.CUTOUT,(0,0))
        self.surface.set_colorkey((0,255,0))
        return super().update()
        
class UIWaveForm(UIElement):
    def __init__(self,
                 rect:pg.Rect,
                 **kwargs) -> None:
        UIC.addElement('uiWaveForm')
        self.UX = UXWaveForm(
            **UnpackManager(
                'ux',
                kwargs,
                {}
                )
            )
        super().__init__(rect,**kwargs)
        self.setImage(self.UX.gen())

class UIButton(UIElement):
    def __init__(self,
                 rect:pg.Rect,
                 **kwargs) -> None:
        UIC.addElement('uiButton')
        
        
        self.UX = UXButton(
            **UnpackManager(
                'ux',
                kwargs,
                {}
                )
            )
            
        self.setImage(self.UX.normalImage)
        super().__init__(rect,**kwargs)
        
        self.oHC = UnpackManager('onHoveredCallback',kwargs,self.noCallback)
        
        self.oPC = UnpackManager('onPressCallback',kwargs,self.noCallback)
        
        self.oUHC = UnpackManager('onUnHoverCallback',kwargs,self.noCallback)
        
        self.oUPC = UnpackManager('onUnPressCallback',kwargs,self.noCallback)
        
    def noCallback(self,btn):
        pass
    def update(self):
        #Change Texture on the fly
        if self.thisFrameHovered:
            self.setImage(self.UX.hoveredImage)
            self.oHC(self)
        if self.thisFramePressed:
            self.setImage(self.UX.pressedImage)
            self.oPC(self)
        if self.thisFrameUnPressed:
            self.setImage(self.UX.normalImage)
            self.oUPC(self)
        if self.thisFrameUnHovered:
            self.setImage(self.UX.normalImage)
            self.oUHC(self)
        super().update()

class UILabel(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        UIC.addElement('uiLabel')
        super().__init__(rect, **kwargs)
        self.UX = UXLabel(
            **UnpackManager(
                'ux',
                kwargs,
                {
                    'size' : self.dest
                    }
                )
            )
        self.setImage(self.UX.surface)
        
    def update(self):
        super().update()

class UIImage(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.addElement('uiImage')
        self.UX = UXVideo(**UnpackManager('ux',kwargs,{}))
        self.setImage(pg.Surface((1,1)))
    def setSprite(self,surface):
        
        if isinstance(surface , pg.Surface):
            self.surface = pg.transform.scale(surface,self.dest)
            self.surface.blit(self.UX.CUTOUT,(0,0))
            self.surface.set_colorkey((0,255,0))
        else:
            self.surface = pg.transform.scale(pg.image.load(surface),self.dest)
            self.surface.blit(self.UX.CUTOUT,(0,0))
            self.surface.set_colorkey((0,255,0))

class UICalendar(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        UIC.addElement('uiCalendar')
        super().__init__(rect, **kwargs)
        
        self.surface = pg.Surface((1,1),pg.SRCALPHA)
        self.buttonArray = []
        self.ids = []
        for i in range(31):
            self.buttonArray.append(UIButton(pg.Rect(-1000,-1000,24,24),onPressCallback=self.setDate,ux={'size':(24,24),'text': f'{i+1}'},parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group))
            self.ids.append(self.buttonArray[-1])
        
        self.currentDate = str(datetime.today()).split(' ')[0].split('-')
        
        self.selectedDay = int(self.currentDate[2])
        self.selectedMonth = int(self.currentDate[1])
        self.selectedYear = int(self.currentDate[0])
        
        
        #self.DateSelectLabel.setImage(self.DateSelectLabel.UX.gen())
        self.dateShowLabel = UILabel(pg.Rect(-1000,-1000,72,24),parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group)
        self.changeMonthBackButton = UIButton(pg.Rect(-1000,-1000,24,24),onPressCallback=self.setMonthLast,ux={'size':(24,24),'text': f'<'},parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group)
        self.changeMonthNextButton = UIButton(pg.Rect(-1000,-1000,24,24),onPressCallback=self.setMonthNext,ux={'size':(24,24),'text': f'>'},parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group)
        self.DateSelectLabel = UILabel(pg.Rect(-1000,-1000,144,24),ux={'text': 'Date Selector','size':(144,24)},parent= UnpackManager('parent',kwargs,None),layer=self.layer,group=self.group)
        self.changeMonth()
        
    def changeMonth(self,*_):
        weekday,days = calendar.monthrange(self.selectedYear,self.selectedMonth)
        self.buttons = []
        x , y = 0 , 0
        d = 0
        for btn in self.buttonArray:
            if x == 6:
                y += 1
                x = 0
            btn:UIButton
            btn.pos = (24*x)+self.pos[0],(24*(y+1))+self.pos[1]
            x += 1
            d += 1
            if d > days:
                btn.visible = False
            else:
                btn.visible = True
        if y < 5: y = 5  
        self.DateSelectLabel.pos = self.pos
        self.changeMonthBackButton.pos = self.pos[0]+(24),(24*(y+1))+self.pos[1]
        self.changeMonthNextButton.pos = self.pos[0]+(24*5),(24*(y+1))+self.pos[1]
        self.dateShowLabel.pos = self.pos[0]+(24*2),(24*(y+1))+self.pos[1] # ADD +1 to y for under placement
        self.dateShowLabel.UX.text = f'{self.selectedDay}/{self.selectedMonth}/{self.selectedYear}'
        self.dateShowLabel.setImage(self.dateShowLabel.UX.gen())
        return x,y
    def setMonthLast(self,*_):
        self.selectedMonth -= 1
        if self.selectedMonth < 1:
            self.selectedMonth += 12
            self.selectedYear -= 1
        self.changeMonth()
    def setMonthNext(self,*_):
        self.selectedMonth += 1
        if self.selectedMonth > 12:
            self.selectedMonth -= 12
            self.selectedYear += 1
        self.changeMonth()
    def setDate(self,*_):
        
        self.selectedDay = self.ids.index(_[0]) + 1
        self.dateShowLabel.UX.text = f'{self.selectedDay}/{self.selectedMonth}/{self.selectedYear}'
        self.dateShowLabel.setImage(self.dateShowLabel.UX.gen())
    def getDate(self):
        _ret = ''
        if self.selectedDay < 10:
            _ret += f'0{self.selectedDay}-'
        else:
            _ret += f'{self.selectedDay}-'
        if self.selectedMonth < 10:
            _ret += f'0{self.selectedMonth}-'
        else:
            _ret += f'{self.selectedMonth}-'
        return _ret + str(self.selectedYear)
    def noCallback(self,btn):
        pass
    
class UIProgressBar(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.addElement('uiProgressBar')
        self.UX = UXLoadingBar(**UnpackManager('ux',kwargs,{}))
        self.setImage(pg.Surface((1,1)))
    def draw(self,progress):
        self.setImage(self.UX.getCurrentProgress(progress))
    def update(self):
        
        return super().update()
    
class UITimeSelect(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.addElement('uiTimeSelect')
        self.setImage(pg.Surface((1,1)))
        self.hour = 0
        self.minute = 0
        self.minuteMultiplier = 15
        
        self.minuteUpButton = UIButton(pg.Rect(24,0,24,24),ux={'size':(24,24),'text': '/\\'},onPressCallback = self.changeMinuteUp,parent=self,layer=self.layer,group=self.group)
        self.minuteDownButton = UIButton(pg.Rect(24,48,24,24),ux={'size':(24,24),'text': '\\/'},onPressCallback = self.changeMinuteDown,parent=self,layer=self.layer,group=self.group)
        self.hourUpButton = UIButton(pg.Rect(0,0,24,24),ux={'size':(24,24),'text': '/\\'},onPressCallback = self.changeHourUp,parent=self,layer=self.layer,group=self.group)
        self.hourDownButton = UIButton(pg.Rect(0,48,24,24),ux={'size':(24,24),'text': '\\/'},onPressCallback = self.changeHourDown,parent=self,layer=self.layer,group=self.group)
        
        self.timeLabel = UILabel(pg.Rect(0,24,48,24,ux={'size':(48,24)}),parent=self,layer=self.layer,group=self.group)
        self.updateTimeLabel()
    def updateTimeLabel(self):
        self.timeLabel.UX.text = f'{self.getDoubleZeros(self.hour)}:{self.getDoubleZeros(self.minute)}'
        self.timeLabel.setImage(self.timeLabel.UX.gen())
    def changeHourUp(self,*_):
            self.hour += 1
            if self.hour > 23:
                self.hour = self.hour % 24
            self.updateTimeLabel()
    def changeHourDown(self,*_):
        self.hour -= 1
        if self.hour < 0:
            self.hour += 24
        self.updateTimeLabel()
    def changeMinuteUp(self,*_):
        self.minute += self.minuteMultiplier
        if self.minute > 59:
            self.minute = self.minute % 60
            self.changeHourUp()
        self.updateTimeLabel()
    def changeMinuteDown(self,*_):
        self.minute -= self.minuteMultiplier
        if self.minute < 0:
            self.minute += 60
            self.changeHourDown()
        self.updateTimeLabel()
    def getDoubleZeros(self,val):
        if val < 10:
            return '0' + str(val)
        return str(val)
    def update(self):
        return super().update()

class UISwitch(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect,**kwargs)
        UIC.addElement('uiSwitch')
        self.toggle = UnpackManager('initialValue',kwargs,False)
        self.UX = UXSwitch()
        self.setImage(self.UX.normalOffImage)
        self.oHC = UnpackManager('onHoveredCallback',kwargs,self.noCallback)
        
        self.oPC = UnpackManager('onPressCallback',kwargs,self.noCallback)
        
        self.oUHC = UnpackManager('onUnHoverCallback',kwargs,self.noCallback)
    def noCallback(self,_):
        pass
    def update(self):
        #Change Texture on the fly
        if self.thisFrameHovered:
            self.setImage([self.UX.hoveredOffImage,self.UX.hoveredOnImage][self.toggle])
            self.oHC(self)
        if self.thisFramePressed:
            self.toggle = not self.toggle
            self.setImage([self.UX.normalOffImage,self.UX.normalOnImage][self.toggle])
            self.oPC(self)
        if self.thisFrameUnHovered:
            self.setImage([self.UX.normalOffImage,self.UX.normalOnImage][self.toggle])
            self.oUHC(self)
        super().update()
   
class UIVideoPlayer(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.addElement('uiVideoPlayer')
        self.nextFrame = 0
        self.nPos = self.pos
        self.currentFrame = 0
        self.isPlaying = False
        self.isLoaded = False
        self.frame = pg.Surface(self.dest)
        self.UX = UXVideo()
        self.fullscreen = False
        self.aP,self.vP = '',''
        self.laP,self.lvP = '',''
        self.playButton = UIButton(pg.Rect(24,216-24,24,24),ux={'text': '|>','size':(24,24)},onPressCallback=self.togglePlay,parent=self,group=self.group)
        
        self.ffButton = UIButton(pg.Rect(48,216-24,24,24),ux={'text': '>>','size':(24,24)},onPressCallback=self.moveFramePlus,parent=self,group=self.group)
        self.rwButton = UIButton(pg.Rect(0,216-24,24,24),ux={'text': '<<','size':(24,24)},onPressCallback=self.moveFrameMinus,parent=self,group=self.group)
        self.fullscreenToggleButton = UIButton(pg.Rect(384-24,216-24,24,24),ux={'text': '=','size':(24,24)},onPressCallback=self.toggleFullscreen,parent=self,group=self.group)
        self.takeThumbnailButton = UIButton(pg.Rect(384-48,216-24,24,24),ux={'text': '[]','size':(24,24)},onPressCallback=self.takeimage,parent=self,group=self.group)
        self.timeLabel = UILabel(pg.Rect(72,216-24,144,24),ux={'text': '<<','size':(144,24)},parent=self,group=self.group)
        self.timeLabel.UX.text = f'00:00 / INF'
        self.timeLabel.setImage(self.timeLabel.UX.gen())
        
        self.progressBar = UIProgressBar(pg.Rect(0,216-32,384,8),ux={'size':(384,8)},parent=self,group=self.group)
        self.progressFullscreenBar = UIProgressBar(pg.Rect(0,720-32,1280,8),ux={'size':(1280,8)},parent=self,group=self.group)
        self.progressFullscreenBar.visible = False
        self.setImage(self.frame)
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
    def toggleFullscreen(self,*_,force:bool=None):
        self.fullscreen = not self.fullscreen if force is None else force
        
        if self.fullscreen:
            self.pos = (0,0)
            self.timeLabel.pos = (72,720-24)
            self.rwButton.pos = (0,720-24)
            self.playButton.pos = (24,720-24)
            self.ffButton.pos = (48,720-24)
            self.fullscreenToggleButton.pos = (1280-24,720-24)
            self.takeThumbnailButton.pos = (1280-48,720-24)
            self.progressBar.visible = False
            self.progressFullscreenBar.visible = True
        else:
            self.pos = self.nPos
            self.rwButton.pos = (0,216-24)
            self.playButton.pos = (24,216-24)
            self.ffButton.pos = (48,216-24)
            self.timeLabel.pos = (72,216-24)
            self.fullscreenToggleButton.pos = (384-24,216-24)
            self.takeThumbnailButton.pos = (384-48,216-24)
            self.progressBar.visible = True
            self.progressFullscreenBar.visible = False
    def getDoubleZeros(self,val):
        if val < 10:
            return '0' + str(val)
        return str(val)
    def mod60(self,val):
        if val == 0: return 0
        return val % 60
    
    def _loadData(self,videoPath,audioPath):
        try:
            if self.visible:
                self.currentFrame = 0
                self.nextFrame = 0
                self.isLoaded = False
                self.videoName = videoPath
                self.audioName = audioPath
                self.video = VideoFileClip(videoPath)
                self.firstAudio = pg.mixer.music.load(self.audioName)
                self.timeLabel.UX.text = f'{self.getTime()}'
                self.timeLabel.setImage(self.timeLabel.UX.gen())
                self.surface.fill((0,0,0))
                self.video.rotation = 90
                self.isLoaded = True
                self.fullscreen = False
                self.toggleFullscreen(force=False)
        except:
            self.isLoaded = False
    def switch(self,trig:bool):
        if trig:
            if not pg.mixer.music.get_busy():pg.mixer.music.play(0,self.currentFrame)
        else:
            if pg.mixer.music.get_busy():pg.mixer.music.stop()
    def moveFramePlus(self,*_):
        self.moveFrame(15)
    def moveFrameMinus(self,*_):
        self.moveFrame(-15)
    def takeimage(self,*_):
        frame = pg.pixelcopy.make_surface(numpy.flipud(numpy.rot90(self.video.get_frame(self.currentFrame),1)))
        pg.image.save(frame,f'{int(time())}.png')
    def moveFrame(self,num:int):
        if self.isPlaying:
            if self.currentFrame + num > self.video.duration:
                self.currentFrame = 0
                self.nextFrame = 0
            elif self.currentFrame + num < 0:
                self.currentFrame = 0
                self.nextFrame = 0
            else: 
                self.currentFrame += num
                self.nextFrame = self.currentFrame
            pg.mixer.music.pause()
            pg.mixer.music.play(0,self.currentFrame)
    def togglePlay(self,*_):
        
        if DM.existFile(self.vP) and DM.existFile(self.aP):
            
            if self.vP != self.lvP or self.aP != self.laP:
                self._loadData(self.vP,self.aP)
                self.lvP = self.vP 
                self.laP = self.aP
            self.isPlaying = not self.isPlaying
            self._play()
        else:
            print(f'video or Audio File dont exist [{self.aP}] [{self.vP}]')
    def _stop(self):
        self.isPlaying = False
        self.isLoaded = False
        self._play()
    def _play(self,*_):
        if self.isPlaying:
            if pg.mixer.music.get_busy():pg.mixer.music.stop()
            pg.mixer.music.play(0,self.currentFrame)
        elif not self.isPlaying:
            if pg.mixer.music.get_busy():pg.mixer.music.stop()
    def getTime(self):
            
        minutes = self.getDoubleZeros(int(self.currentFrame / 60))
        seconds = self.getDoubleZeros(int(self.currentFrame % 60))
        mminutes = self.getDoubleZeros(int(self.video.duration / 60))
        mseconds = self.getDoubleZeros(int(self.video.duration % 60))


        return f'{minutes}:{seconds}/{mminutes}:{mseconds}'
    def update(self):#! Change
        
        if not self.isPlaying: 
            
            return
        if not self.visible: return
        if not self.isLoaded: return
        if self.progressFullscreenBar.isPressed:
            mx = abs(pg.mouse.get_pos()[0] / 1280) if pg.mouse.get_pos()[0] > 0 else 0

            self.currentFrame = self.video.duration * (mx)
            pg.mixer.music.pause()
            pg.mixer.music.play(0,self.currentFrame)
        if self.progressBar.isPressed:
            mx = abs((self.getAbsPosition()[0]-pg.mouse.get_pos()[0]) / self.dest[0])
            

            self.currentFrame = self.video.duration * (mx)
            pg.mixer.music.pause()
            pg.mixer.music.play(0,self.currentFrame)
        if self.fullscreen:
            self.progressFullscreenBar.draw(self.currentFrame / self.video.duration)
        else:
            self.progressBar.draw(self.currentFrame / self.video.duration)
        
        
        
        if self.currentFrame <= self.video.duration:
            self.currentFrame += self.app.deltaTime
            if not pg.mixer.music.get_busy(): 
                pg.mixer.music.play(0,self.currentFrame)
            if self.currentFrame >= self.nextFrame:
                self.nextFrame = self.currentFrame + (1/SETTINGS._['videoPlaybackFps'])
                img = pg.pixelcopy.make_surface(numpy.flipud(numpy.rot90(self.video.get_frame(self.currentFrame),1)))
            else:
                img = self.surface.copy()
            self.timeLabel.UX.text = f'{self.getTime()}'
            self.timeLabel.setImage(self.timeLabel.UX.gen())
            if self.fullscreen:
                
                self.surface = pg.transform.scale(img,(1280,720))
                
                #self.surface.blit(FONTDRAW.draw(self.getTime(),True,size=50),(0,0))
                
            else:
                self.surface = pg.Surface(self.dest)
                if self.dest is not None: img = pg.transform.scale(img,self.dest)
                self.surface.blit(img,(0,0))
                #self.surface.blit(FONTDRAW.draw(self.getTime(),True,size=13),(0,0))
                self.surface.blit(self.UX.CUTOUT,(0,0))
                self.surface.set_colorkey((0,255,0))

        else:
            if pg.mixer.get_busy(): 
                pg.mixer.music.stop()
        super().update()

class UIWindowManager:
    def __init__(self) -> None:
        self.windowMoveId = -1
        self.windowBusy = False
    def checkId(self,id):
        return self.windowMoveId == id
UIWM = UIWindowManager()

class UIWindow(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        UIC.addElement('uiWindow')
        super().__init__(rect, **kwargs)
        self.UX = UXWindow(**UnpackManager('ux',kwargs,{}))
        self.setImage(self.UX.gen())
        self.lastMousePos = (0,0)
        self.drag = False
    def update(self):
        mX,mY = pg.mouse.get_pos()
        x,y = self.getAbsPosition()
        w,h = self.dest[0],24
        
        if self.drag:
            self.pos = (mX) - (self.UX.surface.get_width() // 2), mY - 12
            self.lastMousePos = mX,mY
        
        #! Sollte die Maus über der Bar liegen und gedrückt sein. Dann ist das Fenster beweglich.
        #? Aber nur falls nicht schon ein anderes Fenster UIWM belegt!
        if mX > x and mY > y and mX < x + w and mY < y + h and self.isPressed:
            #? Ist UIWM nicht beschäftigt mit einem anderen Fenster dann:
            if not UIWM.windowBusy:
                self.drag = True
                UIWM.windowBusy = True
                UIWM.windowMoveId = self.elementId
        else:
            #! Ist UIWM beschäftigt nicht mit diesem Element sondern einem anderem
            if not UIWM.checkId(self.elementId):
                self.drag = False
            else:
                self.drag = False
                UIWM.windowBusy = False
                UIWM.windowMoveId = -1
            
            
            
        
            
        
        
        
        super().update()
        
class UIDropDown(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs) -> None:
        super().__init__(rect, **kwargs)
        self.setImage(pg.Surface((1,1)))
        self.toggle = False
        self.motherInstanceButton = UIButton(rect,ux=UnpackManager('ux',kwargs,{}),onPressCallback=self.switch,layer=self.layer,parent=self.parent,group=self.group)
        self.childInstances = []
        ux = UnpackManager('ux',kwargs,{})
        rect.x = 0
        rect.y = 0
        self._callbacks = []
        for text,callback in UnpackManager('childsInstances',kwargs,[]):
            
            ux['text'] = text
            rect.y += 24
            UIB = UIButton(rect,ux=ux,onPressCallback=self.btnPress,parent=self,layer=self.layer,group=self.group)
            self.childInstances.append(UIB)
            self._callbacks.append((callback,UIB.elementId))
        for e in self.childInstances:
            
            e.visible = False
    def btnPress(self,*_):
       
        for callback,id in self._callbacks:
            if id == _[0].elementId:
                _[0].thisFramePressed = False
                callback(_[0])
                break
        self.toggle = False
        for e in self.childInstances:
           
            e.visible = self.toggle
    def switch(self,*_):
        self.toggle = not self.toggle
        for e in self.childInstances:
           
            e.visible = self.toggle

    def update(self):
        return super().update()

class UITextInput(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.addElement('uiTextInput')
        self.deufault_text = UnpackManager('default_text',kwargs,'Enter Text...')
        self.maxLetters = UnpackManager('maxLetters',kwargs,32)
        self.text = ''
        self.active = False
        self.mode = UnpackManager('mode',kwargs,False)
        self.count = 0
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
        self.enterButton = UIButton(rect,ux={'size':self.dest},onPressCallback=self.setActive,parent=self.parent,layer=self.layer+1,group=self.group)
        self.textLabel = UILabel(rect,ux={'size':self.dest},parent=self.parent,layer=self.layer+1,group=self.group)
        self.textLabel.UX.text = self.deufault_text
        self.textLabel.setImage(self.textLabel.UX.gen())
        self.delete = False
    def setI(self,text):
        self.textLabel.UX.text = text
        self.text = text
        self.textLabel.setImage(self.textLabel.UX.gen())
    def setActive(self,*_):
        self.active = not self.active
    def setText(self):
        """
        Check Pygame events for KEYDOWN Events and save them in self.text
        """
        if not self.enterButton.isHovered and pg.mouse.get_pressed()[0]:
            self.active = False
        CTRL = self.app.keyboardInputs['strg']
        pressedList = pg.key.get_pressed()
        if pressedList[pg.K_RETURN]:
            
            self.active = False
        if pressedList[pg.K_BACKSPACE] and not pressedList[pg.K_RETURN] and not self.delete:
            self.text = self.text[:-1]
            self.delete = True
        elif not pressedList[pg.K_BACKSPACE]:
            self.delete = False

            
        for key in self.app.keyboardInputs['currentKeys']:
            if not pressedList[pg.K_RETURN]:
                self.appChars(key)
        if self.text == '' and self.textLabel.UX.text != self.deufault_text:
            self.textLabel.UX.text = self.deufault_text
            self.textLabel.setImage(self.textLabel.UX.gen())
        if self.active:
            self.textLabel.UX.text = f'{self.getTextEx()}'
            self.textLabel.setImage(self.textLabel.UX.gen())
            
                    
        
    def appChars(self,char):
        self.text = str(self.text)
        if len(str(self.text)) < self.maxLetters:
            self.text += char
    def getText(self):
            """
                Get Text Raw
            """
            return '' if self.text is None else self.text
    def getTextEx(self):
        """
        Get Text with Blinker
        """
        return ('' if self.text is None else self.text )+ ('|' if int(self.count) % 2 == 0 else '')
    def update(self):
        self.count += self.app.deltaTime
        if self.active:
            self.setText()
            if self.mode == 'only_numbers':
                text = ''
                for i,char in enumerate(self.text):
                    if char.isdecimal() or (char == '-' and i == 0 ):
                        text += char
                self.text = text
            elif self.mode == 'only_pos_numbers':
                text = ''
                for char in self.text:
                    if char.isdecimal():
                        text += char
                self.text = text
            elif self.mode == 'float':
                text = ''
                spText = self.text.split('.')
                if spText.__len__() == 2:
                    if not spText[0].replace('-','').isdecimal():
                        
                        if not spText[1].isdecimal() and spText[1] != '':
                            
                            self.text = ''
        return super().update()

class UINotification(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        self.notificationButtonLabel = UILabel(rect,ux={'size':self.dest,'text':'','anchor': 'top_center'},group=self.group)
        self.messages = []
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
    def addNotification(self,text):
        self.messages.append(text)
    def update(self):
        
        r = ''
        for idx,msg in enumerate(self.messages):
            msg[1] -= .01 + self.app.deltaTime

            if msg[1] < 0:
                self.messages.pop(idx)
            else:
                r += f'{msg[0]}\n'
                
        
        self.notificationButtonLabel.UX.text = r
        self.notificationButtonLabel.setImage(self.notificationButtonLabel.UX.gen())
            
        return super().update()

class UIColorPicker(UIElement):
    #3 Slider RGB
    def __init__(self, rect: pg.Rect, **kwargs) -> None:
        super().__init__(rect, **kwargs)
        UIC.addElement('uiColorPicker')
        
        self.preview = UIImage(pg.Rect(0,24,64,40),parent=self,layer=self.layer+1,group=self.group)
        self.sliderR = UISliderLR(pg.Rect(0,64,64,24),parent=self,layer=self.layer+1,group=self.group)
        self.sliderG = UISliderLR(pg.Rect(0,88,64,24),parent=self,layer=self.layer+1,group=self.group)
        self.sliderB = UISliderLR(pg.Rect(0,112,64,24),parent=self,layer=self.layer+1,group=self.group)
        _ = pg.Surface((64,64))
        _.fill((0,0,0))
        self.preview.setImage(_)
    def update(self):
        pg.Color(int(self.sliderR.sliderPercent * 255),int(self.sliderG.sliderPercent * 255),int(self.sliderB.sliderPercent * 255))
        
        _ =  self.preview.getImage()
        _.fill(pg.Color(int(self.sliderR.sliderPercent * 255),int(self.sliderG.sliderPercent * 255),int(self.sliderB.sliderPercent * 255)))
       
        self.preview.setImage(_)
        return super().update()
class UINode(UIElement): #+ 1.9
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        _inputs,_outputs = UnpackManager('values',kwargs,[[],[]])
        self._inputLabel = []
        self._outputLabel = []
        self.window = UIWindow(pg.Rect(*self.pos,256,(_inputs.__len__() * 24) + (_outputs.__len__() * 24) + 48),layer=self.layer,ux={'size': (256,(_inputs.__len__() * 24) + (_outputs.__len__() * 24) + 48),'text': ''})
        y = 24
        for name,var in _inputs:
            
            self._inputLabel.append(UILabel(pg.Rect(0,y,128,24),ux={'text': name,'size': (128,24)},layer=self.layer,parent=self.window))
            y += 24
        for key in _outputs:
            self._outputLabel.append(UILabel(pg.Rect(128,y,128,24),ux={'text': key,'size': (128,24)},layer=self.layer,parent=self.window))
            y += 24
        self.idLabel = UILabel(pg.Rect(64,y,128,24),ux={'text': str(self.elementId),'size': (128,24)},layer=self.layer,parent=self.window)
        """
        Colors:
        
        #f23262     Image
        #323262     Mask
        
        #f26232     String
        #32f262     Integer
        #320262     Boolean
        #f2f262     Float
        
        #3262f2     Tuple
        #f262f2     List
        #32f2f2     Dict
        
        #f2f2f2     All
        """
class UIPagination(UIElement):#[1] ... [2,3,4,5,6] ... [43] #+ 1.9
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)

class UILoadingCone(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.addElement('uiBackgroundWobble')
        #16 Iterations
        #Async
        self.isLoading = False
        #get events
        self.UX = UXLoadingCone()
        self.minPrio = 0
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
        self.ATread = None
    
    def start(self,info:str='',prio:int=0):
        
        if self.ATread is None:
            self.loadingText = info
            self.ATread = Thread(target=self.asyncUpdate)
            self.isLoading = True
            self.ATread.start()
            self.minPrio = prio
    def _stop(self,priority:int=0):
        if priority >= self.minPrio:
            
            self.isLoading = False
            if self.ATread is not None:
                while self.ATread.is_alive():
                    pass
        self.ATread = None
    def setInfo(self,info:str):
        self.loadingText = info
    def asyncUpdate(self):
        _finTime = time() + .25
        _currentFrame = 0
        while self.isLoading:
            if _finTime <= time():
                _finTime = time() + .25
                _currentFrame += 1
                if _currentFrame > 3:
                    _currentFrame = 0
                self.app.window.fill(pg.Color('#242424'))
                self.app.window.blit(self.UX.animationFrames[_currentFrame],(640-256,360-256))
                _info = FONTDRAW.draw(self.loadingText,size=80)
                w2,h2 = _info.get_size()
                w2,h2 = w2//2,h2//2
                self.app.window.blit(_info,(640-w2,360-h2))
                
                [e for e in pg.event.get() if e.type == pg.QUIT]
                pg.display.update()
    def update(self):
        
        return super().update()


class UIBackgroundWobble(UIElement):
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        UIC.addElement('uiBackgroundWobble')
        if 'app' in kwargs:
            self.app = kwargs['app']
        else:
            raise Exception('No App. No Game!')
        self.UX = UXBackgroundWobble(**UnpackManager('ux',kwargs,{}))
    def updateBeforeAll(self):
        x,y = pg.mouse.get_pos()
        x,y = x - (self.UX.element.get_width()//2),y - (self.UX.element.get_height()//2)
        self.app.window.blit(self.UX.element,(x,y)) 
    def update(self):
        
        return super().update()

class UISliderLR(UIElement):#Todo
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        #self.btnLeft = UIButton(pg.Rect(0,0,24,24),ux={'text': '<','size': (24,24)},parent=self)
        self.setImage(pg.Surface((rect.w,rect.h)))
        self.surface.fill(pg.Color('#242424'))
        pg.draw.line(self.surface,(128,0,0),(0,0),(0,24),3)
        #self.btnRight = UIButton(pg.Rect(rect.w-24,0,24,24),ux={'text': '>','size': (24,24)},parent=self)
        self.sliderPercent = UnpackManager('percent',kwargs,0)
        #pg.draw.line(self.surface,(128,0,0),(mp,0),(mp,24),3)
    def update(self):
        if self.isPressed:
            mp = pg.mouse.get_pos()[0]

            if mp > self.dest[0]:
                mp = self.dest[0]
            if mp < self.pos[0]:
                mp = self.pos[0]
            mx = abs((self.getAbsPosition()[0]-mp) / self.dest[0])   #Calculates the value bet, 0-1

            self.surface.fill(pg.Color('#242424'))
            
            pg.draw.line(self.surface,(128,0,0),(mp,0),(mp,24),3)
            self.sliderPercent = mx
            
        #mx = abs(pg.mouse.get_pos()[0] / 1280) if pg.mouse.get_pos()[0] > 0 else 0
        return super().update()
class UITree(UIElement): #Todo: FileManager File Show
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        
class UISelection(UIElement): #Todo: FileManager File Selection
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        
class UISearchBar(UIElement): #Todo: FileManager Search
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        
class UILoaderAnimated(UIElement): #Todo: LoadingScreen
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)


 
class UICheckBox(UIElement): #Todo: Settings
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        
class UIRadioButton(UIElement): #Todo: Settings
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)

class UISideBar(UIElement): #+ 1.9
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)

class UITabBar(UIElement): #!      Currently not being useful
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        
class UIBreadCrump(UIElement):#!      Currently not being useful
    #Main>Second>Third>Current + 1.9
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)

class UIStepper(UIElement):#!      Currently not being useful
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)
        
class UIAccordion(UIElement):#!      Currently not being useful
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)

class UISliderTwoSided(UIElement):#!      Currently not being useful
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)

class UITable(UIElement):#!      Currently not being useful
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)

class UIPopUp(UIElement):#!      Currently not being useful
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)

class UIScrollingContainer(UIElement): #!      Currently not being useful
    def __init__(self, rect: pg.Rect, **kwargs):
        super().__init__(rect, **kwargs)