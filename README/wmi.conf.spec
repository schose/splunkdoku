#   Version 7.2.9
#
# This file contains possible attribute/value pairs for configuring Windows
# Management Instrumentation (WMI) access from Splunk.
#
# There is a wmi.conf in $SPLUNK_HOME\etc\system\default\.  To set custom
# configurations, place a wmi.conf in $SPLUNK_HOME\etc\system\local\. For
# examples, see wmi.conf.example.
#
# You must restart Splunk to enable configurations.
#
# To learn more about configuration files (including precedence) please see
# the documentation located at
# http://docs.splunk.com/Documentation/Splunk/latest/Admin/Aboutconfigurationfiles

###################################################################
#----GLOBAL SETTINGS-----
###################################################################

[settings]
* The settings stanza specifies various runtime parameters.
* The entire stanza and every parameter within it is optional.
* If the stanza is missing, Splunk assumes system defaults.

initial_backoff = <integer>
* How long, in seconds, to wait before retrying the connection to
  the WMI provider after the first connection error.
* If connection errors continue, the wait time doubles until it reaches
  the integer specified in max_backoff.
* Defaults to 5.

max_backoff = <integer>
* The maximum time, in seconds, to attempt to reconnect to the
  WMI provider.
* Defaults to 20.

max_retries_at_max_backoff = <integer>
* Once max_backoff is reached, tells Splunk how many times to attempt
  to reconnect to the WMI provider.
* Splunk will try to reconnect every max_backoff seconds.
* If reconnection fails after max_retries, give up forever (until restart).
* Defaults to 2.

checkpoint_sync_interval = <integer>
* The minimum wait time, in seconds, for state data (event log checkpoint)
  to be written to disk.
* Defaults to 2.

###################################################################
#----INPUT-SPECIFIC SETTINGS-----
###################################################################

[WMI:<name>]
* There are two types of WMI stanzas:
  * Event log: for pulling event logs. You must set the
    event_log_file attribute.
  * WQL: for issuing raw Windows Query Language (WQL) requests. You
    must set the wql attribute.
* Do not use both the event_log_file or the wql attributes.  Use
  one or the other.

server = <comma-separated strings>
* A comma-separated list of servers from which to get data.
* If not present, defaults to the local machine.

interval = <integer>
* How often, in seconds, to poll for new data.
* This attribute is required, and the input will not run if the attribute is
  not present.
* There is no default.

disabled = [0|1]
* Specifies whether the input is enabled or not.
* 1 to disable the input, 0 to enable it.
* Defaults to 0 (enabled).

hostname = <host>
* All results generated by this stanza will appear to have arrived from
  the string specified here.
* This attribute is optional.
* If it is not present, the input will detect the host automatically.

current_only = [0|1]
* Changes the characteristics and interaction of WMI-based event
  collections.
* When current_only is set to 1:
  * For event log stanzas, this will only capture events that occur
    while Splunk is running.
  * For WQL stanzas, event notification queries are expected.  The
    queried class must support sending events.  Failure to supply
    the correct event notification query structure will cause
    WMI to return a syntax error.
  * An example event notification query that watches for process creation:
    * SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE
      TargetInstance ISA 'Win32_Process'.
* When current_only is set to 0:
  * For event log stanzas, all the events from the checkpoint are
    gathered. If there is no checkpoint, all events starting from
    the oldest events are retrieved.
  * For WQL stanzas, the query is executed and results are retrieved.
    The query is a non-notification query.
  * For example
    * Select * Win32_Process where caption = "explorer.exe"
* Defaults to 0.

use_old_eventlog_api = <bool>
* Whether or not to read Event Log events with the Event Logging API.
* This is an advanced setting. Contact Splunk Support before you change it.
  If set to true, the input uses the Event Logging API (instead of the Windows Event Log API) to read from the Event Log on Windows Server 2008, Windows Vista, and later installations.
* Defaults to false (Use the API that is specific to the OS.)

use_threads = <integer>
* Specifies the number of threads, in addition to the default writer thread, that can be created to filter events with the blacklist/whitelist regular expression.
  The maximum number of threads is 15.
* This is an advanced setting. Contact Splunk Support before you change it.
* Defaults to 0

