# Copyright (C) 2005-2016 Splunk Inc. All Rights Reserved.

# DO NOT EDIT THIS FILE
# This file configuration file must not be edited manually because others files
# must be updated to apply the modifications such as server.vmopts and commands.conf.
# This file is edited by dbx_settings.py. Please use the UI or the API to apply
# some modifications on stanzas defined below.


[java]
javaHome = <string>
# optional
# Specifies the path to Java home. The path defined will be used to resolve the
# java command location. Typically, the /bin/java or \bin\java.exe will be
# appended to this path to resolve the command location on *nix and windows
# respectively.
# If not specified the JAVA_HOME environment variable is used.
# If JAVA_HOME is also undefined, java command is directly used. In that case,
# java command must be defined in the PATH environment variable.

[loglevel]
dbxquery = [TRACE | DEBUG | INFO | WARN | ERROR]
# set the log level for dbxquery command

dbxoutput = [TRACE | DEBUG | INFO | WARN | ERROR]
# set the log level for dbxoutput command

dbxlookup = [TRACE | DEBUG | INFO | WARN | ERROR]
# set the log level for dbxlookup command

dbinput = [TRACE | DEBUG | INFO | WARN | ERROR]
# set the log level for db inputs

dboutput = [TRACE | DEBUG | INFO | WARN | ERROR]
# set the log level for db outputs

connector = [TRACE | DEBUG | INFO | WARN | ERROR]
# set the log level for all the interactions with DBs

processor = [TRACE | DEBUG | INFO | WARN | ERROR]
# set the log level for all the interactions involving HEC

[hec]
# when HEC failed to forward data to Splunk Indexer, it will return 503 error,
# then DBX will retry 3 times by default with exponential backoff
maxRetryWhenHecUnavailable = <integer>

# maxHecContentLength setup max event size, default is 10MB
maxHecContentLength = <integer>

# Comma separated HEC URIs: https://<idx-host1>:8088,https://<idx-host2>:8088,...
hecUris = <string>

# Comma separated HEC token per HEC URIs
# In case a single token is provided, then it will be used for each HEC
hecToken = <string>

# Lower case field name for backward compatibility with dbx 1.x
# By default it is false
hecFieldNameLowerCase = <true|false>

[security]
denylist = <string>
# Comma separated IP addresses or domain names to be denied when configuring HEC URIs or others
