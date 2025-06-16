from bin.automation.obsow import OBSObserver
from bin.letsplay_file import LetsPlayFile
def c_text(text:str, color: tuple) -> str:
    r,g,b = color
    return f'\033[38;2;{r};{g};{b}m{text}\033[39m'
def main():
    
    lpc = LetsPlayFile('C:\\\\Users\\Justus\\jri_data\\lps\\astroneer.json')
    obs = OBSObserver(lpc)
    while 1:
        print(obs.time,c_text(obs.time,obs.color))
        obs.update()
main()

"""
{
    "name": "astroneer",
    "icon": "C:\\Users\\Justus\\jri_data\\logos\\subnautica_logo.png",
    "path2save": "",
    "episode_length": 35,
    "gameName": "raft",
    "titleEnding": " | raft #",
    "description": "No description",
    "episodes": [
        {
            "path": "C:/Users/Justus/Videos/2025-04-04 23-04-33.mp4",
            "episodeNumber": 1,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\1_astroneer_Thumbnail.png",
            "thumbnailFrame": 1105.5243014738498,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\1_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-04 23-27-13.mp4",
            "episodeNumber": 2,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\2_astroneer_Thumbnail.png",
            "thumbnailFrame": 270.5572073819805,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\2_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-04 23-51-53.mp4",
            "episodeNumber": 3,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\3_astroneer_Thumbnail.png",
            "thumbnailFrame": 312.50249886053444,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\3_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 00-14-28.mp4",
            "episodeNumber": 4,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\4_astroneer_Thumbnail.png",
            "thumbnailFrame": 586.1111025858643,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\4_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 00-36-31.mp4",
            "episodeNumber": 5,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\5_astroneer_Thumbnail.png",
            "thumbnailFrame": 873.2504817203712,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\5_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 01-01-53.mp4",
            "episodeNumber": 6,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\6_astroneer_Thumbnail.png",
            "thumbnailFrame": 999.378417575098,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\6_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 01-23-12.mp4",
            "episodeNumber": 7,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\7_astroneer_Thumbnail.png",
            "thumbnailFrame": 1038.751164242635,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\7_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 01-53-23.mp4",
            "episodeNumber": 8,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\8_astroneer_Thumbnail.png",
            "thumbnailFrame": 24.190480536477835,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\8_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 02-17-12.mp4",
            "episodeNumber": 9,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\9_astroneer_Thumbnail.png",
            "thumbnailFrame": 537.4194305084646,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\9_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 22-04-42.mp4",
            "episodeNumber": 10,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\10_astroneer_Thumbnail.png",
            "thumbnailFrame": 343.2352991891516,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\10_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 22-26-45.mp4",
            "episodeNumber": 11,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\11_astroneer_Thumbnail.png",
            "thumbnailFrame": 367.03719434049555,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\11_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 22-50-21.mp4",
            "episodeNumber": 12,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\12_astroneer_Thumbnail.png",
            "thumbnailFrame": 1341.9474011091452,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\12_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-05 23-13-43.mp4",
            "episodeNumber": 13,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\13_astroneer_Thumbnail.png",
            "thumbnailFrame": 811.9298291408511,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\13_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-06 10-58-21.mp4",
            "episodeNumber": 14,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\14_astroneer_Thumbnail.png",
            "thumbnailFrame": 56.757234665328454,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\14_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-06 11-21-53.mp4",
            "episodeNumber": 15,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\15_astroneer_Thumbnail.png",
            "thumbnailFrame": 1333.7216093317031,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\15_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-06 11-44-59.mp4",
            "episodeNumber": 16,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\16_astroneer_Thumbnail.png",
            "thumbnailFrame": 992.9884258310511,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\16_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-06 12-07-08.mp4",
            "episodeNumber": 17,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\17_astroneer_Thumbnail.png",
            "thumbnailFrame": 840.092876315494,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\17_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-06 22-24-51.mp4",
            "episodeNumber": 18,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\18_astroneer_Thumbnail.png",
            "thumbnailFrame": 919.0647223184602,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\18_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-06 22-48-54.mp4",
            "episodeNumber": 19,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\19_astroneer_Thumbnail.png",
            "thumbnailFrame": 1061.9106295222891,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\19_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-10 14-36-56.mp4",
            "episodeNumber": 20,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\20_astroneer_Thumbnail.png",
            "thumbnailFrame": 203.89791719992652,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\20_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-10 14-57-48.mp4",
            "episodeNumber": 21,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\21_astroneer_Thumbnail.png",
            "thumbnailFrame": 431.6858368154445,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\21_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-10 15-18-53.mp4",
            "episodeNumber": 22,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\22_astroneer_Thumbnail.png",
            "thumbnailFrame": 1106.5686866462345,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\22_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-10 15-40-31.mp4",
            "episodeNumber": 23,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\23_astroneer_Thumbnail.png",
            "thumbnailFrame": 914.8450615020429,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\23_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-10 16-09-36.mp4",
            "episodeNumber": 24,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\24_astroneer_Thumbnail.png",
            "thumbnailFrame": 854.233948386326,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\24_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-10 16-31-07.mp4",
            "episodeNumber": 25,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\25_astroneer_Thumbnail.png",
            "thumbnailFrame": 996.3453880338568,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\25_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-04-10 16-51-59.mp4",
            "episodeNumber": 26,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\26_astroneer_Thumbnail.png",
            "thumbnailFrame": 753.5416458467574,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\26_astroneer_track.mp3"
        },
        {
            "path": "C:/Users/Justus/Videos/2025-06-14 22-22-40.mp4",
            "episodeNumber": 27,
            "status": 0,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": null,
            "thumbnailFrame": 0,
            "uploadAt": "",
            "audioFilePath": null
        },
        {
            "path": "C:/Users/Justus/Videos/2025-06-14 22-22-40.mp4",
            "episodeNumber": 28,
            "status": 0,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": null,
            "thumbnailFrame": 0,
            "uploadAt": "",
            "audioFilePath": null
        },
        {
            "path": "C:/Users/Justus/Videos/2025-06-14 22-26-05.mp4",
            "episodeNumber": 29,
            "status": 7,
            "markers": [],
            "episodeTitle": "",
            "thumbnailPath": "C:\\Users\\Justus\\jri_data\\thumbs\\astroneer\\29_astroneer_Thumbnail.png",
            "thumbnailFrame": 22.9409222932163,
            "uploadAt": "",
            "audioFilePath": "C:\\Users\\Justus\\jri_data\\audio\\astroneer\\29_astroneer_track.mp3"
        }
    ],
    "thumbnailAutomationData": {
        "text_epNum": {
            "text": "Minecraft",
            "font": "C:\\Users\\Justus\\jri_data\\fonts\\Conthrax-SemiBold.otf",
            "align": "center",
            "size": 150,
            "color": "#92c8e0",
            "pos": [
                640,
                200
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
            }
        },
        "images": [
            {
                "path": "C:\\Users\\Justus\\jri_data\\logos\\subnautica_thumb_logo.png",
                "scale": 1,
                "pos": [
                    640,
                    80
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
        ]
    },
    "tags": [
        "minecraft",
        "lets play"
    ]
}"""