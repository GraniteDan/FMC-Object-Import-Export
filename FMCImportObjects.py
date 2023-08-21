from fireREST import FMC
import csv, json
from colors import red, green, blue, yellow, magenta, cyan
from getpass import getpass
import logging
logging.basicConfig(filename='FMCObjectImport.log',level=logging.INFO)
## Global Variables ##
global fmc

def GetObject (otype,oname):
    try:
        obj = (getattr(fmc.object, otype).get(name=oname))
    except:
        obj = None
    return obj

def GetObjectID (otype,oname):
    try:
        obj = (getattr(fmc.object, otype).get(name=oname))
    except:
        obj = None
    return obj['id']

def GetPortObject (portname):
    try:
        obj = fmc.object.protocolportobject.get(name=portname)
    except:
        obj = None
    return obj

def GetPortGroup (groupname):
    try:
        obj = fmc.object.portobjectgroup.get(name=groupname)
    except:
        obj = None
    return obj

def sanitize_object (obj):
    del obj['id']
    del obj['metadata']
    del obj['links']
    if 'interfaces' in obj:
        del obj['interfaces']
    return obj

def import_object(filename,type):
    #IMPORT NETWORK OBJECTS FROM JSON FILE
    with open(filename, 'r') as file:
        obj = json.load(file)
        
        print('Importing ' + type + ' objects')

        for o in obj:
            o = sanitize_object(obj=o)
            if not GetObject(otype=type, oname=o['name']):
                try:
                    print('Creating New ' + type + ' Object ' + o['name'])
                    getattr(fmc.object, type).create(data=o)
                except Exception as e:
                    print(red(e))
                    logging.error(o['name'] + ' - ' + type + ':' + e)

def search_dictionaries(key, value, list_of_dictionaries):
  return [element for element in list_of_dictionaries if element[key] == value]

h1 = """
################################################################################################

Cisco Firepower Managment Console API Object Importer

!!! ENSURE API ACCESS IS ENABLED IN THE FMC @: SYSTEM > CONFIGURATION > REST API PREFERENCES !!!

Author: Dan Parr / @GraniteDan
Created: August 7 2023
Version: 1.0

This Script Relies on a number of Python Libraries (fireREST, csv, ansicolors)
################################################################################################

"""

print(yellow(h1))
filename = 'protoports.csv'
SZones=[]
CSVData=[]

ip = input("Enter your FMC Management IP/Hostname:")
user = input("Enter FMC Username:")
pwd = getpass()
fmc = FMC(hostname=ip, username=user, password=pwd, domain='Global')
pwd = None


netgrpfile='networkgroup.json'
prtgrpfile = 'portobjectgroup.json'


objlist = [
    {
    'type': 'securityzone',
    'filename': 'securityzone.json'
    },
    {
    'type':'interfacegroup',
    'filename': 'interfacegroup.json'
    },
    {
    'type': 'icmpv4object',
    'filename': 'icmpv4object.json'
    },
    {
    'type': 'protocolportobject',
    'filename': 'protocolportobject.json'
    },
    {
    'type': 'network',
    'filename': 'network.json'
    },
    {
    'type': 'range',
    'filename': 'range.json'
    },
    {
    'type': 'host',
    'filename': 'host.json'
    },
    {
    'type': 'fqdn',
    'filename': 'fqdn.json'
    }
]

for o in objlist:
    import_object(filename=o['filename'], type=o['type'])

#IMPORT PORT GROUPS
with open(prtgrpfile, 'r') as pgfile:
    print('Importing Port Groups')
    obj = json.load(pgfile)
    for pgobj in obj:
        pgobj = sanitize_object(obj=pgobj)
        if 'objects' in pgobj:
            for ref in pgobj['objects']:
                membername = ref['name']
                print(yellow('Group: ' + pgobj['name'] + ' Updating Member IDs:'))
                print(membername + ' Original ID: ' + ref['id'])
                ref['id'] = GetObjectID(otype = (ref['type']).lower(), oname=membername)
                print(membername + ' New ID: ' + ref['id'])
        else:
            print('Group: ' + pgobj['name'] + ' defined with no memebers')
        if not GetObject(otype='portobjectgroup', oname=pgobj['name']):
            try:
                print('Creating New Port Group Object ' + pgobj['name'])
                print(magenta(json.dumps(pgobj, indent=2)))
                fmc.object.portobjectgroup.create(data=pgobj)
            except Exception as e:
                print(red(e))
                logging.error(pgobj['name'] + ' - ' + pgobj['type'] + ':' + e)
#IMPORT NETWORK GROUPS
with open(netgrpfile, 'r') as ngfile:
    print('Importing Network Groups')
    obj = json.load(ngfile)
    for ngobj in obj:
        del ngobj['id']
        del ngobj['metadata']
        del ngobj['links']
        if 'interfaces' in ngobj:
            del ngobj['interfaces']
        if 'objects' in ngobj:
            for ref in ngobj['objects']:

                print(yellow('Group: ' + ngobj['name'] + ' Updating Member IDs:'))
                print(ref['name'] + ' Original ID: ' + ref['id'])
                ref['id'] = GetObjectID(otype = (ref['type']).lower(), oname=ref['name'])
                print(ref['name'] + ' New ID: ' + ref['id'])
        else:
            print('Group: ' + ngobj['name'] + ' defined with no memebers')
        if not GetObject(otype='networkgroup', oname=ngobj['name']):
            try:
                print('Creating New NetworkGroup Object ' + ngobj['name'])
                fmc.object.networkgroup.create(data=ngobj)
            except Exception as e:
                print(red(e))
                logging.error(ngobj['name'] + ' - ' + ngobj['type'] + ':' + e)

