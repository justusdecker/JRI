from bin.dataManagement import DM,UnpackManager
from pygame import image,Surface,transform,SRCALPHA,Color

from pygame.surfarray import make_surface
from pygame.transform import scale, flip, rotate, scale_by
from pygame.font import Font

from moviepy.video.io.VideoFileClip import VideoFileClip
from random import random as rnd,randint as rint
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
                frame = rnd()*(self.video_src.duration)
            
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
        
        # timg is used to outline text
        
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
    
    def save_image(self,file_name: str,folder: str,surface:Surface) -> None:

        DM.createFolder(folder)
        
        image.save(surface,file_name)
        
    def create_thumbnail(self,
                        episode_number:int,
                        video_path: str | None,
                        frame: int,
                        tad:dict, # Thumbnail Automation Data
                        title:str,
                        over_image: Surface | None = None):
        """
        Call this function to get a new thumbnail from a video!
        
        
        .. p::
            position
        .. rp_x::
            random_x_position
        .. rp_y::
            random_y_position
        .. rr::
            random_rotation
        """
        epnum = tad['text_epNum']
        
        if not DM.existFile(epnum['font']):
            epnum['font'] = "C:\\Windows\\Fonts\\Arial.ttf"
            print('File Not existing')
        #Try get C:\\Windows\\Fonts\\Bahnschrift.ttf
        if over_image is not None: 
            
            self.save_image(f'{self.get_path(title)}\\{episode_number}_{title}_Thumbnail.png',
                       self.get_path(title),
                       over_image
                       )
            
            return over_image
        
        if episode_number == str(episode_number):
            
            self.text = str(episode_number)
            
            return self.surface
        
        THUMBNAIL = Surface(self.default_size)
        
        if video_path is None: 
            #! Video Path does not exist so fill Background
            THUMBNAIL.fill(Color('#535353'))
            
        else:

            self.render_background()
        
        self.render_images(tad['images'],THUMBNAIL)
        
        _textSurface: Surface = self.get_text(
            epnum['font'],
            epnum['size'],
            str(episode_number),epnum['outline'],
            (255,255,255) if not 'color' in epnum else epnum['color']
            )
        
        _textSurface: Surface = transform.rotate(_textSurface,epnum['rot'])
        
        textX = int(epnum['pos'][0] - (_textSurface.get_width() *.5))
        
        textY = int(epnum['pos'][1] - (_textSurface.get_height() *.5))
        
        THUMBNAIL.blit(_textSurface,(textX,textY))
        
        DM.createFolder(self.get_path(title))
        
        self.save_image(f'{self.get_path(title)}\\{episode_number}_{title}_Thumbnail.png',
                       self.get_path(title),
                       THUMBNAIL
                       )
        #LOG all values
        self.surface = THUMBNAIL
        
        return self.surface
    def get_path(self, title: str) -> str:
        return f"{THUMBNAIL_PATH}{title}"
    def get_rnd_pos(self,rp_x,rp_y) -> tuple:
        
        if rp_x < 0:
                    
            rp_x = rint(rp_x,0)
            
        elif rp_x > 0:
            
            rp_x = rint(0,rp_x)
            
        if rp_y < 0:
            
            rp_y = rint(rp_y,0)
            
        elif rp_y > 0:
            
            rp_y = rint(0,rp_y)

        return rp_x, rp_y
    def render_images(self,images: list,thumbnail: Surface):
        for entry in images:
            
            if not DM.existFile(entry['path']):
                
                continue
            
            surf : Surface = image.load(entry['path'])
            
            surf : Surface = scale(surf,self.default_size)
            
            surf : Surface = scale_by(surf,entry['scale'])
            
            surf : Surface = rotate(surf,entry['rot'])
            
            surf : Surface = IVFX.cropping(*entry['cropping'],surf)
            
            x = int(entry['pos'][0] - (surf.get_width() *.5))
            
            y = int(entry['pos'][1] - (surf.get_height() *.5))
            
            thumbnail.blit(surf,(x,y))
    def render_background(self,
                          tad,
                          video_path,
                          frame,
                          thumbnail: Surface):
        surf = self.get_src_image(video_path,frame)
            
        p: tuple[int,int] = (0,0)
        
        
        if 'background' in tad:
            
            bg_data: dict = tad['background']

            center: bool = bg_data.get('center', False)

            p: tuple[int,int] = bg_data.get('position', (0,0))
            
            rp_x: int = bg_data.get('randomPositionX', 0)
            
            rp_y: int = bg_data.get('randomPositionY', 0)
            
            rp_x, rp_y = self.get_rnd_pos(rp_x,rp_y)
            
            p: tuple[int,int] = p[0] + rp_x , p[1] + rp_y
            
            rr: tuple[int,int] = bg_data.get('randomRotation', (0,0))
            
            if rint(0,1) == 1:
                
                rr: float = rnd() * rr[1]
                
            else:
                
                rr: float = rnd() * rr[0]
            
            r: float | int = bg_data.get('rotation', 0) + rr
            
            s: float = bg_data.get('scale', 0)
            
            rs: int = bg_data.get('randomScale', 0)
            
            if rint(0,1) == 1:
                
                rs: float = rnd() * rs[1]
                
            else:
                
                rs: float = rnd() * rs[0]
            
            if rs != 0:#? The Random Values are 0 so dont add data
                s = s + rs
            
            hue = UnpackManager('hue',bg_data,0)
            
            saturation = UnpackManager('saturation',bg_data,1)
            
            lightness = UnpackManager('lightness',bg_data,1)
            
            w,h = surf.get_size()
            
            w,h = int(w*s),int(h*s)
            
            surf = scale(surf,(w,h))
            
            surf = rotate(surf,r)
            
            
            
            if hue != 0 and saturation != 1 and lightness != 1:
                surf = IFXHSVManipulation(thumbnail,hue,saturation,lightness)

            if center:
                
                w , h = surf.get_size()
                
                w , h = w * .5, h * .5
                
                x , y = self.default_size[0] * .5 , self.default_size[1] * .5
                
                p = x - w , y - h
                
            thumbnail.blit(surf,p)
                
        else:
            
            thumbnail.blit(surf,p)