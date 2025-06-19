from bin.query.thumbnail_generator_query import ThumbnailGeneratorQuery
from bin.automation.thumbnail_generator import ThumbnailGenerator,ThumbnailAutomationData
from bin.letsplay_file import LetsPlayFile,get_lpf_by_hash
from bin.constants import PATHS
from os import listdir
from json import dumps
query = "lp=b0f77dbed3fa65c549497ee2034923fb200c2a6b45aa5e41ea006f3c1770775f&px=50&py=60&text_font=&text_align=align_center&font_s=&text_r=&logo_path=internet.PNG&logo_s=&logo_r=&logo_x=&logo_y=&logo_align=align_center&p_x=&p_y=&rp_x=&rp_y=&r=&rr_x=&rr_y=&s=&rs_x=&rs_y=&hue=&sat=&lig=&background="
TGQ = ThumbnailGeneratorQuery(query)
TG = ThumbnailGenerator()

lp = get_lpf_by_hash([LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')],TGQ.lp)

print(dumps(TGQ.asdict(),indent=4))

TG.create_thumbnail(
    TGQ.ep,
    lp.get_episode(TGQ.ep).video_path,
    -1,
    ThumbnailAutomationData(TGQ.asdict()),
    lp.name

)