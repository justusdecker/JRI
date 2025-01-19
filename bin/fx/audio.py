
from os.path import isfile

import subprocess

from moviepy.audio.io.AudioFileClip import AudioFileClip

from numba import jit

from bin.debugFunctions import debugExecutionTimeCheck

class AFX:
    """
    A Collection of Audio FX and Convert Methods!
    """
    
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
    def LoudnessNormalization(filePath,savePath,decibel:int = -15):
        f"Command: ffmpeg -i {filePath} -filter:a \"loudnorm\"{decibel} {savePath}"
        
        subprocess.run(
                [
                    'ffmpeg',
                    '-y',
                    '-i',
                    filePath,
                    '-af',
                    f'loudnorm={decibel}',
                    savePath
                    ]
                )
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