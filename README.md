Prometheus
==========

Prometheus monitoring server, includes prometheus, alertmanager and blackbox-exporter.
This requires docker to be running (not handled by this role).

This role is still in development.


Parameters
----------

- `prometheus_targets`: Optional list of dictionaries of targets:
  - `group`: A list of Ansible groups (optional)
  - `hosts`: A list of hosts (optional)
  - `port`: The port to be monitored
  - `jobname`: The prometheus job-name
  - `scrape_interval`: Prometheus scrape interval (optional)
  - `metrics_path`: Path to metrics (optional)
- `prometheus_sd_targets`: Optional list of dictionaries of additional targets:
  - `groupname`: The name of the configuration target file, used to name a configuration file so must be unique
  - `group`: A list of Ansible groups (optional)
  - `hosts`: A list of hosts (optional)
  - `port`: The port to be monitored
  - `jobname`: The prometheus job-name
  This is intended to be an example.
  In practice these configuration files could be dynamically generated outside this role, prometheus will automatically reload them.


Example playbook
----------------

    - hosts: localhost
      roles:
      - role: openmicroscopy.docker
      - role: prometheus


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
