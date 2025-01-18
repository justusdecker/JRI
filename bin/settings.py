from bin.dataManagement import DM
from bin.constants import SettingCollection
from bin.constants import ABSOLUTE_PATH
class Settings:
    def __init__(self) -> None:
        if not DM.existFile('settings.json'):
            DM.save('settings.json',
                 SettingCollection)
        
        self._ = DM.loads('settings.json')
        
        #! Check for each option existing If not create it and save it
        okay = True
        for key in SettingCollection.keys():
            if key not in self._:   #Set Defaul If not exist
                self._[key] = SettingCollection[key]
                okay = False
        if not okay:
            DM.save('settings.json',self._)
        if not 'fastLoad' in self._:
            self._['fastLoad'] = False
            DM.save('settings.json',self._)
    def _getWindowSize(self):
        return self._['width'],self._['height'] 
    def ce(self,key,dir,default):
        if not key in dir:
            return default
        else:
            return dir[key]
    def save(self):
        DM.save('settings.json',self._)
    def _unpack(self):
        self.SIZE = self.ce('width',self._,480),self.ce('height',self._,720)
        #self.ce('width',self._,480)

SETTINGS = Settings()
