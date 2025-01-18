from bin.ui_elements import UIGroup


class GUI:
    def __init__(self,
                 **kwargs) -> None:
        self.createUIGroups()
        
        
    def createUIGroups(self):
        self.groupTaskbar = UIGroup('taskbar')
        self.groupVideoPreview = UIGroup('videoPreview')
        self.groupInfo = UIGroup('info')
        self.groupEpisodeManipulation = UIGroup('episodeManipulation')
        self.groupOthers = UIGroup('others')
        self.groupTitle = UIGroup('title')
        self.groupAudio = UIGroup('audio')
        self.groupJtg = UIGroup('jtg')