import re
import logging

from zope.interface import implements
from Products.ZenEvents.interfaces import IPostEventPlugin
from Products.ZenEvents import ZenEventClasses


LOG = logging.getLogger('zen.devicePriority')

_PRIORITY_SEVERITIES = {
    5: 5,
    4: 4,
    3: 3,
    2: 3,
    1: 2,
    0: 1,
}
_PRIORITY_ADJUSTMENTS = {
    5: 2,
    4: 1,
    3: 0,
    2: -1,
    1: -2,
    0: -3,
}


def findSeverity(behavior, currentSev, devicePriority):
    if behavior == 'Adjust':
        newSev = currentSev + _PRIORITY_ADJUSTMENTS.get(devicePriority, 0)
        if newSev < 1:
            newSev = 1
        elif newSev > 5:
            newSev = 5
        return newSev
    elif behavior == 'Base':
        newSev = _PRIORITY_SEVERITIES.get(devicePriority, currentSev)
        return newSev

def matchEvent(event, condition):
    match = False
    filters = condition.split(',')
    for f in filters:
        if not '=' in f:
            # misconfigured filter
            return False

        eventField, regex = f.split('=')
        data = getattr(event, eventField, '')
        if not data:
            return False
        
        m = re.search(regex, data)
        if m:
            match = True
        else:
            return False

    return match


class DevicePriorityPlugin(object):
    """
    Update event severity based on device priority
    """
    implements(IPostEventPlugin)

    @staticmethod
    def apply(eventProxy, dmd):
        if str(getattr(eventProxy, 'ignoreDevicePriority', '')) == 'True':
            return

        if eventProxy.severity == ZenEventClasses.Clear:
            return

        deviceId = getattr(eventProxy, 'device', '')
        device = dmd.Devices.findDeviceByIdExact(deviceId)
        if not deviceId or not device:
            return

        devicePriority = device.getPriority()
        if devicePriority == 3:
            return

        maxSeverity = device.getZ('zDevicePriorityChangeSkip')
        if not maxSeverity:
            return

        maxSevNum = getattr(ZenEventClasses, maxSeverity, False)
        if not maxSevNum or maxSevNum == eventProxy.severity:
            return

        behavior = device.getZ('zDevicePriorityBehavior')
        eventTypes = device.getZ('zDevicePriorityEventTypes')
        inclusions = device.getZ('zDevicePriorityInclusionEvents', [])
        exclusions = device.getZ('zDevicePriorityExclusionEvents', [])
        currentSev = eventProxy.severity

        if not behavior or device.getZ('zDevicePriorityBehavior') == 'Ignore':
            return

        if not eventTypes:
            return

        if exclusions:
            for exclusion in exclusions:
                if matchEvent(eventProxy, exclusion):
                    return

        if eventTypes == 'Ping Down':
            if (getattr(eventProxy, 'eventClass', '') == '/Status/Ping' and
                    (
                        getattr(eventProxy, 'agent', '') == 'zenping' or
                        getattr(eventProxy, 'eventGroup', '') == 'Ping'
                    )):

                eventProxy.severity = findSeverity(behavior, currentSev, devicePriority)
                eventProxy.oldSeverity = currentSev

        elif eventTypes == 'Windows Services':
            if (getattr(eventProxy, 'eventClass', '') == '/Status/WinService' and
                    getattr(eventProxy, 'agent', '') == 'zenpython' and
                    getattr(eventProxy, 'eventClassKey', '') == 'WindowsService'):

                eventProxy.severity = findSeverity(behavior, currentSev, devicePriority)
                eventProxy.oldSeverity = currentSev

        elif eventTypes == 'All':
            eventProxy.severity = findSeverity(behavior, currentSev, devicePriority)
            eventProxy.oldSeverity = currentSev

        elif eventTypes == 'Custom':
            for inclusion in inclusions:
                if matchEvent(eventProxy, inclusion):
                    eventProxy.severity = findSeverity(behavior, currentSev, devicePriority)
                    eventProxy.oldSeverity = currentSev
