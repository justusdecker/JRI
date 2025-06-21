import pygame as pg

from colorsys import hsv_to_rgb
from random import randint,random
from pygame import Surface,SRCALPHA,mask,Color



def getHexColor(col:int):
    if col < 10:
        
        col = '0' + hex(col).split('0x')[1]
        
    else:
        
        col = hex(col).split('0x')[1]
        
    return col

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