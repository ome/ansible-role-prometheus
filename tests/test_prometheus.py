import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('prometheus')


@pytest.mark.parametrize("name", [
    "prometheus",
    "prometheus-alertmanager",
    "prometheus-node-exporter",
])
def test_services_running_and_enabled(Service, name):
    assert Service(name).is_running
    assert Service(name).is_enabled


@pytest.mark.parametrize("address", [
    "http://localhost:9090",
    "http://localhost:9093",
    "http://localhost:9100",
])
def test_prometheus_metrics(Command, address):
    out = Command.check_output('curl %s/metrics' % address)
    assert 'process_cpu_seconds_total' in out