thread_wait_time_msec = <integer>
* The interval, in milliseconds, between attempts to re-read Event Log files when a read error occurs.
* This is an advanced setting. Contact Splunk Support before you change it.
* Defaults to 5000

suppress_checkpoint = <bool>
* Whether or not the Event Log strictly follows the 'checkpointInterval' setting when it saves a checkpoint.
  By default, the Event Log input saves a checkpoint from between zero and 'checkpointInterval' seconds, depending on incoming event volume.
* This is an advanced setting. Contact Splunk Support before you change it.
* Defaults to false

suppress_sourcename = <bool>
* Whether or not to exclude the 'sourcename' field from events.
  When set to true, the input excludes the 'sourcename' field from events and thruput performance (the number of events processed per second) improves.
* This is an advanced setting. Contact Splunk Support before you change it.
* Defaults to false

suppress_keywords = <bool>
* Whether or not to exclude the 'keywords' field from events.
  When set to true, the input excludes the 'keywords' field from events and thruput performance (the number of events processed per second) improves.
* This is an advanced setting. Contact Splunk Support before you change it.
* Defaults to false

suppress_type = <bool>
* Whether or not to exclude the 'type' field from events.
  When set to true, the input excludes the 'type' field from events and thruput performance (the number of events processed per second) improves.
* This is an advanced setting. Contact Splunk Support before you change it.
* Defaults to false

suppress_task = <bool>
* Whether or not to exclude the 'task' field from events.
  When set to true, the input excludes the 'task' field from events and thruput performance (the number of events processed per second) improves.
* This is an advanced setting. Contact Splunk Support before you change it.
* Defaults to false

suppress_opcode = <bool>
* Whether or not to exclude the 'opcode' field from events.
  When set to true, the input excludes the 'opcode' field from events and thruput performance (the number of events processed per second) improves.
* This is an advanced setting. Contact Splunk Support before you change it.
* Defaults to false

batch_size = <integer>
* Number of events to fetch on each query.
* Defaults to 10.

checkpointInterval = <integer>
* How often, in seconds, that the Windows Event Log input saves a checkpoint.
* Checkpoints store the eventID of acquired events. This lets the input
  continue monitoring at the correct event after a shutdown or outage.
* The default value is 0.

index = <string>
* Specifies the index that this input should send the data to.
* This attribute is optional.
* When defined, "index=" is automatically prepended to <string>.
* Defaults to "index=main" (or whatever you have set as your default index).

#####
# Event log-specific attributes:
#####

event_log_file = <Application, System, etc>
* Tells Splunk to expect event log data for this stanza, and specifies
  the event log channels you want Splunk to monitor.
* Use this instead of WQL to specify sources.
* Specify one or more event log channels to poll.  Multiple event log
  channels must be separated by commas.
* There is no default.

disable_hostname_normalization = [0|1]
* If set to true, hostname normalization is disabled
* If absent or set to false, the hostname for 'localhost' will be converted
  to %COMPUTERNAME%.
* 'localhost' refers to the following list of strings: localhost, 127.0.0.1,
  ::1, the name of the DNS domain for the local computer, the fully
  qualified DNS name, the NetBIOS name, the DNS host name of the local
  computer

#####
# WQL-specific attributes:
#####

wql = <string>
* Tells Splunk to expect data from a WMI provider for this stanza, and
  specifies the WQL query you want Splunk to make to gather that data.
* Use this if you are not using the event_log_file attribute.
* Ensure that your WQL queries are syntactically and structurally correct
  when using this option.
* For example,
  SELECT * FROM Win32_PerfFormattedData_PerfProc_Process WHERE Name = "splunkd".
* If you wish to use event notification queries, you must also set the
  "current_only" attribute to 1 within the stanza, and your query must be
  appropriately structured for event notification (meaning it must contain
  one or more of the GROUP, WITHIN or HAVING clauses.)
* For example,
  SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE TargetInstance ISA
  'Win32_Process'
* There is no default.

namespace = <string>
* The namespace where the WMI provider resides.
* The namespace spec can either be relative (root\cimv2) or absolute
  (\\server\root\cimv2).
* If the server attribute is present, you cannot specify an absolute
  namespace.
* Defaults to root\cimv2.

