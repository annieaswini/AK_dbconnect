from os import environ
from subprocess import Popen

# A simple Python implementation from splunk_app_db_connect/bin/java.path
process = Popen(
    [
        environ["SPLUNK_HOME"] + "/etc/apps/splunk_app_db_connect/bin/command.sh",
        "-cp",
        environ["SPLUNK_HOME"] + "/etc/apps/splunk_app_db_connect/jars/dbxquery.jar",
        "com.splunk.dbx.command.DbxAlertOutput",
    ]
)
process.communicate()
