import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_service(Service):
    assert Service('prometheus').is_running
    assert Service('prometheus').is_enabled


def test_metrics(Command):
    out = Command.check_output('curl http://localhost:9090/metrics')
    assert 'process_cpu_seconds_total' in out
