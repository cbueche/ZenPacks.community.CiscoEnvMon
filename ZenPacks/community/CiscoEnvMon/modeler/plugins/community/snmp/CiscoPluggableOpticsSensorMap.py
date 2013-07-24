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
        # build dictionary of ifName,index.
        ifNames = {}
        # iterate over ifNames to find matching sensors
            # fancy code goes here....

        # remove this, it is for debugging:
        om = self.objectMap()
        om.id = 'GigabitEthernet0_3 Module Temperature Sensor'
        om.ifName = 'Gi0_3'
        om.ifIndex = 10103
        om.zifName = 'GigabitEthernet0_3'
        om.snmpindex = 1015
        rm.append(om)

        return rm
