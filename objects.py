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

options_available_config_host = {"get":["host_name"], 
                "post":["host_name", "address", "max_check_attempts", "check_period", "contacts", "contact_groups", "notification_interval", "notification_period"], 
                "put":["host_name", "address", "max_check_attempts", "check_period", "contacts", "contact_groups", "notification_interval", "notification_period"], 
                "delete":["host_name"]}

options_available_config_service = {"get":["config_name", "service_description"], 
                "post":["host_name", "service_description", "check_command", "max_check_attempts", "check_interval", "retry_interval", "check_period", "notification_interval", "notification_period", "contacts", "contact_groups", "config_name"], 
                "put":["config_name", "host_name", "service_description", "check_command", "max_check_attempts", "check_interval", "retry_interval", "check_period", "notification_interval", "notification_period", "contacts", "contact_groups"],
                "delete":["host_name", "service_description"]}

options_available_config_hostgroup = {"get":["hostgroup_name"],
                "post":["hostgroup_name", "alias"],
                "put":["hostgroup_name", "alias"],
                "delete":["hostgroup_name"]}

options_available_config_servicegroup = {"get":["servicegroup_name"],
                "post":["servicegroup_name", "alias"],
                "put":["servicegroup_name", "alias"],
                "delete":["servicegroup_name"]}

options_available_config_command = {"get":["command_name"],
                "post":["command_name", "command_line"],
                "put":["command_name", "command_line"],
                "delete":["command_name"]}

options_available_config_contact = {"get":["contact_name"],
                "post":["contact_name", "host_notifications_enabled", "service_notifications_enabled", "host_notification_period", "service_notification_period", "host_notification_options",	"service_notification_options", "host_notification_commands", "service_notification_commands"],
                "put":["contact_name", "host_notifications_enabled", "service_notifications_enabled", "host_notification_period", "service_notification_period", "host_notification_options",	"service_notification_options", "host_notification_commands", "service_notification_commands"],
                "delete":["contact_name"]}

options_available_config_contactgroup = {"get":["contactgroup_name"],
                "post":["contactgroup_name", "alias", "members", "contactgroup_members"],
                "put":["contactgroup_name", "alias", "members", "contactgroup_members"],
                "delete":["contactgroup_name"]}

options_available_config_timeperiod = {"get":["timeperiod_name"],
                "post":["timeperiod_name", "alias", "\[weekday\]", "\[exception\]", "exclude"],
                "put":["timeperiod_name", "alias", "\[weekday\]", "\[exception\]", "exclude"],
                "delete":["timeperiod_name"]}


available_objects_system = {"system/status":"system/status",
                "system/statusdetail":"system/statusdetail",
                "system/info":"system/info",
                "system/command":"system/command",
                "system/applyconfig":"system/applyconfig",
                "system/importconfig":"system/importconfig",
                "system/corecommand":"system/corecommand",
                "system/scheduleddowntime":"system/scheduleddowntime",
                "system/user":"system/user",
                "system/authserver":"system/authserver"
                }

options_available_system_status = {"get":[]}
options_available_system_statusdetail = {"get":[]}
options_available_system_info = {"get":[]}
options_available_system_command = {"get":[]}
options_available_system_applyconfig = {"get":[], "post":[]}
options_available_system_importconfig = {"get":[], "post":[]}
options_available_system_corecommand = {}
options_available_system_scheduleddowntime = {"post":["start", "end", "comment", "author", "hosts", "child_hosts", "all_services", "services", "hostgroups", "servicegroups", "flexible", "duration", "triggered_by", "only"],
                "delete":["internal_id"]}
options_available_system_user = {"get":["advanced"],
                "post":["username", "password", "name", "email", "force_pw_change", "email_info", "monitoring_contact", "enable_notifications", "language", "date_format", "number_format", "auth_level"], 
                "delete":["user_id"]
                }
options_available_system_authserver = {"get":[], 
                "post":["conn_method", "enabled", "base_dn", "security_level"],
                "delete":["server_id"]
                }