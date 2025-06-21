from os import path,mkdir,remove
from json import load,dumps
#from bin.log import LOG
from bin.constants import PATHS

class DataManagement:
    """
    Many Modules for loading and saving files
    """
    def ine(value:str,default):
        raise DeprecationWarning()
        return value if value else default

    def ifane(value:str,default):
        "Is float and not empty"
        raise DeprecationWarning()
        spl = value.split('.')
        if value != '' and spl.__len__() == 2:
            id = spl[0].replace('-','').isdecimal() + spl[1].isdecimal()
            lr = spl[0] == '' + spl[0] == ''
            
            if lr > 1 or id < 1:
                return default
            
            return float(value)
        else:
            if value.replace('-','').isdecimal():
                return float(value)
            return default
    
    def idane(value:str,default):
        "Is decimal and not empty"
        raise DeprecationWarning()
        if value != '' and value.replace('-','').isdecimal():
            return int(value)
        else:
            return default
        
    def get_file_size(filePath:str):
        """
        Returns the fileSize in Bytes
        """
        
        if path.isfile(filePath):
            
            return path.getsize(filePath)
        
    def save(filePath:str,data:dict | tuple | list):
        """
        Saves the Data in JSON File Format With Indent 4
        """
        raise DeprecationWarning()
        #LOG.nlog(1,'save file: $',[filePath])
        with open(filePath,'w') as fOut:
            
            fOut.write(
                dumps(
                    data,
                    indent=4
                    )
                )
            
    def loads(filePath:str):
        """
        Reads the Data from JSON File Format and converts it to Dict or List
        """
        #raise DeprecationWarning()
        #LOG.nlog(1,'load file: $',[filePath])
        with open(filePath,'r') as fIn:
            
            return load(fIn)
        
    def remove_file(filePath: str):
        if path.isfile(filePath):
            #LOG.nlog(2,'Removed : $',[filePath])
            remove(filePath)
        else:
            pass
            #LOG.nlog(3,'File not found : $',[filePath])
         
    def load_def(filePath:str,searchL:list | tuple,default):
        """
        Returns Specific Value in a JSON File if not existing return Default
        """
        
        with open(filePath,'r') as fIn:
            
            _ret = load(fIn)
            
            for key in searchL:
                
                if key in _ret:
                    
                    _ret = _ret[key]
                    
                else:
                    
                    return default
                    
            return _ret
        
    def load_save(filePath:str,data:dict):
        """
        Load, Edit & Save
        """
        
        _sav = load(filePath)
        
        _sav |= data
        
        DataManagement.save(filePath,_sav)
    def exist_file(filePath):
        if filePath is not None:
            return path.isfile(filePath)
        return False
    def create_folder(filePath):
        
        if not path.isdir(filePath):
            #LOG.nlog(1,'created Folder: $',[filePath])
            mkdir(filePath)

DM = DataManagement
#! essentialFAFOnStart


DM.create_folder(PATHS.root)
DM.create_folder(PATHS.audio)
DM.create_folder(PATHS.letsplay)
DM.create_folder(PATHS.thumbnail)
DM.create_folder(PATHS.logos)
DM.create_folder(PATHS.fonts)
DM.create_folder(PATHS.att)
DM.create_folder(PATHS.wv)