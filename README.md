# Device Priority
Device Priority can be setup to automatically adjust event severity for devices.

## Behavior
Device Priority can be used in 3 different ways. The behavior is set using the zProperty zDevicePriorityBehavior.
* Default – Using this behavior type will make device priority work as default, which does not change severity of any events. And is used as more of a tag.
* Base – Using this behavior will change any events setup to a severity based on device priority
  * Highest = Critical
  * Higher = Error
  * Normal = No change to events
  * Low = Warning
  * Lowest = Informational
  * Trivial = Debug
* Adjust – Using this behavior will adjust the severity any events setup based on device priority
  * Highest = +2
  * Higher = +1
  * Normal = No change to events
  * Low = -1
  * Lowest = -2
  * Trivial = -3
Adjust will never drop an event severity below Debug or raise a severity above Critical.

## Adjusting Events Based on Event Types
You can setup Device Priority to only adjust certain events. This is done by using the following zProperties:
* zDevicePriorityChangeSkip – This will skip changing events for the set severity and lower. If set to Critical, no events will ever be changed. Options are:
  * Info
  * Warning
  * Error
  * Critical
* zDevicePriorityEventTypes – A few options have been preprogrammed in for ease of use.
  * Ping Down – This will change any ping down events
  * Windows Services – This will change any windows service events
  * All – This will change all events
  * Custom – This will only change events for conditions defined in zDevicePriorityInclusionEvents
* zDevicePriorityInclusionEvents – This is a multiline zProperty that allows for custom conditions to be entered by a user. These conditions will be evaluated against each event and if it matches, that event will be changed. This zProperty is used only for if zDevicePriorityEventTypes is set to Custom.
* zDevicePriorityExclusionEvents – This is a multiline zProperty that allows for custom conditions to be entered by a user. These conditions will be evaluated against each event and if it matches, the event will NOT be changed. This zProperty is used for all options under zDevicePriorityEventTypes.

## How to use Inclusions and Exclusions
These zProperties are multiline, each line is considered a condition. Each condition is evaluated against each event.
Each condition can have multiple rules. These are separated by a comma. Each rule should be formatted as eventField=Regex.
* eventField – This is the exact naming and capitalization of the event field found within the event. A few examples:
  * eventClass
  * eventClassKey
  * summary
  * component
* Regex – This is a regex for the contents of the event field. A few examples:
  * /Status/Ping.* will match /Status/Ping and /Status/Ping/Lag
  * ^Ethernet\d/\d will match Ethernet3/7

