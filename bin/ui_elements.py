import pygame as pg
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