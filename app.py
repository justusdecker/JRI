from flask import Flask


from bin.letsplay_file import LetsPlayFile
from bin.constants import PATHS
from os import listdir,remove
from os.path import isfile

from flask import render_template, request
from json import load, dumps
from markdown import markdown

from bin.automation.obsow import OBSObserver

from pygame.image import load as img_load, save as img_save
from pygame.transform import scale

"""for file in listdir('static\\img\\temps'):
    remove( f'static\\img\\temps\\{file}')
for lpf in [LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')]:
    for ep in lpf.episodes:
        if ep.thumbnail_path:
            if isfile(ep.thumbnail_path):
                img_save(scale(img_load(ep.thumbnail_path),(384,216)),f'static\\img\\temps\\{lpf.name}_{ep.episode_number}.png')"""
def rgb2hex(rgb: tuple[int]) -> str:
    r,g,b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"

def get_lets_play(lpf: str | None = None):
    lpf_files = [LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')]
    if lpf is not None:
        for lp in lpf_files:
            if lp.name == lpf:
                return lp
    if lpf_files:
        return lpf_files[0]
    
OBS = OBSObserver(get_lets_play()) if [file for file in listdir(PATHS.letsplay) if file.endswith('.json')] else None

app = Flask(__name__)

def load_file(file_path: str) -> str:
    with open(file_path,'r') as f_in:
        return f_in.read()


def getsearch(string: str) -> str:
    if not string: return ""
    for i in string.split('?'):
        if 'search=' in i:
            return i.split('=')[1]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all_videos/')
def video_show():
    
    
    site = render_template('all_videos.html')
    
    # GET QUERY
    search = getsearch(request.query_string.decode())
    
    OUTPUT_STRING = ""

    
    EPISODE = load_file("templates\\lets_play_episode.html")
    
    lets_plays: list[LetsPlayFile] = [LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')]
    
    
    i = 0
    for lp in lets_plays:
        TMP_OP_STRING = ''

        for ep in lp.episodes:
            i += 1
            TMP_EPISODE = EPISODE
            _is_in = []
            for before, after in (
                ('__EP_VIDEO_EXISTS__','🟢' if isfile(ep.video_path) else '🔴'),
                ('__EP_TRACK_1_EXISTS__','🟢' if ep.audio_path else '🔴'),#! Missing Attr Track 2
                ('__EPISODE_NUMBER__',str(ep.episode_number)),
                ('__EP_TITLE__',str(ep.title)),
                ('__EP_VIDEO_FILE_SIZE__',str(ep.video_size)),
                ('__EP_VIDEO_LENGTH__',str(ep.video_length)),
                ('__EP_MARKER_COUNT__',str(len(ep.markers))),
                ('__EP_THUMBNAIL_FRAME__',str(ep.frame)),
                ('__VIDEO_PATH__',ep.video_path),
                ('__AUDIO_TRACK_1_PATH__',ep.audio_path.replace('\\','/') if ep.audio_path is not None else 'n.a.'),
                ('__THUMBNAIL__',f'../static/img/temps/{lp.name}_{ep.episode_number}.png'),
                ('__ID__',f'{i}')
            ):
                TMP_EPISODE = TMP_EPISODE.replace(before, after)
                _is_in.append(after) #nasty but it works
            if not search or search.lower() in "".join(_is_in).lower():
                TMP_OP_STRING += TMP_EPISODE + '\n'

        
        OUTPUT_STRING += TMP_OP_STRING
        
    return site.replace("__VIDEOS_GO_HERE__",OUTPUT_STRING)

@app.route('/lets-play/<lp_title>/<ep_id>')
def get_episode(lp_title: str, ep_id: str):
    if not ep_id.isdecimal():
        return "<h1>Somethings went wrong: (1002) episode id must be an integer</h1>"
    lets_plays: list[LetsPlayFile] = [LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')]
    for lp in lets_plays:
        if lp.name == lp_title:
            return f"<p>{dumps(lp.get_episode(int(ep_id)).asdict(),indent=4).replace('\n','<br>')}</p>"
    else:
        return "<h1>Somethings went wrong: (1001) No Lets Play found!</h1>"


@app.route('/lets-play/options/<lp_name>')
def option_change(lp_name:str) -> str:
    return 'WIP'



@app.route('/settings')
def set_settings():
    return "WIP"

@app.route('/picker', methods=['GET', 'POST'])
def set_lets_play():
    
    if request.method == "POST" and 'lp' in request.form:
        OBS.load_lpf(LetsPlayFile(PATHS.letsplay + request.form['lp']))
        
    site = render_template('lets_play_picker.html')
    TMP = '<form method="POST">'
    for idx, lp in enumerate(listdir(PATHS.letsplay)):
       TMP += f'<p><input type="radio" name="lp" value="{lp}">{lp}</p>'
    site = site.replace('__LETS_PLAY_GO_HERE__', TMP) + '<p><input type="submit"></p></form>'
    return site

@app.route('/record')
def get_recording_status():
    OBS.update()
    temp = render_template('lets_play_record.html')
    col = rgb2hex(OBS.color)
    
    
        
    return temp.replace('__TIME_CODE__',f'<h1 style="color:{col};">{OBS.timecode}</h1>')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)