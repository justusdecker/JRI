from bin.jf_filereader import JFFile
from os.path import isfile, getsize

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip

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
    """
        A Lets Play Episode must be formatted like:
        - video_path            0
        - audio_mic_path        1
        - audio_desktop_path    2
        - thumbnail_path        3
        - title                 4
        - thumbnail_frame       5
        
        Generate:
        - video_length              defaults to -1 if file not exist
        - audio_mic_length          defaults to -1 if file not exist
        - audio_desktop_length      defaults to -1 if file not exist 
        - video_file_size           defaults to -1 if file not exist
        - audio_file_size           defaults to -1 if file not exist
        
        Status will be replaced by:
        - video_exist / not ""
        - audio_mic_exist / not ""
        - audio_desktop_exist / not ""
        - thumbnail_exist / not ""
        
        """
    def __init__(self,l: list):
        self.l = l # Reference to the JFFile List
    
    @property
    def video_file_size(self) -> int:
        return getsize(self.video_path) if self.video_exist else -1

    @property
    def audio_mic_file_size(self) -> int:
        return getsize(self.audio_mic_path) if self.audio_mic_exist else -1
    
    @property
    def audio_desktop_file_size(self) -> int:
        return getsize(self.audio_desktop_path) if self.audio_desktop_exist else -1
    
    @property
    def audio_desktop_duration(self) -> float:
        return AudioFileClip(self.audio_desktop_path).duration if self.audio_desktop_exist else -1
    @property
    def audio_mic_duration(self) -> float:
        return AudioFileClip(self.audio_mic_path).duration if self.audio_mic_exist else -1
    @property
    def video_duration(self) -> float:
        return VideoFileClip(self.video_path).duration if self.video_exist else -1
    
    @property
    def video_exist(self) -> bool:
        return isfile(self.video_path)
    @property
    def audio_mic_exist(self) -> bool:
        return isfile(self.audio_mic_path)
    @property
    def audio_desktop_exist(self) -> bool:
        return isfile(self.audio_desktop_path)
    @property
    def thumbnail_exist(self) -> bool:
        return isfile(self.thumbnail_path)
    
    @property
    def video_path(self) -> str:
        return self.l[0]
    @video_path.setter
    def video_path(self, value: str):
        self.l[0] = value
        
    @property
    def audio_mic_path(self) -> str:
        return self.l[1]
    @audio_mic_path.setter
    def audio_mic_path(self, value: str):
        self.l[1] = value
        
    @property
    def audio_desktop_path(self) -> str:
        return self.l[2]
    @audio_desktop_path.setter
    def audio_desktop_path(self, value: str):
        self.l[2] = value
    
    @property
    def thumbnail_path(self) -> str:
        return self.l[3]
    @thumbnail_path.setter
    def thumbnail_path(self, value: str):
        self.l[3] = value
        
    @property
    def title(self) -> str:
        return self.l[4]
    @title.setter
    def title(self, value: str):
        self.l[4] = value
    
    @property
    def thumbnail_frame(self) -> float:
        return self.l[5]
    @thumbnail_frame.setter
    def thumbnail_frame(self, value: float):
        return self.l[5]
class LetsPlayTADText:
    def __init__(self):
        pass

class LetsPlayTADLogo:
    def __init__(self):
        pass
 
class LetsPlayTADBackground:
    def __init__(self):
        pass