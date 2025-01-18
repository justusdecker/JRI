import gdown
from bin.dataManagement import DM
from bin.appinfo import VERSION
print(f'Current Version: [{VERSION[3]}]{VERSION[0]}.{VERSION[1]}.{VERSION[2]}')

DM.createFolder('_temp\\')

FILELINK = 'https://drive.google.com/uc?id=17YBV3EWbYxyX7Nac5gP6PVV36N5I49WK'
VERSIONLINK = 'https://drive.google.com/uc?id=1CW2mAoiaLCU8ty0sOVO0gE7WffoI8EdE'
overwrite = False
if input('force update? [y/n]: ') == 'y':
    overwrite = True
try:
    print(f'Start Download: version.txt')
    gdown.download(VERSIONLINK,f'_temp\\version.txt',quiet=True)
    print(f'Download Completed: version.txt')
    
    updateable = True
except Exception as E:
    updateable = False
    print(f'Cant Download: version.txt. Exiting!')
if overwrite or updateable:
    try:
        print(f'Start Download: files.json')
        gdown.download(FILELINK,f'_temp\\files.json',quiet=True)
        print(f'Download Completed: files.json')
        filesOkay = True
    except Exception as E:
        filesOkay = False
        print(f'Cant Download: files.json. Exiting!')


#All needed links into files.jri >> google
#check version file
#check

if (filesOkay and updateable) or (filesOkay and overwrite):
    LINKS = DM.loads('_temp\\files.json')
    for name,format,link in LINKS:
        try:
            print(f'Start Download: {name}')
            gdown.download(link,f'_temp\\{name}.{format}',quiet=True,fuzzy=True)
            print(f'Download Completed: {name}')
        except Exception as E:
            print(f'Cant Download: {name}')
