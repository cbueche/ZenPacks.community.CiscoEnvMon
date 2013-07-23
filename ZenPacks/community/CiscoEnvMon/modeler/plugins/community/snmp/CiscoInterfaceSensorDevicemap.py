from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class CiscoInterfaceSensorDevicemap(SnmpPlugin):

    modname = "ZenPacks.community.CiscoEnvMon.CiscoInterfaceSensorDevice"


    def process(self, device, results, log):
        log.debug('Creating CiscoInterfaceSensorDevice')
        om = self.objectMap()
        return om

