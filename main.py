

from bin.application import Application
from bin.programs import StateManager



class Main(Application):
    def __init__(self, size: tuple | list = (1280,720), avs=False, con=True,mov=True) -> None:
        super().__init__(size, avs, con,mov)
    def update(self):
        if STM.crashed: self.isAlive = False
        STM.update()
        return super().update()

T = Main()
STM = StateManager(T)


T.run()
#subprocess.Popen(SETTINGS._getPath('resolvePath'))
