################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CiscoInterfaceSensor

CiscoInterfaceSensor is used to measure temperature, supply voltage, bias
current, transmit power and receiver power on Cisco pluggable optical
modules.
"""

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS, ZEN_VIEW_HISTORY

from Products.ZenModel.ExpansionCard import ExpansionCard

import logging
log = logging.getLogger('CiscoInterfaceSensor')


class CiscoInterfaceSensor(ExpansionCard):
    """CiscoInterfaceSensor object"""

    portal_type = meta_type = 'CiscoInterfaceSensor'

    # set default _properties
    ifName = 'Not set by modeler'   # from IF-MIB ifXTable
    ifIndex = -1                    # index for above
    zifName = 'Not set by modeler'  # interface name as set in zenoss
    # the following are indexes from the entPhysicalTable for entPhysicalName
    # for temperature, etc. for this interface
    eptTemperatureIndex = -1
    eptVoltageIndex = -1
    eptCurrentIndex = -1
    eptTxPwrIndex = -1                 # transmit power
    eptRxPwrIndex = -1                 # receive power

    _properties = (
        {'id':'ifName', 'type':'string', 'mode':''},
        {'id':'ifIndex', 'type':'int', 'mode':''},
        {'id':'zifName', 'type':'string', 'mode':''},
        {'id': 'eptTemperatureIndex','type': 'int','mode':''},
        {'id': 'eptVoltageIndex','type': 'int','mode':''},
        {'id': 'eptCurrentIndex','type': 'int','mode':''},
        {'id': 'eptTxPwrIndex','type': 'int','mode':''},
        {'id': 'eptRxPwrIndex','type': 'int','mode':''}
    )

    factory_type_information = (
        {
            'id'             : 'CiscoInterfaceSensor',
            'meta_type'      : 'CiscoInterfaceSensor',
            'description'    : "Environment monitoring of interface hardware",
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCiscoInterfaceSensor',
            'immediate_view' : 'viewCiscoInterfaceSensor',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCiscoInterfaceSensor'
                , 'permissions'   : (ZEN_VIEW)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS)
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_HISTORY)
                },
            )
          },
        )

    def viewName(self):
        return self.id
    name = viewName

    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete Component
        """
        self.getPrimaryParent()._delObject(self.id)
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(self.device().hw.absolute_url())


InitializeClass(CiscoInterfaceSensor)

