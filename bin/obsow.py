from bin.settings import SETTINGS
from bin.letsPlayFile import LetsPlayFile
import obsws_python as obsws
from websocket import _exceptions
from subprocess import call as callSubProcess
from bin.dataManagement import DM
from bin.fx.audio import AFX
from threading import Thread
from keyboard import is_pressed
from bin.thumbnailGenerator import ThumbnailGenerator
from bin.crashHandler import CrashBox,ERRORIDS

from bin.constants import THUMBNAIL_PATH, AUDIO_PATH

OUTPUT_TYPE = 'adv_file_output'



class OBSObserver:
    """
    The new OBS Observer
    -----
    
    
    """
    is_recording: bool = False
    connection_established: bool = False
    warnings: int = 0
    obsncw: bool = False
    key_marker_pressed: bool = False
    login_thread: bool = False # is false if connection establishment is all right otherwise true
    
    def __init__(self, lets_play_file: LetsPlayFile):
        self.pressed_key = ''
        self.jtg: ThumbnailGenerator = ThumbnailGenerator()
        self.options = {
            'host': SETTINGS._['obsHost'],
            'port': SETTINGS._['obsPort'],
            'password': SETTINGS._['obsPassword'],
            'timeout': SETTINGS._['obsTimeout']
            }
        self.connect()
        self.current_lp_data: LetsPlayFile = lets_play_file
        self.kb_pressed = False
        self.ignored_warnings = 0
    
    def connect(self):
        """
        Establish Connection to OBS Webserver
        
        ..Catches::
        
            - WindowsError
            - WebSocketTimeoutExeception
        """
        # Try to connect
        try:
            self.obs = obsws.ReqClient(host=self.options['host'], port=self.options['port'], password=self.options['password'],timeout=self.options['timeout'])
            self.connection_established = True
        except WindowsError as E: #! Some error occured
            #CrashBox([f'[{ERRORIDS.OBSWSTE}] OBS cant connect {E.errno}', str(E)])
            self.connection_established = False
        except _exceptions.WebSocketTimeoutException as E: #! Some error occured
            CrashBox([f'[{ERRORIDS.OBSWE}] OBS cant connect [WS-TimeOut]', str(E)])
            self.connection_established = False
        self.login_thread = False
    @property
    def time(self) -> str:
        """
        Returns the OBS TimeCode if not avaiable it returns 'OBS is not activated'
        """
        try:
            return str(self.obs.get_output_status(OUTPUT_TYPE)[0]['outputTimecode'])
        except:
            return 'OBS is not activated'
    @property
    def formatted_time(self) -> int:
        return self.get_rtime_as_int(self.timecode()),self.timecode() if self.is_recording else 0
    @property
    def timecode(self) -> int:
        """Get The Current Time In String Form"""
        return str(self.obs.get_output_status(OUTPUT_TYPE)[0]['outputTimecode'])
    @property
    def current_filepath(self) -> str:
        return str(self.obs.get_output_settings(OUTPUT_TYPE)[0]['outputSettings']['path'])
    @property
    def color(self) -> tuple[int,int,int]:
        """ color based on current state """
        ep_len = self.current_lp_data._getEpisodeLength()
        ft = self.formatted_time[0]
        ir = self.is_recording
        
        if ep_len <= ft and ir: return (255,0,0)
        elif ep_len - 30 <= ft and ir: return (255,255,0)
        elif ir: return (0,128,0)
        else: return (255,255,255)
    
    def get_rtime_as_int(self,t = '00:00:00.000') -> int:
        """ 
        Converts a "hh:mm:ss:{ms}" like string to an integer
        """
        tmp_t: list[str] = t.split('.')[0].split(':')
        return (int(tmp_t[0]) * 60 * 60) + (int(tmp_t[1]) * 60) + int(tmp_t[2])
    
    def on_start(self):
        """
        processes events "on Start"
        """
        if self.timecode != '00:00:00.000' and not self.is_recording:
            self.is_recording = True
            self.current_lp_data._addEpisode({
                "path": self.current_filepath,
                "episodeNumber": self.current_lp_data._getEpisodeCount() + 1,
                "status": 0,
                "markers": [],
                "episodeTitle": '',
                "thumbnailPath": None,
                "thumbnailFrame": 0,
                "uploadAt": '',
                "audioFilePath": None
            }
            )
            self.current_lp_data.save()
    
    def on_stop(self):
        """
        processes events "on Stop"
        """
        if self.is_recording and self.timecode() == '00:00:00.000':
            self.current_lp_data._setEpisode(-1, 'status', self.current_lp_data._getEpisodeEx(-1,'status') + 1)
            self.current_lp_data._setEpisode(-1, 'thumbnailPath',f"{THUMBNAIL_PATH}{self.current_lp_data._getName()}\\{self.current_lp_data._getEpisodeCount()}_{self.current_lp_data._getName()}_Thumbnail.png")
            self.current_lp_data.save()
            
            #! VERY UNSAFE Implementation of threads! Make sure that threads are accessible to stop the app from moving on!
            Thread(target=self.thumbnailGeneration,args=[self.current_lp_data._getEpisodeCount()]).start()
            Thread(target=self.audioExtraction,args=[self.current_lp_data._getEpisodeCount()]).start()
            self.is_recording = False
            self.warnings = False


            
    
    def setMarker(self):
        """
        Append a timeStamp to the current Episode
        """
        if is_pressed('K') and not self.kb_pressed and self.is_recording:
            self.pressed_key = 'K'
            markers = self.current_lp_data._getEpisodeEx(-1,'markers')
            markers.append(f'<$TimeLapse:{self.time}>')
            self.current_lp_data._setEpisode(-1,'markers',markers)


            self.current_lp_data.save()
            self.kb_pressed = True
        if not is_pressed('K') and self.kb_pressed and self.pressed_key == 'K':
            self.kb_pressed = False
        if is_pressed('L') and not self.kb_pressed and self.is_recording:
            self.pressed_key = 'L'
            markers = self.current_lp_data._getEpisodeEx(-1,'markers')
            markers.append(f'<$Interest:{self.time}>')
            self.current_lp_data._setEpisode(-1,'markers',markers)

            self.current_lp_data.save()
            self.kb_pressed = True
        if not is_pressed('L') and self.kb_pressed and self.pressed_key == 'L':
            self.kb_pressed = False
        
    def update(self):
        try:
            self.on_start()
            self.on_stop()
            self.setMarker()
        except Exception as E:
            self.ignored_warnings += 1
            if self.ignored_warnings > 2:
                CrashBox([f'[{ERRORIDS.JRICANTCONNECT}] JRI cant connect to OBS', 'Check Settings: IP Adress, Port, Password & timeout.\n And use Advance Settings in OBS!\nJRI close itself!'])
            else:
                CrashBox([f'[{ERRORIDS.OBSMO}] OBS moved out', str(E) + str({E.args})])
            self.connection_established = False
            if not self.login_thread: 
                self.login_thread = True
                Thread(target=self.connect).start()
    
    
    def thumbnailGeneration(self,epn):
        DM.createFolder(THUMBNAIL_PATH + self.current_lp_data._getName())
        self.jtg.createThumbnail(self.current_lp_data._getEpisodeCount(),
                                 self.current_filepath,
                                 -1,
                                 self.current_lp_data._getThumbnailAutomationData(),
                                 self.current_lp_data._getName()
                                 )

        self.current_lp_data._setEpisode(
            epn - 1,
            'status',
            self.current_lp_data._getEpisodeEx(epn - 1,'status') + 2  # TODO : Use the new ST values
            )
        self.current_lp_data._setEpisode(
            epn - 1,
            'thumbnailFrame',
            self.jtg.idx
            )
        self.current_lp_data.save()
        
    def _cvtAudio(fileName:str,
                 fromType:str= '.mp3',
                 toType:str= '.wav'):
        """Convert Audio Formats"""
        callSubProcess(
            [
                'ffmpeg', 
                '-i', 
                fileName.split('.')[0] + fromType,
                fileName.split('.')[0] + toType
                ]
            )
        return fileName.split('.')[0] + toType

    def audioExtraction(self,epn):
        """Audio Extraction out of current Episode Video File"""
        
        DM.createFolder(f'{AUDIO_PATH}{self.current_lp_data._getName()}\\')
        AFX.extractAudio(self.current_lp_data._getEpisodeEx(-1,'path'),f"{AUDIO_PATH}{self.current_lp_data._getName()}\\{self.current_lp_data._getEpisodeCount()}_{self.current_lp_data._getName()}_track.mp3")

        self.current_lp_data._setEpisode(
            epn - 1,
            'status',
            self.current_lp_data._getEpisodeEx(epn - 1,'status') + 4 # TODO : Use the new ST values
            )
        self.current_lp_data._setEpisode(
            epn - 1,
            'audioFilePath',
            f"{AUDIO_PATH}{self.current_lp_data._getName()}\\{epn}_{self.current_lp_data._getName()}_track.mp3"
            )
        self.current_lp_data.save()

