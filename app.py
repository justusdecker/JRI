from flask import Flask

from bin.letsPlayFile import LetsPlayFile
from bin.constants import LETSPLAY_PATH
from os import listdir

from flask import render_template
from json import load
from markdown import markdown

app = Flask(__name__)






@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all_videos/')
def video_show():
    site = render_template('all_videos.html')
    
    OUTPUT_STRING = ""
    markdown()
    
    temp_string = """
# GAME_NAME

[Image](ICON_PATH)


"""
    
    
    
    lets_plays: list[LetsPlayFile] = [LetsPlayFile(LETSPLAY_PATH + file) for file in listdir(LETSPLAY_PATH) if file.endswith('.json')]
    
    for lp in lets_plays:
        for ep in lp._getEpisodes():
            pass
    
    return site



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)