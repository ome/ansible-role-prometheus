Prometheus
==========

Prometheus monitoring server.

This includes prometheus, alertmanager and blackbox-exporter.


Parameters
----------

- `prometheus_targets`: Optional list of dictionaries of additional targets:
  - `groupname`: The name of the configuration target file
  - `hosts`: A list of hosts
  - `port`: The port to be monitored, must be a string
  - `jobname`: The prometheus job-name
  This is intended tpo be an example.
  In practice these configuration files should be dynamically generated outside this role, prometheus will automatically load them.


Example playbook
----------------

    - hosts: localhost
      roles:
      - role: prometheus


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
