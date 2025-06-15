from bin.minfuncs import getDoubleZeros,no
from bin.constants import VERSION
VERSIONSTRING = f"[{VERSION[3]}]{VERSION[0]}.{VERSION[1]}.{VERSION[2]}"
from bin.fx.video import IVFX
from bin.dataManagement import DM
from bin.runtimeSettingsRI import RUNTIMESETTIGS,JTGFONTPATH,JTGIMGPATH
from bin.thumbnail_generator import ThumbnailGenerator
from bin.fx.audio import AFX
from bin.letsPlayFile import LetsPlayFile,LetsPlayComp,createDefaultLPF
from bin.settings import SETTINGS
from os import listdir, path,remove
from bin.log import LOG
from pygame import (
    key,
    image,
    Color,
    Rect,
    font,
    display,
    transform,
    K_LCTRL,
    key,
    mixer,
    Surface,
    Clock
    )
from time import time as TIME
from bin.constants import LC,EC
from bin.resolvePipe import DVRPL
from subprocess import call as callSubProcess
from bin.audio2Text import Audio2Text
from bin.fx.image import generateIcon
from bin.tree import FinalizedTree     

from bin.debugFunctions import OutsourceWarn

from bin.constants import (
    AUDIO_PATH,
    LETSPLAY_PATH,
    THUMBNAIL_PATH,
    DEFAULT_LPF_FILE,
    ATT_PATH
)

font.init()


from bin.ui_elements import (
    UIButton,
    UILabel,
    UICalendar,
    UIGroup,
    UIVideoPlayer,
    UISwitch,
    UIWindow,
    UITimeSelect,
    UIDropDown,
    UIImage,
    UITextInput,
    UIM,
    UIC,
    UIColorPicker,
    UIBackgroundWobble,
    UILoadingCone
    )



class StateManager:
    """
    A Essential Class for managing all Subprograms
    -----
    :Mode:
        
    0: ``VideoEdit``
        
    1: ``ThumbnailPresetGen``
    
    2: ``Node System``
    
    3: ``Settings``
    
    :Values:

    ``crashed``     | Only triggers if something went totally wrong!
    
    ``current``     | The currently loaded Subprogram
    """
    def __init__(self,app) -> None:

        self.mode = 0
        self.app = app
        self.current = VideoEditor(self.app,self)
        self.clock = Clock()
        self.crashed = False
        #self.ThumbnailBuild = ThumbnailCheck
    def switchMode(self,mode:int):
        """
        Based on ``mode`` the current Program will change
        """
        match mode:
            case 0:
                self.current = VideoEditor(self.app,self)
            case 1:
                self.current = FileManager(self.app,self)
        self.mode = mode
    def update(self):
        self.current.update()
        self.clock.tick(60)
 
class FileManager:
    def __init__(self,app,stateSystem:StateManager) -> None:
        self.app = app
        UIM.queue.clear()
        self.ft = FinalizedTree()
        self.ft.run()
        self.rT,self.lpfs,self.epi = self.ft.renderTree()
        self.unpackedrT = []
        print(len(self.rT))
        self.uiElements = []
        self.folder = []
        self.files = []
        self.min = 0
        self.elementDepth = 0
        self.root = UIButton(Rect(0,0,128,24),ux={'text':'root' , 'size':(128,24)})
        #insert all select checkbox
        #insert delete if st == 31
        for index,line in enumerate(self.rT):
            #insert checkboxes each line
            #insert episode count each line
            self.elementDepth += 1
            for idx, f2 in enumerate(line):
                
                if f2.startswith('#folder'):
                    #dest 0
                    _data = f2.split('|')[1]
                    
                        
                    _element = UIButton(Rect(0,index*24,256*3,24),onPressCallback=self.folderCallback,ux={'text':_data , 'size':(256*3,24)},parent=self.root)
                    self.folder.append(_element.elementId)
                    self.files.append(-1)
                    self.uiElements.append(_element)
                    self.unpackedrT.append(f2)
                else:
                    _data = f2.split('|')[2].split('\\')[-1]
                    if f2.split('|')[1] != 'True':
                    
                        _element = UIButton(
                            Rect(256*idx,index*24,256,24),
                            onPressCallback=self.filesCallback,
                            ux={
                                'text':_data , 
                                'size':(256,24),
                                'normal_text_color': Color('#FF9999'),
                                'hovered_text_color': Color('#FFBF99'),
                                'pressed_text_color': Color('#FF0099')
                                },
                            parent=self.root
                            )
                    else:
                        _element = UIButton(
                            Rect(256*idx,index*24,256,24),
                            onPressCallback=self.filesCallback,
                            ux={
                                'text':_data , 
                                'size':(256,24)
                                },
                            parent=self.root
                            )
                    
                    self.files.append(_element.elementId)
                    self.folder.append(-1)#spacer
                    self.uiElements.append(_element)
                    self.unpackedrT.append(f2)
    def folderCallback(self,*_):
        for index, folder in enumerate(self.folder):
            if folder == _[0].elementId:
                print('No Data')
    def filesCallback(self,*_):
        #get first object from this lp and last
        for index, file in enumerate(self.files):
            if file == _[0].elementId:
                
                print(self.lpfs[index]._getEpisode(self.epi[index][1]-1))
    def update(self):
        t1 = TIME()
        self.min += (self.app.scrollY*24)
        if self.min < -((self.elementDepth*24)-(30*24)):
            self.min -= (self.app.scrollY*24)
        if self.min > 0:
            self.root.pos = self.root.pos[0],0
            self.min = 0
        if self.app.scrollY != 0:
            
            self.root.pos = self.root.pos[0],self.min

        self.app.window.fill(Color('#141414'))
        UIM.renderQueue(self.app)
        display.set_caption(f'ft:{round((TIME()-t1)*1000,1)}ms fps: {int(1/(TIME()-t1))}')
        
