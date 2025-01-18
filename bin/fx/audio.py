
from os.path import isfile
import subprocess
#from subprocess import run as runSubProcess,call as callSubProcess
#from subprocess import CREATE_NO_WINDOW
from bin.log import LOG
from moviepy.audio.io.AudioFileClip import AudioFileClip
#import speech_recognition as sr
import soundfile as sf
import pyloudnorm as pyln
from numpy import frombuffer,int16
from numpy.fft import fft
from os import path
from threading import Thread

from numba import jit
import soundfile as sf
from os import path
from bin.debugFunctions import debugExecutionTimeCheck,debugExecutionTimeCheckWOV
from bin.dataManagement import DM
import wave
from numpy import array_split
try:
    from vosk import Model,KaldiRecognizer
except:
    print('This dont work')
from json import loads,dumps

from math import sqrt
from bin.debugFunctions import DeprecationWarn

class audaCityPipeLine:
    def __init__(self):
        """
        Initialize the pipe folder
        """
        self.toName = '\\\\.\\pipe\\ToSrvPipe'
        self.fromName = '\\\\.\\pipe\\FromSrvPipe'
        self.eol = '\r\n\0'

    @DeprecationWarn
    def doCommand(self,command: list):
        """
        Communicates with the Audacity Pipeline
        """
        if not path.exists(self.toName) or not path.exists(self.fromName):
            return False
        print("-- Both pipes exist.  Good.")
        c = False
        while not c:
            try: 
                toFile = open(self.toName, 'w')
                fromFile = open(self.fromName, 'rt')
                cmd = f'{command[0]}: '
                command.pop(0)
                cmd += cmd.join(command)
                print(cmd)
                
                toFile.write(cmd + self.eol)
                toFile.flush()
                print(fromFile.readline())
                toFile.close()
                c = True
            except:
                pass

ACPL = audaCityPipeLine()
@DeprecationWarn
def peakNormalization(filePath,savePath):
    fName = AFX.cvtAudio(filePath)
    data, rate = sf.read(fName) # load audio
    peak_normalized_audio = pyln.normalize.peak(data, -1.0)
    sf.write(savePath,peak_normalized_audio,rate)
@DeprecationWarn
def LoudnessNormalization(filePath,savePath):
    fName = AFX.cvtAudio(filePath)
    data, rate = sf.read(fName) # load audio
    meter = pyln.Meter(rate) # create BS.1770 meter
    loudness = meter.integrated_loudness(data)
    # loudness normalize audio to -15 dB LUFS
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -15.0)
    sf.write(savePath,loudness_normalized_audio,rate)
    
