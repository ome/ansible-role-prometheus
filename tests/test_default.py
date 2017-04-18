import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_docker_running(Sudo, Command):
    out = Command.check_output("docker ps --format '{{.Names}}'")
    names = sorted(out.split())
    assert names == ['alertmanager', 'blackbox-exporter', 'prometheus']


def test_docker_volumes(Sudo, Command):
    out = Command.check_output("docker volume ls --format '{{.Name}}'")
    names = sorted(out.split())
    assert names == ['alertmanager-data', 'prometheus-data']


@pytest.mark.parametrize("address", [
    "http://localhost:9090",
    "http://localhost:9093",
    "http://localhost:9115",
])
def test_prometheus_metrics(Command, address):
    out = Command.check_output('curl %s/metrics' % address)
    assert 'process_cpu_seconds_total' in out


def test_prometheus_targets(Command):
    out = Command.check_output('curl http://localhost:9090/targets')
    assert 'http://localhost:9090/metrics' in out
    assert 'http://blackbox-exporter:9115/probe' in out
