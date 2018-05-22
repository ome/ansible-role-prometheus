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
 External ports, set to 0 to disable
- `prometheus_port`: External Prometheus port, set to `0` to disable, default `9090`
- `prometheus_alertmanger_port`: External Alertmanager port, set to `0` to disable, default `9093`
- `prometheus_blackboxexporter_port`: External Blackbox-exporter port, set to `0` to disable, default `9115`
- `prometheus_docker_network`: Docker network for prometheus Docker applications, default `prometheus`


Example playbook
----------------

    - hosts: localhost
      roles:
      - role: openmicroscopy.docker
      - role: prometheus


Testing Slack alerts (manual)
-----------------------------

Change `prometheus_alertmanager_slack_webhook` in `playbook.yml` to a real Slack webhook. Run:

    molecule test --destroy never
    molecule login
    docker stop fake-metrics

Wait a few minutes, a Slack alert should be generated.

If this fails try creating a [manual alert](https://github.com/prometheus/alertmanager/issues/437#issuecomment-263413632):

    curl -H "Content-Type: application/json" -d '[{"labels":{"alertname":"TestAlert1"}}]' localhost:9093/api/v1/alerts


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