class AFX:
    """
    A Collection of Audio FX and Convert Methods!
    """
    @debugExecutionTimeCheck
    def LoudnessNormalization(filePath,savePath,decibel:int = -15):
        #fName = AFX.cvtAudio(filePath)
        data, rate = sf.read(filePath) # load audio
        meter = pyln.Meter(rate) # create BS.1770 meter
        loudness = meter.integrated_loudness(data)
        # loudness normalize audio to -15 dB LUFS
        loudness_normalized_audio = pyln.normalize.loudness(data, loudness, decibel)
        sf.write(savePath,loudness_normalized_audio,rate)
    
    def _getAudioLength(filename):
        if isfile(filename):
            return AudioFileClip(filename).duration
        return -1
    @debugExecutionTimeCheck
    def extractAudio(fr:str,to:str,t:int=1):
        subprocess.run(
                    (
                        'ffmpeg',
                        '-loglevel',
                        'error',
                        '-y',
                        '-i',
                        f"{fr}",
                        '-map',
                        f'0:{t}',
                        f"{to}"
                        ),
                    subprocess.CREATE_NO_WINDOW,
                    shell= True
                    )
        pass
    @debugExecutionTimeCheck
    def limiter(iFileName: str,
                oFileName: str,
                limiter: str = '0/-3|10/-3|20/-3'):
        subprocess.run(
                [
                    'ffmpeg',
                    '-y',
                    '-i',
                    iFileName,
                    #'-c:a',     #Copy Audio. No Reencoding
                    #'-af compand=0 0:1 1:{limiter}:0.01:12:0:0',
                    '-af',
                    f'compand=0|0:1|1:{limiter}:0.1:0:0:0',
                    oFileName
                    ]
                )
    @debugExecutionTimeCheck
    def cvtAudio(fileName:str,#call
                    fromType:str= '.mp3',
                    toType:str= '.wav'):
            """Convert Audio Formats"""
            subprocess.run(
                [
                    'ffmpeg',
                    
                    '-n',
                    '-i',
                    fileName.split('.')[0] + fromType,
                    fileName.split('.')[0] + toType
                    ],
                    subprocess.CREATE_NO_WINDOW,
                    shell= True
                )
            return fileName.split('.')[0] + toType
    @debugExecutionTimeCheck
    def cvtAudioEx(fromName,toName):
            """Convert Audio Formats"""
            subprocess.run(
                [
                    'ffmpeg',
                    
                    '-n',
                    '-i',
                    fromName,
                    toName
                    ],
                    subprocess.CREATE_NO_WINDOW,
                    shell= True
                )
            return toName
    """
    
    
                    #'-vf',
                    #'"scale=512:384, setsar=1"',
    
    #-90/-900 Sets if -90 dB to -900dB(Complete Silence)
                    #-70/-70 Sets if -70 dB to -70dB
                    #-21/-21 Sets if -21 dB to -21dB
                    #-90/-900 -70/-70 -21/-21 0/-15
                    #0/-15 Sets if 0 dB to -15dB
                    #'-c:v',     #Copy Audio. No Reencoding
                    #'libxvid',
                    #'-b:v',     #Set the Video Bitrate
                    #'800k',     #Set the Video Bitrate
                    #'-r',       #!  SET FPS to 24 
                    #'24',       #!  SET FPS to 24 
    
    
    #'libmp3lame',
                #'-b:a',     #Set the Audio Bitrate
                #'128k',     #Set the Audio Bitrate
                #'-ar',      #sampling frequency.
                #'48000',    #sampling frequency.
                #'-ac',      #Set the number of audio channels.
                #'2',        #Set the number of audio channels.
    """
    @debugExecutionTimeCheck
    def cvtAudioNew(fileName:str,#call
                    fromType:str= '.mp3',
                    toType:str= '.wav'):
            """Convert Audio Formats"""
            subprocess.run(
                [
                    'ffmpeg',
                    '-y',
                    '-i',
                    fileName.split('.')[0] + fromType,
                    'temp.wav',
                    '-ac',
                    '1'
                    ],
                    subprocess.CREATE_NO_WINDOW,
                    shell=True
                )
            subprocess.run(
                [
                    'ffmpeg',
                    '-y',
                    '-i',
                    'temp.wav',
                    
                    '-ar',
                    '8000',
                    '-ac',
                    '1',
                    '-c:a',
                    'pcm_s16le',
                    fileName.split('.')[0] + toType
                    ],
                    subprocess.CREATE_NO_WINDOW,
                    shell= True
                )
            #ffmpeg -i input.wav -ar 8000 -ac 1 -c:a pcm_s16le output.wa
            return fileName.split('.')[0] + toType
from bin.constants import EC,WAVEFORM_PATH,AUDIO_PATH

