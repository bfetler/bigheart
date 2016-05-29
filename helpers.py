# helper methods

import datetime
import time

def getDateStr(dateint):
    ddate = datetime.datetime.fromtimestamp(dateint)
    return str(ddate.strptime(str(ddate), "%Y-%m-%d %H:%M:%S"))

def getNowTimeInt():
    '''get current time as int since 1970'''
    return int(time.mktime(datetime.datetime.now().timetuple()))

def get_menu(label, choices):
    return [ {label:choice} for choice in choices ]

def get_gender_menu():
    return get_menu('gender', ['Female','Male'])

# this should be order in html menu, not same order as formula
def get_ddensity_menu():
    return get_menu('ddensity', ['True','False','Unsure'])

def get_appendage_menu():
    return get_menu('appshape', ['Convex','Concave','Flat','Unsure'])

# use boolean not string?
def int2bool(intval):
    return 'True' if intval == 1 else 'False'

def bool2int(str):
    return 1 if str == 'True' else 0

def int2choice(intval):
    if intval == 2:
        r = 'True'
    elif intval == 0:
        r = 'False'
    else:
        r = 'Unsure'
    return r

def choice2int(str):
    if str == 'True':
        r = 2
    elif str == 'False':
        r = 0
    else:
        r = 1
    return r

# use dict instead of nested if?
def appendage2choice(intval):
    intval = int(intval)
    if intval == 2:
        r = 'Convex'
    elif intval == 0:
        r = 'Concave or Flat'
    else:
        r = 'Unsure'
    return r

def choice2appendage(str):
    if str == 'Convex':
        r = 2
    elif str == 'Concave':
        r = 0
    elif str == 'Flat':
        r = 0
    else:
        r = 1
    return r


