
import ctypes  # An included library with Python install.
class ERRORIDS:
    OBSWSTE : int = 1
    OBSWE : int = 2
    OBSMO : int = 3
    LPFNAMEEMPTY : int = 4
    JRICANTCONNECT : int = 5
class ERRORDICT:
    NOLPFEXIST_JRI : list = ['JRI Crashed','No LPF File in destination\ndefault.json created.\nProgram closes!']
    NOLPFEXIST_JVE : list = ['JVE Crashed','No LPF File in destination']
    OBSCANTCONNECT : list = ['OBS cant connect', '']
class Styles:
    OK =                    0
    OK_CANCEL =             1
    ABORT_RETRY_IGNORE =    2
    YES_NO_CANCEL =         3
    YES_NO =                4
    RETRY_NO =              5
    CANCEL_RETRY_CONTINUE = 6
class Icons:
    STOP        =   16
    QUESTION    =   32
    EXCLAMATION =   48
    INFORMATION =   64
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
def CrashBox(error:list):
    return Mbox(error[0], error[1], Icons.STOP + Styles.OK)

def QuestionBox(error:list):
    return Mbox(error[0], error[1], Icons.QUESTION + Styles.YES_NO)
