from tkinter import filedialog
fName = filedialog.askopenfilename()
from json import dumps,load
import pygame
SURF = pygame.image.load(fName)



class TupleImage:
    def __init__(self,var):
        SURF = pygame.Surface((len(var),len(var[-1])),pygame.SRCALPHA)
        for x in range(len(var)):
            for y in range(len(var[-1])):
                if var[x][y][3] == 0: continue
                SURF.set_at((x,y),var[x][y])
        self.surf = SURF

data = []
for x in range(SURF.get_width()):
    data.append([])
    for y in range(SURF.get_height()):
        PIXEL = SURF.get_at((x,y))
        data[-1].append((PIXEL.r,PIXEL.g,PIXEL.b,PIXEL.a))



with open('test.txt','w') as f:
    f.write(dumps(data))
