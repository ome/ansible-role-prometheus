import testinfra.utils.ansible_runner
import pytest
import json

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_docker_running(Sudo, Command):
    with Sudo():
        # BUG: Doesn't work (bug in testinfra?)
        # docker ps --format '{{.Names}}'
        out = Command.check_output(
            "docker ps | tail -n+2 | rev | cut -d' ' -f1 | rev")
    names = sorted(out.split())
    assert names == [
        'alertmanager',
        'blackbox-exporter',
        'fake-metrics',
        'prometheus',
    ]


def test_docker_volumes(Sudo, Command):
    with Sudo():
        # BUG: Doesn't work (bug in testinfra?)
        # docker volume ls --format '{{.Name}}'"
        out = Command.check_output("docker volume ls -q")
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


@pytest.mark.parametrize("jobname", [
    'prometheus',
    'blackbox_http_2xx_internal',
    'fake-metrics',
])
def test_prometheus_targets_up(Command, jobname):
    out = Command.check_output('curl http://localhost:9090/api/v1/targets')
    targets = json.loads(out)['data']['activeTargets']
    found = False
    for t in targets:
        if t['labels']['job'] == jobname:
            found = True
            assert t['health'] == 'up'
    assert found


def test_alternative_metrics(Command):
    out = Command.check_output(
        'curl http://localhost:9090/api/v1/query?query=up')
    assert 'fake-metrics' in out
    out = Command.check_output(
        'curl http://localhost:9090/api/v1/query?query=fake_metric_value')
    r = json.loads(out)
    assert r['data']['result'][0]['value'][1] == '5'
