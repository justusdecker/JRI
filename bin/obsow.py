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
    login_thread: bool = False
    
    def __init__(self,
                 currentLP,
                 current_letsplay_path
                 ):
        self.pressedKey = ''
        self.JTG: ThumbnailGenerator = ThumbnailGenerator()
        self.current_letsplay_path = current_letsplay_path
        self.options = {
            'host': SETTINGS._['obsHost'],
            'port': SETTINGS._['obsPort'],
            'password': SETTINGS._['obsPassword'],
            'timeout': SETTINGS._['obsTimeout']
            }
        self.connect()
        self.currentLPData: LetsPlayFile = currentLP
        self.tna = False
        self.isPressed = False
        self.ignoredWarnings = 0
    
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
            self.connectionEstablished = True
            self.obsncw = False
            self.tna = False
        except WindowsError as E: #! Some error occured
            #CrashBox([f'[{ERRORIDS.OBSWSTE}] OBS cant connect {E.errno}', str(E)])
            self.connectionEstablished = False
            

            self.obsncw = True
        except _exceptions.WebSocketTimeoutException as E: #! Some error occured
            CrashBox([f'[{ERRORIDS.OBSWE}] OBS cant connect [WS-TimeOut]', str(E)])
            self.connectionEstablished = False

            self.obsncw = True
        self.loginThread = False
    @property
    def time(self) -> str:
        """
        Returns the OBS TimeCode if not avaiable it returns 'OBS is not activated'
        """
        try:
            return str(self.obs.get_output_status(OUTPUT_TYPE)[0]['outputTimecode'])
        except:
            if not self.tna: #What the fuck is tna? Why did i did this god damnit!?
                self.tna = True
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
        ep_len = self.currentLPData._getEpisodeLength()
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
    
    
    def onStart(self):
        """
        processes events "on Start"
        """
        if self.timecode != '00:00:00.000' and not self.is_recording:
            self.is_recording = True
            self.currentLPData._addEpisode({
                "path": self.current_filepath,
                "episodeNumber": self.currentLPData._getEpisodeCount() + 1,
                "status": 0,
                "markers": [],
                "episodeTitle": '',
                "thumbnailPath": None,
                "thumbnailFrame": 0,
                "uploadAt": '',
                "audioFilePath": None
            }
            )
            self.currentLPData.save()
    
    def thumbnailGeneration(self,epn):
        DM.createFolder(THUMBNAIL_PATH + self.currentLPData._getName())
        self.JTG.createThumbnail(self.currentLPData._getEpisodeCount(),
                                 self.current_filepath,
                                 -1,
                                 self.currentLPData._getThumbnailAutomationData(),
                                 self.currentLPData._getName()
                                 )

        self.currentLPData._setEpisode(
            epn - 1,
            'status',
            self.currentLPData._getEpisodeEx(epn - 1,'status') + 2  # TODO : Use the new ST values
            )
        self.currentLPData._setEpisode(
            epn - 1,
            'thumbnailFrame',
            self.JTG.idx
            )
        self.currentLPData.save()
        
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
        
        DM.createFolder(f'{AUDIO_PATH}{self.currentLPData._getName()}\\')
        AFX.extractAudio(self.currentLPData._getEpisodeEx(-1,'path'),f"{AUDIO_PATH}{self.currentLPData._getName()}\\{self.currentLPData._getEpisodeCount()}_{self.currentLPData._getName()}_track.mp3")

        self.currentLPData._setEpisode(
            epn - 1,
            'status',
            self.currentLPData._getEpisodeEx(epn - 1,'status') + 4 # TODO : Use the new ST values
            )
        self.currentLPData._setEpisode(
            epn - 1,
            'audioFilePath',
            f"{AUDIO_PATH}{self.currentLPData._getName()}\\{epn}_{self.currentLPData._getName()}_track.mp3"
            )
        self.currentLPData.save()

    def onStop(self):
        """
        processes events "on Stop"
        """
        if self.is_recording and self.timecode() == '00:00:00.000':
            self.currentLPData._setEpisode(
            -1,
            'status',
            self.currentLPData._getEpisodeEx(-1,'status') + 1 # TODO : Use the new ST values
            )
            self.currentLPData._setEpisode(
            -1,
            'thumbnailPath',
            f"{THUMBNAIL_PATH}{self.currentLPData._getName()}\\{self.currentLPData._getEpisodeCount()}_{self.currentLPData._getName()}_Thumbnail.png"
            )
            self.currentLPData.save()
            
            Thread(
                target=self.thumbnailGeneration,
                args=[
                    self.currentLPData._getEpisodeCount()
                    ]
                ).start()
            Thread(
                target=self.audioExtraction,
                args=[
                    self.currentLPData._getEpisodeCount()
                      ]
                ).start()
            self.is_recording = False
            self.warnings = False


            
    
    def setMarker(self):
        """
        Append a timeStamp to the current Episode
        """
        if is_pressed('K') and not self.isPressed and self.is_recording:
            self.pressedKey = 'K'
            markers = self.currentLPData._getEpisodeEx(-1,'markers')
            markers.append(f'<$TimeLapse:{self.time}>')
            self.currentLPData._setEpisode(-1,'markers',markers)


            self.currentLPData.save()
            self.isPressed = True
        if not is_pressed('K') and self.isPressed and self.pressedKey == 'K':
            self.isPressed = False
        if is_pressed('L') and not self.isPressed and self.is_recording:
            self.pressedKey = 'L'
            markers = self.currentLPData._getEpisodeEx(-1,'markers')
            markers.append(f'<$Interest:{self.time}>')
            self.currentLPData._setEpisode(-1,'markers',markers)

            self.currentLPData.save()
            self.isPressed = True
        if not is_pressed('L') and self.isPressed and self.pressedKey == 'L':
            self.isPressed = False
        
    def update(self):
        try:
            self.onStart()
            self.onStop()
            self.setMarker()
        except Exception as E:
            self.ignoredWarnings += 1
            if self.ignoredWarnings > 2:
                CrashBox([f'[{ERRORIDS.JRICANTCONNECT}] JRI cant connect to OBS', 'Check Settings: IP Adress, Port, Password & timeout.\n And use Advance Settings in OBS!\nJRI close itself!'])
            else:
                CrashBox([f'[{ERRORIDS.OBSMO}] OBS moved out', str(E) + str({E.args})])
            self.connectionEstablished = False
            if not self.loginThread: 
                self.loginThread = True
                Thread(target=self.connect).start()
