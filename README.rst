==============================
ZenPacks.community.CiscoEnvMon
==============================

About
=====

This Monitoring ZenPack provides Cisco Environmental monitoring including fans,
temperature sensors, power supplies, pluggable optics modules and expansion
modules.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2, Zenoss 3.2 and Zenoss 4.2. You can download the free Core
version of Zenoss from http://community.zenoss.org/community/download.


Installation
============

Normal Installation (packaged egg)
----------------------------------

Download the `CiscoEnvMon ZenPack <http://http://wiki.zenoss.org/ZenPack:Cisco_Environmental_Monitor>`_.
Copy the .egg file to your Zenoss server and run the following commands as the zenoss
user.

    ::

        zenpack --install ZenPacks.community.CiscoEnvMon-1.2.0.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the CiscoEnvMon
ZenPack you should clone the git `repository <https://github.com/epuzanov/ZenPacks.community.CiscoEnvMon>`_,
then install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.CiscoEnvMon.git
        zenpack --link --install ZenPacks.community.CiscoEnvMon
        zenoss restart


Usage
=====

Installing the ZenPack will add the following items to your Zenoss system.

Modeler Plugins
---------------

- **community.snmp.CiscoExpansionCardMap** - this modeler plugin tries to
  identify the Model, Vendor and Serial Number of installed expansion modules.
- **community.snmp.CiscoFanMap** - Fan modeler plugin.
- **community.snmp.CiscoPowerSupplyMap** - Power Supply modeler plugin.
- **community.snmp.CiscoTemperatureSensorMap** - Temperature Sensor modeler
- **community.snmp.CiscoPluggableOpticsSensorMap** - Pluggable Optics Sensor
  modeler plugin.

Monitoring Templates
--------------------

- Devices/CiscoFan
- Devices/CiscoPowerSupply
- Devices/CiscoTemperatureSensor
- Devices/CiscoTemperatureSensor
- Devices/CiscoPluggableOpticsSensorAmperes
- Devices/CiscoPluggableOpticsSensorCelcius
- Devices/CiscoPluggableOpticsSensorDbm
- Devices/CiscoPluggableOpticsSensorVoltsdc

Reports
-------

- Reports/Device Reports/Cisco Reports/Cisco Devices
- Reports/Device Reports/Cisco Reports/Modules
