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
        
        !bg_pos_x
    .. p_y::
        `int` position Y
        
        !bg_pos_y

    .. rp_x::
        `int` random position X
        
        !bg_pos_x
    .. rp_y::
        `int` random position Y
        
        !bg_pos_y

    .. r::
        `float` rotation
        
        !bg_rot
    .. rr_x::
        `float` random rotation
        
        !bg_rrot_x
    .. rr_y::
        `float` random rotation
        
        !bg_rrot_y

    .. s::
        `float` scale
        
        !bg_rot
    .. rs_x::
        `float` random scale
        
        !bg_rscale_x
    .. rs_y::
        `float` random scale
        
        !bg_rscale_y
    
    .. hue::
        `float` the hue value of each pixel manipulation in the image
        
        !hue
    .. sat::
        `float` the saturation value of each pixel manipulation in the image
        
        !sat
    .. lig::
        `float` the lightness value of each pixel manipulation in the image
        
        !lig

    .. background::
     `str` Defines the location of the background image(If not set the image will be fetched out of the video!)
     
        !bg
    """
    def __init__(self,query: str):
        self.query = {}
        for arg in query.split('&'):
            v = arg.split('=')
            if len(v) == 2:
                self.query[v[0]] = v[1]
    
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
    
    