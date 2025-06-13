from flask import Flask

from bin.letsPlayFile import LetsPlayFile
from bin.constants import LETSPLAY_PATH
from os import listdir

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
            ep['name']
            TMP_EPISODE = EPISODE
        
        
        
        OUTPUT_STRING += TMP_OP_STRING
        
    return site.replace("__VIDEOS_GO_HERE__",OUTPUT_STRING)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)