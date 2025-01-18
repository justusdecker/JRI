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

class OBSObserver:
    isRecording: bool = False
    connectionEstablished: bool = False
    warnings: int = 0
    obsncw: bool = False
    keyMarkerPressed: bool = False
    loginThread: bool = False
    
    def __init__(self,
                 TimerApp,
                 currentLP,
                 cLPPath
                 ):
        self.pressedKey = ''
        self.JTG: ThumbnailGenerator = ThumbnailGenerator()
        self.currentLPPath = cLPPath
        self.timerApp = TimerApp
        self.color = (255,255,255)
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
        """
        #while not self.connectionEstablished:
        try:
            self.OBS = obsws.ReqClient(host=self.options['host'], port=self.options['port'], password=self.options['password'],timeout=self.options['timeout'])
            self.connectionEstablished = True

            self.obsncw = False
            self.tna = False
        except WindowsError as E:
            #CrashBox([f'[{ERRORIDS.OBSWSTE}] OBS cant connect {E.errno}', str(E)])
            self.connectionEstablished = False
            

            self.obsncw = True
        except _exceptions.WebSocketTimeoutException as E:
            CrashBox([f'[{ERRORIDS.OBSWE}] OBS cant connect [WS-TimeOut]', str(E)])
            self.connectionEstablished = False

            self.obsncw = True
        self.loginThread = False

    def getTime(self):
        """
        Returns the OBS TimeCode if not avaiable it returns 'OBS is not activated'
        """
        try:
            t = str(
                self.OBS.get_output_status('adv_file_output')[0]['outputTimecode']
                )
            return t
        except:
            if not self.tna:
                self.tna = True
            return 'OBS is not activated'
        
    def getConvTime(self):
        return self.convertTime(self._getTimeCode()),self._getTimeCode() if self.isRecording else 0

    def convertTime(self,timeString = '00:00:00.000'):
        _time = timeString.split('.')[0].split(':')
        return (int(_time[0]) * 60) + (int(_time[1]) * 60) + int(_time[2])
    
    def _getTimeCode(self):
        """Get The Current Time In String Form"""
        return str(self.OBS.get_output_status('adv_file_output')[0]['outputTimecode'])
    
    def _getFilePath(self):
        "Get The Current OBS Filepath"
        return str(self.OBS.get_output_settings('adv_file_output')[0]['outputSettings']['path'])
    
    def onStart(self):
        """
        processes events "on Start"
        """
        if self._getTimeCode() != '00:00:00.000' and not self.isRecording:
            self.isRecording = True
            self.currentLPData._addEpisode({
                "path": self._getFilePath(),
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
            self.color = (0,128,0)
    
    def thumbnailGeneration(self,epn):
        DM.createFolder(THUMBNAIL_PATH + self.currentLPData._getName())
        self.JTG.createThumbnail(self.currentLPData._getEpisodeCount(),
                                 self._getFilePath(),
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
        if self.isRecording and self._getTimeCode() == '00:00:00.000':
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
            self.isRecording = False
            self.warnings = False
            self.color = (255,255,255)

            
    
    def setMarker(self):
        """
        Append a timeStamp to the current Episode
        """
        if is_pressed('K') and not self.isPressed and self.isRecording:
            self.pressedKey = 'K'
            markers = self.currentLPData._getEpisodeEx(-1,'markers')
            markers.append(f'<$TimeLapse:{self.getTime()}>')
            self.currentLPData._setEpisode(-1,'markers',markers)


            self.currentLPData.save()
            self.isPressed = True
        if not is_pressed('K') and self.isPressed and self.pressedKey == 'K':
            self.isPressed = False
        if is_pressed('L') and not self.isPressed and self.isRecording:
            self.pressedKey = 'L'
            markers = self.currentLPData._getEpisodeEx(-1,'markers')
            markers.append(f'<$Interest:{self.getTime()}>')
            self.currentLPData._setEpisode(-1,'markers',markers)

            self.currentLPData.save()
            self.isPressed = True
        if not is_pressed('L') and self.isPressed and self.pressedKey == 'L':
            self.isPressed = False
        
    def update(self):
        if not self.warnings and self.isRecording:
            _ = self.getConvTime()
            
            if self.currentLPData._getEpisodeLength() - 30 <= _[0]:
                self.warnings = True
                self.color = (255,255,0)

        if self.warnings == 1 and self.isRecording:
            _ = self.getConvTime()
            if self.currentLPData._getEpisodeLength() <= _[0]:
                self.warnings = 2
                self.color = (255,0,0)

        try:
            self.onStart()
            self.onStop()
            self.setMarker()
        except Exception as E:
            self.ignoredWarnings += 1
            if self.ignoredWarnings > 2:
                self.timerApp.isAlive = False
                CrashBox([f'[{ERRORIDS.JRICANTCONNECT}] JRI cant connect to OBS', 'Check Settings: IP Adress, Port, Password & timeout.\n And use Advance Settings in OBS!\nJRI close itself!'])
            else:
                CrashBox([f'[{ERRORIDS.OBSMO}] OBS moved out', str(E) + str({E.args})])
            self.connectionEstablished = False
            if not self.loginThread: 
                self.loginThread = True
                Thread(target=self.connect).start()
