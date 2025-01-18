from pygame import Color



class Log:
    """
    The Logging Module
    """
    def __init__(self,
                 file:str='log.txt') -> None:
        """Create & Clean the Log File"""
        with open('log.txt','w') as f:
            f.write('')
    def getDefaultModuleInfo(self):
        return {
            'version': '02102024:1.6',
            'name': 'log',
            'state': 'isFinished',
            'copyright': 'Justus Decker'
        }
    def initLog(self,__module__:dict):
        """
        This is a predefined Log Message for loading Modules
        """
        self.log(msg= f"Loaded Version: ${__module__['version']} of Module: ${__module__['name']} State: ${__module__['state']}")
    def getRGB(self,col,text):
        col = Color(col)
        return f'\033[38;2;{col.r};{col.g};{col.b}m{text}\033[0m'
    def clog(self,id:int=0,msg:str='',vars: list | tuple = [],ind: list | tuple = []):
        "⚠❗💠💬"
        """
        Checks value is identical with...
        Prints & Write custom Log Messages to the logfile: {file}
        [0] Debug Log
        [1] Info Log
        [2] Warning Log
        [3] Error Log
        """

        #$ Declares a variable
        
        colorMap = [
            '#CCFF99',
            '#FFCC99',
            '#FF9999',
            '#99FFFF',
            '#FFFF99',
            '#FF99FF',
            '#9999FF',
            '#FF99CC',
            '#FFCC00'
        ]
        
        entry = msg.split(' ')
        output = ''
        varStep = 0
        ok = True
        for idx,word in enumerate(entry):
            if word == '$' and varStep <= len(vars) - 1:
                #print(vars[varStep])
                colorPicker = [
                isinstance(vars[varStep],int),
                isinstance(vars[varStep],str),
                isinstance(vars[varStep],bool),
                isinstance(vars[varStep],float),
                isinstance(vars[varStep],dict),
                isinstance(vars[varStep],tuple),
                isinstance(vars[varStep],list),
                isinstance(vars[varStep],bytes)].index(True)
                
                
                
                word = self.getRGB(colorMap[colorPicker],vars[varStep])
                
                if vars[idx-1] == ind[idx-1]:
                    beg = '✅'
                else:
                    beg = '❌'
                    ok = False
                word = f'[{beg} | {word} == {ind[idx-1]}]'
                varStep += 1
            elif varStep > len(vars) - 1:
                word = '[NULL]'

            output += ' ' + word
        

        print('[' + ('\033[34;1;1m','\033[32;1;1m','\033[33;1;1m','\033[31;1;1m')[id] + ('DEB','INF','WAR','ERR')[id] + '\033[0m]❗ ' + output  + '\033[0m')
        msg = msg.replace('μ','n')
        with open('log.txt','a') as f:
            f.write(f'[{id}]:   {msg}\n')
            
    def tlog(self,msg:str='',version: str = '',r='',f='',l=''):
        """
        Prints & Write custom Todo Log Messages to the logfile: {file}
        [0] Debug Log
        [1] Info Log
        [2] Warning Log
        [3] Error Log
        """
        f,r,l = self.getRGB(Color('#FFCC00'),f),self.getRGB(Color('#CCFF99'),r),self.getRGB(Color('#FF9999'),l)
        ver = self.getRGB(Color('#9999FF'),version)
        msgP = self.getRGB(Color('#FFCC99'),msg)
        
        print(f'[{ver}] {msgP} {l} {r} {f}\033[0m')
        msg = msg.replace('μ','n')
        with open('todo.txt','w') as f:
            f.write(f'[{version}]:   {msg}\n')
            
    def nlog(self,id:int=0,msg:str='',vars: list | tuple = []):
        """
        Prints & Write custom Log Messages to the logfile: {file}
        [0] Debug Log
        [1] Info Log
        [2] Warning Log
        [3] Error Log
        """

        #$ Declares a variable
        
        colorMap = [
            '#CCFF99',
            '#FFCC99',
            '#FF9999',
            '#99FFFF',
            '#FFFF99',
            '#FF99FF',
            '#9999FF',
            '#FF99CC',
            '#FFCC00'
        ]
        
        entry = msg.split(' ')
        output = ''
        varStep = 0
        for idx,word in enumerate(entry):
            if word == '$' and varStep <= len(vars) - 1:
                #print(vars[varStep])
                colorPicker = [
                isinstance(vars[varStep],int),
                isinstance(vars[varStep],str),
                isinstance(vars[varStep],bool),
                isinstance(vars[varStep],float),
                isinstance(vars[varStep],dict),
                isinstance(vars[varStep],tuple),
                isinstance(vars[varStep],list),
                isinstance(vars[varStep],bytes)].index(True)
                
                
                if colorPicker == 1:
                    if vars[varStep].startswith('#') and vars[varStep].__len__() == 7:

                        word = self.getRGB(vars[varStep],vars[varStep])
                    else:
                        word = self.getRGB(colorMap[colorPicker],vars[varStep])
                else:
                    word = self.getRGB(colorMap[colorPicker],vars[varStep])
                varStep += 1
            elif varStep > len(vars) - 1 and word == '$':
                word = '[NULL]'
            output += ' ' + word
        

        print('[' + ('\033[34;1;1m','\033[32;1;1m','\033[33;1;1m','\033[31;1;1m')[id] + ('DEB','INF','WAR','ERR')[id] + '\033[0m] ' + output  + '\033[0m')
        msg = msg.replace('μ','n')
        with open('log.txt','a') as f:
            f.write(f'[{id}]:   {msg}\n')
            
    def log(self,id:int=0,msg:str=''):
        """
        Prints & Write custom Log Messages to the logfile: {file}
        [0] Debug Log
        [1] Info Log
        [2] Warning Log
        [3] Error Log
        """
        msgL = msg.split(' ')
        for idx,word in enumerate(msgL):
            if word.startswith('$'):
                msgL[idx] = '\033[35;1;4m' + word.replace('$','') + '\033[0m'
        print('[' + ('\033[34;1;1m','\033[32;1;1m','\033[33;1;1m','\033[31;1;1m')[id] + ('DEB','INF','WAR','ERR')[id] + '\033[0m] ' + ' '.join(msgL)  + '\033[0m')
        msg = msg.replace('μ','n')
        with open('log.txt','a') as f:
            f.write(f'[{id}]:   {msg}\n')

LOG = Log()#- Outsource