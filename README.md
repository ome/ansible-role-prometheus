Prometheus
==========

[![Build Status](https://travis-ci.org/ome/ansible-role-prometheus.svg)](https://travis-ci.org/ome/ansible-role-prometheus)
[![Ansible Role](https://img.shields.io/ansible/role/41324.svg)](https://galaxy.ansible.com/ome/prometheus/)

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
 External ports, set to 0 to disable
- `prometheus_port`: External Prometheus port, set to `0` to disable, default `9090`
- `prometheus_alertmanager_port`: External Alertmanager port, set to `0` to disable, default `9093`
- `prometheus_blackboxexporter_port`: External Blackbox-exporter port, set to `0` to disable, default `9115`
- `prometheus_additional_command_args`: Additional command line arguments for prometheus
- `prometheus_alertmanager_additional_command_args`: Additional command line arguments for alertmanager
- `prometheus_additional_rules_template`: Template with additional alert rules.
  See https://awesome-prometheus-alerts.grep.to/rules for some ideas but note the labels may be different.


- `prometheus_docker_network`: Docker network for prometheus Docker applications, default `prometheus`


Example playbook
----------------

    - hosts: localhost
      roles:
      - role: ome.docker
      - role: ome.prometheus


Testing Slack alerts (manual)
-----------------------------

Change `prometheus_alertmanager_slack_webhook` in `playbook.yml` to a real Slack webhook. Run:

    molecule test --destroy never
    molecule login
    docker stop fake-metrics

Wait a few minutes, a Slack alert should be generated.

If this fails try creating a [manual alert](https://github.com/prometheus/alertmanager/issues/437#issuecomment-263413632):

    curl -H "Content-Type: application/json" -d '[{"labels":{"alertname":"TestAlert1"}}]' localhost:9093/api/v1/alerts

The molecule test also includes a disk space alert configuration.
To test this fill up at least 90% of the `/run` partition:

    molecule login
    dd if=/dev/zero of=/run/fill.space bs=1M count=...

Wait a few minutes and you should see a disk space warning.


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
