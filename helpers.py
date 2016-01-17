# helper methods

import datetime
import time

def getDateStr(dateint):
    ddate = datetime.datetime.fromtimestamp(dateint)
    return str(ddate.strptime(str(ddate), "%Y-%m-%d %H:%M:%S"))

def getNowTimeInt():
    '''get current time as int since 1970'''
    return int(time.mktime(datetime.datetime.now().timetuple()))

# use boolean not string?
def int2bool(intval):
    return 'True' if intval == 1 else 'False'

def bool2int(str):
    return 1 if str == 'True' else 0

def int2choice(intval):
    if intval == 1:
        r = 'True'
    elif intval == 2:
        r = 'False'
    else:
        r = 'Unsure'
    return r

def choice2int(str):
    if str == 'True':
        r = 1
    elif str == 'False':
        r = 2
    else:
        r = 0
    return r

# use dict instead of nested if?
def appendage2choice(intval):
    intval = int(intval)
    if intval == 1:
        r = 'Concave or Flat'
    elif intval == 2:
        r = 'Convex'
    else:
        r = 'Unsure'
    return r

def choice2appendage(str):
    if str == 'Concave':
        r = 1
    elif str == 'Flat':
        r = 1
    elif str == 'Convex':
        r = 2
    else:
        r = 0
    return r