class VideoEditor:
    """
    A Wrapper for all Essentials in JVE
    -----
    Functions
    -----
    .. changeMode:: change the mode in a specific Range.

        ``_`` : ``UIElement`` -> ``None``
        
        This is for switching between ``Inspection`` , ``AI Gen Title`` & ``Thumbnail Data Manipulation``
        
        Using a predefined list for remembering the UIID`s
    
    .. close:: save the current LetsPlayComp[*LetsPlayFiles]
        
        ``_`` : *NOTHING* -> ``None``
        
    .. changeStatus:: change the status of an episode up & down
    
        ``_`` : ``UIElement`` -> ``None``
        
        The predefined List of Status Values: ``0,1,3,7,15,31``
        
        Using a predefined list for remembering the UIID`s
        
    .. onEpisodeLoad:: This Function loads all the data and create if needed missing data
        
        ``_`` : -> ``None``
        
        !not finished!
        
    .. createUIElements:: create all necessary UI Elements for later use
    
        ``_`` : *NOTHING* -> ``None``
        
        This Elements should not be deleted!
        
    .. createUIGroups:: create all necessary UI Elements for later use
    
        ``_`` : *NOTHING* -> ``None``
        
        This Elements should not be deleted!
    
    .. setNewThumbnailAutomationData:: User TAD Manipulation
    
        ``_`` : ``UIElement`` -> ``None``
    
    .. setRecordingTimeTo:: Updates ``episode_length`` in a ``LetsPlayFile`` 
    
        ``_`` : ``UIElement`` -> ``None``
        
    .. onBubbleShowLoad:: 
    
        *Currently not in use. Probably will be deprecated in the future*
        
    .. openEssentialFolders:: Opens the Essential Folders if existent
    
        ``_`` : ``UIElement`` -> ``None``
        
    .. rerollThumbnail:: Create a new Thumbnail for current episode
    
        ``_`` : ``UIElement`` , ``frame`` : ``-1`` , ``overImage`` : *NOT IN USE* -> ``None``
        
        Get a random video-frame if ``frame`` is ``-1`` else it gets the video-frame by using ``frame``

        :For more details see: ``bin.thumbnailGenerator``
        
    .. setUploadAt:: Opens the Essential Folders if existent
    
        ``_`` : ``UIElement`` -> ``None``
        
        !not finished
    
    .. sendEp2Resolve:: Opens the Essential Folders if existent
    
        ``_`` : ``UIElement`` -> ``None``
    
    .. sendEp2ResolveFA:: Opens the Essential Folders if existent
    
        ``_`` : ``UIElement`` -> ``None``
    
    .. reExtractAudio:: Opens the Essential Folders if existent
    
        ``_`` : ``UIElement`` -> ``None``
    
    .. generateComp:: Opens the Essential Folders if existent
    
        ``_`` : ``UIElement`` -> ``None``
    
    .. update:: Opens the Essential Folders if existent
    
        ``_`` : ``UIElement`` -> ``None``
    
    .. checkKeyBinds:: Opens the Essential Folders if existent
    
        ``_`` : ``UIElement`` -> ``None``
    
    :Info: ``Graphics``, ``Interaction`` & ``Editing`` will be in here
    
    :Subfunctions: 
    
        ``RerollThumbnail`` Changes the ``Episode Thumbnail`` to a random image of any given video.
        ``sendEp2Resolve`` Sends Data to Davinci Resolve. Like ``Video Paths``, Audio Paths, TimeLine Manipulation etc.
    """
    def __init__(self,app,stateSystem:StateManager) -> None:
        self.isLoading = False
        self.stateSystem = stateSystem

        UIM.queue.clear()   #! Deletes / Resets all UIElements in queue
        self.start = 0 # the pointer for all kinds of functions in Array

        self.thumbnailGenerator = ThumbnailGenerator()
        
        self.lastThumbnailTime = -1
        
        self.app:Application = app
            
        self.mode = 0
        #0: Info
        #1: Title
        #2: Audio




        self.createUIGroups()
        self.wb = UIBackgroundWobble(Rect(1,1,1,1),app=self.app,group=self.groupOthers)
        self.letsPlayComp = LetsPlayComp(
            JTGFONTPATH,
            JTGIMGPATH
            )
        
        if SETTINGS._['autoSave']:
            self.app.quitJob = self.letsPlayComp.save
            
        self.createUIElements()

        self.letsPlayComp.setTADInputs(
            [
                self.jtgTextSizeInput,
                self.jtgTextPosXInput,
                self.jtgTextPosYInput,
                self.jtgTextRotInput,
                self.jtgImageScaleInput,
                self.jtgImagePosXInput,
                self.jtgImagePosYInput,
                self.jtgImageRotInput,
                self.jtgBackgroundPosXInput,
                self.jtgBackgroundPosYInput,
                self.jtgBackgroundRandomPosXInput,
                self.jtgBackgroundRandomPosYInput,
                self.jtgBackgroundRotInput,
                self.jtgBackgroundRandomRotationLInput,
                self.jtgBackgroundRandomRotationRInput,
                self.jtgBackgroundRandomScaleLInput,
                self.jtgBackgroundRandomScaleRInput,
                self.jtgBackgroundSizeInput,
                self.jtgBackgroundHueInput,
                self.jtgBackgroundSatInput,
                self.jtgBackgroundLigInput
            ],
            self.jtgColorPicker,
            self.jtgCenterSwitch,
            [
                self.lpfNameInput,
                self.lpfIconPathInput,
                
            ]
        )
        self.episodeRecordingTime = -1
        _l = []
        for _ in UIC.count:
            _l.append(_)
            _l.append(UIC.count[_])
            
        LOG.nlog(0,'UIE:\n' + (' $ \n'*((len(UIC.count)*2))),_l)
        self.lc = UILoadingCone(Rect(0,0,512,512),app=self.app)
        self.onEpisodeLoad()
        
        
    
    @OutsourceWarn(version='1.13.0',to='bin...')
    def createUIGroups(self):
        self.groupTaskbar = UIGroup('taskbar')
        self.groupVideoPreview = UIGroup('videoPreview')
        self.groupInfo = UIGroup('info')
        self.groupEpisodeManipulation = UIGroup('episodeManipulation')
        self.groupOthers = UIGroup('others')
        self.groupTitle = UIGroup('title')
        self.groupAudio = UIGroup('audio')
        self.groupJtg = UIGroup('jtg')
    @OutsourceWarn(version='1.13.0',to='bin.uiElementCreator')
    def createUIElements(self):
        self.thumbnail = UIImage(
            Rect(
                48,
                48,
                576,
                324
                ),
            ux={
                'size': (576,324)
                },
            group=self.groupInfo
            )
        
        self.icon = UIImage(
            Rect(
                1232,
                0,
                48,
                48
                ),
            group=self.groupInfo
            )
        
        self.videoUpdate = True #? If False the Video will not play
        
        self.win = UIWindow(    #? Window Canvas for Uploadtime Manipulation
            Rect(
                48,
                444,
                192,
                192
                ),
            ux={
                'size':(192,192),
                'text': 'UploadTime'
                },
            layer=30,
            group=self.groupEpisodeManipulation
            )
        
        self.nameLabel = UILabel(
            Rect(
                48,
                372,
                576,
                24
                ),
            change=True,
            clean=True,
            text='',
            group=self.groupInfo
            )
        
        self.audioPathLabel = UILabel(
            Rect(
                48,
                420,
                576,
                24
                ),
            ux={
                'size':(576,24),
                'text': 'UploadTime'
                },
            group=self.groupInfo
            )
        
        self.pathLabel = UILabel(
            Rect(
                48,
                396,
                576,
                24
                ),
            ux={
                'size':(576,24),
                'text': 'UploadTime'
                },
            group=self.groupInfo
            )

        self.calendar = UICalendar(
            Rect(
                0,
                24,
                640,
                360
                ),
            layer = 40,
            parent=self.win,
            group=self.groupEpisodeManipulation
            )
        
        self.timeSelect = UITimeSelect(
            Rect(
                144,
                24,
                72,
                108
                ),
            parent=self.win,
            layer=30,
            group=self.groupEpisodeManipulation
            )

        self.titleChangeBox = UITextInput(
            Rect(
                624,
                48,
                384,
                24
                ),
            text=self.letsPlayComp.getCuEp(EC.TITLE),
            app=self.app,
            maxLetters=64,
            group=self.groupEpisodeManipulation
            )
        
        #self.audioSlider = UISliderLR(Rect(24,472,1232,24),group=self.groupAudio,layer=100)
        #self.aW = UIAudioWave(Rect(24,24,1232,200),app=self.app,group=self.groupAudio,layer=100,slider=self.audioSlider)
        #self.aWTrack2 = UIAudioWave(Rect(24,24+248,1232,200),app=self.app,group=self.groupAudio,layer=100,slider=self.audioSlider)
        
        #self.audioWindow = UIWindow(Rect(0,696,256,256),ux={'size': (256,256),'text':'loudness Normalization'})
        
        #! Values to change:
        #Decibel
        #Save as comp
        #load from original audio Path or original desktop audio path
        #create an tasklist for batching
        #['command','{args...}']
        
        #self.aW.adaptor = [self.aWTrack2]
        #self.aWTrack2.adaptor = [self.aW]
        
        #Auto Loudness Normalize on Episode Load if no file exists
        
        
        
        self.fileDD = UIDropDown(
            Rect(
                0,
                0,
                48,
                24
                ),
            ux= {
                'size': (48,24),
                'text': 'File'
                },
            childsInstances= [
                ('New',createDefaultLPF),
                ('Load',self.letsPlayComp.load),
                ('Save',self.letsPlayComp.saveLetsPlays),
                ('Exit',self.close)
                ],
            layer=100,
            group= self.groupTaskbar
            )
        
        self.actionsDD = UIDropDown(
            Rect(
                48,
                0,
                192,
                24
                ),
            ux= {
                'size': (192,24),
                'text': 'Actions'
                },
            childsInstances= [
                ('Reextract Audio',self.reExctractAudio),
                ('Send2Resolve',self.sendEp2Resolve),
                ('Reroll Thumbnail',self.rerollThumbnail),
                ('Status up',self.changeStatus),
                ('Status down',self.changeStatus)
                ],
            layer=100,
            group= self.groupTaskbar
            )
        self.changeStatusButtons = [self.actionsDD.childInstances[4],self.actionsDD.childInstances[3]]
        
        
        self.lpfDD = UIDropDown(
            Rect(
                240,
                0,
                192,
                24
                ),
            ux= {
                'size': (192,24),
                'text': 'LetsPlayFile Open'
                },
            childsInstances= [
                ('LetsPlayFile',self.openEssentialFolders),
                ('Audio Folder',self.openEssentialFolders),
                ('Video Folder',self.openEssentialFolders),
                ('Thumbnail Folder',self.openEssentialFolders)
                ],
            layer=100,
            group= self.groupTaskbar
            )
        self.essentialFolderButtons = [i.elementId for i in self.lpfDD.childInstances]
        self.modeDD = UIDropDown(
            Rect(
                240+192,
                0,
                192,
                24
                ),
            ux= {
                'size': (192,24),
                'text': 'Programs'
                },
            childsInstances= [
                ('Info & Edit',self._changeMode),
                ('Thumbnail',self._changeMode),
                ],
            layer=100,
            group= self.groupTaskbar
            )
        
        self.modeButtons = [i.elementId for i in self.modeDD.childInstances]

        self.autoSwitchToNextEpisode = UISwitch(
            Rect(
                1008,
                48,
                24,
                24
                ),
            layer=30,
            group=self.groupOthers
            )

        self.autoSwitchLabel = UILabel(
            Rect(
                1032,
                48,
                128,
                24
                ),
            ux={
                'text': 'Auto Switch',
                'size': (128,24)
                },
            layer=30,
            group=self.groupOthers
            )
        
        self.autoForewardToNextEpisode = UISwitch(
            Rect(
                1008,
                72,
                24,
                24
                ),
            layer=30,
            group=self.groupOthers
            )
        
        self.autoForewardLabel = UILabel(
            Rect(
                1032,
                72,
                128,
                24
                ),
            ux={
                'text': 'Auto Foreward',
                'size': (128,24)
                },
            layer=30,
            group=self.groupOthers
            )
        
        self.fastLoadSwitch = UISwitch(
            Rect(
                1008,
                96,
                24,
                24
                ),
            layer=30,
            group=self.groupOthers
            )
        
        self.fastLoadSwitchLabel = UILabel(
            Rect(
                1032,
                96,
                128,
                24
                ),
            ux={
                'text': 'Fast Load',
                'size': (128,24)
                },
            layer=30,
            group=self.groupOthers
            )
        
        self.autoGenerateComp = UISwitch(
            Rect(
                1008,
                120,
                24,
                24
                ),
            layer=30,
            group=self.groupOthers
            )
        
        self.autoGenerateCompLabel = UILabel(
            Rect(
                1032,
                120,
                128,
                24
                ),
            ux={
                'text': 'Auto Comp[!]',
                'size': (128,24)
                },
            layer=30,
            group=self.groupOthers
            )
        
        self.autoSend2Resolve = UISwitch(
            Rect(
                1008,
                144,
                24,
                24
                ),
            layer=30,
            group=self.groupOthers
            )
        
        self.autoSend2ResolveLabel = UILabel(
            Rect(
                1032,
                144,
                128,
                24
                ),
            ux={
                'text': 'Auto Resolve',
                'size': (128,24)
                },
            layer=30,
            group=self.groupOthers
            )
        
        self.thumbnailAutoUpdateThumbnailLabel = UILabel(
            Rect(
                1032,
                168,
                128,
                24
                ),
            ux={
                'text': 'Auto Thumb',
                'size': (128,24)
                },
            layer=40,
            group=self.groupEpisodeManipulation
            )
        
        self.thumbnailAutoUpdateSwitch = UISwitch(
            Rect(
                1008,
                168,
                24,
                24
                ),
            layer=40,
            group=self.groupEpisodeManipulation
            )
        
        self.videoPlayer = UIVideoPlayer(
            Rect(
                624,
                96,
                384,
                216
                ),
            app=self.app,
            group=self.groupVideoPreview
            )

        self.letsPlaySettingsWin = UIWindow(
            Rect(
                496,
                444,
                256,
                300
                ),
            ux={
                'size':(256,192),
                'text': 'LetsPlay Settings'
                },
            layer=30,
            group=self.groupEpisodeManipulation
            )

        self.lpfNameInput = UITextInput(
            Rect(
                0,
                24,
                256,
                24
                ),
            ux={
                'size':(256,24),
                'text':self.letsPlayComp.getCuLp(LC.NAME)
                },
            text=self.letsPlayComp.getCuLp(LC.NAME),
            app=self.app,
            maxLetters=32,
            default_text='LPF Name',
            parent=self.letsPlaySettingsWin,
            group=self.groupEpisodeManipulation
            )
        
        self.lpfIconPathInput = UITextInput(
            Rect(
                0,
                48,
                128,
                24
                ),
            ux={
                'size':(128,24),
                'text':self.letsPlayComp.getCuLp(LC.ICON)
                },
            text=self.letsPlayComp.getCuLp(LC.ICON),
            app=self.app,
            maxLetters=128,
            default_text='Icon Path',
            parent=self.letsPlaySettingsWin,
            group=self.groupEpisodeManipulation
            )
        
        self.lpfIconPathButton = UIButton(
            Rect(
                128,
                48,
                72,
                36
                ),
            onPressCallback=no,
            ux={'text':'open'},
            parent=self.letsPlaySettingsWin,
            layer=30,
            group=self.groupEpisodeManipulation
            )

        self.lpfSettingsButtons = [
            self.lpfIconPathButton.elementId
            ]
        
        
        self.lpfEpisodeLengthDD = UIDropDown(
            Rect(
                0,
                120,
                48,
                24
                ),
            ux= {
                'size': (48,24),
                'text': 'RT'
                },
            childsInstances= [
                ('10m',self._setRecordingTimeTo),
                ('15m',self._setRecordingTimeTo),
                ('20m',self._setRecordingTimeTo),
                ('25m',self._setRecordingTimeTo),
                ('30m',self._setRecordingTimeTo),
                ('40m',self._setRecordingTimeTo),
                ('50m',self._setRecordingTimeTo),
                ('60m',self._setRecordingTimeTo)
                ],
            layer=100,
            parent=self.letsPlaySettingsWin,
            group=self.groupEpisodeManipulation
            )
        
        self.episodeLengthButtons = [i.elementId for i in self.lpfEpisodeLengthDD.childInstances]
        self.updateSettingsButton = UIButton(
            Rect(
                48,
                120,
                72,
                36
                ),
            onPressCallback=self.letsPlayComp.updateLetsPlaySettings,
            ux={'text':'update settings'},
            parent=self.letsPlaySettingsWin,
            layer=30,
            group=self.groupEpisodeManipulation
            )
        
        self.letsPlayCreateSettingsWin = UIWindow(
            Rect(
                240,
                444,
                256,
                300
                ),
            ux={
                'size':(256,192),
                'text': 'LetsPlay Create'
                },
            layer=30
            )

        #self.titleBubbleShow = UIBubbleText(rect=Rect(48,48,1280-96,720-96),group=self.groupTitle,app=self.stateSystem.app,ux={'size':(1280-96,720-96)})
        #*Image Show
        
        self.jtgImage = UIImage(Rect(0,0,1280,720),group=self.groupJtg)
        
        #*Images Window
        
        self.jtgImagesWin = UIWindow(
            Rect(
                0,
                24,
                128,
                96
                ),
            ux={
                'size':(128,96),
                'text': 'Image'
                },
            layer=30,
            group=self.groupJtg
            )
        
        self.jtgLoadImageButton = UIButton(
            Rect(
                0,
                24,
                128,
                24
                ),
            onPressCallback=JTGIMGPATH.setPath,
            ux={'size': (128,24),'text':'open'},
            parent=self.jtgImagesWin,
            layer=30,
            group=self.groupJtg
            )
        
        self.jtgImagePosXInput = UITextInput(
            Rect(
                0,
                48,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='X',
            parent=self.jtgImagesWin,
            group=self.groupJtg
            )
        
        self.jtgImagePosYInput = UITextInput(
            Rect(
                64,
                48,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='Y',
            parent=self.jtgImagesWin,
            group=self.groupJtg
            )
        
        self.jtgImageRotInput = UITextInput(
            Rect(
                0,
                72,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=5,
            mode='float',
            default_text='R',
            parent=self.jtgImagesWin,
            group=self.groupJtg
            )
        
        self.jtgImageScaleInput = UITextInput(
            Rect(
                64,
                72,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='float',
            default_text='S',
            parent=self.jtgImagesWin,
            group=self.groupJtg
            )
        
        #*text Window
        
        self.jtgTextWin = UIWindow(
            Rect(
                0,
                120,
                128,
                96
                ),
            ux={
                'size':(128,96),
                'text': 'Text'
                },
            layer=30,
            group=self.groupJtg
            )
        
        self.jtgLoadFontButton = UIButton(
            Rect(
                0,
                24,
                128,
                24
                ),
            onPressCallback=JTGFONTPATH.setPath,
            ux={'size': (128,24),'text':'open'},
            parent=self.jtgTextWin,
            layer=30,
            group=self.groupJtg
            )
        
        self.jtgTextPosXInput = UITextInput(
            Rect(
                0,
                48,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='X',
            parent=self.jtgTextWin,
            group=self.groupJtg
            )
        
        self.jtgTextPosYInput = UITextInput(
            Rect(
                64,
                48,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='Y',
            parent=self.jtgTextWin,
            group=self.groupJtg
            )
        
        self.jtgTextRotInput = UITextInput(
            Rect(
                0,
                72,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=5,
            mode='float',
            default_text='R',
            parent=self.jtgTextWin,
            group=self.groupJtg
            )
        
        self.jtgTextSizeInput = UITextInput(
            Rect(
                64,
                72,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='S',
            parent=self.jtgTextWin,
            group=self.groupJtg
            )
        
        #*background Window
        
        self.jtgBackgroundWin = UIWindow(
            Rect(
                0,
                216,
                128,
                168
                ),
            ux={
                'size':(128,168),
                'text': 'Background'
                },
            layer=30,
            group=self.groupJtg
            )
        
        self.jtgBackgroundPosXInput = UITextInput(
            Rect(
                0,
                24,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='X',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundPosYInput = UITextInput(
            Rect(
                64,
                24,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='Y',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundRotInput = UITextInput(
            Rect(
                0,
                48,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=5,
            mode='float',
            default_text='R',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundSizeInput = UITextInput(
            Rect(
                64,
                48,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='float',
            default_text='S',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )

        self.jtgBackgroundRandomPosXInput = UITextInput(
            Rect(
                0,
                72,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='RX',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundRandomPosYInput = UITextInput(
            Rect(
                64,
                72,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='RY',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
          
        self.jtgBackgroundRandomScaleLInput = UITextInput(
            Rect(
                0,
                96,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='float',
            default_text='RSL',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundRandomScaleRInput = UITextInput(
            Rect(
                64,
                96,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='float',
            default_text='RSR',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundRandomRotationLInput = UITextInput(
            Rect(
                0,
                120,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='RRL',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundRandomRotationRInput = UITextInput(
            Rect(
                64,
                120,
                64,
                24
                ),
            ux={'size':(64,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='only_numbers',
            default_text='RRR',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundHueInput = UITextInput(
            Rect(
                0,
                144,
                32,
                24
                ),
            ux={'size':(32,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='float',
            default_text='hue',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundSatInput = UITextInput(
            Rect(
                32,
                144,
                32,
                24
                ),
            ux={'size':(32,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='float',
            default_text='sat',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgBackgroundLigInput = UITextInput(
            Rect(
                64,
                144,
                32,
                24
                ),
            ux={'size':(32,24)},
            text='',
            app=self.app,
            maxLetters=4,
            mode='float',
            default_text='lig',
            parent=self.jtgBackgroundWin,
            group=self.groupJtg
            )
        
        self.jtgCenterSwitch = UISwitch(
            Rect(
                96,
                144,
                24,
                24
                ),
            layer=30,
            group=self.groupJtg,
            parent=self.jtgBackgroundWin
            )
        
        
        self.jtgsaveButton = UIButton(
            Rect(
                1280-24-128,
                24,
                128,
                24
                ),
            onPressCallback=self._setNewThumbnailAutomationData,
            ux={'size': (128,24),'text':'save'},
            layer=30,
            group=self.groupJtg
            )
        
        #* Text Color Window
        

        
        self.jtgColorPicker = UIColorPicker(Rect(0,126+268,64,172),group=self.groupJtg)
        #Insert the last inputs
        #create a function to overwrite atc
        #change resolve to end in fairlight
        self.textInputs = [
            self.titleChangeBox,
            self.lpfIconPathInput,
            self.jtgImagePosXInput,
            self.jtgImagePosYInput,
            self.jtgImageRotInput,
            self.jtgImageScaleInput,
            self.jtgTextPosXInput,
            self.jtgTextPosYInput,
            self.jtgTextRotInput,
            self.jtgTextSizeInput,
            self.jtgBackgroundPosXInput,
            self.jtgBackgroundPosYInput,
            self.jtgBackgroundRotInput,
            self.jtgBackgroundSizeInput,
            self.jtgBackgroundRandomPosXInput,
            self.jtgBackgroundRandomPosYInput,
            self.jtgBackgroundRandomScaleLInput,
            self.jtgBackgroundRandomScaleRInput,
            self.jtgBackgroundRandomRotationLInput,
            self.jtgBackgroundRandomRotationRInput,
            self.jtgBackgroundHueInput,
            self.jtgBackgroundSatInput,
            self.jtgBackgroundLigInput
        ]

    def _setNewThumbnailAutomationData(self,*_):#! Change Name
        self.letsPlayComp._setNewThumbnailAutomationData()
        self.rerollThumbnail()
        self.jtgImage.setImage(image.load(self.letsPlayComp.getThumbnailPath()))

    def _changeMode(self,*_) -> None:
        for index, buttonId in enumerate(self.modeButtons):
            if buttonId == _[0].elementId:
                self.mode = index
                break
            
    def _setRecordingTimeTo(self,*_):
        for index, buttonId in enumerate(self.episodeLengthButtons):
            if buttonId == _[0].elementId:
                self.episodeRecordingTime = [600,900,1200,1500,1800,2400,3600][index]
                self.letsPlayComp.setCuLp(LC.EPISODE_LENGTH,[600,900,1200,1500,1800,2400,3600][index])
                break

    def _onBubbleShowLoad(self):

        _filePath = f'{ATT_PATH}{self.letsPlayComp.getCuEp(EC.EPISODE_NUMBER)}_{self.letsPlayComp.getCuLp(LC.NAME)}.att'
        print(self.letsPlayComp.getCuEp(EC.ORIGINAL_AUDIO_PATH),_filePath)
        if not DM.existFile(_filePath):
            self.titleBubbleShow.data = Audio2Text(self.letsPlayComp.getCuEp(EC.ORIGINAL_AUDIO_PATH)).get(_filePath)
        else:
            self.titleBubbleShow.data = DM.loads(_filePath)
        
        self.titleBubbleShow.generateBubbleElementsLow()
        
    def close(self,*_):
        self.letsPlayComp.saveLetsPlays()
        self.app.isAlive = False

    def openEssentialFolders(self,*_):
        for index, buttonId in enumerate(self.essentialFolderButtons):
            if buttonId == _[0].elementId:
                
                callSubProcess(self.letsPlayComp.getEssentialFolderCommands()[index])
                break

    def rerollThumbnail(self,*_,frame : int = -1,overImage=None):
        """
        Get a random Thumbnail Position in given Video, create it and update it!
        """
        self.lc.start('Generating Thumbnail...')
        LOG.nlog(1,'Generating Thumbnail...')
        self.lastThumbnailTime = self.letsPlayComp.getCuEp(EC.THUMBNAIL_FRAME)
        self.thumbnailGenerator.create_thumbnail(self.letsPlayComp.getEpisodeIndex()+1,
                                                self.letsPlayComp.getCuEp(EC.ORIGINAL_VIDEO_PATH),
                                                frame,
                                                self.letsPlayComp.getCuLp(LC.THUMBNAIL_AUTOMATION_DATA),
                                                self.letsPlayComp.getCuLp(LC.NAME))
        
        self.letsPlayComp.setCuEp(EC.THUMBNAIL_FRAME,self.thumbnailGenerator.idx)
        self.letsPlayComp.setCuEp(EC.THUMBNAIL_PATH,f'{THUMBNAIL_PATH}{self.letsPlayComp.getCuLp(LC.NAME)}\\{self.letsPlayComp.getCuEp(EC.EPISODE_NUMBER)}_{self.letsPlayComp.getCuLp(LC.NAME)}_Thumbnail.png')
        _bg = transform.scale(image.load(self.letsPlayComp.getCuEp(EC.THUMBNAIL_PATH)),(576,324))
        _bg.blit(self.thumbnail.UX.CUTOUT,(0,0))
        _bg.set_colorkey((0,255,0))
        self.thumbnail.setImage(_bg)

        LOG.nlog(1,f'Id: $', [self.thumbnailGenerator.idx])
        if self.autoSwitchToNextEpisode.toggle: #? Auto Switch for automation
            self.letsPlayComp.change2Episode(1,self.onEpisodeLoad)
        self.lc._stop()

    def _setUploadAt(self):
        """
        set episode["uploadAt"]
        """
        t = f'{self.calendar.getDate()} {getDoubleZeros(self.timeSelect.hour)}:{getDoubleZeros(self.timeSelect.minute)}'
        
        self.letsPlayFiles[self.episodesInQueue[self.start][0]]._setEpisode(self.episodesInQueue[self.start][1],'uploadAt',t)

        LOG.nlog(1,f'UploadAt: $', [t])

    def changeStatus(self,*_):
        statusList = [0,1,3,7,15,31]
        for index, buttonId in enumerate(self.changeStatusButtons):
            if buttonId.elementId == _[0].elementId:
                idx = statusList.index(self.letsPlayComp.getCuEp(EC.STATUS))+[-1,1][index] # TODO : Use the new ST values
                break
        
        if idx >= 0 and idx < len(statusList):
            
            statusIndex = statusList[idx]
            self.letsPlayComp.setCuEp(EC.STATUS,statusIndex) # TODO : Use the new ST values

        self._changeEpisodeLeftView()
    
    def sendEp2ResolveFA(self,*_):
        """
            Uses the DVRPL for sending Davinci Resolve the current Episode
            Gets the results from resolve
        """
        self.lc.start(f'Send DVR FAData')
        LOG.nlog(1,f'Send DVR FAData')
        
        video = self.letsPlayComp.getCuEp(EC.ORIGINAL_VIDEO_PATH)
        comp = f'{AUDIO_PATH}{self.letsPlayComp.getCuLp(LC.NAME)}\\comps\\{self.letsPlayComp.getEpisodeIndex()+1}_comp.mp3'
        LOG.nlog(1,'Sending Data to Resolve: \n $ \n $',[video,comp])
        if not path.isfile(video):
            self.lc._stop()
            LOG.nlog(3,'Sending Data Failed: Video does not exist')
            return
        if not path.isfile(comp):
            self.lc._stop()
            LOG.nlog(3,'Sending Data Failed: Comp does not exist')
            return
        DVRPL.send2File(
                    DVRPL.davinciPipe,
                    f'import<{video}<{comp}<{self.letsPlayComp.getEpisodeIndex()+1}'
                    )
        while DVRPL.recvFromFile(DVRPL.davinciPipe) != '':
            pass
        else:
            LOG.nlog(1,'Sending Data Succeeded')
        if self.autoSwitchToNextEpisode.toggle: #? Auto Switch for automation
            self.letsPlayComp.change2Episode(1,self.onEpisodeLoad)
        self.lc._stop()

    def sendEp2Resolve(self,*_):
        """
            Uses the DVRPL for sending Davinci Resolve the current Episode
            Gets the results from resolve
        """
        self.lc.start(f'Send DVR Data')
        startTime = TIME()
        LOG.nlog(1,f'Send DVR Data')
        video = self.letsPlayComp.getCuEp(EC.ORIGINAL_VIDEO_PATH)
        comp = f'{AUDIO_PATH}{self.letsPlayComp.getCuLp(LC.NAME)}\\comps\\{self.letsPlayComp.getEpisodeIndex()+1}_comp.mp3'
        print(comp)
        if not path.isfile(video):
            LOG.nlog(1,f'Video does not exist')
            self.lc._stop()
            return
        if not path.isfile(comp):
            LOG.nlog(1,f'Comp does not exist')
            self.lc._stop()
            return
        DVRPL.send2File(
                    DVRPL.davinciPipe,
                    f'import<{video}<{comp}<{self.letsPlayComp.getEpisodeIndex()+1}'
                    )
        while DVRPL.recvFromFile(DVRPL.davinciPipe) != '':
            if TIME() - startTime > 5:
                DVRPL.send2File(
                    DVRPL.davinciPipe,
                    f''
                    )
                LOG.nlog(1,f'DVR Data Transfer [404]')
                break#! This is not correct. The Result is 404 everytime!
        else:
            LOG.nlog(1,f'DVR Data Transfer finished')
        if self.autoSwitchToNextEpisode.toggle: #? Auto Switch for automation
            self.letsPlayComp.change2Episode(1,self.onEpisodeLoad)
        self.lc._stop()
    
    def reExctractAudio(self,*_):
        """
        Recreates audio file if broken or something
        """
        self.lc.start('Start reextracting Audio')
        LOG.nlog(1,'Start reextracting Audio')
        dest = self.letsPlayComp.getAudioPath()
        _newDest = f"{AUDIO_PATH}{self.letsPlayComp.getCuLp(LC.NAME)}\\{self.letsPlayComp.getCuEp(EC.EPISODE_NUMBER)+1}_{self.letsPlayComp.getCuLp(LC.NAME)}_track.mp3"
        if DM.existFile(dest):
            LOG.nlog(2,'Delete file Reason: Already exists')
            mixer.music.unload()
            remove(dest)
        self.letsPlayComp.setCuEp('audioFilePath',f"{AUDIO_PATH}{self.letsPlayComp.getCuLp(LC.NAME)}\\{self.letsPlayComp.getCuEp(EC.EPISODE_NUMBER)+1}_{self.letsPlayComp.getCuLp(LC.NAME)}_track.mp3")
        if dest is None:
            AFX.extractAudio(self.letsPlayComp.getVideoPath(),_newDest)
            
            mixer.music.load(_newDest)
        else:
            AFX.extractAudio(self.letsPlayComp.getVideoPath(),dest)
        
            mixer.music.load(dest)

        LOG.nlog(1,f'saved Audio to $',[dest])
        self.lc._stop()
    
    def generateComp(self):
        if not DM.existFile(self.letsPlayComp.getCompPath()):
            self.lc.start('Audio Loudness Normalization')
            display.set_caption('ALN')
            LOG.nlog(0,'ALN: $ >>> $', [self.letsPlayComp.getCuEp(EC.ORIGINAL_AUDIO_PATH),AUDIO_PATH + '_tmp.mp3'])
            AFX.LoudnessNormalization(self.letsPlayComp.getCuEp(EC.ORIGINAL_AUDIO_PATH),AUDIO_PATH + '_tmp.mp3')
            DM.createFolder(self.letsPlayComp.getCompPathWOF())
            display.set_caption('ALM')
            self.lc.setInfo('Audio Limiter')
            LOG.nlog(0,'ALM: $ >>> $', [AUDIO_PATH + '_tmp.mp3',self.letsPlayComp.getCompPath()])
            AFX.limiter(AUDIO_PATH + '_tmp.mp3',self.letsPlayComp.getCompPath())
            display.set_caption('RMF')
            self.lc.setInfo('Remove Temps')
            if DM.existFile(AUDIO_PATH + '_tmp.mp3'):
                remove(AUDIO_PATH + '_tmp.mp3')
            self.lc._stop()
    
    def onEpisodeLoad(self):
        self.lc.start(f'Loading Episode',1)
        display.set_caption(f'Loading...')
        LOG.nlog(1,f'switch to Episode: $ - $',[self.letsPlayComp.getCuEp(EC.EPISODE_NUMBER),self.letsPlayComp.getCuLp(LC.NAME)])
        
        self.videoPlayer._stop()
        
        if not DM.existFile(self.letsPlayComp.getCuEp(EC.ORIGINAL_AUDIO_PATH)):
            self.reExctractAudio()

        #Auto Create the Comps Folder for the current Lets Play. 
        #Used for storing finished Audio Files.
        DM.createFolder(self.letsPlayComp.getCompPathWOF())
        
        if self.autoGenerateComp.toggle:
            self.generateComp()
        
        if self.autoSend2Resolve.toggle:
            self.sendEp2ResolveFA()
        #! Set Image for JTG
        
        self.jtgImage.setImage(image.load(self.letsPlayComp.getThumbnailPath()))
        
        #! Insert here default text for jtg
        
        

        #? Here we check exist for each key if not set Default Path
        
        if not self.letsPlayComp.getCuEpKeyExist(EC.ORIGINAL_VIDEO_LENGTH):
            self.letsPlayComp.setCuEp(
                EC.ORIGINAL_VIDEO_LENGTH,
                IVFX._getVideoLength(self.letsPlayComp.getCuEp(EC.ORIGINAL_VIDEO_PATH))
                )
            
        if not self.letsPlayComp.getCuEpKeyExist(EC.ORIGINAL_AUDIO_LENGTH):
            self.letsPlayComp.setCuEp(
                EC.ORIGINAL_AUDIO_LENGTH,
                AFX._getAudioLength(self.letsPlayComp.getCuEp(EC.ORIGINAL_AUDIO_PATH))
                )
        
        if not self.letsPlayComp.getCuEpKeyExist(EC.ORIGINAL_VIDEO_SIZE):
            self.letsPlayComp.setCuEp(
                EC.ORIGINAL_VIDEO_SIZE,
                DM.getFileSize(self.letsPlayComp.getCuEp(EC.ORIGINAL_VIDEO_PATH))
                )
        
        if not self.letsPlayComp.getCuEpKeyExist(EC.ORIGINAL_AUDIO_SIZE):
            self.letsPlayComp.setCuEp(
                EC.ORIGINAL_AUDIO_SIZE,
                DM.getFileSize(self.letsPlayComp.getCuEp(EC.ORIGINAL_AUDIO_PATH))
                )
        
        
        if SETTINGS._['fastLoad'] != self.fastLoadSwitch.toggle:
            SETTINGS._['fastLoad'] = self.fastLoadSwitch.toggle
            SETTINGS.save()
        
        #! Deprecated: self.generateAudioWave()
        if self.thumbnailAutoUpdateSwitch.toggle:
            self.rerollThumbnail()

        try:
            self.thumbnail.setSprite(self.letsPlayComp.getCuEp(EC.THUMBNAIL_PATH))
        except:
            self.rerollThumbnail()
            self.thumbnail.setSprite(self.letsPlayComp.getCuEp(EC.THUMBNAIL_PATH))
        
        if DM.existFile(self.letsPlayComp.getCuLp(LC.ICON)):
        
            self.icon.setSprite(self.letsPlayComp.getCuLp(LC.ICON))
        else:
            self.icon.setSprite(Surface((48,48)))
        self.titleChangeBox.setI(self.letsPlayComp.getCuEp(EC.TITLE))
        display.set_caption(f'{VERSIONSTRING} {self.letsPlayComp.getCuLp(LC.NAME)} - ep: {self.letsPlayComp.getEpisodeIndex()+1}')

        self.videoPlayer.aP,self.videoPlayer.vP = self.letsPlayComp.getAudioPath(),self.letsPlayComp.getVideoPath()

        self.lastThumbnailTime = self.letsPlayComp.getCuEp(EC.THUMBNAIL_FRAME)
        
        LOG.nlog(1,f'loaded: $ - $ ',[self.letsPlayComp.getCuLp(LC.NAME),self.letsPlayComp.getEpisodeIndex()+1])
        self._changeEpisodeLeftView()
        self.lc._stop(priority=1)
    
    def _changeEpisodeLeftView(self,*_):
        self.audioPathLabel.UX.text = str(self.letsPlayComp.getCuEp(EC.ORIGINAL_AUDIO_PATH))
        self.audioPathLabel.setImage(self.audioPathLabel.UX.gen())
        
        self.pathLabel.UX.text = str(self.letsPlayComp.getCuEp(EC.ORIGINAL_VIDEO_PATH))
        self.pathLabel.setImage(self.pathLabel.UX.gen())
        
        self.nameLabel.UX.text = f'{self.letsPlayComp.getCuLp(LC.NAME)} #{self.letsPlayComp.getEpisodeIndex() + 1} - [{self.letsPlayComp.getCuEp(EC.STATUS)}] {self.letsPlayComp.getCuEp(EC.UPLOAD_AT)}' # TODO : Use the new ST values
        self.nameLabel.setImage(self.nameLabel.UX.gen())

    def update(self):
        self.letsPlayComp.setCuEp(EC.TITLE,self.titleChangeBox.text)
        self.app.window.fill(Color('#141414'))
        self.wb.updateBeforeAll()
        match self.mode:
            case 0:
                if self.videoPlayer.fullscreen:
                    UIM.renderQueue(self.app,['videoPreview'])
                else:
                    UIM.renderQueue(self.app,['info','taskbar','episodeManipulation','videoPreview','others'])
        
                if not SETTINGS._['fastLoad']:
                    if not self.videoPlayer.fullscreen:
                        if self.letsPlayComp.getCuEp(EC.STATUS) < 31 and self.videoUpdate:  # TODO : Use the new ST values
                            self.videoPlayer.visible = True
                    else:
                        if self.letsPlayComp.getCuEp(EC.STATUS) < 31 and self.videoUpdate:  # TODO : Use the new ST values
                            self.videoPlayer.visible = True
            case 1:
                UIM.renderQueue(self.app,['taskbar','jtg'])
        textBoxActive = any([tI.active for tI in self.textInputs])#!ESSENTIAL!
        
        if not textBoxActive : self.checkKeyBinds()
        
        
        
        if self.letsPlayComp.getIsLastEpisode():
            
            # Wenn alle Folgen durchlaufen wurden setze die Werte zurück
            self.autoSwitchToNextEpisode.toggle = False
            self.autoForewardToNextEpisode.toggle = False
            self.autoGenerateComp.toggle = False
            self.autoSend2Resolve.toggle = False
        # Falls auto foreward laufe durch alle folgen und mache dinge
        
        if self.autoForewardToNextEpisode.toggle or self.autoSend2Resolve.toggle:
            self.letsPlayComp.change2Episode(1,self.onEpisodeLoad)
              
    def checkKeyBinds(self):
        
        KEYS = [str(key).lower() for key in self.app.keyboardInputs['currentKeys']]
        
        STRG = key.get_pressed()[K_LCTRL]
        if 'i' in KEYS:
            self.stateSystem.switchMode(1)
        if 'n' in KEYS or '\x0e' in KEYS:
            self.letsPlayComp.change2Episode(1,self.onEpisodeLoad)
        elif 'b' in KEYS or '\x02' in KEYS:
            self.letsPlayComp.change2Episode(-1,self.onEpisodeLoad)
        #elif '+' in KEYS:
        #    self.changeStatusPlus(None)
        #elif '-' in KEYS:
        #    self.changeStatusMinus(None)
        elif 'f' in KEYS:
            display.toggle_fullscreen()
        elif 'c' in KEYS:
            self.changeStatus(self.changeStatusButtons[1])
        elif 'x' in KEYS:
            self.changeStatus(self.changeStatusButtons[0])
        elif 'a' in KEYS:
            self.reExctractAudio(None)
        
        elif 's' in KEYS:
            self.sendEp2Resolve(None)

        elif 'd' in KEYS:
            if STRG:
                self.rerollThumbnail(None,frame=self.lastThumbnailTime)
            else:
                self.rerollThumbnail(None,frame=-1)
        """elif '6' in KEYS:
            if STRG:
                        self.rerollThumbnail(None,frame=self.lastThumbnailTime)
            else:
                _file = filedialog.askopenfilename()
                if _file != '':
                    try:
                        self.rerollThumbnail(None,frame=-1,overImage=image.load(_file))
                    except:
                        LOG.nlog(3,'File not readable')
                        
                else:
                    LOG.nlog(3,'File cant be empty!')"""
            
        

class LetsPlayPicker(Application):
    """
    The LetsPlayPicker:
        Used for picking a Lets Play for using in RecordingIndicator
    """
    def __init__(self, size: tuple | list = SETTINGS.window_size) -> None:
        super().__init__((256,48*10),avs=False,mov=True)
        #Get all lets plays
        display.set_caption(f'{VERSIONSTRING} LetsPlayPicker')
        display.set_icon(generateIcon(RI_LOGO))
        self.options = [LetsPlayFile(LETSPLAY_PATH + file) for file in listdir(LETSPLAY_PATH) if file.endswith('.json')]
        
        if self.options.__len__() == 0:
            #! The Program crashes if no LPF exists
            
            DM.save('default.json',DEFAULT_LPF_FILE)   #? Maybe create a default LPF will help
            CrashBox(ERRORDICT.NOLPFEXIST_JRI)
            self.isAlive = False
            self.crashed = True
            return
        
        self.buttons = []
        
        for idx,option in enumerate(self.options):      #For each lp in given path this method creates a button
            option: LetsPlayFile
            
            btn = UIButton(Rect(0,(idx*24),256,24),onPressCallback=self.select,ux={'text': option._getName(),'size':(256,24)})
            option.buttonId = btn.elementId
            self.buttons.append(btn)
    def select(self,*args):
        """
        Set the current Lets Play
        """
        for x in self.options:
            if x.buttonId == args[0].elementId:
                RUNTIMESETTIGS['letsPlay'] = self.options[x.buttonId]
                RUNTIMESETTIGS['path'] = self.options[x.buttonId].filePath
                self.isAlive = False

class RecordingIndicator(Application):
    """
    The Recording Indicator
    """
    def __init__(self, size: tuple | list = SETTINGS.window_size) -> None:
        super().__init__((512,217),avs=False,mov=True)
        UIM.queue.clear()

        self.maxLength = None
        display.set_caption(f'{VERSIONSTRING} RecordingIndicator')
        display.set_icon(generateIcon(RI_LOGO))
        
        self.count = 0
    def update(self,obso):
        if obso.connectionEstablished:
            clamText = 'Connected'
        else:
            clamText = 'Search'
        display.set_caption(f'{VERSIONSTRING} RecordingIndicator({clamText}) {obso.currentLPData._getName()} - {obso.currentLPData._getEpisodeCount()}')
        time = str(obso.getTime())      #Get Time
        try: time = f"{time.split(':')[1]}:{time.split(':')[2]}"
        except: time = '00:00'
        time = time.split('.')[0]
        
        
        if obso.warnings > 1:
            self.count += TIME()
            if int(time.split(':')[1]) % 2 == 0:
                self.window.fill(Color('#cfcfcf'))
            else:
                self.window.fill(Color('#121212'))
        else:
            self.window.fill(Color('#121212'))
            self.count = 0
        
        #time += f' - {obso.currentLPData._getEpisodeCount()}' #Adds the print on screen the episode Ammount!

        FONT = FONT180BS.render(f'{time}',True,obso.color)
        
        self.window.blit(FONT,(256-(FONT.get_width()//2),0))
        
        return super().update()
    

            