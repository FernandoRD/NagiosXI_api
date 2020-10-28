available_objects = {"objects/hoststatus": "hoststatus",
                "objects/servicestatus": "servicestatus",
                "objects/logentries": "logentry",
                "objects/statehistory": "stateentry",
                "objects/comment": "comment",
                "objects/downtime": "scheduleddowntime",
                "objects/contact": "contact",
                "objects/host": "host",
                "objects/service": "service",
                "objects/hostgroup": "hostgroup",
                "objects/servicegroup": "servicegroup",
                "objects/contactgroup": "contactgroup",
                "objects/timeperiod": "timeperiod",
                "objects/unconfigured": "unconfigured",
                "objects/hostgroupmembers": "hostgroup",
                "objects/servicegroupmembers": "servicegroup",
                "objects/contactgroupmembers": "contactgroup"}

available_objects_config = {"config/host":"config/host",
                "config/service":"config/service",
                "config/hostgroup":"config/hostgroup",
                "config/servicegroup":"config/servicegroup",
                "config/command":"config/command",
                "config/contact":"config/contact",
                "config/contactgroup":"config/contactgroup",
                "config/timeperiod":"config/timeperiod"}
#                "config/import":"config/import"}

options_available_host = {"get":["host_name"], 
                "post":["host_name", "address", "max_check_attempts", "check_period", "contacts", "contact_groups", "notification_interval", "notification_period"], 
                "put":["host_name", "address", "max_check_attempts", "check_period", "contacts", "contact_groups", "notification_interval", "notification_period"], 
                "delete":["host_name"]}

options_available_service = {"get":["config_name", "service_description"], 
                "post":["host_name", "service_description", "check_command", "max_check_attempts", "check_interval", "retry_interval", "check_period", "notification_interval", "notification_period", "contacts", "contact_groups", "config_name"], 
                "put":["config_name", "host_name", "service_description", "check_command", "max_check_attempts", "check_interval", "retry_interval", "check_period", "notification_interval", "notification_period", "contacts", "contact_groups"],
                "delete":["host_name", "service_description"]}

options_available_hostgroup = {"get":["hostgroup_name"],
                "post":["hostgroup_name", "alias"],
                "put":["hostgroup_name", "alias"],
                "delete":["hostgroup_name"]}

options_available_servicegroup = {"get":["servicegroup_name"],
                "post":["servicegroup_name", "alias"],
                "put":["servicegroup_name", "alias"],
                "delete":["servicegroup_name"]}

options_available_command = {"get":["command_name"],
                "post":["command_name", "command_line"],
                "put":["command_name", "command_line"],
                "delete":["command_name"]}

options_available_contact = {"get":["contact_name"],
                "post":["contact_name", "host_notifications_enabled", "service_notifications_enabled", "host_notification_period", "service_notification_period", "host_notification_options",	"service_notification_options", "host_notification_commands", "service_notification_commands"],
                "put":["contact_name", "host_notifications_enabled", "service_notifications_enabled", "host_notification_period", "service_notification_period", "host_notification_options",	"service_notification_options", "host_notification_commands", "service_notification_commands"],
                "delete":["contact_name"]}

options_available_contactgroup = {"get":["contactgroup_name"],
                "post":["contactgroup_name", "alias", "members", "contactgroup_members"],
                "put":["contactgroup_name", "alias", "members", "contactgroup_members"],
                "delete":["contactgroup_name"]}

options_available_timeperiod = {"get":["timeperiod_name"],
                "post":["timeperiod_name", "alias", "\[weekday\]", "\[exception\]", "exclude"],
                "put":["timeperiod_name", "alias", "\[weekday\]", "\[exception\]", "exclude"],
                "delete":["timeperiod_name"]}
