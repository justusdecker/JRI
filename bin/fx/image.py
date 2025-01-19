import pygame as pg

from colorsys import hsv_to_rgb
from random import randint,random
from pygame import Surface,SRCALPHA,mask,Color
class TupleImage:
    def __init__(self,var):
        
        SURF = Surface((len(var),len(var[-1])),SRCALPHA)
        
        for x in range(len(var)):
            
            for y in range(len(var[-1])):
                
                if var[x][y][3] == 0: continue
                
                SURF.set_at((x,y),var[x][y])
                
        self.surf = SURF
        
def generateIcon(var):#- Outsource
    
    SURF = Surface((len(var),len(var[-1])),SRCALPHA)
    
    for x in range(len(var)):
        
        for y in range(len(var[-1])):
            
            if var[x][y][3] == 0: continue
            
            SURF.set_at((x,y),var[x][y])
            
    return SURF

def loadImage(filePath:str) -> list[pg.Surface , int , int, tuple , int]:
    """
    The Classic Loading System of an Image
    """
    
    IMAGE = pg.image.load(filePath)
    
    return IMAGE , IMAGE.get_width() , IMAGE.get_height() , IMAGE.get_blendmode() , IMAGE.get_size()

def IFXLightness(surface:pg.Surface,multiplicator:float) -> pg.Surface:
    
    for x in range(surface.get_width()):#O(n2*3)
        
        for y in range(surface.get_height()):
            
            pixel = (surface.get_at((x,y)).r,surface.get_at((x,y)).g,surface.get_at((x,y)).b)
            
            _p = []
            
            for value in pixel:
                
                value *= multiplicator
                
                value = int(value) if value < 255 else 255
                
                _p.append(value)
                
            alpha = 255 if pixel.__len__() == 3 else surface.get_at((x,y)).a

            surface.set_at((x,y),pg.Color(*_p,alpha))
                
    return surface

def IFXGrayScale(surface:pg.Surface) -> pg.Surface:
    
    for x in range(surface.get_width()):#O(n2*3)
        
        for y in range(surface.get_height()):
            
            pixel = (surface.get_at((x,y)).r,surface.get_at((x,y)).g,surface.get_at((x,y)).b)
            
            _p = (sum(pixel) / 3) if sum(pixel) != 0 else 0
            
            _p = int(_p) if _p < 255 else 255
            
            pixel = tuple([_p for i in range(3)])
            
            alpha = 255 if pixel.__len__() == 3 else surface.get_at((x,y)).a

            surface.set_at((x,y),pg.Color(*pixel,alpha))
            
    return surface

def getHexColor(col:int):
    if col < 10:
        
        col = '0' + hex(col).split('0x')[1]
        
    else:
        
        col = hex(col).split('0x')[1]
        
    return col

def IFXShiftManipulation(surface:pg.Surface,hue:int) -> pg.Surface:
    
    for x in range(surface.get_width()):#O(n2*3)
        
        for y in range(surface.get_height()):
            
            _hx = int('0x' + getHexColor(surface.get_at((x,y)).r) + getHexColor(surface.get_at((x,y)).g) + getHexColor(surface.get_at((x,y)).b),16)
            
            _hx += hue
            
            _hx = int(_hx % 16777215)
            
            _t = '#' + hex(_hx).split('0x')[1]
            
            _t = _t + ((7 - _t.__len__())*'0')

            surface.set_at((x,y),pg.Color(_t))
                
    return surface

def IFXHSVManipulation(surface:pg.Surface,hue:float,saturation:float,value:float) -> pg.Surface:#! BIG PROBLEM
    _oS = pg.Surface(surface.get_size())
    for x in range(surface.get_width()):#O(n2*3)
        for y in range(surface.get_height()):
            h,s,v,a = surface.get_at((x,y)).hsva
            s = (s*saturation) / 100
            v = (v*value) / 100
            h = abs((hue + h) % 360) / 360
            rgb = hsv_to_rgb(h,s,v)
            r,g,b = rgb
            r,g,b = r * 255,g*255,b*255
            rgb = r,g,b
            _oS.set_at((x,y),rgb)

                
    return _oS

def IFXDistortion(surface:pg.Surface,hue:float) -> pg.Surface:
    for x in range(surface.get_width()):#O(n2*3)
        for y in range(surface.get_height()):
            h,s,v,a = surface.get_at((x,y)).hsva
            
            r,g,b = hsv_to_rgb(h,s,v)
            _hx = int('0x' + getHexColor(int(r)) + getHexColor(int(g)) + getHexColor(int(b)),16)


            _hx = int(_hx % 16777215)
            _t = '#' + hex(_hx).split('0x')[1]
            _t = _t + ((7 - _t.__len__())*'0')

            surface.set_at((x,y),pg.Color(_t))
                
    return surface

def IFXRGBManipulation(surface:pg.Surface,rm:float,gm:float,bm:float) -> pg.Surface:
    for x in range(surface.get_width()):#O(n2*3)
        for y in range(surface.get_height()):
            r,g,b,a = (surface.get_at((x,y)).r,surface.get_at((x,y)).g,surface.get_at((x,y)).b,surface.get_at((x,y)).a)
            r,g,b = int(r*rm) % 255,int(g*gm) % 255,int(b*bm) % 255
            

            surface.set_at((x,y),pg.Color(r,g,b,a))
                
    return surface

def Map2Surface(nMap:list):
    w,h = nMap.__len__(),nMap[0].__len__()
    surf = pg.Surface((w,h))
    for x in range(w):
        for y in range(h):
            col = (255 * nMap[x][y])
            if col > 255:
                col = 255
            surf.set_at((x,y),(col,col,col))
    return surf

def Pluck(nMap:list,m:float):
    w,h = nMap.__len__(),nMap[0].__len__()
    for x in range(w):
        for y in range(h):
            nMap[x][y] = (nMap[x][y] * (random() * m) ) % 1
    return nMap
def NoiseMap(size: tuple[int,int],iterations=15000) -> tuple[tuple]:
    comb = size[0]*size[1]
    _ret = '0' * (comb)
    _ret = list(_ret)
    for i in range(iterations):
        _ret[randint(0,comb)] = "1"
    return _ret
    

def outLining(xMinus:int,
                xPlus:int,
                yMinus:int,
                yPlus:int,
                image:Surface,
                color:list | tuple = ((1,1,1),(1,1,1),(1,1,1),(1,1,1))):
        """
        Outlines an Image
        """
        shade = mask.from_surface(image).to_surface()
        shade.set_colorkey((0,0,0))
        imgL = []
        for i in range(4):
            normal = Surface(image.get_size(),SRCALPHA)

            for x in range(shade.get_width()):
                for y in range(shade.get_height()):
                    if shade.get_at((x,y)) != Color(0,0,0,255):
                        normal.set_at((x,y),color[i])
            imgL.append(normal)   
        surface = Surface(image.get_size(),SRCALPHA)
        surface.blit(imgL[0],(-abs(xMinus),0))
        surface.blit(imgL[1],(abs(xPlus),0))
        surface.blit(imgL[2],(0,-abs(yMinus)))
        surface.blit(imgL[3],(0,abs(yPlus)))
        surface.blit(image,(0,0))
        return surface