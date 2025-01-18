from tkinter import filedialog
from json import load
from bin.dataManagement import DM
from bin.log import LOG
from os import remove,path

lpFilePath = filedialog.askopenfilename()
with open(lpFilePath) as fIn:LPINFO = load(fIn)
directory = filedialog.askdirectory()

for idx,episode in enumerate(LPINFO['episodes']): 
    d = episode['path'],episode['path'].split('/')[-1] 
    if path.isfile(episode['path']):
        old = episode['path']
        if old != directory + '/' + episode['path'].split('/')[-1]:
            with open(episode['path'],'rb') as fIn:
                with open(directory + '/' + episode['path'].split('/')[-1],'wb') as fOut:
                    LOG.log(1,f'start moving: ${episode["episodeNumber"]}')
                    fOut.write(fIn.read())
                    LPINFO['episodes'][idx]['path'] = directory + '/' + episode['path'].split('/')[-1]
            LOG.log(1,f'moved: ${episode["episodeNumber"]}')
            DM.save(lpFilePath,LPINFO)
            remove(old)
        else:
            LOG.log(3,f'skipped: ${episode["episodeNumber"]}')
LOG.log(1,f'finished...')