@DeprecationWarn
def convertWave2WVInfo(filePath):
    height: int = 720
    resolution: int = 128
    chunk: int = 1024

    sF = wave.open(filePath,'rb')
    
    length = sF.getnframes()
    frames = [sF.readframes(chunk) for i in range(length//chunk)]
    
    _finished = []
    
    for buff in frames:
        
        fft_complex = fft(frombuffer(buff, dtype=int16), n=chunk)
        fft_complex_result = [v.real * v.real + v.imag * v.imag for idx,v in enumerate(fft_complex) if idx % resolution == 0]
        
        scale_right = sqrt(max(fft_complex_result))
        
        scale = (height / scale_right) if scale_right != 0 else 0
        _result = sum([sqrt(x) * scale for x in fft_complex_result])

        _finished.append((_result / len(fft_complex)) if _result != 0 else 0)
    return _finished


class AudioWaveOnlyWvi:
    width = 1232
    def __init__(self,
                 filePath:str) -> None:
        if not DM.existFile(filePath):
            raise Exception(f'WVI dont exist {filePath}')
        self.data = DM.loads(filePath)
        #! Hier ist ein Bug der verhindert das Audio gespeichert wird und ein Bugs welcher scheinbar die AudioDaten vertauscht
        self.hashMap : set = {} #Here goes finished Data
        
    def get(self,start_id:int,zoom:int):
                
        _returnData = []
        ids = []

        for i in range(start_id,(self.width)+start_id):
            ids.append(int(i*zoom))
            
        for id in ids:
            _returnData.append(self.data[id])
    
        return _returnData,ids


class AudioWaveNew:
    magicNumber: float = 1 / 720
    height: int = 720
    width: int = 1232
    resolution: int = 128
    chunk: int = 1024
    def __init__(self,
                 app=None,
                 episode=None,
                 lpName='',
                 ending='') -> None:
        self.isLoaded = False
        self.app = app
        self.isAlive = True
        self.fileExist = False
        #! Hier ist ein Bug der verhindert das Audio gespeichert wird und ein Bugs welcher scheinbar die AudioDaten vertauscht
        self.hashMap : set = {} #Here goes finished Data

        AUDIO = f'{AUDIO_PATH}{lpName}\\{episode[EC.EPISODE_NUMBER]}_{lpName}_track.mp3'
        AUDIO_WAV = f'{AUDIO_PATH}{lpName}\\{episode[EC.EPISODE_NUMBER]}_track_{ending}.wav'
        WVI_PATH = f'{WAVEFORM_PATH}{lpName}\\{episode[EC.EPISODE_NUMBER]}_track_{ending}.wvi'
        
        
        self.savePath = WVI_PATH
        
        if not DM.existFile(WVI_PATH):
            if not path.isfile(AUDIO_WAV):
                #convert
                AFX.extractAudio(
                    episode[EC.ORIGINAL_VIDEO_PATH],
                    AUDIO,1 if ending == 'mic' else 2
                    )
                AFX.cvtAudioEx(AUDIO,AUDIO_WAV)
                
                
            sF = wave.open(AUDIO_WAV,'rb')
            
            self.length = sF.getnframes()
            self.frames = [sF.readframes(self.chunk) for i in range(self.length//self.chunk)]
            
            Thread(target=self.threadingArray,args=[[i for i in range(self.frames.__len__())]]).start()
            self.mobileThread = Thread(target=self.threadingArray,args=[])
            self.fullyLoaded = False
            self.saved = False
        else:
            sF = wave.open(AUDIO_WAV,'rb')
            
            self.length = sF.getnframes()
            self.frames = [0 for i in range(self.length//self.chunk)]
            for idx,data in enumerate(DM.loads(f'{WAVEFORM_PATH}{lpName}\\{episode[EC.EPISODE_NUMBER]}_track_{ending}.wvi')):
                self.hashMap[idx] = data
            if len(self.hashMap) == len(self.frames):
                self.fullyLoaded = True
                self.saved = True
            else:
                self.frames = [sF.readframes(self.chunk) for i in range(self.length//self.chunk)]
                Thread(target=self.threadingArray,args=[[i for i in range(self.frames.__len__())]]).start()
                self.mobileThread = Thread(target=self.threadingArray,args=[])
                self.fullyLoaded = False
                self.saved = False
        self.isLoaded = True
    def saveProgress(self):
        _copy = self.hashMap.copy()
        DM.save(f'{self.savePath}',[self.hashMap[e] for e in _copy])
        
    def get(self,start_id:int,zoom:int):
        if not self.fullyLoaded: 
            self.fullyLoaded = int(len(self.hashMap) // len(self.frames))
        if self.fullyLoaded and not self.saved:
            self.saveProgress()
            
            self.saved = True
                
        _returnData = []
        ids = []
        #! Kill mobile thread if start_id changed
        #len(self.frames) / len(self.hashMap)
        
        
        
        for i in range(start_id,(self.width)+start_id):
            ids.append(int(i*zoom))
            
        if not self.fullyLoaded: 
            if not self.mobileThread.is_alive():
                self.mobileThread = Thread(target=self.threadingArray,args=[ids])
            for id in ids:
                if id in self.hashMap:
                    _returnData.append(self.hashMap[id])
                else:
                    
                    if not self.mobileThread.is_alive():
                        self.mobileThread = Thread(target=self.threadingArray,args=[ids])#? Start from spec id
                        self.mobileThread.start()
                    if id <= len(self.frames):
                        _returnData.append(0)
        else:
            for id in ids:
                if id in self.hashMap:
                    _returnData.append(self.hashMap[id])
                    
        return _returnData,ids
    def threadingArray(self,frames):

        for i,buff in enumerate(frames):
            #if len(self.frames) > buff:
                #break
            if not self.app.isAlive or not self.isAlive: break
            if not i in self.hashMap:
                    
                fft_complex = fft(frombuffer(self.frames[buff], dtype=int16), n=self.chunk)
                fft_complex_result = [v.real * v.real + v.imag * v.imag for idx,v in enumerate(fft_complex) if idx % self.resolution == 0]
                
                scale_right = sqrt(max(fft_complex_result))
                
                scale = (self.height / scale_right) if scale_right != 0 else 0
                _result = sum([sqrt(x) * scale for x in fft_complex_result])

                    
                self.hashMap[buff] = (_result / len(fft_complex)) if _result != 0 else 0

#! Rewrite audioWave to only load prerendered


class AudioWave:
    def __init__(self,
                 fileName:str,
                 chunk:int=1024,
                 saveDivider:int=64) -> None:
        self.chunk = chunk
        self.optimizedChunk = chunk // saveDivider
        if not fileName.endswith('.wav'):
            if not path.isfile(fileName.split('.')[0] + '.wav'):
                
                    self.fileName = AFX.cvtAudioNew(fileName)
            else:
                self.fileName = fileName.split('.')[0] + '.wav'
        else:
            self.fileName = fileName
        sF = wave.open(self.fileName,'rb')
        self.length = sF.getnframes()
        self.frames = [sF.readframes(self.chunk) for i in range(self.length//self.chunk)]
        
        self.compAudioData = []
    def get(self):
        """
        ? Generates an Array Based on the File Given the values are in between 0 and 1 sometimes 2,3,4 etc. Why I dont know
        
        ! For Performance Reasons the bytes in the chunks will only be calculated chunk / optimizedChunk times
        
        """
        for buff in self.frames:
            
            fft_complex = fft(frombuffer(buff, dtype=int16), n=self.chunk)

            s = sum((int(v.real * v.real + v.imag * v.imag) for i,v in enumerate(fft_complex) if i % self.optimizedChunk == 0))

            self.compAudioData.append(s)

        maxChunk = max(self.compAudioData)
        for idx,chunk in enumerate(self.compAudioData):
            if chunk > 0:
                self.compAudioData[idx] = int((chunk / maxChunk) * 4096)
        
        #! Compression
        currentNum = -1
        compressionData = 0
        lastCompressed = -1
        _retData = []
        for idx,chunk in enumerate(self.compAudioData):
            count = 0
            currentNum = chunk
            if lastCompressed != chunk:
                for chunki in self.compAudioData[idx:]:
                    if chunki == currentNum:
                        count += 1
                    else:
                        if count > 1:
                            _retData.append(f'{count}_{currentNum}')
                        else:
                            _retData.append(currentNum)
                        break
            lastCompressed = chunk
        return _retData

class AudioWrapper:
    def __init__(self,
                 videoPath,
                 microphonPath,
                 desktopPath
                 ) -> None:
        """
        !   If Shape < 2: The Audio is not really converted to wav. 
        !   It is corruptes so create a new AudioFile
        
        """
        
        if path.exists(microphonPath):
            self.track1Data,self.track1Rate = sf.read(microphonPath)
           
            if len(self.track1Data.shape) < 2:
                print('shape of Track1 is not okay. Create new wav!')
                AFX.extractAudio(videoPath,microphonPath)
            self.track1Data,self.track1Rate = sf.read(microphonPath)
        else:
            print('shape of Track1 does not exist. Create new wav!')
            AFX.extractAudio(videoPath,microphonPath)
            self.track1Data,self.track1Rate = sf.read(microphonPath)

        if path.exists(desktopPath):
            self.track2Data,self.track2Rate = sf.read(desktopPath)
           
            if len(self.track2Data.shape) < 2:
                print('shape of Track2 is not okay. Create new wav!')
                AFX.extractAudio(videoPath,desktopPath)
            self.track2Data,self.track2Rate = sf.read(desktopPath)
        else:
            print('shape of Track2 does not exist. Create new wav!')
            AFX.extractAudio(videoPath,desktopPath)
            self.track2Data,self.track2Rate = sf.read(desktopPath)

        self.mobileThread = None
        self.audioData = None
        self.loadingComplete = False
        
    def playAudio(self):
        """
        Sollte sd beschäftigt sein. Stop
        Sollte sd nicht beschäftigt sein. Start
        
        """

    def loadCombinedAudio(self,a,b):
        self.audioData = combineTracks(self.track1Data,self.track2Data,a,b)

    def loadCombinedAudioLimiter(self,a,b):
        self.audioData = combineTracks(self.track1Data[:5*self.track1Rate],self.track2Data[:5*self.track1Rate],a,b)


class Audio2Text:
    def __init__(self,
                 fileName:str,
                 chunk:int=1024) -> None:
        self.recognizer = KaldiRecognizer(Model(lang='de'),16000)
        if not fileName.endswith('.wav'):
            if not path.isfile(fileName.split('.')[0] + '.wav'):
                
                    self.fileName = AFX.cvtAudioNew(fileName)
            else:
                self.fileName = fileName.split('.')[0] + '.wav'
        else:
            self.fileName = fileName
        sF = wave.open(self.fileName,'rb')
        self.length = sF.getnframes()
        self.frames = [sF.readframes(chunk) for i in range(self.length//chunk)]
        sF.close()
    def get(self):
        """
        Generates Two Things:
            -Wordcounter dict
            -Text Complete
        """
        _allText = ''
        _dict = {}
        for buff in self.frames:
            
            
            if self.recognizer.AcceptWaveform(buff):
                text = self.recognizer.Result()
                print(loads(text)['text'])
                for word in loads(text)['text'].split(' '):
                    if word in _dict:
                        _dict[word] += 1
                    else:
                        _dict[word] = 1
                _allText += loads(text)['text'] + '\n'
            _dict = {'words': _dict,'text': _allText}
        with open('recog.txt','w') as f:
            f.write(dumps(_dict,indent=4))

@jit(nopython=True)
def combineTracksLimiter(t1,t2,a,b,limit):

    for idy,chunk in enumerate(t1):
        if idy >= limit:
            break
        for idx,byte in enumerate(chunk):

            t1[idy][idx] = (byte*a) + (t2[idy][idx]*b)
            
    return t1  
@jit(nopython=True)
def combineTracks(t1,t2,a,b):

    for idy,chunk in enumerate(t1):

        for idx,byte in enumerate(chunk):

            t1[idy][idx] = (byte*a) + (t2[idy][idx]*b)
            
    return t1
@DeprecationWarn
def peakNormalization(filePath,savePath):
    fName = AFX.cvtAudio(filePath)
    data, rate = sf.read(fName) # load audio
    peak_normalized_audio = pyln.normalize.peak(data, -1.0)
    sf.write(savePath,peak_normalized_audio,rate)
@DeprecationWarn
def LoudnessNormalization(filePath: str,
                          savePath: str,
                          decibel: int = -15) -> None:
    """
    Normalize Audio based on given loudness
    ! Only Wave Files are Valid
    Arguments:
        filePath    load from this Path
        savePath    save to this Path
        decibel     the desired loudness
    """
    LOG.log(1,f'lod << {filePath}')
    data, rate = sf.read(filePath) # load audio
    LOG.log(1,f'mtr | rate: {rate}Hz | duration: {int(len(data) // rate//60)}:{int(len(data) // rate%60)}')
    meter = pyln.Meter(rate) # create BS.1770 meter
    LOG.log(1,f'itl')
    loudness = meter.integrated_loudness(data)
    # loudness normalize audio to {decibel} dB LUFS
    LOG.log(1,f'nor | loudness: ${round(loudness,2)} LUFS')
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, decibel)
    LOG.log(1,f'sav >> {savePath}')
    LOG.log(0,f'chg | rate: {rate}Hz | duration: {int(len(data) // rate//60)}:{int(len(data) // rate%60)} | loudness: ${round(loudness,2)} > ${decibel} LUFS')
    sf.write(savePath,loudness_normalized_audio,rate)