
def no(*_): pass


def getDoubleZeros(val):
    if val < 10:
        return '0' + str(val)
    return str(val)

def getHexDoubleZeros(val):
    if val.__len__() < 2:
        return '0' + str(val)
    return str(val)