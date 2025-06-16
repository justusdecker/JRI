from bin.settings import SETTINGS
from bin.letsplay_file import LetsPlayFile
import obsws_python as obsws
from websocket import _exceptions
from subprocess import call as callSubProcess
from bin.dataManagement import DM
from bin.fx.audio import AFX
from threading import Thread
from keyboard import is_pressed
from bin.automation.thumbnail_generator import ThumbnailGenerator

from bin.constants import PATHS

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
        self.threads = []
        self.pressed_key = ''
        self.jtg: ThumbnailGenerator = ThumbnailGenerator()
        self.options = {
            'host': SETTINGS.obs_ip,
            'port': SETTINGS.obs_port,
            'password': SETTINGS.obs_pw,
            'timeout': SETTINGS.obs_timeout
            }
        self.connect()
        self.load_lpf(lets_play_file)
        self.kb_pressed = False
        self.ignored_warnings = 0
    def load_lpf(self,lpf: LetsPlayFile):
        if not self.is_recording and not self.threads_active:
            self.lpf: LetsPlayFile = lpf
            print(f'updated lets play to {lpf.name}')
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
            #CrashBox([f'[{ERRORIDS.OBSWE}] OBS cant connect [WS-TimeOut]', str(E)])
            self.connection_established = False
        self.login_thread = False
    @property
    def time(self) -> str:
        """
        Returns the OBS TimeCode if not avaiable it returns 'OBS is not activated'
        """

        try:
            return self.timecode
        except:
            return 'OBS is not activated'
    @property
    def formatted_time(self) -> int:
        return self.get_rtime_as_int(self.timecode),self.timecode if self.is_recording else 0
    @property
    def timecode(self) -> int:
        """Get The Current Time In String Form"""
        return str(self.obs.get_output_status(OUTPUT_TYPE).output_timecode)
    @property
    def current_filepath(self) -> str:
        print(self.obs.get_output_settings(OUTPUT_TYPE).__dict__)
        return str(self.obs.get_output_settings(OUTPUT_TYPE).output_settings['path'])
    @property
    def color(self) -> tuple[int,int,int]:
        """ color based on current state """
        ep_len = self.lpf.episode_length
        ft = self.formatted_time[0]
        ir = self.is_recording
        print(ep_len, ft,ir)
        
        if ep_len <= ft and ir: return (255,0,0)
        elif ep_len - 30 <= ft and ir: return (255,255,0)
        elif ir: return (0,128,0)
        else: return (255,255,255)
    
    @property
    def threads_active(self) -> bool:
        if self.threads:
            return any([i.is_alive() for i in self.threads])
        return self.threads
    
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
            self.lpf.add_episode({
                "path": self.current_filepath,
                "episodeNumber": self.lpf.episode_count + 1,
                "status": 0,
                "markers": [],
                "episodeTitle": '',
                "thumbnailPath": None,
                "thumbnailFrame": 0,
                "uploadAt": '',
                "audioFilePath": None
            }
            )
            self.lpf.save()
    
    def on_stop(self):
        """
        processes events "on Stop"
        """
        if self.is_recording and self.timecode == '00:00:00.000':
            ep = self.lpf.get_episode(-1)
            ep.status += 1
            ep.thumbnail_path = f"{PATHS.thumbnail}{self.lpf.name}\\{self.lpf.episode_count}_{self.lpf.name}_Thumbnail.png"
            self.lpf.save()
            
            
            self.threads = [
                Thread(target=self.thumbnailGeneration,args=[self.lpf.episode_count]),
                Thread(target=self.audioExtraction,args=[self.lpf.episode_count])
                ]
            for i in self.threads:
                i.start()
            self.is_recording = False
            self.warnings = False


            
    
    def setMarker(self):
        """
        Append a timeStamp to the current Episode
        """
        if is_pressed('K') and not self.kb_pressed and self.is_recording:
            self.pressed_key = 'K'
            ep = self.lpf.get_episode(-1)
            ep.markers.append(f'<$TimeLapse:{self.time}>')

            self.lpf.save()
            self.kb_pressed = True
        if not is_pressed('K') and self.kb_pressed and self.pressed_key == 'K':
            self.kb_pressed = False
        if is_pressed('L') and not self.kb_pressed and self.is_recording:
            self.pressed_key = 'L'
            ep = self.lpf.get_episode(-1)
            ep.markers.append(f'<$Interest:{self.time}>')

            self.lpf.save()
            self.kb_pressed = True
        if not is_pressed('L') and self.kb_pressed and self.pressed_key == 'L':
            self.kb_pressed = False
        
    def update(self):
        self.on_start()
        self.on_stop()
        self.setMarker()
        try:
            self.on_start()
            self.on_stop()
            self.setMarker()
        except Exception as E:
            #i dont think this stuff is needed anymore
            #self.ignored_warnings += 1
            #if self.ignored_warnings > 2:
                #CrashBox([f'[{ERRORIDS.JRICANTCONNECT}] JRI cant connect to OBS', 'Check Settings: IP Adress, Port, Password & timeout.\n And use Advance Settings in OBS!\nJRI close itself!'])
            #else:
                
                #CrashBox([f'[{ERRORIDS.OBSMO}] OBS moved out', str(E) + str({E.args})])
            self.connection_established = False
            if not self.login_thread: 
                self.login_thread = True
                Thread(target=self.connect).start()
    
    
    def thumbnailGeneration(self,epn):
        DM.createFolder(PATHS.thumbnail + self.lpf.name)
        self.jtg.create_thumbnail(self.lpf.episode_count,
                                 self.current_filepath,
                                 -1,
                                 self.lpf.tad.asdict(),
                                 self.lpf.name
                                 )
        ep = self.lpf.get_episode(epn - 1)
        ep.status += 2
        ep.frame = self.jtg.idx

        self.lpf.save()
        
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
        ep = self.lpf.get_episode(-1)
        DM.createFolder(f'{PATHS.audio}{self.lpf.name}\\')
        AFX.extractAudio(ep.video_path,f"{PATHS.audio}{self.lpf.name}\\{self.lpf.episode_count}_{self.lpf.name}_track.mp3")
        ep.status += 4

        ep.audio_path = f"{PATHS.audio}{self.lpf.name}\\{epn}_{self.lpf.name}_track.mp3"

        self.lpf.save()

