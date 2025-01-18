RUNTIMESETTIGS = {
    'letsPlay': None,
    'path': None
}
from tkinter import filedialog
class FilePath:
    def __init__(self) -> None:
        self.path = ''
    def setPath(self,*_):
        self.path = filedialog.askopenfilename()
        
JTGIMGPATH = FilePath()
JTGFONTPATH = FilePath()