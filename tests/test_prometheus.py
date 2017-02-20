import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('prometheus')


@pytest.mark.parametrize("name", [
    "prometheus",
    "prometheus-alertmanager",
])
def test_services_running_and_enabled(Service, name):
    assert Service(name).is_running
    assert Service(name).is_enabled


def test_prometheus_metrics(Command):
    out = Command.check_output('curl http://localhost:9090/metrics')
    assert 'process_cpu_seconds_total' in out
