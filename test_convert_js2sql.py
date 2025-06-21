from bin.data_management import DM
LP = DM.loads('C:\\Users\\Justus\\jri_data\\lps\\thief simulator.json')
import sqlite3

CONNECTION = sqlite3.connect('episodes.db')

with open('bin\\sql\\crt_episode.sql') as f:
    sql_create = f.read()
    CONNECTION.execute(sql_create)

with open('bin\\sql\\ins_episode.sql') as f:
    sql_insert = f.read()
for ep in LP['episodes']:
    inj = sql_insert.replace(
        '__VALUES__',
        str( (ep['path'],ep['audioFilePath'],ep['audioDesktopFilePath'] if 'audioDesktopFilePath' in ep else "",ep['thumbnailPath'],ep['thumbnailFrame']) )
    )
    CONNECTION.execute(inj)
    
CONNECTION.commit()
CONNECTION.close()