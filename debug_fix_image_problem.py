from bin.letsplay_file import LetsPlayFile

from bin.constants import PATHS
from os import listdir
LPF = [LetsPlayFile(PATHS.letsplay + file) for file in listdir(PATHS.letsplay) if file.endswith('.json')]

for lp in LPF:
    print(lp.asdict())
    