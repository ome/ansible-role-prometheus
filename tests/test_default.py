import testinfra.utils.ansible_runner
import pytest
import json

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_docker_running(Sudo, Command):
    with Sudo():
        out = Command.check_output("docker ps --format '{{.Names}}'")
    names = out.split()
    assert 'alertmanager' in names
    assert 'blackbox-exporter' in names
    assert 'prometheus' in names


def test_docker_volumes(Sudo, Command):
    with Sudo():
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


def test_alternative_metrics(Command):
    out = Command.check_output(
        'curl http://localhost:9090/api/v1/query?query=up')
    assert 'fake-metrics' in out
    out = Command.check_output(
        'curl http://localhost:9090/api/v1/query?query=fake_metric_value')
    r = json.loads(out)
    assert r['data']['result'][0]['value'][1] == '5'
