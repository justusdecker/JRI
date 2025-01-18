
"""
Dieses Modul übernimmt die Kommunikation via Pipeline mit Davinci Resolve
Hier sind unter anderem auch gelistet die Code Snippets für Resolve Receive
"""

from json import load,loads
from socket import socket,AF_INET6,SOCK_STREAM,gethostbyname,gethostname
from threading import Thread
from os import path
resolve = ''
"""
class DavinciServer:
    def __init__(self,
                 letsPlayFileLocation:str):
        
        with open(letsPlayFileLocation,'r') as fIn:
            self.letsPlayData = load(fIn)
        
        self.project = resolve.GetProjectManager().GetCurrentProject()
        self.rootFolder = self.project.GetMediaPool().GetRootFolder()
        self.project.SetCurrentRenderFormatAndCodec('mov', 'H264')
        self.project.SetRenderSettings({
                    "SelectAllFrames": True,
                    "FormatWidth": 1920,
                    "FormatHeight": 1080,
                    "TargetDir" : "C:\\Users\\Justus\\Videos"
                })
        
        resolve.OpenPage('edit')
        
        self.ip = gethostbyname(gethostname())
        self.port = 9999
        self.socket = socket(AF_INET6,SOCK_STREAM)
        
        self.isRunning = True
        self.header = 8

        self.socket.bind((self.ip,self.port))
        self.socket.listen()
    def _deleteUnusedTrack(self):
        resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().DeleteTrack('audio',1)
        resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().DeleteTrack('audio',2)
        resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().AddTrack('audio','stereo')
        
    def addRenderJob(self):
        self.project.AddRenderJob()                                              #Adds Renderjob {''}
    def timeLineAppend(self,media):
        self.project.GetMediaPool().CreateTimelineFromClips('test', media)
    def render(self):
            self.project.StartRendering(0)                                           #Starts Rendering
    def addMedia(self,media: list | tuple):
        resolve.GetMediaStorage().AddItemListToMediaPool(media)
    def getElements(self,searchFor=list):
        _ret = []
        for item in searchFor:
            for clip in self.rootFolder.GetClipList():
                if clip.GetName() == item.split('\\')[-1]:
                    _ret.append(clip)
        return _ret
    def getElementNames(self,searchFor:str='mp4'):
        #Shows all Files in ClipList
        _ret = {}
        for idx,clip in enumerate(self.rootFolder.GetClipList()):
            if clip.GetName().endswith(f'.{searchFor}'): 
                _ret[idx] = clip.GetName()
        return _ret
    def createNewEpisode(episodeNumber:int,clipsByName:list):
        resolve.GetMediaStorage().CreateTimelineFromClips(str(episodeNumber), [clipsByName])
    def getLastRender(self):
        video = resolve.GetProjectManager().GetCurrentProject().GetRenderJobList()[-1]
        return video['targetDir'] + '\\' + video['OutputFilename']
    def handleClient(self,conn:socket,addr:str):
        if conn.recv(self.header).decode() != '<$INIT>': 
            conn.send('<$NO>'.encode())
            raise Exception('Connection cannot be initialized!')
        self.header = int(conn.recv(self.header).decode()) #headersize
        
        
        
        while self.isRunning:
            INSTANCE = conn.recv(self.header).decode()
            if INSTANCE.startswith('<$IMPORT>'):
                epNum,file = INSTANCE.split('<$IMPORT>')[1].split(':')
                self.createNewEpisode(epNum,file)
                conn.send(('.'*self.header).encode())
            if INSTANCE.startswith('<$GETRENDERFILENAME>'):
                msg = self.getLastRender()
                l = len(msg)
                conn.send((msg+('.'*(self.header-l))).encode())
                conn.send(self.getLastRender().encode())
            if INSTANCE.startswith('<$DELETETRACK>'):
                self._deleteUnusedTrack()
                conn.send(('.'*self.header).encode())
    def update(self):
        while 1:
            client, addr = self.socket.accept()
            thread = Thread(target=self.handleClient,args=(client,addr))
            thread.start()
     """   
