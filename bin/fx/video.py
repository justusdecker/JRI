from moviepy.video.io.VideoFileClip import VideoFileClip
from os.path import isfile
from pygame import Surface,SRCALPHA

def checkLengthWithTolerance(vid:float,aud:float,tol:float =0.04):
    "Vergleicht Audio und Video Länge mit gewisser Toleranz da selten gleich!"
    return aud < vid + tol and aud > vid - tol

class IVFX:
    """
    A Collection of Image & Video FX Effects
    """
    def _getVideoLength(filename):
        if isfile(filename):
            return VideoFileClip(filename).duration
        return -1
    def manipulateColors(size,mul,rgb):
        """
        multiplies every pixel times mul
        Its like gamma!
        """
        for x in range(size[0]):
            for y in range(size[1]):
                
                if rgb[x][y] == 0 or rgb[x][y] == 255: continue
                rgba = tuple(
                    
                        hex(
                            int((int
                            (str
                            (hex
                            (rgb[x][y])
                            )[i+2:i+4], 16) * mul) % 256)).split('0x')[1]
                        for i in (0, 2, 4, 6)
                    )
                rgb[x][y] = int('0x' + ''.join(rgba),16)
        return rgb

    def cropping(xMinus:int,
                xPlus:int,
                yMinus:int,
                yPlus:int,
                image:Surface):
        """
        cropps an image to size
        """
        normal = Surface(
            (
                image.get_width()-abs(xPlus),
                image.get_height()-abs(yPlus)
                ),
            SRCALPHA
            )
        normal.blit(
            image,
            (
                -abs(xMinus),
                -abs(yMinus)
                )
            )
        return normal

    
