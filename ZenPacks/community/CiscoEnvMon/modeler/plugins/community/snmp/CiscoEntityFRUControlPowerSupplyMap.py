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

__doc__= """ CiscoEntityFRUControlPowerSupplyMap

CiscoEntityFRUControlPowerSupplyMap maps the FRUPowerOperStatus table to powersupplies objects

"""

__version__ = '1.3.0'

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap


class CiscoEntityFRUControlPowerSupplyMap(SnmpPlugin):
    """Map CiscoEntityFRUControl PowerSupplies table to model."""

    maptype = "CiscoEntityFRUControlPowerSupplyMap"
    modname = "ZenPacks.community.CiscoEnvMon.CiscoPowerSupply"
    relname = "powersupplies"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('FRUPowerStatusEntry',
                    '.1.3.6.1.4.1.9.9.117.1.1.2.1',
                    {
                        '.2': 'state',
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

    states = {1: 'offEnvOther',
              2: 'on',
              3: 'offAdmin',
              4: 'offDenied',
              5: 'offEnvPower',
              6: 'offEnvTemp',
              7: 'offEnvFan',
              8: 'failed',
              9: 'onButFanFail',
              10: 'offCooling',
              11: 'offConnectorRating',
              12: 'onButInlinePowerFail',
              }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('CiscoEntityFRUControlPowerSupplyMap : processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()

        # find the list of power supplies from the physical entities
        _indexes = []
        _descr = {}
        _name = {}
        _entity_psu_nr = 0
        log.debug('looking for power supplies in entities')
        for oid, entity in tabledata.get("entPhysicalEntry", {}).iteritems():
            log.debug('found entity <%s> from class %s', str(entity['_name']), str(entity['_class']))
            # within 1.3.6.1.2.1.47.1.1.1.1.5, class=6 --> powerSupply
            if entity['_class'] == 6:
                log.debug('CiscoEntityFRUControlPowerSupplyMap : found powerSupply entity : <%s>', str(entity['_name']))
                snmpindex = oid.strip('.')
                _indexes.append(snmpindex)
                _descr[str(snmpindex)] = entity['_descr']
                _name[str(snmpindex)] = entity['_name']
                _entity_psu_nr += 1

        # construct a powerSupply list
        log.debug('selecting powerSupply for monitoring')
        _real_psu_nr = 0
        for oid, ps in tabledata.get("FRUPowerStatusEntry", {}).iteritems():
            snmpindex = oid.strip('.')
            if snmpindex in _indexes:
                try:
                    n = _name[str(snmpindex)]
                    if not n:
                        n = _descr[str(snmpindex)]
                    ps['id'] = n

                    om = self.objectMap(ps)
                    om.snmpindex = snmpindex
                    om.id = self.prepId(om.id)
                    om.state = self.states.get(int(om.state), 'unknown')
                    _real_psu_nr += 1
                except AttributeError:
                    continue
                log.debug('adding powerSupply %s having state %s and index %s' % (om.id, om.state, str(om.snmpindex)))
                rm.append(om)

        log.info('CiscoEntityFRUControlFanMap : found %s entity fan(s), %s monitored fan(s)' % (_entity_psu_nr, _real_psu_nr))

        return rm
