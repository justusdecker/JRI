from time import time
from bin.constants import VERSION, Styles, Icons
import ctypes
from bin.log import LOG
from bin.dataManagement import DM
import sys
from os import listdir
_DEPRECATOR_CRASH = False

def debugExecutionTimeCheckWOV(func):
    """
    Simply caching the input & output for later use
    """
    def wrapper():
        LOG.nlog(0,f'run: $',[func.__name__])
        _t = time()
        _ret = func()
        _t = (time()-_t)*1_000_000
        LOG.nlog(0,f'fin: $ in $ μs ]',[func.__name__,_t])

        return _ret
    return wrapper

def debugExecutionTimeCheck(func):
    """
    Simply caching the input & output for later use
    """
    def wrapper(*args,**kwargs):
        LOG.nlog(0,f'run: $',[func.__name__])
        _t = time()
        _ret = func(*args,**kwargs)
        _t = int((time()-_t)*1_000_000)
        LOG.nlog(0,f'fin: $ in $ μs args: $ kwargs: $',[func.__name__,_t,len(args),len(kwargs)])
        return _ret
    return wrapper

def DeprecationWarn(func):
    """
    Simply caching the input & output for later use
    """
    def wrapper(*args,**kwargs):
        if _DEPRECATOR_CRASH: 
            LOG.nlog(3,f'DeprecationError for $ lr: $ - $ in $ cL: $',[func.__name__,*convCoL(func.__code__.co_lines()),func.__code__.co_filename,sys._getframe().f_back.f_lineno])
            raise Exception(f'DeprecationError {func.__name__:<15} origin: line {convCoL(func.__code__.co_lines())} in {func.__code__.co_filename} traceback: line {sys._getframe().f_back.f_lineno}')
        
        LOG.nlog(2,f'DeprecationWarning for $ lr: $ - $ in $ cL: $',[func.__name__,*convCoL(func.__code__.co_lines()),func.__code__.co_filename,sys._getframe().f_back.f_lineno])
        
        _ret = func(*args,**kwargs)
        
        return _ret
    return wrapper
def convCoL(val):
    val = list(val)[0]
    #return f'{val[2]}-{val[2]+val[1]}'
    return val[2],val[2]+val[1]

def DeprecationError(func):
    """
    Simply caching the input & output for later use
    """
    def wrapper():
        #.co_filename()
        LOG.nlog(3,f'DeprecationError for $ lr: $ - $ in $ cL: $',[func.__name__,*convCoL(func.__code__.co_lines()),func.__code__.co_filename,sys._getframe().f_back.f_lineno])
        raise Exception(f'DeprecationError {func.__name__:<15} origin: line {convCoL(func.__code__.co_lines())} in {func.__code__.co_filename} traceback: line {sys._getframe().f_back.f_lineno}')
    return wrapper


def DeprecationLineWarn(name):
    LOG.nlog(2,f'DeprecationWarning for [ ${name:<15} ] in line ${sys._getframe().f_back.f_lineno}')

def OutsourceWarn(version,to,crash=False):
    """
    Simply caching the input & output for later use
    """
    def decorator(func):
        def wrapper(*args,**kwargs):
            LOG.nlog(2,f'OutsourceWarn for $ lr: $ - $ in $ cL: $ | $ $',[func.__name__,*convCoL(func.__code__.co_lines()),func.__code__.co_filename,sys._getframe().f_back.f_lineno,version,to])
            
            _ret = func(*args,**kwargs)
            
            return _ret
        return wrapper
    return decorator


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
def CrashBox(error:list):
    return Mbox(error[0], error[1], Icons.STOP + Styles.OK)

def QuestionBox(error:list):
    return Mbox(error[0], error[1], Icons.QUESTION + Styles.YES_NO)