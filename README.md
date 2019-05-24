# usgs-api-client
A Python client for the USGS EarthExplorer Inventory API

## Installation
The usgs-api-client was developed in Python 3.6, targetting specific CentOS/RHEL 6 and 7 systems. The instructions here will cover this specific case. Adapt as necessary for other target environments.

### Pre-requisites
To use Python 3.x on CentOS/RHEL based systems, enable [Software Collections](https://www.softwarecollections.org/en/docs/). On CentOS:
```
$ sudo yum install centos-release-scl
```
On RHEL:
```
$ sudo yum-config-manager --enable rhel-server-rhscl-6-rpms
```
Note that for RHEL above, "6" indicates the OS version (i.e. RHEL 6). Change the version as appropriate for your target system.

Install the required Python distribution. On both CentOS and RHEL:
```
$ sudo yum install rh-python36
```
To enable the installed package for use in the current terminal session:
```
$ scl enable rh-python36 bash
```
You can (probably) use the following shebang in shell scripts directly:
```
#!/opt/rh/rh-python36/root/usr/bin/python3
```

### Release installation
Go to the [releases page](https://github.com/solomchuk/usgs-api-client/releases) and choose a desired release - most likely the latest one. Download the source ZIP to your target system:
```
$ wget https://github.com/solomchuk/usgs-api-client/archive/v0.2.3.zip
```
The actual URL will depend on the release chosen (v0.2.3.zip in this case).
Unpack the archive to the target directory:
```
$ unzip v0.2.3.zip -d /destination/path
```
Replace "/destination/path" with the target directory.
Enable the Python 3 package via SCL:
```
$ scl enable rh-python36 bash
```
Change to the client directory and perform a local install with PIP:
```
$ cd /destination/path/usgs-api-client-0.2.3/
$ pip install --user --editable .
```
Change the path and version number in the destination directory as appropriate. The --user flag will install the client only for the current user. This prevents issues with permissions when running the client. Keep in mind that you will need to run it as the user that installed it.

### Logging configuration
The logging.conf file in the client directory defines the logging parameters for the client. By default, DEBUG logging is enabled both in the console and for log files. A separate log file for ERROR level is also included. Most of the options here can be left as they are, but it is recommended to configure the path to your log files as appropriate for your system. For this, change the filename parameters in the handlers section, e.g.:
```
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: default
    stream: ext://sys.stdout
  debug_file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: default
    filename: /var/log/usgs-api-client/usgs_api_client_debug.log
    maxBytes: 10485760
    backupCount: 9
  error_file:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: default
    filename: /var/log/usgs-api-client/usgs_api_client_error.log
    maxBytes: 10485760
    backupCount: 9
```
You can also control the log rotation with maxBytes and backupCount parameters.

### Upgrading
To upgrade the client from a previous version, simply re-run the installation procedure.