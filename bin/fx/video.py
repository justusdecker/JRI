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

    
