######################################################################
#
# CiscoInterfaceSensorDevice object class
# Used so CiscoInterfaceSensor has something to relate to
#
# Copyright (C) 2013 Russell Dwarshuis, Merit Network, Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
######################################################################

from Globals import InitializeClass
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class CiscoInterfaceSensorDevice(Device,ZenPackPersistence):
    "A device with Cisco Interface Sensors"

    meta_type = 'CiscoInterfaceSensorDevice'

    _relations = Device._relations + (
        ('CiscoInterfaceSensor',
         ToManyCont(ToOne,
                    'ZenPacks.community.CiscoEnvMon.CiscoInterfaceSensor',
                    'CiscoInterfaceSensorDevice')
        )
    )

    factory_type_information = deepcopy(Device.factory_type_information)

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(CiscoInterfaceSensorDevice)
