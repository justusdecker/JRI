FPS = 60

VERSION = (1,14,24,'beta')

NATIVE_FILE_EXTENSION_LPF = '.lpf'

DAVINCIRESOLVESCRIPTFOLDER = "C:\\Users\\Justus\\AppData\\Roaming\\Blackmagic Design\\DaVinci Resolve\\Support\\Fusion\\Scripts\\Edit"

from os import getlogin

USERNAME = getlogin()

ABSOLUTE_PATH = f'C:\\Users\\{USERNAME}\\jri_data\\'

AUDIO_PATH = f'{ABSOLUTE_PATH}audio\\'#!Switch to if all eps are gone
LETSPLAY_PATH = f'{ABSOLUTE_PATH}lps\\'
THUMBNAIL_PATH = f'{ABSOLUTE_PATH}thumbs\\'
LOGOS_PATH = f'{ABSOLUTE_PATH}logos\\'
FONT_PATH = f'{ABSOLUTE_PATH}fonts\\'
LOWRES_PATH = f'{ABSOLUTE_PATH}lowres\\'
ATT_PATH = f'{ABSOLUTE_PATH}att\\'
WAVEFORM_PATH = f'{ABSOLUTE_PATH}wv\\'

DEFAULT_LPF_FILE = {
    "name": "",
    "icon": "",
    "path2save": "",
    "episode_length": 3600,
    "gameName": "",
    "titleEnding": "",
    "description": "",
    "episodes": [],
    "thumbnailAutomationData": {
        "text_epNum": {
            "text": "",
            "font": "",
            "align": "center",
            "size": 100,
            "pos": [
                0,
                0
            ],
            "rot": 0,
            "cropping": [
                0,
                0,
                0,
                0
            ],
            "outline": {
                "xMinus": 2,
                "xPlus": 2,
                "yMinus": 2,
                "yPlus": 2,
                "color": [
                    [
                        50,
                        50,
                        50
                    ],
                    [
                        14,
                        14,
                        14
                    ],
                    [
                        14,
                        14,
                        14
                    ],
                    [
                        50,
                        50,
                        50
                    ]
                ]
            },
            "color": "#ffffff"
        },
        "images": [
            {
                "path": "",
                "scale": 0.4,
                "pos": [
                    260,
                    160
                ],
                "rot": 0,
                "align": "center",
                "cropping": [
                    0,
                    0,
                    0,
                    0
                ]
            }
        ],
        "background": {
            "position": [
                0,
                0
            ],
            "randomPositionX": 0,
            "randomPositionY": 0,
            "rotation": 0,
            "randomRotation": [
                -4.5,
                4.5
            ],
            "randomScale": [
                0.35,
                0.5
            ],
            "scale": 1.9,
            "hue": 0,
            "saturation": 1,
            "lightness": 1,
            "center": True
        }
    },
    "tags": [
        ""
    ]
}

SettingCollection: dict = {
            'width': 480,
            'height': 720,
            'obsDirPath': "C:\\Program Files (x86)\\Steam\\steamapps\\common\\OBS Studio\\bin\\64bit\\",
            'obsHost': '192.168.0.12',
            'obsPort': 4455,
            'obsPassword': '',
            'obsTimeout': 1,
            'fastLoad': False,
            'autoSave': True,
            'videoPlaybackFps': 8
        }

class EC:
    """
    ! All keys listed for reading & writing to any episode
    """        
    THUMBNAIL_PATH = 'thumbnailPath' 
    ORIGINAL_VIDEO_PATH = 'path'
    EPISODE_NUMBER = 'episodeNumber'
    STATUS = 'status' 
    MARKERS = 'markers'
    TITLE = 'episodeTitle'
    THUMBNAIL_FRAME = 'thumbnailFrame'
    UPLOAD_AT = 'uploadAt'
    ORIGINAL_AUDIO_PATH = 'audioFilePath'
    ORIGINAL_DESKTOP_AUDIO_PATH = 'audioDesktopFilePath'
    LOW_RES_VIDEO_PATH = 'lowResFilePath'
    LOW_RES_AUDIO_PATH = 'lowResAudioFilePath'
    ORIGINAL_VIDEO_SIZE = 'videoFileSize'
    ORIGINAL_AUDIO_SIZE = 'audioFileSize'
    ORIGINAL_VIDEO_LENGTH = 'videoLength'
    ORIGINAL_AUDIO_LENGTH = 'audioLength'
    ORIGINAL_AUDIO_WAVEFORM_PATH = 'waveFormPath'

class LC:
    """
    ! All keys listed for reading & writing to any letsPlayFile
    """
    NAME = 'name'
    ICON = 'icon'
    EPISODE_LENGTH = 'episode_length'
    GAME_NAME = 'gameName'
    TITLE_ENDING = 'titleEnding'
    DESCRIPTION = 'description'
    EPISODES = 'episodes'
    THUMBNAIL_AUTOMATION_DATA = 'thumbnailAutomationData'
    TAGS = 'tags'

DAVINCIRESOLVESCRIPTFOLDER = "C:\\Users\\Justus\\AppData\\Roaming\\Blackmagic Design\\DaVinci Resolve\\Support\\Fusion\\Scripts\\Edit"
