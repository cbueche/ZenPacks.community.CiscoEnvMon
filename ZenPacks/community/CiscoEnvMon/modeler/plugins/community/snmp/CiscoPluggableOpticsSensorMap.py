################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Walk IF-MIB ifEntry ifDescr to find names of interfaces, then
walk entSensorValueTable to find similar entries in entSensorMeasuredEntity
for temperature, bias current, voltage, transmit and receive optical power.
Exclude sensors that have entSensorStatus not equal to 1 (ok)
"""

import re
from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetTableMap

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
                                     '1.3.6.1.4.1.9.9.91.1.1.1.1',
                                     { '.1' : 'entSensorType',
                                       '.2' : 'entSensorScale',
                                       '.3' : 'entSensorPrecision',
                                       '.5' : 'entSensorStatus' }
                                    ),
                       )

    def process(self, device, results, log):
        """
Run SNMP queries, process returned values, find Cisco PluggableOptics sensors
        """
        log.info('Starting process() for modeler CiscoPluggableOpticsSensorMap')

        # sensor names match if they contain an interface name append with:
        _sensor_regex = r'\s+.*[temperature|current|voltage|power]'

        # from CISCO-ENTITY-SENSOR-MIB
        _SensorDataType = {
          1  : 'other',
          2  : 'unkown',
          3  : 'voltsAC',
          4  : 'voltsDC',
          5  : 'amperes',
          6  : 'watts',
          7  : 'hertz',
          8  : 'celsius',
          9  : 'percentRH',
          10 : 'rpm',
          11 : 'cmm',
          12 : 'truthvalue',
          13 : 'specialEnum',
          14 : 'dBm' }
        _SensorDataScale = {
           7  : .000001,
           8  : .001,
           9  : 1,
           10 : 1000 }

        getdata, tabledata = results
        rm = self.relMap()
        # build dictionary of ifDescr,index and entPhysicalDescr,index
        ifDescrs = {}
        physDescrs = {}
        for index, ifDescr in tabledata.get("ifEntry").iteritems():
            ifDescrs[ifDescr['ifDescr']] = index
        for index, physDescr in tabledata.get("entPhysicalEntry").iteritems():
            physDescrs[physDescr['entPhysicalDescr']] = index

        if not ifDescrs:
            log.info('No ifDescrs found in ifEntry SNMP table')
            return
        if not physDescrs:
            log.info(
                'No entPhysicalDescrs found in entPhysicalEntry SNMP table')
            return

        entSensorValueEntry = tabledata.get('entSensorValueEntry')
        if not entSensorValueEntry:
            log.info('No data returned from entSensorValueEntry SNMP table')
            return
        
        # iterate over ifDescrs to find matching sensors
        for ifDescr, ifIndex in ifDescrs.iteritems():
            for physDescr, physIndex in physDescrs.iteritems():
                if re.search(ifDescr + _sensor_regex, physDescr, re.IGNORECASE):
                    log.info('Found sensor %s' % physDescr)
                    if entSensorValueEntry[physIndex]['entSensorStatus'] != 1:
                        log.info('entSensorStatus != ok on %s' % physDescr)
                        continue
                    om = self.objectMap()
                    om.id = self.prepId(physDescr)
                    om.snmpindex = int(physIndex.strip('.'))
                    om.ifDescr= ifDescr
                    om.ifIndex = int(ifIndex.strip('.'))
                    om.entSensorType = _SensorDataType[
                         int(entSensorValueEntry[physIndex]['entSensorType'])]
                    om.entSensorScale = _SensorDataScale[
                         int(entSensorValueEntry[physIndex]['entSensorScale'])]
                    om.entSensorPrecision = \
                         int(entSensorValueEntry[physIndex]['entSensorPrecision'])
                    om.monitor = True
                    rm.append(om)

        return rm
