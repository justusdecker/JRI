from bin.dataManagement import DM,UnpackManager
from pygame import image,Surface,transform,SRCALPHA,Color

from pygame.surfarray import make_surface
from pygame.transform import scale, flip
from pygame.font import Font

from moviepy.video.io.VideoFileClip import VideoFileClip
from random import random,randint
from numpy import rot90
from bin.fx.image import IFXHSVManipulation,outLining
from bin.fx.video import IVFX
from bin.constants import THUMBNAIL_PATH
class ThumbnailGenerator:
    
    default_size: tuple = (1280,720)
    
    def __init__(self):
        
        self.font_path = ''
        
        self.text = ''
        
        self.surface = None
        
        self.font = None
        
        self.idx = 0
        
        self.video_path = ''
        
        self.video_src = None
        
        self.font_size = -1
        
    def get_src_image(self, 
                      file: str, 
                      frame: float | int = -1
                      ): # should not be none!
        """
        Get a frame from a video
        -----
        
        .. file::
            - Must be a string
            - Can be a relative or absolut path
        .. frame::
            - Must be numeric
            - ``frame`` can be -1 or from ``0`` to ``video length``.
            - Possible crashed if ``frame`` > ``video length ``
        
        **ATTENTION**
            ``video_src`` will only be updated if the ``file`` path changes

        """
        
        # What happens here?
        #Creates a new Surface from a videoframe.
        # At first get a numpy like object from VideoFileClip.get
        # The result must be rotated to show up correctly
        # Then a Surface will be created, scaled & flipped at the x axis.
        
        if DM.existFile(file):
            
            if self.video_path != file: 
                # Create a new Video Source to get images from
                self.video_src = VideoFileClip(file,audio=False)

            if frame == -1: 
                # Frame is not valid so take a random value from 0 to video.duration
                frame = random()*(self.video_src.duration)
            
            # Sets the index for the last image. Use: Pick the last Thumbnail
            self.idx = frame if frame >= 0 and frame  <= self.video_src.duration else 0 

            _returnImage: Surface = make_surface(rot90(self.video_src.get_frame(self.idx)))
            _returnImage: Surface = scale(_returnImage,self.default_size)
            _returnImage: Surface = flip(_returnImage,True,False)
            
            return _returnImage
        
    def get_text(self,
                 font_path: str,
                 font_size: int,
                 text: str,
                 outline: dict,
                 color=(255,255,255)
                 ) -> Surface:
        """
        Returns the Text Image
        """

        if self.font_path != font_path or self.font_size != font_path:
            
            self.font = Font(font_path,font_size)
            
            self.font_path, self.font_size = font_path, font_size
        
        img: Surface = self.font.render(text,False,color)
        
        w1,h1 = img.get_size()
        
        timg = Surface((w1 * 1.05,h1 * 1.05),SRCALPHA)
        
        w2,h2 = timg.get_size()
        
        x = (w2 / 2) - (w1 / 2)
        
        y = (h2 / 2) - (h1 / 2)
        
        timg.blit(img,(x,y))
        
        timg = outLining(
            outline['xMinus'],
            outline['xPlus'],
            outline['yMinus'],
            outline['yPlus'],
            timg,outline['color']
            )
        
        return timg
    
    def save_image(self,fileName: str,folderPath,surface:Surface):
        #FAILSAFE If not saveable!
        DM.createFolder(folderPath)
        
        image.save(surface,fileName)
        
    def createThumbnail(self,
                        episodeNumber:int,
                        videoPath: str | None,
                        frame: int,
                        tad:dict, # Thumbnail Automation Data
                        episodeTitle:str,
                        overImage: Surface | None = None):
        if not DM.existFile(tad['text_epNum']['font']):
            tad['text_epNum']['font'] = "C:\\Windows\\Fonts\\Arial.ttf"
            print('File Not existing')
        #Try get C:\\Windows\\Fonts\\Bahnschrift.ttf
        if overImage is not None: 
            
            self.save_image(f'{THUMBNAIL_PATH}{episodeTitle}\\{episodeNumber}_{episodeTitle}_Thumbnail.png',
                       f'{THUMBNAIL_PATH}{episodeTitle}',
                       overImage
                       )
            
            return overImage
        
        if episodeNumber == str(episodeNumber):
            
            self.text = str(episodeNumber)
            
            return self.surface
        
        THUMBNAIL = Surface(self.default_size)
        
        if videoPath is None: #! Video Path does not exist so fill Background
            
            THUMBNAIL.fill(Color('#535353'))
            
        else:
            
            _surface = self.get_src_image(videoPath,frame)
            
            position: tuple[int,int] = (0,0)
            
            
            if 'background' in tad:
                
                backgroundData = tad['background']

                center: bool = UnpackManager('center',backgroundData,False)

                position: tuple[int,int] = UnpackManager('position',backgroundData,(0,0))
                
                randomPositionX: int = UnpackManager('randomPositionX',backgroundData,0)
                
                randomPositionY: int = UnpackManager('randomPositionY',backgroundData,0)
                
                if randomPositionX < 0:
                    
                    randomPositionX = randint(randomPositionX,0)
                    
                elif randomPositionX > 0:
                    
                    randomPositionX = randint(0,randomPositionX)
                    
                if randomPositionY < 0:
                    
                    randomPositionY = randint(randomPositionY,0)
                    
                elif randomPositionY > 0:
                    
                    randomPositionY = randint(0,randomPositionY)
                
                position: tuple[int,int] = position[0] + randomPositionX , position[1] + randomPositionY
                
                randomRotation: tuple[int,int] = UnpackManager('randomRotation',backgroundData,[0,0])
                
                if randint(0,1) == 1:
                    
                    randomRotation: float = random() * randomRotation[1]
                    
                else:
                    
                    randomRotation: float = random() * randomRotation[0]
                
                rotation: float | int = UnpackManager('rotation',backgroundData,0) + randomRotation
                
                scale: float = UnpackManager('scale',backgroundData,0)
                
                randomScale: int = UnpackManager('randomScale',backgroundData,0)
                
                if randint(0,1) == 1:
                    
                    randomScale: float = random() * randomScale[1]
                    
                else:
                    
                    randomScale: float = random() * randomScale[0]
                
                if randomScale != 0:#? The Random Values are 0 so dont add data
                    scale = scale + randomScale
                
                hue = UnpackManager('hue',backgroundData,0)
                
                saturation = UnpackManager('saturation',backgroundData,1)
                
                lightness = UnpackManager('lightness',backgroundData,1)
                
                w,h = _surface.get_size()
                
                w,h = int(w*scale),int(h*scale)
                
                _surface = transform.scale(_surface,(w,h))
                
                _surface = transform.rotate(_surface,rotation)
                
                
                
                if hue != 0 and saturation != 1 and lightness != 1:
                    _surface = IFXHSVManipulation(THUMBNAIL,hue,saturation,lightness)

                if center:
                    
                    w , h = _surface.get_size()
                    
                    w , h = w * .5, h * .5
                    
                    x , y = self.default_size[0] * .5 , self.default_size[1] * .5
                    
                    position = x - w , y - h
                    
                THUMBNAIL.blit(_surface,position)
                    
            else:
                
                THUMBNAIL.blit(_surface,position)
        
        for entry in tad['images']:
            
            if not DM.existFile(entry['path']):
                
                continue
            
            _surface : Surface = image.load(entry['path'])
            
            _surface : Surface = transform.scale(_surface,self.default_size)
            
            _surface : Surface = transform.scale_by(_surface,entry['scale'])
            
            _surface : Surface = transform.rotate(_surface,entry['rot'])
            
            _surface : Surface = IVFX.cropping(*entry['cropping'],_surface)
            
            x = int(entry['pos'][0] - (_surface.get_width() *.5))
            
            y = int(entry['pos'][1] - (_surface.get_height() *.5))
            
            THUMBNAIL.blit(_surface,(x,y))
        
        _textSurface: Surface = self.get_text(
            tad['text_epNum']['font'],
            tad['text_epNum']['size'],
            str(episodeNumber),tad['text_epNum']['outline'],
            (255,255,255) if not 'color' in tad['text_epNum'] else tad['text_epNum']['color']
            )
        
        _textSurface: Surface = transform.rotate(_textSurface,tad['text_epNum']['rot'])
        
        textX = int(tad['text_epNum']['pos'][0] - (_textSurface.get_width() *.5))
        
        textY = int(tad['text_epNum']['pos'][1] - (_textSurface.get_height() *.5))
        
        THUMBNAIL.blit(_textSurface,(textX,textY))
        DM.createFolder(f"{THUMBNAIL_PATH}{episodeTitle}")
        self.save_image(f'{THUMBNAIL_PATH}{episodeTitle}\\{episodeNumber}_{episodeTitle}_Thumbnail.png',
                       f'{THUMBNAIL_PATH}{episodeTitle}',
                       THUMBNAIL
                       )
        #LOG all values
        self.surface = THUMBNAIL
        
        return self.surface
    