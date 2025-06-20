from bin.jf_filereader import JFFile
# Uploadat will be replaced with:
# Header::start_date
# Header::time_delta_between_uploads
#
# This will reduce filesize & make it more readable
class LetsPlay:
    def __init__(self, filepath: str):
        self.jf = JFFile(filepath)
        self.header = LetsPlayHeader(self.jf)
        self.episodes = [LetsPlayEpisode(i) for i in self.jf.get('<EP>::EPISODES')]
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
        """
        A Lets Play Episode must be formatted like:
        - video_path
        - audio_path
        - thumbnail_path
        - title
        - episode_number
        
        Generate:
        - video_length
        - audio_length
        - video_file_size
        - audio_file_size
        
        Status will be replaced by:
        - video_exist / not ""
        - audio_exist / not ""
        - thumbnail_exist / not ""
        
        """
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