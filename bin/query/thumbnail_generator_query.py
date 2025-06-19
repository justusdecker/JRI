from bin.minfuncs import isnumeric
class ThumbnailGeneratorQuery:
    """
    
    A Wrapper to get a bunch of values without a BIG HEADACHE because some elements don't exist!
    
    Mapper
    *****
    
    Lets Play
    -----
    .. lp::
        `str` Lets Play Hash
        
        *lp

    Text / Font
    -----
    .. px::
        `int` Position X
        
        *text_pos_x
    .. py::
        `int` Position Y
        
        *text_pos_y
    .. text_font::
        `str` Font Path
        
        *font
    .. text_align::
        `str` Alignment **center, left, right**
        
        *text_align
    .. font_s::
        `int` The Font size
        
        *font_size
    .. text_r::
        `float` The Font rotation
        
        *text_rotation
    
    Logo
    -----
    .. logo_path:
        `str` Defines the location of the logo image
        
        *logo_path
    .. logo_r::
        `float` The Logo rotation
        
        *logo_rot
    .. logo_s::
        `float` The Logo scale
        
        *logo_scale
    .. logo_x::
        `int` The Logo position X
        
        *logo_pos_x
    .. logo_y::
        `int` The Logo position Y
        
        *logo_pos_y
    .. logo_align::
        `str` Alignment **center, left, right**
        
        *logo_align
    
    Background
    -----
    .. p_x::
        `int` position X
        
        *bg_pos_x
    .. p_y::
        `int` position Y
        
        *bg_pos_y

    .. rp_x::
        `int` random position X
        
        *bg_rpos_x
    .. rp_y::
        `int` random position Y
        
        *bg_rpos_y

    .. r::
        `float` rotation
        
        *bg_rot
    .. rr_x::
        `float` random rotation
        
        *bg_rrot_x
    .. rr_y::
        `float` random rotation
        
        *bg_rrot_y

    .. s::
        `float` scale
        
        *bg_scale
    .. rs_x::
        `float` random scale
        
        *bg_rscale_x
    .. rs_y::
        `float` random scale
        
        *bg_rscale_y
    
    .. hue::
        `float` the hue value of each pixel manipulation in the image
        
        *hue
    .. sat::
        `float` the saturation value of each pixel manipulation in the image
        
        *sat
    .. lig::
        `float` the lightness value of each pixel manipulation in the image
        
        *lig

    .. background::
     `str` Defines the location of the background image(If not set the image will be fetched out of the video!)
     
        *bg
    """
    def __init__(self,query: str):
        self.query = {}
        for arg in query.split('&'):
            v = arg.split('=')
            if len(v) == 2:
                self.query[v[0]] = v[1]
    
    def asdict(self) -> dict:
        """
        Format the query into [LPF - TAD] like
        """
        return {
            "tad": {
                "text": {
                    "font": self.font,
                    "align": self.text_align,
                    "size": self.font_size,
                    "pos": [self.text_pos_x,self.text_pos_y],
                    "rot": self.text_rotation,
                    "cropping": [0,0,0,0],
                    "outline": {
                        "xMinus": 2,
                        "xPlus": 2,
                        "yMinus": 2,
                        "yPlus": 2,
                        "color": [
                            [50,50,50],
                            [14,14,14],
                            [14,14,14],
                            [50,50,50]
                        ]
                    }
                },
                "images": {
                    "path": self.logo_path,
                    "scale": self.logo_scale,
                    "pos": [self.logo_pos_x, self.logo_pos_y],
                    "rot": self.logo_rot,
                    "align": self.logo_align,
                    "cropping": [0,0,0,0]
                    },
                "background": {
                    "position": [self.bg_pos_x,self.bg_pos_y],
                    "random_position": [self.bg_rpos_x, self.bg_rpos_y],
                    "rotation": self.bg_rot,
                    "random_rotation": [self.bg_rrot_x,self.bg_rrot_y],
                    "random_scale": [self.bg_rscale_x,self.bg_rscale_y],
                    "scale": self.bg_scale,
                    "hue": self.hue,
                    "sat": self.sat,
                    "lig": self.lig,
                    "background": self.bg
                }
                    
                
            }
        }
    # LP
    
    @property
    def lp(self) -> str:
        return self.query.get('lp', '')
    
    # TEXT
         
    @property
    def __tr(self) -> str:
        return self.query.get('font_s', '')
    @property
    def text_rotation(self) -> float:
        return self.__tr if isnumeric(self.__tr) else 13
    @property
    def font(self) -> str:
        return self.query.get('text_font', '')
    @property
    def text_align(self) -> str:
        return self.query.get('text_align', 'center')
    @property
    def __text_px(self) -> str:
        return self.query.get('px', '')
    @property
    def __fs(self) -> str:
        return self.query.get('font_s', '')
    @property
    def font_size(self) -> int:
        return self.__fs if self.__fs.isdecimal() else 13
    @property
    def text_pos_x(self) -> int:
        return self.__text_px if self.__text_px.isdecimal() else 0
    @property
    def __text_py(self) -> str:
        return self.query.get('py', '')
    @property
    def text_pos_y(self) -> int:
        return self.__text_py if self.__text_py.isdecimal() else 0
    
    # LOGO
    
    @property
    def logo_path(self) -> str:
        return self.query.get('logo_path', '')
    @property
    def __logo_r(self) -> str:
        return self.query.get('logo_r', '')
    @property
    def logo_rot(self) -> float:
        return self.__logo_r if isnumeric(self.__logo_r) else 0
    @property
    def __logo_s(self) -> str:
        return self.query.get('logo_s', '')
    @property
    def logo_scale(self) -> float:
        return self.__logo_s if isnumeric(self.__logo_s) else 1.
    @property
    def __lx(self) -> str:
        return self.query.get('logo_x', '')
    @property
    def logo_pos_x(self) -> int:
        return self.__lx if self.__lx.isdecimal() else 0
    @property
    def __ly(self) -> str:
        return self.query.get('logo_y', '')
    @property
    def logo_pos_y(self) -> int:
        return self.__ly if self.__ly.isdecimal() else 0
    @property
    def logo_align(self) -> str:
        return self.query.get('logo_align', 'center')
    
    # BACKGROUND
    
    @property
    def __bgx(self) -> str:
        return self.query.get('p_x', '')
    @property
    def bg_pos_x(self) -> int:
        return self.__bgx if self.__bgx.isdecimal() else 0
    @property
    def __bgy(self) -> str:
        return self.query.get('p_y', '')
    @property
    def bg_pos_y(self) -> int:
        return self.__bgy if self.__bgy.isdecimal() else 0
    @property
    def __bgrx(self) -> str:
        return self.query.get('rp_x', '')
    @property
    def bg_rpos_x(self) -> int:
        return self.__bgrx if self.__bgrx.isdecimal() else 0
    @property
    def __bgry(self) -> str:
        return self.query.get('rp_y', '')
    @property
    def bg_rpos_y(self) -> int:
        return self.__bgry if self.__bgry.isdecimal() else 0
    
    @property
    def __bg_r(self) -> str:
        return self.query.get('r', '')
    @property
    def bg_rot(self) -> float:
        return self.__bg_r if isnumeric(self.__bg_r) else 0
    @property
    def __bg_rx(self) -> str:
        return self.query.get('rr_x', '')
    @property
    def bg_rrot_x(self) -> float:
        return self.__bg_rx if isnumeric(self.__bg_rx) else 0
    @property
    def __bg_ry(self) -> str:
        return self.query.get('rr_y', '')
    @property
    def bg_rrot_y(self) -> float:
        return self.__bg_ry if isnumeric(self.__bg_ry) else 0
    
    @property
    def __bg_s(self) -> str:
        return self.query.get('s', '')
    @property
    def bg_scale(self) -> float:
        return self.__bg_s if isnumeric(self.__bg_s) else 0
    @property
    def __bg_sx(self) -> str:
        return self.query.get('rs_x', '')
    @property
    def bg_rscale_x(self) -> float:
        return self.__bg_sx if isnumeric(self.__bg_sx) else 0
    @property
    def __bg_sy(self) -> str:
        return self.query.get('rs_y', '')
    @property
    def bg_rscale_y(self) -> float:
        return self.__bg_sy if isnumeric(self.__bg_sy) else 0
    
    @property
    def __hue(self) -> str:
        return self.query.get('hue', '')
    @property
    def hue(self) -> float:
        return self.__hue if isnumeric(self.__hue) else 0
    @property
    def __sat(self) -> str:
        return self.query.get('sat', '')
    @property
    def sat(self) -> float:
        return self.__sat if isnumeric(self.__sat) else 0
    @property
    def __lig(self) -> str:
        return self.query.get('lig', '')
    @property
    def lig(self) -> float:
        return self.__lig if isnumeric(self.__lig) else 0
    @property
    def bg(self) -> str:
        return self.query.get('background', '')