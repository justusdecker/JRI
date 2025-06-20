from bin.jf_filereader import JFFile

class LetsPlay:
    def __init__(self, filepath: str):
        self.jf = JFFile(filepath)
        self.header = LetsPlayHeader(self.jf)

class LetsPlayHeader:
    def __init__(self, jf: JFFile):
        self.jf = jf
    
    @property
    def name(self) -> str:
        return self.jf.get('<HEADER>::NAME')
    @name.setter
    def name(self, value: str):
        self.jf.set('<HEADER>::NAME', value)
        
    @property
    def game_name(self) -> str:
        return self.jf.get('<HEADER>::GAME_NAME')
    @game_name.setter
    def game_name(self, value: str):
        self.jf.set('<HEADER>::GAME_NAME', value)
        
    @property
    def icon_path(self) -> str:
        return self.jf.get('<HEADER>::ICON_PATH')
    @icon_path.setter
    def icon_path(self, value: str):
        self.jf.set('<HEADER>::ICON_PATH', value)
        
    @property
    def episode_length(self) -> int:
        return self.jf.get('<HEADER>::EPISODE_LENGTH')
    @episode_length.setter
    def episode_length(self, value: int):
        self.jf.set('<HEADER>::EPISODE_LENGTH', value)
    
class LetsPlayEpisode:
    def __init__(self):
        pass

class LetsPlayTADText:
    def __init__(self):
        pass

class LetsPlayTADLogo:
    def __init__(self):
        pass
 
class LetsPlayTADBackground:
    def __init__(self):
        pass