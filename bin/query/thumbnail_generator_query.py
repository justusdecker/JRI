class ThumbnailGeneratorQuery:
    """
    
    A Wrapper to get a bunch of values without a BIG HEADACHE because some elements don't exist!
    
    Mapper
    *****
    
    Lets Play
    -----
    .. lp::
        `str` Lets Play Hash
        
        lp

    Text / Font
    -----
    .. px::
        `int` Position X
        
        pos_x
    .. py::
        `int` Position Y
        
        pos_y
    .. text_font::
        `str` Font Path
        
        font
    .. text_align::
        `str` Alignment **center, left, right**
        
        text_align
    .. font_s::
        `float` The Font size
        
        font_size
    .. text_r::
        `float` The Font rotation
        
        text_rotation
    
    Logo
    -----
    .. logo_path:
        `str` Defines the location of the logo image
        
        logo_path
    .. logo_r::
        `float` The Logo rotation
        
        logo_rot
    .. logo_s::
        `float` The Logo scale
        
        logo_scale
    .. logo_x::
        `int` The Logo position X
        
        will be combined with `logo_y` to logo_pos
    .. logo_y::
        `int` The Logo position Y
        
        will be combined with `logo_x` to logo_pos
    logo_s          float
    logo_x          int
    logo_y          int
    logo_align      str - center, left, right
    
    """
    def __init__(self,query: str):
        self.query = {}
        for arg in query.split('&'):
            v = arg.split('=')
            if len(v) == 2:
                self.query[v[0]] = v[1]
    @property
    def lp(self) -> str:
        return self.query.get('lp', '')
    @property
    def font(self) -> str:
        return self.query.get('text_font', '')
    @property
    def __text_px(self) -> str:
        return self.query.get('px', '')
    @property
    def text_pos_x(self) -> int:
        return self.__text_px if self.__text_px.isdecimal() else 0
    @property
    def __text_py(self) -> str:
        return self.query.get('py', '')
    @property
    def text_pos_y(self) -> int:
        return self.__text_py if self.__text_py.isdecimal() else 0
    
"""




p_x             int
p_y             int
rp_x            int
rp_y            int
r               float
rr_x            float
rr_y            float
s               float
rs_x            float
rs_y            float
hue             float
sat             float
lig             float
background      str
"""