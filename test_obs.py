from bin.obsow import OBSObserver
from bin.letsPlayFile import LetsPlayFile
def main():
    
    lpc = LetsPlayFile('C:\\\\Users\\Justus\\jri_data\\lps\\astroneer.json')
    obs = OBSObserver(lpc)
    while 1:
        print(obs.time)
main()