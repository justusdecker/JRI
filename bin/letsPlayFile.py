from bin.dataManagement import DM
from bin.appinfo import VERSION
from moviepy.video.io.VideoFileClip import VideoFileClip
from bin.minfuncs import getHexDoubleZeros
from bin.constants import LC,EC,DEFAULT_LPF_FILE
from bin.constants import LETSPLAY_PATH,THUMBNAIL_PATH,AUDIO_PATH,ABSOLUTE_PATH
from os import listdir
from typing import Any
from bin.crashHandler import QuestionBox
from pygame import key,K_LCTRL

class LetsPlayFile:
    #Defaults
    default_EpisodeLength: int = 900
    default_IconPath: str = ''
    default_Name: str = 'None'
    default_Description: str = ''
    default_TitleEnding: str = ''
    default_gameName: str = ''
    default_Tags: list = []
    absolutePath = 'E:\\Server\\Programmierung\\JRI\\'
    default_ThumbnailAutomationData: dict = {
        "text_epNum": {
            "text": "",
            "font": "E:\\Server\\Programmierung\\JRI\\bin\\fonts\\Jersey.ttf",
            "align": "center",
            "size": 100,
            "pos": [
                800,
                260
            ],
            "rot": -15,
            "cropping": [
                0,
                0,
                0,
                0
            ],
            "outline": {
                "xMinus": 2,
                "xPlus": 2,
                "yMinus": 2,
                "yPlus": 2,
                "color": [
                    [
                        50,
                        50,
                        50
                    ],
                    [
                        14,
                        14,
                        14
                    ],
                    [
                        14,
                        14,
                        14
                    ],
                    [
                        50,
                        50,
                        50
                    ]
                ]
            }
        },
        "images": [
            {
                "path": "logos\\7d2d_logo.png",
                "scale": 0.4,
                "pos": [
                    640,
                    140
                ],
                "rot": 0,
                "align": "center",
                "cropping": [
                    0,
                    0,
                    0,
                    0
                ]
            }
        ]
    }
    def __init__(self,filePath:str) -> None:
        self.filePath = filePath
        self.load()
    def _isIdentical(self,epIndex:int,value:dict) -> bool:
        for key in self.data['episodes'][epIndex]:
            if key in value:
                if value != self.data['episodes'][epIndex]:
                    return False
            else:
                return False
        return True
    def _getEpisodes(self) -> dict[str,Any]:
        return self.data['episodes']
    def _addEpisode(self,data:dict):
        self.data['episodes'].append(data)
    def _getEpisodeCount(self):
        return len(self.data['episodes'])
    def _getEpisodeExist(self,episodeId:int,key:str):
        return key in self.data['episodes'][episodeId]
    def _getEpisodeEx(self,episodeId:int,key:str):
        return self.data['episodes'][episodeId][key]
    def _getEpisode(self,episodeId:int):
        return self.data['episodes'][episodeId]
    def _setEpisode(self,episodeId:int,key:str,value:list):
        self.data['episodes'][episodeId][key] = value
    def _getGameName(self):
        if not self._isIn('gameName',self.data):
            self._setTitleEnding(self.default_gameName)
        return self.data['gameName']
    def _setGameName(self,value:str):
        self.data['gameName'] = value
    def _getTitleEnding(self):
        if not self._isIn('titleEnding',self.data):
            self._setTitleEnding(self.default_TitleEnding)
        return self.data['titleEnding']
    def _setTitleEnding(self,value:str):
        self.data['titleEnding'] = value
    
    
    def _getDescription(self):
        if not self._isIn('description',self.data):
            self._setDescription(self.default_Description)
        return self.data['description']
    def _setDescription(self,value:str):
        self.data['description'] = value
    
    def _getTags(self):
        if not self._isIn('tags',self.data):
            self._setTags(self.default_Tags)
        return self.data['tags']
    def _setTags(self,value:list):
        self.data['tags'] = value
    
    def _getThumbnailAutomationData(self):
        if not self._isIn('thumbnailAutomationData',self.data):
            raise Exception('No TAD')
        return self.data['thumbnailAutomationData']
    
    def _setThumbnailAutomationData(self,key:str,value):
        if not self._isIn('thumbnailAutomationData',self.data):
            raise Exception('No TAD')
        self.data['thumbnailAutomationData'][key] = value
    
    def _setThumbnailAutomationDataFont(self,value:str):
        if not self._isIn('thumbnailAutomationData',self.data):
            raise Exception('No TAD')
        self.data['thumbnailAutomationData']['text_epNum']['font'] = value
        
    def _setThumbnailAutomationDataLogo(self,value:str):
        if not self._isIn('thumbnailAutomationData',self.data):
            raise Exception('No TAD')
        self.data['thumbnailAutomationData']['images'][0]['path'] = value
        
    def _getEpisodeLength(self):
        if not self._isIn('episode_length',self.data):
            self._setEpisodeLength(self.default_EpisodeLength)
        return self.data['episode_length']
    def _setEpisodeLength(self,value:int):
        self.data['episode_length'] = value
    
    def _getIconPath(self):
        if not self._isIn('icon',self.data):
            self._setIconPath(self.default_IconPath)
        return self.data['icon']
    def _setIconPath(self,value:str):
        self.data['icon'] = value
        
    def _getName(self):
        if not self._isIn('name',self.data):
            self._setName(self.default_Name)
        return self.data['name']
    def _setName(self,value:str):
        self.data['name'] = value
        
    def _getVersion(self):
        if not self._isIn('version',self.data):
            self.data['version'] = VERSION
        return self.data['version']
    
    def _isIn(self,key:str='',data:dict={}):
        return key in data
    
    def updateVersion2Newest(self):
        #HIGH:
        if not 'version' in self.data:      #1.5 > 1.6
            
            for episode in self.data['episode']:
                
                if DM.existFile(episode['path']):
                    
                    episode['length'] = VideoFileClip(episode['path']).duration
                else:
                    episode['length'] = None
                    
                episode['videoFileSize'] = DM.getFileSize(episode['path'])
                episode['audioFilePath'] = ''
                episode['compFilePath'] = ''
                episode['youTubeVideoId'] = ''
                episode['audioFilePath'] = ''
                episode['titleGenerationWords'] = []
                episode['lowResVideo'] = ''
        if self._getVersion() != VERSION:
            print('something changed!')
        self.save()
    def _getBackUpPath(self):
        pass
    def createBackUp(self):
        DM.createFolder(f'{ABSOLUTE_PATH}')
        DM.createFolder(f'{LETSPLAY_PATH}backups')
        fName,ending = self.filePath.split('\\')[-1].split('.')
        DM.save(f"{LETSPLAY_PATH}backups\\{fName}_backup.{ending}",self.data)
    def load(self):
        try:
            self.data = DM.loads(self.filePath)
            self.createBackUp()
        except:
            fName,ending = self.filePath.split('\\')[-1].split('.')
            
            self.data = DM.loads(f"data\\backups\\{fName}_backup.{ending}",self.data)
            DM.save()
    def save(self):
        DM.save(self.filePath,self.data)

