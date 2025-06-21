
def no(*_): pass

def getHexDoubleZeros(val):
    if val.__len__() < 2:
        return '0' + str(val)
    return str(val)

def isnumeric(number: float | int) -> bool:
    try: 
        float(number)
        return True
    except:
        return False