class DavinciClient:
    def __init__(self) -> None:
        self.ip = 'localhost'
        self.port = 9999
        self.socket = socket(AF_INET6,SOCK_STREAM)
        self.isRunning = True
        self.header = 8
        self.socket.connect((self.ip,self.port))
        self.socket.send("<$INIT>")
        if self.socket.recv(self.header).decode() == '<$NO>':
            return
        self.socket.send("128".encode())
        
            
    def sendInstruction(self,message: str):
        """
        Send Davinci Resolve one of the following instructions:
        <$CIMPORT> {filePath} - creates an TimeLine with given Element
        <$IMPORT> {filePath} - Load Element in existing TimeLine
        <$GETRENDERFILENAME> - Get the current filePath for saving
        <$DELETETRACK> {id} - Deletes an AudioTrack with given id
        """
        self.socket.send(message)
            
class DavinciResolvePipeLine:
    def __init__(self) -> None:
        self.davinciPipe = 'E:\\davinciResolve\\dvp.txt'
        self.userPipe = 'E:\\davinciResolve\\up.txt'
        self.eol = '\r\n\0'
    def send2File(self,filePath,command):
        try:
            if not path.isfile(filePath):
                with open(filePath,'w') as file:
                    file.write('')
            with open(filePath,'w') as file:
                file.write(command)
        except PermissionError as E:
            print(E)
    def recvFromFile(self,filePath):
        try:
            if not path.isfile(filePath):
                with open(filePath,'w') as file:
                    file.write('')
            with open(filePath,'r') as file:
                _ret =  file.read()
                return _ret
        except PermissionError as E:
            print(E)
    def clean(self):
        with open(self.davinciPipe,'w') as file:
            file.write('')
    def cleanU(self):
        with open(self.userPipe,'w') as file:
            file.write('')
    def checkCommands(self,msg:str):
        if msg.startswith('import'):
            if '<' in msg:
                media = loads(msg.split('<')[1])
                #DVRSF.addMedia(media)
                #DVRSF.getElements(media)
                print('import')
            
            self.clean()
        if msg.startswith('reset'):
            print('reset')
            self.clean()
        if msg.startswith('addRender'):
            #DVRSF.addRenderJob()
            self.clean()
        if msg.startswith('render'):
            #DVRSF.render()
            print('render')
            self.clean()
        if ':' in msg:
            msg.split()
"""
!Only Used in DAVINCI Resolve
class DaVinciResolveScriptFundation:
    def __init__(self,letsPlayFileLocation:str):
        with open(letsPlayFileLocation,'r') as fIn:
            self.letsPlayData = load(fIn)
        #Check Existing Projects [letsplay 'name']
        
        self.project = resolve.GetProjectManager().GetCurrentProject()
        self.rootFolder = self.project.GetMediaPool().GetRootFolder()
        self.project.SetCurrentRenderFormatAndCodec('mov', 'H264')
        self.project.SetRenderSettings({
                    "SelectAllFrames": True,
                    "FormatWidth": 1920,
                    "FormatHeight": 1080,
                    "TargetDir" : "C:\\Users\\Justus\\Videos"
                })
        resolve.OpenPage('edit')
    def _deleteUnusedTrack(self):
        resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().DeleteTrack('audio',1)
        resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().DeleteTrack('audio',2)
        resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().AddTrack('audio','stereo')
    def getLastRender(self):
        video = resolve.GetProjectManager().GetCurrentProject().GetRenderJobList()[-1]
        return video['targetDir'] + '\\' + video['OutputFilename']
    def addRenderJob(self):
        self.project.AddRenderJob()                                              #Adds Renderjob {''}
    def timeLineAppend(self,media):
        self.project.GetMediaPool().CreateTimelineFromClips('test', media)
    def render(self):
            self.project.StartRendering(0)                                           #Starts Rendering
    def addMedia(self,media: list | tuple):
        resolve.GetMediaStorage().AddItemListToMediaPool(media)
    def getElements(self,searchFor=list):
        _ret = []
        for item in searchFor:
            for clip in self.rootFolder.GetClipList():
                if clip.GetName() == item.split('\\')[-1]:
                    _ret.append(clip)
        return _ret
    def getElementNames(self,searchFor:str='mp4'):
        #Shows all Files in ClipList
        _ret = {}
        for idx,clip in enumerate(self.rootFolder.GetClipList()):
            if clip.GetName().endswith(f'.{searchFor}'): 
                _ret[idx] = clip.GetName()
        return _ret
    def createNewEpisode(episodeNumber:int,clipsByName:list):
        resolve.GetMediaStorage().CreateTimelineFromClips(str(episodeNumber), [clipsByName])

"""
DVRPL = DavinciResolvePipeLine()