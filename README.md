# NOT USED - DEPRECATED

# prometheus-mysqld-exporter

## Introduction

Based on the ideas and code from https://github.com/meowtochondria/node_exporter-rpm, this project packages various versions of mysqld_exporter.

## Features

Added features:
* Add /etc/sysconfig/mysqld_exporter, where sysadmins can override default values defined in `/usr/lib/systemd/system/prometheus-mysqld-exporter.service.d/environment.conf` and customize DATA_SOURCE_NAME, required to connect to mysql database.

Features inherited from *node_exporter-rpm* projects:
* Includes logrotate and rsyslog config to manage and write logs to `/var/log/prometheus/node_exporter.log`.
* Has SystemD setup to restart node_exporter on failure.
* Tries to find a balance between practical conventions and file system hierarchy specification at http://www.pathname.com/fhs/pub/fhs-2.3.html.
* Creates its own user and group called `prometheus` with no interactive shell configured.
* Various paths that will appear after installation:
    * Bin path for `mysqld_exporter`: `/usr/bin`
    * Path to store LICENSE and NOTICE: `/usr/share/prometheus/mysqld_exporter`
    * Log file: `/var/log/prometheus/mysqld_exporter.log`
    * Logrotate config: `/etc/logrotate.d/prometheus-mysqld-exporter.conf`
    * RSyslog config: `/etc/rsyslog.d/prometheus-mysqld-exporter.conf`
    * SystemD Unit definiton: `/usr/lib/systemd/system/prometheus-mysqld-exporter.service`
    * Environment variables: `/usr/lib/systemd/system/prometheus-mysqld-exporter.service.d/environment.conf`

## Pre-requisites

* RedHat or its derivatives like CentOS.
* Network connection to public internet to reach repositories and github.

## Limitations

* Script has been only tested on CentOS 7 to package latest available node_exporter. Please feel free to make pull requests if you want to add more nuanced support for older versions.
* No guarantees are being made for fitness of purpose or merchantabilities. Any results of usage of work herein is not author's or contributor's responsibility.

## Usage

* Clone the repo.
* Build with default settings (build tree in current directory, latest version of Prometheus)
    ```
    ./build.sh
    ```
* See various options available by looking at help:
    ```
    ./build.sh -h
    ```
* See versions available upstream (because there are huge number of releases upstream and there is no caching going, script takes a few seconds to execute)
    ```
    ./build.sh -l
    ```
* Because the new packages like prometheus should not make changes to systemd configuration, notice appears after installation that tells how to modify various services.
    ```
    NOTES ############################################################################
    Please restart RSyslog so that logs are written to /var/log/prometheus:
        systemctl restart rsyslog.service
    To have prometheus start automatically on boot:
        systemctl enable prometheus-mysql-exporter.service
    Start prometheus:
        systemctl daemon-reload
        systemctl start prometheus-mysqld-exporter.service
    ##################################################################################
    ```

## License

Apache License 2.0