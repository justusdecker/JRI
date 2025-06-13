from flask import Flask

from bin.letsPlayFile import LetsPlayFile
from bin.constants import LETSPLAY_PATH
from os import listdir
from os.path import isfile

from flask import render_template
from json import load
from markdown import markdown

app = Flask(__name__)

def load_file(file_path: str) -> str:
    with open(file_path,'r') as f_in:
        return f_in.read()




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all_videos/')
def video_show():
    site = render_template('all_videos.html')
    
    OUTPUT_STRING = ""

    HEADER = load_file("templates\\lets_play_header.html")
    
    EPISODE = load_file("templates\\lets_play_episode.html")
    
    lets_plays: list[LetsPlayFile] = [LetsPlayFile(LETSPLAY_PATH + file) for file in listdir(LETSPLAY_PATH) if file.endswith('.json')]
    
    
    
    for lp in lets_plays:
        TMP_OP_STRING = ''
        
        TMP_HEADER = HEADER
        TMP_HEADER = TMP_HEADER.replace('__LP_NAME__',lp._getName())
        TMP_HEADER = TMP_HEADER.replace('__ICON_PATH__',lp._getIconPath())
        TMP_HEADER = TMP_HEADER.replace('__GAME_NAME__',lp._getGameName())
        TMP_HEADER = TMP_HEADER.replace('__EPISODE_LENGTH__',str(lp._getEpisodeLength()))
        
        TMP_OP_STRING += TMP_HEADER + '\n'
        
        for ep in lp._getEpisodes():

            TMP_EPISODE = EPISODE
            
            TMP_EPISODE = TMP_EPISODE.replace('__EP_VIDEO_EXISTS__','🟢' if isfile(ep['path']) else '🔴')
            TMP_EPISODE = TMP_EPISODE.replace('__EP_TRACK_1_EXISTS__','🟢' if ep['audioFilePath'] else '🔴')
            #! Missing Attr Track 2
            TMP_EPISODE = TMP_EPISODE.replace('__EP_NUMBER__',str(ep['episodeNumber']))
            
            TMP_EPISODE = TMP_EPISODE.replace('__EP_TITLE__',str(ep['episodeTitle']))
            TMP_EPISODE = TMP_EPISODE.replace('__EP_VIDEO_FILE_SIZE__',str(ep['videoFileSize']))
            TMP_EPISODE = TMP_EPISODE.replace('__EP_VIDEO_LENGTH__',str(ep['videoLength']))
            
            TMP_EPISODE = TMP_EPISODE.replace('__EP_MARKER_COUNT__',str(len(ep['markers'])))
            TMP_EPISODE = TMP_EPISODE.replace('__EP_THUMBNAIL_FRAME__',str(ep['thumbnailFrame']))
            
            
            
            TMP_EPISODE = TMP_EPISODE.replace('__VIDEO_PATH__',ep['path'])
            TMP_EPISODE = TMP_EPISODE.replace('__AUDIO_TRACK_1_PATH__',ep['audioFilePath'].replace('\\','/'))
            
            
            TMP_OP_STRING += TMP_EPISODE + '\n'

        
        OUTPUT_STRING += TMP_OP_STRING
        
    return site.replace("__VIDEOS_GO_HERE__",OUTPUT_STRING)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)