from bin.dataManagement import DM
from bin.constants import SettingCollection

class Settings:
    def __init__(self) -> None:
        if not DM.existFile('settings.json'):
            DM.save('settings.json',
                 SettingCollection)
        self.__settings: dict = DM.loads('settings.json')
        if not isinstance(self.__settings,dict):
            raise TypeError('SETTINGS MUST BE A DICT')
        
    def save_settings(self) -> None:
        DM.save('settings.json',{
            'width': self.width,
            'height': self.height,
            'obsDirPath': self.obs_path,
            'obsHost': self.obs_ip,
            'obsPassword': self.obs_pw,
            'obsPort': self.obs_port,
            'obsTimeout': self.obs_timeout
        })
    @property
    def width(self) -> int:
        return self.__settings.get('width',1280)
    @property
    def height(self) -> int:
        return self.__settings.get('height',720)
    @property
    def obs_path(self) -> str:
        return self.__settings.get('obsDirPath','C:\\Program Files (x86)\\Steam\\steamapps\\common\\OBS Studio\\bin\\64bit\\')
    @property
    def obs_ip(self) -> str:
        return self.__settings.get('obsHost','')
    @property
    def obs_pw(self) -> str:
        return self.__settings.get('obsPassword','')
    @property
    def obs_port(self) -> int:
        return self.__settings.get('obsPort',4455)
    @property
    def obs_timeout(self) -> int:
        return self.__settings.get('obsTimeout',1)
    @property
    def window_size(self) -> tuple[int,int]:
        return self.width, self.height

SETTINGS = Settings()
