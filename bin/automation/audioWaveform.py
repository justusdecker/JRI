
import wave
from math import sqrt
from numpy import frombuffer,int16
from numpy.fft import fft
from time import time
from os import path
from fx.audio import AFX
from json import dumps

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
                self.compAudioData[idx] = chunk / maxChunk

        return self.compAudioData

        

t = time()
D = AudioWave('data\\audio\\subnautica\\1_subnautica_track.mp3',saveDivider=64).get()
print(time() - t)
with open('test.json','w') as f:
    f.write(dumps(D))
