# FMC-Objec-tImport-Export
Scripts for Exporting and Objects from one Firepower Management Console and Importing them into another.

# FMCPortImport
API Import and Grouping of Common Protocol Port Objects into Cisco Firepower Managment Console

## Pre-Requisits
This python script requires the addition of two non-standard libraries (fireREST, and ansicolors).  These pre-requisits can be installed using the pip:

**`pip install ansicolors fireREST`**

## Purpose
This Script is being developed in response to a recent project where I was unable to upgrade FMC to support the newer Cisco Secure Firewall devices, without loosing managment support for existing legacy ASA devices.

**Logging**
Export and Import Scripts will create log files named **FMCObjectImport.log** and **FMCObjectExport.log** respectively.  The default logging leve is set to INFO.  Logging level can be changed my modifying line 6 of each script:

```
logging.basicConfig(filename='FMCObjectImport.log',level=logging.INFO)
```
For more information on python logging levels reference the [Python Documentation Site]("https://docs.python.org/3/library/logging.html")


**FMCExportObjects.py**
This Python script will export Objects from an FMC Deployment to json files. This script will also export various policy objects, along will Access Control Policy rules.  Additional work will be done to develop further capabilities to export and import Policies.

***Exported Objects and Associated Files***
| Object Type | JSON Export File | 
|-------------|-------------|
| Security Zones| securityzone.json |
| Interface Groups | interfacegroup.json |
| ICMP V4 Port Objects | icmpv4object.json |
| Port Objects | protocolportobject.json |
| Network Subnet Objects | network.json |
| Network Host Objects | host.json |
| Network Range Objects | range.json |
| Network FQDN Objects | fqdn.json |
| Port Object Groups | portobjectgroup.json |
| Network Object Groups | networkgroup.json |

***Exported Policies and Associated Files***
| Policy Type | JSON Export File |
|-------------|------------------|
| Access Policies | accesspolicy.json |
| File Policies | filepolicy.json |
| Intrusion Policies | intrusionpolicy.json |
| Prefilter Policies | prefilterpolicy.json |

Each Access Policy is also exported along with Its associated Categories and Rules.

| Access Policy Elements | JSON Export File |
|------------------------|------------------|
| Access Policy | \<PolicyName\>_Policy.json |
| Access Policie Categories | \<PolicyName\>_Policy_Categories.json |
| Access Policy Rules | \<PolicyName\>_Policy_Rules.json |

**NOTE:**
All file names referenced in the above tables are used during object import.  Renaming these files will have a negative impact on object imports

**FMCImportObjects.py**

This Script will import objects to an other FMC deployment, by reading the json data files saved by FMCExportObjects.py. The process will remove unwanted metadata from the exported json data before importing and creating new objects. Object groups will also be imported and member objects will be matched to the newly created object id's in the new FMC deployment.

**NOTE:**
Curently No import action is taken for Access, Intrusion, File, or Prefilter Policies.  This functionality will require a fair amount of tested as so many objects are referenced by each poicy rule.  Each object will need to have it's name validated and it's id attribute update