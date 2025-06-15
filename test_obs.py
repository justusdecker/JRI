from bin.automation.obsow import OBSObserver
from bin.letsPlayFile import LetsPlayFile
def c_text(text:str, color: tuple) -> str:
    r,g,b = color
    return f'\033[38;2;{r};{g};{b}m{text}\033[39m'
def main():
    
    lpc = LetsPlayFile('C:\\\\Users\\Justus\\jri_data\\lps\\astroneer.json')
    obs = OBSObserver(lpc)
    while 1:
        print(obs.time,c_text(obs.time,obs.color))
        obs.update()
main()