from flask import Flask


from bin.letsplay_file import LetsPlayFile,get_lpf_by_hash,get_ep_by_hash
from bin.constants import PATHS
from os import listdir,remove
from os.path import isfile

from flask import render_template, request, redirect
from json import load, dumps
from markdown import markdown

from bin.automation.obsow import OBSObserver

from pygame.image import load as img_load, save as img_save
from pygame.transform import scale
from bin.convert_help import whelp

from bin.query.thumbnail_generator_query import ThumbnailGeneratorQuery
whelp()

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
    lets_plays: list[LetsPlayFile] = [LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')]
    return render_template('all_videos.html', lps=lets_plays,isfile=isfile,l=len)

@app.route('/create')
def create():
    return render_template('lets_play_create.html')

@app.route('/edit')
def edit():
    return render_template('lets_play_edit.html')

@app.route('/delete')
def delete():

    """
    ! DELETE CODE HERE
    ? GET QUERY 'lp name'
    """
    return redirect('/')

@app.route('/lp/<ep_hash>/<int:ep_id>')
def get_episode(ep_hash: str, ep_id: int):
    lp = get_lpf_by_hash([LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')],ep_hash)
    if lp is None:
        return f"<h1>Let's Play with {ep_hash} doesn't exist!</h1>", 404
    if ep_id >= len(lp.episodes):
        return f"<h1>Episode with ID: {ep_id} doesn't exist!</h1>", 404
    
    return f'<p>{dumps(lp.get_episode(ep_id).asdict(),indent=4)}</p>'

@app.route('/lp/options/<lp_name>')
def option_change(lp_name:str) -> str:
    return 'WIP' ,404



@app.route('/settings')
def set_settings():
    return "WIP", 404



@app.route('/picker', methods=['GET', 'POST'])
def set_lets_play():
    lpfs = [LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')]
    if request.method == "POST" and 'lp' in request.form:
        OBS.load_lpf(get_lpf_by_hash(lpfs,request.form['lp']))
    return render_template('lets_play_picker.html', lps=lpfs)

@app.route('/record')
def get_recording_status():
    OBS.update()
    temp = render_template('lets_play_record.html')
    col = rgb2hex(OBS.color)
    
    
        
    return temp.replace('__TIME_CODE__',f'<h1 style="color:{col};">{OBS.timecode}</h1>')

@app.route('/help')
def help_site():
    return render_template('help.html')     

@app.route('/thumbnail-generator', methods=['GET', 'POST'])
def thumbnail_gen():
    TGQ = ThumbnailGeneratorQuery(request.query_string.decode())
    
    print(TGQ.pos_x,TGQ.pos_y)
    return render_template('thumbnail_generator.html',lps=[LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)