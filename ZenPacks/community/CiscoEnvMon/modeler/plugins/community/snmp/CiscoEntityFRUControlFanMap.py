################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2010-2013 Egor Puzanov.
# Changes by Lionel Seydoux and Charles Bueche
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """CiscoEntityFRUControlFanMap

CiscoEntityFRUControlFanMap maps the FanTrayStatusEntry table to fans objects

"""

__version__ = '1.3.0'

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap


class CiscoEntityFRUControlFanMap(SnmpPlugin):
    """Map CiscoEntityFRUControl Fan table to model."""

    maptype = "CiscoEntityFRUControlFanMap"
    modname = "ZenPacks.community.CiscoEnvMon.CiscoFan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('FanTrayStatusEntry',
                    '.1.3.6.1.4.1.9.9.117.1.4.1.1',
                    {
                        '.1': 'state',
                    }
                    ),
        GetTableMap('entPhysicalEntry',
                    '.1.3.6.1.2.1.47.1.1.1.1',
                    {
                        '.2': '_descr',
                        '.5': '_class',
                        '.7': '_name',
                    }
                    ),
    )

    states = {1: 'unknown',
              2: 'up',
              3: 'down',
              4: 'warning',
              }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('CiscoEntityFRUControlFanMap : processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()

        # find the list of fans from the physical entities
        log.debug('looking for fans in entities')
        _indexes = []
        _descr = {}
        _name = {}
        _entity_fan_nr = 0
        for oid, entity in tabledata.get("entPhysicalEntry", {}).iteritems():
            log.debug('found entity <%s> from class %s', str(entity['_name']), str(entity['_class']))
            # within 1.3.6.1.2.1.47.1.1.1.1.5, class=7 --> fan
            if entity['_class'] == 7:
                log.debug('CiscoEntityFRUControlFanMap : found fan entity : <%s>', str(entity['_name']))
                snmpindex = oid.strip('.')
                _indexes.append(snmpindex)
                _descr[str(snmpindex)] = entity['_descr']
                _name[str(snmpindex)] = entity['_name']
                _entity_fan_nr += 1

        # construct a fan list
        log.debug('selecting fans for monitoring')
        _real_fan_nr = 0
        for oid, fan in tabledata.get("FanTrayStatusEntry", {}).iteritems():
            snmpindex = oid.strip('.')
            if snmpindex in _indexes:
                try:
                    n = _name[str(snmpindex)]
                    if not n:
                        n = _descr[str(snmpindex)]
                    fan['id'] = n

                    om = self.objectMap(fan)
                    om.snmpindex = snmpindex
                    om.id = self.prepId(om.id)
                    om.state = self.states.get(int(om.state), 'unknown')
                    _real_fan_nr += 1
                except AttributeError:
                    continue
                log.debug('adding fan %s having state %s and index %s' % (om.id, om.state, str(om.snmpindex)))
                rm.append(om)

        log.info('CiscoEntityFRUControlFanMap : found %s entity fan(s), %s monitored fan(s)' % (_entity_fan_nr, _real_fan_nr))
        return rm