class Episode:
    def __init__(self,data:dict) -> None:
        pass

class LetsPlayComp:
    def __init__(self,fontPath,imgPath) -> None:

        self.imgPath = imgPath
        self.fontPath = fontPath
        self.start = 0
        self.load()
    
    def setTADInputs(self,l:list,cp,cs,lpf:list):
        self.dataTAD = l.copy()
        self.cpTAD = cp
        self.csTAD = cs
        self.dataLPF = lpf.copy()
        
    
    def change2Episode(self,side:int=0,callback:Any=None):
        """
            Change the current Episode
        """
        add = 0
        if key.get_pressed()[K_LCTRL]:
            add = 9
            
        
        if side == 1:
            self.start += (1 + add)
        else:
            self.start -= (1 + add)
            
        if self.start > len(self.episodesInQueue) - 1:
            self.start = len(self.episodesInQueue) - 1
        elif self.start < 0:
            self.start = 0
        if callback is not None:
            callback()
    
    def saveLetsPlays(self,*_): self.save()
    
    def load(self,*_):
        
        self.letsPlayFiles = []
        self.episodesInQueue = []

        DIR = listdir(LETSPLAY_PATH)
        DIR = [f for f in DIR if f.endswith('.json')]
        if DIR.__len__() == 0:
            return False #! Program crashed
        _deletableFiles = []
        for letsPlayIndex, filePath in enumerate(DIR):
            
            LPF = LetsPlayFile(LETSPLAY_PATH + filePath)
            self.letsPlayFiles.append(LPF)
            for episodeId in range(LPF._getEpisodeCount()):
                if LPF._getEpisodeEx(episodeId,'status') < 31: # TODO : Use the new ST values
                    self.episodesInQueue.append((letsPlayIndex,episodeId))
                else:
                    for p in [
                        LPF._getEpisodeEx(episodeId,EC.ORIGINAL_AUDIO_PATH),
                        LPF._getEpisodeEx(episodeId,EC.ORIGINAL_VIDEO_PATH),
                        LPF._getEpisodeEx(episodeId,EC.THUMBNAIL_PATH),
                        f'{AUDIO_PATH}{LPF._getName()}\\comps\\{episodeId+1}_comp.mp3'
                        ]:
                        if DM.existFile(p):
                            _deletableFiles.append(p)
                    LPF._setEpisode(episodeId,EC.STATUS,64)  # TODO : Use the new ST values
        _ = "\n".join(_deletableFiles)
        if len(_deletableFiles) > 0:
            _answer = QuestionBox(['Unused Data Detected',f'Delete? {_}'])
            if _answer == 6:
                self.deleteFiles(_deletableFiles)  
    def deleteFiles(self,_data):
        for f in _data:
            
            DM.removeFile(f)
                    
    def save(self):
        for letsPlayFile in self.letsPlayFiles:
            letsPlayFile.save()
            
    def getLPDataComp(self) -> dict:
        """
        Returns:
            dict: The Complete Lets Play File Data
        """
        return self.letsPlayFiles[self.episodesInQueue[self.start][0]].data
    
    def getIsLastEpisode(self) -> bool:
        """
        Returns:
            bool: Returns whether the current Episode is the last in the Lets Play File
        """
        return self.getEpisodeIndex() == self.getLPEpisodeAmmount() - 1
    
    def getLPIndex(self) -> int:
        """
        Returns:
            int: Current Index
        """
        return self.episodesInQueue[self.start][0]
    
    def setCuLp(self,key,value):
        self.letsPlayFiles[self.episodesInQueue[self.start][0]][key] = value
    
    def getCuLp(self,key):
        return self.getLPDataComp()[key]
    
    def getEpisodeIndex(self) -> int:
        return self.episodesInQueue[self.start][1]
    
    def getLPF(self) -> LetsPlayFile:
        return self.letsPlayFiles[self.getLPIndex()]
    
    def getLPEpisodeAmmount(self) -> int:
        return self.getLPF()._getEpisodeCount()
    
    def getCuEpKeyExist(self,key: str = '') -> bool: 
        return self.getLPF()._getEpisodeExist(self.getEpisodeIndex(),key)
    
    def getCuEpComp(self) -> dict:
        return self.getLPF()._getEpisode(self.getEpisodeIndex())
    
    def getCuEp(self,key: str = '') -> str | int | float | dict | list | bool:
        return self.getLPF()._getEpisodeEx(self.getEpisodeIndex(),key)
    
    def setCuEp(self,key: str = '',value: Any = None) -> None: 
        self.getLPF()._setEpisode(self.getEpisodeIndex(),key,value)

    def getThumbnailPath(self):
        return f'{THUMBNAIL_PATH}{self.getCuLp(LC.NAME)}\\{self.getCuEp(EC.EPISODE_NUMBER)}_{self.getCuLp(LC.NAME)}_Thumbnail.png'
    
    def getVideoPath(self):
        return self.getCuEp(EC.ORIGINAL_VIDEO_PATH)

    def getAudioPath(self):
        return self.getCuEp(EC.ORIGINAL_AUDIO_PATH)

    def getCompPathWOF(self):
        return f'{AUDIO_PATH}{self.getCuLp(LC.NAME)}\\comps\\'

    def getCompPath(self):
        return f'{AUDIO_PATH}{self.getCuLp(LC.NAME)}\\comps\\{self.getCuEp(EC.EPISODE_NUMBER)}_comp.mp3'
    
    def setTAD(self,data):
        self.getLPF().data[LC.THUMBNAIL_AUTOMATION_DATA] = data
    
    def getTAD(self):
        return self.getCuLp(LC.THUMBNAIL_AUTOMATION_DATA)
    
    def _setNewThumbnailAutomationData(self,*_):
        """
        self.jtgTextSizeInput
        """

        
        
        TAD = self.getTAD()
        _COPY = TAD.copy()
        
        bgExist = 'background' in TAD
        
        TE = TAD['text_epNum']
        IMG = TAD['images']
        
        if bgExist:
            BG = TAD['background']
        else:
            BG = {}
        
        TE['font'] = DM.ine(self.fontPath.path,TE['font'])
        TE['size'] = DM.ifane(self.dataTAD[0].text,TE['size'])
        TE['pos'] = DM.idane(self.dataTAD[1].text,TE['pos'][0]),DM.idane(self.dataTAD[2].text,TE['pos'][1])
        TE['rot'] = DM.ifane(self.dataTAD[3].text,TE['rot'])
        
        TAD['text_epNum'] = TE  #* Reapply Values
        
        IMG[0]['path'] = DM.ine(self.imgPath.path,IMG[0]['path'])
        IMG[0]['scale'] = DM.ifane(self.dataTAD[4].text,IMG[0]['scale'])
        IMG[0]['pos'] = DM.idane(self.dataTAD[5].text,IMG[0]['pos'][0]),DM.idane(self.dataTAD[6].text,IMG[0]['pos'][1])
        IMG[0]['rot'] = DM.ifane(self.dataTAD[7].text,IMG[0]['rot'])
        
        R = int(self.cpTAD.sliderR.sliderPercent * 255)
        G = int(self.cpTAD.sliderG.sliderPercent * 255)
        B = int(self.cpTAD.sliderB.sliderPercent * 255)
        
        R = getHexDoubleZeros(hex(R).replace('0x',''))
        G = getHexDoubleZeros(hex(G).replace('0x',''))
        B = getHexDoubleZeros(hex(B).replace('0x',''))
        
        TE['color'] = f'#{R}{G}{B}'
        
        TAD['images'] = IMG  #* Reapply Values
        
        #Weise Alle Werte zu
        if bgExist:
            BG['position'] = DM.idane(self.dataTAD[8].text,BG['position'][0]),DM.idane(self.dataTAD[9].text,BG['position'][1])
            
            BG['randomPositionX'] = DM.idane(self.dataTAD[10].text,BG['randomPositionX'])
            BG['randomPositionY'] = DM.idane(self.dataTAD[11].text,BG['randomPositionY'])
            
            BG['rotation'] = DM.ifane(self.dataTAD[12].text,BG['rotation'])
            
            BG['randomRotation'] = DM.ifane(self.dataTAD[13].text,BG['randomRotation'][0]),DM.ifane(self.dataTAD[14].text,BG['randomRotation'][1])
            BG['randomScale'] = DM.idane(self.dataTAD[15].text,BG['randomScale'][0]),DM.idane(self.dataTAD[16].text,BG['randomScale'][1])
            
            BG['scale'] = DM.ifane(self.dataTAD[17].text,BG['scale'])
            
            BG['hue'] = DM.ifane(self.dataTAD[18].text,BG['hue'])
            BG['saturation'] = DM.ifane(self.dataTAD[19].text,BG['saturation'])
            BG['lightness'] = DM.ifane(self.dataTAD[20].text,BG['lightness'])
            BG['center'] = self.csTAD.toggle
        
            TAD['background'] = BG  #* Reapply Values
        else:#!
            BG['position'] = DM.idane(self.dataTAD[8].text,0),DM.idane(self.dataTAD[9].text,0)
            
            BG['randomPositionX'] = DM.idane(self.dataTAD[10].text,0)
            BG['randomPositionY'] = DM.idane(self.dataTAD[11].text,0)
            
            BG['rotation'] = DM.ifane(self.dataTAD[12].text,0)
            
            BG['randomRotation'] = DM.ifane(self.dataTAD[13].text,0),DM.ifane(self.dataTAD[14].text,0)
            BG['randomScale'] = DM.idane(self.dataTAD[15].text,0),DM.idane(self.dataTAD[16].text,0)
            
            BG['scale'] = DM.ifane(self.dataTAD[17].text,1)
            
            BG['hue'] = DM.ifane(self.dataTAD[18].text,0)
            BG['saturation'] = DM.ifane(self.dataTAD[19].text,1)
            BG['lightness'] = DM.ifane(self.dataTAD[20].text,1)
            BG['center'] = self.csTAD.toggle
        
            TAD['background'] = BG  #* Reapply Values
        print(TAD['background'])
        self.setTAD(TAD)

    def getEssentialFolderCommands(self):
        _temp = self.getCuEp(EC.ORIGINAL_VIDEO_PATH).split('/')[0:-1]
        _path = ''
        for i in _temp:
            _path += i + '\\'
        return [
            f"explorer {self.getLPF().filePath}",
            f"explorer {AUDIO_PATH}{self.getCuLp(LC.NAME)}",
            f"explorer {_temp}",
            f"explorer {THUMBNAIL_PATH}{self.getCuLp(LC.NAME)}",
        ]
    
    def updateLetsPlaySettings(self,*_):
        if self.dataLPF[0].text != '':
            self.getLPF()._setName(self.dataLPF[0].text)
        if self.dataLPF[1].text != '':
            self.getLPF()._setIconPath(self.dataLPF[1].text)
    
        
    
    #change Lets Play
    
    #Getter & Setter
 
 
def createDefaultLPF(*_):
    DM.save(LETSPLAY_PATH + 'default.json',DEFAULT_LPF_FILE)