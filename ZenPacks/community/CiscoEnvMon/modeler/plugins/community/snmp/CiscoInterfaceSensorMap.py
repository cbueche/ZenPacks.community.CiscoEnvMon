################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Walk IF-MIB ifXTable ifName to find names of interfaces, then walk
entSensorValueTable to find similar entries in entSensorMeasuredEntity
for temperature, bias current, voltage, transmit and receive optical power
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class CiscoInterfaceSensorMap(SnmpPlugin):
    """Map Cisco Enviroment sensors to intefaces."""

    maptype = "CiscoInterfaceSensorMap"
    modname = "ZenPacks.community.CiscoInterfaceSensor"
    relname = "CiscoInterfaceSensor"
    compname = "hw"

    snmpGetTableMaps = ( GetTableMap('ifXTable',
                                     '1.3.6.1.2.1.31.1.1.1',
                                     { '.1': 'ifName' }
                                    ),
                         GetTableMap('entSensorValue',
                                     '1.3.6.1.4.1.9.9.91.1.1',
                                     { '.7': 'EntPhysicalIndexOrZero' }
                                    )
                       )

    def process(self, device, resluts, log):
        """ Run SNMP queries, process returned values, find Cisco Interface
sensors"""
        log.info('Modeling device %s using %s', device.id, self.name)
        getdata, tabledata = results
        rm = self.relMap()
        # build dictionary of ifName,index.
        ifNames = {}
        # iterate over ifNames to find matching sensors
            # fancy code goes here....

        # remove this, it is for debugging:
        om = self.objectMap()
        om.ifName = 'Gi0/3'
        om.ifIndex = 10103
        om.zifName = 'GigabitEthernet0_3'
        om.eptTemperatureIndex = 1015
        om.eptVoltageIndex = 1016
        om.eptCurrentIndex = 1017
        om.eptTxPwrIndex = 1018
        om.eptRxPwrIndex = 1019
        rm.append(om)

        return rm
