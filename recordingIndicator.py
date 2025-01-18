import subprocess
import os

from bin.settings import SETTINGS
from bin.obsObserver import OBSObserver
from bin.thumbnailGenerator import ThumbnailGenerator

from bin.programs import LetsPlayPicker,RecordingIndicator,RUNTIMESETTIGS
from bin.crashHandler import CrashBox,ERRORIDS

oldDir = os.getcwd()
os.chdir(SETTINGS._['obsDirPath'])
os.system(SETTINGS._['obsDirPath'] + "obs64.exe")
#subprocess.Popen(SETTINGS._['obsDirPath'] + "obs64.exe",stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
os.chdir(oldDir)
JTG = ThumbnailGenerator()


LPP = LetsPlayPicker()
LPP.run()

if not LPP.crashed and RUNTIMESETTIGS['letsPlay'] is not None and RUNTIMESETTIGS['path'] is not None:
    if RUNTIMESETTIGS['letsPlay']._getName() == '':
        CrashBox([f'[{ERRORIDS.LPFNAMEEMPTY}] LPF is Empty', 'Please set a name for LPF'])
    else:
        T = RecordingIndicator()
        OBSO = OBSObserver(T,RUNTIMESETTIGS['letsPlay'],RUNTIMESETTIGS['path'])

        while T.isAlive:
            OBSO.update()
            
            T.update(OBSO)
