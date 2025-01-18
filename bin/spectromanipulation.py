import numpy as np
from numpy.fft import rfftfreq,irfft
from scipy.fft import rfft
import soundfile as sf
from tkinter import filedialog
import cmath

from log import LOG
#from spectrogram import my_specgram #! Fehlt
class SpectroManipulation:
    DTYPE = np.float32
    def __init__(self,
                 filePath,
                 low: int = 1,
                 high: int = 100,
                 factor: int = 0):
        LOG.log(1,f'loading <<< {filePath}')
        self.data, self.samplerate = sf.read(filePath,dtype=self.DTYPE)
        
        self.duration = len(self.data)
        self.total_ts_sec = self.duration/self.samplerate
        self.absSignalCoeff,self.angleSignalCoeff = self.getRfft()
        self.frequencies = rfftfreq(self.duration, 1 / self.samplerate)
        self.low,self.high,self.factor = low,high,factor
        # The maximum frequency is half the sample rate
        self.freqLen = len(self.frequencies)
        self.points_per_freq = self.freqLen / (self.samplerate / 2)
    def save2Disk(self,fileName):
        print('pfb')
        self.processFrequencyBand(self.low,self.high,self.factor)
        print('w')
        sf.write(
            fileName,
            self.createNewSignal().astype(self.DTYPE), 
            self.samplerate
            )
        self.kill()
    def createNewSignal(self):
        return self.reconstructCoefficients()
        #return irfft(_ret)
    
    def processFrequencyBand(self,low, high, factor):
        for f in self.frequencies:
            if low < f < high:
                f_idx = int(self.points_per_freq * f)
                self.absSignalCoeff[f_idx] = self.absSignalCoeff[f_idx] * factor
                
    def reconstructCoefficients(self):
        print('rcc')
        #! Only Take Mono NOT Stereo
        # constructing fft coefficients again (from amplitudes and phases) after processing the amplitudes
        _nFftCoeff = np.zeros((self.freqLen,), dtype=complex)
        #! MEMORY LEAK AHEAD !
        for f in self.frequencies:
            f_idx = int(self.points_per_freq * f)
            _a = 1j * self.angleSignalCoeff[f_idx-1]
            _b = cmath.exp(_a)
            _c = _b * self.absSignalCoeff[f_idx-1]
            _nFftCoeff[f_idx-1] = _c #
        self.absSignalCoeff = np.array([0])
        self.angleSignalCoeff = np.array([0])
        
        return irfft(_nFftCoeff)
    
    def getRfft(self):
        """
        Usage
        -----
        
        Get the ``np.abs`` & ``np.angle`` of ``self.data``
        
        Attention
        -----
        The Memory Usage is 
        
        .. gigantic::
        
        Up to 4.4 gigs for a 30 minute Mono Audio Clip
        """

        rfftCoeff = rfft(self.data,overwrite_x=True)
        return np.abs(rfftCoeff) , np.angle(rfftCoeff)
    def kill(self):
        
        del self
        
SM = SpectroManipulation(filedialog.askopenfilename())
SM.save2Disk('test.mp3')
input('finished')