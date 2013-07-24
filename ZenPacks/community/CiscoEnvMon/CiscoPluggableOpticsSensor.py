################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2013 Russell Dwarshuis
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CiscoPluggableOpticsSensor

CiscoPluggableOpticsSensor is used to measure temperature, supply voltage, bias
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
log = logging.getLogger('CiscoPluggableOpticsSensor')


class CiscoPluggableOpticsSensor(ExpansionCard):
    """CiscoPluggableOpticsSensor object"""

    portal_type = meta_type = 'CiscoPluggableOpticsSensor'

    # set default _properties
    ifName = 'Not set by modeler'   # from IF-MIB ifXTable
    ifIndex = -1                    # index for above
    zifName = 'Not set by modeler'  # interface name as set in zenoss
    # the following are from the entSensorValues table
    entSensorType = 'unknown' # like amperes, celsius, dBm, voltsDC
    entSensorScale = 1        # a power of 10
    entSensorPrecision = 1

    _properties = (
        {'id':'ifName', 'type':'string', 'mode':''},
        {'id':'ifIndex', 'type':'int', 'mode':''},
        {'id':'zifName', 'type':'string', 'mode':''},
        {'id': 'entSensorType','type': 'string','mode':''},
        {'id': 'entSensorScale','type': 'float','mode':''},
        {'id': 'entSensorPrecision','type': 'int','mode':''},
    )

    factory_type_information = (
        {
            'id'             : 'CiscoPluggableOpticsSensor',
            'meta_type'      : 'CiscoPluggableOpticsSensor',
            'description'    : "Environment monitoring of optical modules",
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCiscoPluggableOpticsSensor',
            'immediate_view' : 'viewCiscoPluggableOpticsSensor',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCiscoPluggableOpticsSensor'
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


InitializeClass(CiscoPluggableOpticsSensor)

