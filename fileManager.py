

from bin.letsPlayFile import LetsPlayFile
from os import listdir,remove,path
from bin.constants import LETSPLAY_PATH,AUDIO_PATH
def removeFile(filePath: str):
    if path.isfile(filePath):
        remove(filePath)
        print(f'removed {filePath}')
    else:
        print(f'Dont exist: {filePath}')
for file in listdir(LETSPLAY_PATH):
    LPF = LetsPlayFile(LETSPLAY_PATH + file)
    _eps = [x['episodeNumber'] for x in LPF._getEpisodes() if x['status'] == 31]
    
    if _eps.__len__() > 0:
        print(_eps)
        if input(f'delete all files for this lp [{LPF._getName()}] episodes?') == 'y':
            for idx,episode in enumerate(LPF._getEpisodes()):
                if episode['status'] == 31:  # TODO : Use the new ST values
                    print(f"{str(LPF._getName()):<15}{episode['episodeNumber']:<4}{str(episode['episodeTitle']):<50}")
                    #if input('delete all files for this episode?') == 'y':
                    removeFile(episode['path'])
                    removeFile(episode['audioFilePath'])
                    removeFile(episode['thumbnailPath'])
                    compPath = f'{AUDIO_PATH}{LPF._getName()}\\comps\\{idx+1}_comp.mp3'
                    removeFile(compPath)
                    LPF._setEpisode(idx,'waveForm',None)
                    LPF._setEpisode(idx,'status',64)  # TODO : Use the new ST values
            LPF.save()