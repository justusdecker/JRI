from functools import lru_cache
from time import time,sleep
from threading import Thread
from random import randint
class CACHE:
    """
    Simply caching the input & output for later use
    """
    def __init__(self,deleteAfterX: int = 10,sleepInterval: int = 5) -> None:
        self.clear()
        self.gcThreading = True
        
        self.deleteAfterX = deleteAfterX
        self.sleepInterval = sleepInterval
        self.gcThread()
        #hold massivly used caches in memory even deleteAfterX
    def gcThread(self):
        if not hasattr(self,'th'):
            self.th = Thread(target=self.gc)
            self.th.start()
        else:
            if not self.th.is_alive():
                self.th = Thread(target=self.gc)
                self.th.start()
    def read(self,key):
        self.rws[0] += 1
        return self.data[key][0]
    def write(self,key,val):
        self.rws[1] += 1
        _l = len(bin(val[0]).split("0b")[1])+len(bin(val[1]).split("0b")[1])
        print(f'cached: {_l} bits')
        self.data[key] = (val,int(time()*1000)+self.deleteAfterX)
    def clear(self):
        self.data = {}
        self.rws = [0,0]
    def gc(self):
        while self.gcThread:
            sleep(self.sleepInterval)
            _t = int(time()*1000)
            self.data = {object: self.data[object] for object in self.data.keys() if _t < self.data[object][1]}


C = CACHE()

def simpleCache(func):
    """
    Simply caching the input & output for later use
    """
    def wrapper(a,b):
        _inputValues = f'{a}_{b}'
        if not _inputValues in C.data:
            C.write(_inputValues,func(a,b))
        return C.read(_inputValues)
        
    return wrapper

@simpleCache
def testFunction(a,b):
    print(f'generated at {a} {b} {int(time())}')
    return a+1,b**2


while 1:
    testFunction(randint(0,3),randint(0,3))
testFunction(4,2)
print(testFunction(4,6))