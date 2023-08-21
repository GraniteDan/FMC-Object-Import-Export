from fireREST import FMC
import csv, json
from colors import red, green, blue, yellow, magenta, cyan
from getpass import getpass
import logging
logging.basicConfig(filename='FMCObjectExport.log',level=logging.INFO)

h1 = """
################################################################################################

Cisco Firepower Managment Console API Object Exporter

!!! ENSURE API ACCESS IS ENABLED IN THE FMC @: SYSTEM > CONFIGURATION > REST API PREFERENCES !!!

Author: Dan Parr / @GraniteDan
Created: August 7 2023
Version: 1.0

This Script Relies on a number of Python Libraries (fireREST, csv, ansicolors)
################################################################################################

"""

print(yellow(h1))
filename = 'protoports.csv'
Groups=[]
CSVData=[]

ip = input("Enter your FMC Management IP/Hostname:")
user = input("Enter FMC Username:")
pwd = getpass()
fmc = FMC(hostname=ip, username=user, password=pwd, domain='Global')
pwd = None


objdata = ['fqdn','host','icmpv4object','interfacegroup','network','networkgroup','portobjectgroup','protocolportobject','range','securityzone']
poldata = ['accesspolicy','filepolicy','intrusionpolicy','prefilterpolicy']

for o in objdata:
    fn = o + '.json'
    data = (getattr(fmc.object, o).get())
    with open (fn, 'w', encoding='utf-8') as jfile:
        jdata = json.dump(data, jfile, ensure_ascii=False, indent=2)

for o in poldata:
    fn = o + '.json'
    data = (getattr(fmc.policy, o).get())
    with open (fn, 'w', encoding='utf-8') as jfile:
        jdata = json.dump(data, jfile, ensure_ascii=False, indent=2)

with open ('accesspolicy.json', 'r') as polfile:
    APlist = json.load(polfile)
    for pol in APlist:
        polname = pol['name']
        objdata = fmc.policy.accesspolicy.get(name=polname)
        objid=objdata['id']
        catdata = fmc.policy.accesspolicy.category.get(container_uuid=objid)
        poldata = fmc.policy.accesspolicy.accessrule.get(container_uuid=objid)
        print(cyan(json.dumps(poldata, indent=2)))
        print(yellow('#############################################################################################'))
        print(green(json.dumps(catdata, indent=2)))

        with open (polname + '_Policy_Rules.json', 'w', encoding='utf-8') as jfile:
            json.dump(poldata, jfile, ensure_ascii=False, indent=2)

        with open (polname + '_Policy_Categories.json', 'w', encoding='utf-8') as jfile:
            json.dump(catdata, jfile, ensure_ascii=False, indent=2)
 
        with open (polname + '_Policy.json', 'w', encoding='utf-8') as jfile:
            json.dump(objdata, jfile, ensure_ascii=False, indent=2)