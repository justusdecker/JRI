from bin.letsplay_file import LetsPlayFile
from os import listdir
from bin.data_management import DM

def cS2BS(inp:str):
    """Convert Slash to Backslash"""
    if inp is not None:
        return inp.replace('/','\\')
    return ''

from bin.constants import EC

class FinalizedTree:
    """
    A Tree View of the Lets Play Files
    -----
    .. addFile::
    
        :Arguments:
            
            ``episode`` : An Episode Like Object from ``LPF``
    
        :Cache: 
            
            ``path`` , ``audioFilePath`` & ``thumbnailPath`` for later use 

        :Return: 
        
            None
        
        
    .. getFolder::
        ``addFile`` : pass
    """
    def __init__(self) -> None:
        self.data = {}
        self.lpfs = []
    def addFile(self, episode):
        _pre = []
        for i in [EC.THUMBNAIL_PATH,EC.ORIGINAL_VIDEO_PATH,EC.ORIGINAL_AUDIO_PATH]:
            
            _folder = self.getFolder(episode[i])
            _file = self.getFileName(episode[i])
            _pre.append((_folder,_file))
        
        if episode['lp'] not in self.data:
            self.data[episode['lp']] = []
        self.data[episode['lp']].append((_pre,episode))
    def getFolder(self,file:str):
        return '\\'.join(cS2BS(file).split('\\')[0:-1])
    def getFileName(self,file:str):
        return cS2BS(file).split('\\')[-1]
    def getTextManipulated(self,file,folder,ent):
        #?File is no longer in existance and status is finished
        if not DM.existFile(f'{folder}\\{file}') and ent['status'] >= 31:
            return f'\033[1;90m\033[9m{file}\033[0m'
        
        #!File is no longer in existance and status is NOT finished
        #?Something possibly went wrong
        if ent['status'] < 31 and not DM.existFile(f'{folder}\\{file}'):
            return f'\033[1;31m{file}\033[0m'
        
        return f'{file}'
    def getText(self,file,folder,ent):
        return f'{folder}\\{file}', DM.existFile(f'{folder}\\{file}') and ent['status'] < 31
    def run(self):

        for file in listdir(LETSPLAY_PATH):
            LPF = LetsPlayFile(LETSPLAY_PATH + file)
            for episode in LPF._getEpisodes():
                _epCopy = episode.copy()
                _epCopy['lp'] = LPF._getName()
                _epCopy['lpf'] = LPF

                self.addFile(_epCopy)
    def renderTree(self):
        _ret = []
        _lpfs = []
        _epi = []
        for key in self.data:
            _ret.append([f'#folder|{key}'])
            _lpfs.append(None)
            _epi.append([None,None])
            for entry in self.data[key]:
                _l = []
                for f in entry[0]:
                    
                    _path,_exist = self.getText(f[1],f[0],entry[1])
                    
                    _l.append(f'#file|{_exist}|{_path}')
                    _lpfs.append(entry[1]['lpf'])
                    _epi.append([entry[1]['lp'],entry[1]['episodeNumber']])
                _ret.append(_l)
                #print(f'{self.getTextManipulated(entry[0][0][1],entry[0][0][0],entry[1]) } {self.getTextManipulated(entry[0][1][1],entry[0][1][0],entry[1])} {self.getTextManipulated(entry[0][2][1],entry[0][2][0],entry[1])} {entry[1]["episodeNumber"]} {entry[1]["lp"]}')
        return _ret,_lpfs,_epi
