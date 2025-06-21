from bin.data_management import DM
LP = DM.loads('C:\\Users\\Justus\\jri_data\\lps\\thief simulator.json')
import sqlite3
from os.path import isfile
def load_and_execute_sql(sql_connection,filepath: str,replacer: list[tuple[str,str]]):
    with open(filepath) as f:
        sql: str = f.read()
        for old, new in replacer:
            sql = sql.replace(old, new)
        sql_connection.execute(sql)
        sql_connection.commit()
def read_one_line_sql(sql_connection,filepath: str,id: int) -> list:
    with open(filepath) as f:
        sql: str = f.read().replace('__ID__',f'{id}')
    return sql_connection.execute(sql).fetchone()

def remove_by_id_sql(sql_connection,filepath: str,id: int) -> list:
    with open(filepath) as f:
        sql: str = f.read().replace('__ID__',f'{id}')
        sql_connection.execute(sql)

# TODO
# Delete entry
class Episodes:
    def __init__(self, filepath: str):
        exist = isfile(filepath)
        self.connection = sqlite3.connect(filepath)
        if not exist: # Create a new table in db if file not exist before creating by this class
            load_and_execute_sql(self.connection,'bin\\sql\\crt_episode.sql',[])
            print('added file')
        
        self.filepath = filepath
    def on_close(self):
        self.connection.close()
    def delete(self,id: int) -> list:
        return remove_by_id_sql(self.connection,'bin\\sql\\del_episode.sql',id)
    def read(self,id: int) -> list:
        return read_one_line_sql(self.connection,'bin\\sql\\rea_episode.sql',id)
    def update(self,id: int, key: str, value):
        load_and_execute_sql(
            self.connection,
            'bin\\sql\\upd_episode.sql',
            [('__ID__',f'{id}'),('__KEY__',key),("__VALUE__",value)]
            )
    def create(self,
                    video_path: str,
                    audio_mic_path: str,
                    audio_desktop_path: str,
                    thumbnail_path: str,
                    thumbnail_frame: float) -> None:
        
        load_and_execute_sql(
            self.connection,
            'bin\\sql\\ins_episode.sql',
            [('__VALUES__',str( (video_path,audio_mic_path,audio_desktop_path,thumbnail_path,thumbnail_frame) ))]
            )
EP = Episodes('ep.db')

EP.create('abc','def','ghi','jkm',123.2)
EP.update(2,'VIDEO_PATH', '"ABC123"')
print(EP.read(1))
EP.delete(1)
EP.on_close()