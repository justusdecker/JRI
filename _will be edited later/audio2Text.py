try: 
    from vosk import Model,KaldiRecognizer
except:
    pass
from json import loads,dumps
import wave
from os import path
from bin.fx.audio import AFX

class Audio2Text:
    def __init__(self,
                 fileName:str,
                 chunk:int=4096) -> None:
        self.recognizer = KaldiRecognizer(Model(lang='de'),60000)
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
    def get(self,filePath:str):
        """
        Generates Two Things:
            -Wordcounter dict
            *Text Complete
        """
        #RETRY if too many ''
        
        _allText = ''
        empty = 0
        finished = False
        for _try in [16000,48000,60000]:
            _dict = {}
            if finished:
                break
            self.recognizer = KaldiRecognizer(Model(lang='de'),_try)
            
            print(f'try: {_try}')
            for buff in self.frames:
                
                
                if self.recognizer.AcceptWaveform(buff):
                    text = self.recognizer.Result()
                    if loads(text)['text'] == '':
                        empty += 1
                    else:
                        empty = 0
                    if empty > 10:
                        
                        break
                    print(loads(text)['text'])
                    loads(text)['text']
                    for word in loads(text)['text'].split(' '):
                        if word in _dict:
                            _dict[word] += 1
                        else:
                            _dict[word] = 1
                    _allText += loads(text)['text'] + '\n'
                
            finished = True
        with open(filePath,'w') as f:
            f.write(dumps(_dict,indent=4))
        return _dict

