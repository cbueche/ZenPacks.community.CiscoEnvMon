################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Walk IF-MIB ifXTable ifName to find names of interfaces, then
walk entSensorValueTable to find similar entries in entSensorMeasuredEntity
for temperature, bias current, voltage, transmit and receive optical power.
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class CiscoPluggableOpticsSensorMap(SnmpPlugin):
    "Map Cisco Enviroment sensors on intefaces to the python class for them"

    modname = "ZenPacks.community.CiscoEnvMon.CiscoPluggableOpticsSensor"
    relname = "cards"
    compname = "hw"

    snmpGetTableMaps = ( GetTableMap('ifEntry',
                                     '1.3.6.1.2.1.2.2.1',
                                     { '.2' : 'ifDescr' }
                                    ),
                         GetTableMap('entPhysicalEntry',
                                     '1.3.6.1.2.1.47.1.1.1.1',
                                     { '.2' : 'entPhysicalDescr' }
                                    ),
                         GetTableMap('entSensorValueEntry',
                                     '1.3.6.1.4.1.9.9.91.1.1',
                                     { '.1' : 'entSensorType',
                                       '.2' : 'entSensorScale',
                                       '.3' : 'entSensorPrecision' }
                                    ),
                       )

    def process(self, device, results, log):
        """ Run SNMP queries, process returned values, find Cisco PluggableOptics
sensors"""
        log.info('Starting process() for modeler CiscoPluggableOpticsSensorMap')
        getdata, tabledata = results
        rm = self.relMap()
        # build dictionary of ifName,index and entPhysicalDescr,index
        ifNames = {}
        physDecrs = {}
        for oid, ifName in tabledata.get("ifEntry").iteritems():
            ifNames[ifName['ifDescr']] = int(oid.strip('.'))
        for oid, physDecr in tabledata.get("entPhysicalEntry").iteritems():
            physDecrs[physDecr['entPhysicalDescr']] = int(oid.strip('.'))
        
        log.debug('ifNames: %s' % ifNames)
        log.debug('physDecrs: %s' % physDecrs)
        intfSensors = []
        ifIndexes = []
        # iterate over ifNames to find matching sensors
        for ifName, ifIndex in ifNames.iteritems():
            for physDescr, physIndex in physDecrs.iteritems():
                isSensor = '%s%s' % \
                    (ifName,r'\s+.*[temperature|current|voltage|power]')
                if re.match(isSensor,physDescr,re.IGNORECASE):
                    intfSensors.append(physDescr)
                    ifIndexes.append(ifIndex)

        for sensor in intfSensors:
            om = self.objectMap()
            om.id = self.prepId(sensor)
            om.snmpindex = physDecrs[sensor]
            rm.append(om)

        return rm
