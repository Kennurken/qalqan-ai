"""SSRF host-blocking tests (literal IPs only — hermetic, no DNS)."""
import pytest

from api.services.domain_intel import _is_internal_host

BLOCKED = [
    "127.0.0.1",            # loopback
    "10.0.0.5",             # RFC1918
    "192.168.1.1",          # RFC1918
    "172.16.0.1",           # RFC1918
    "169.254.169.254",      # cloud metadata
    "100.64.0.1",           # CGNAT
    "2130706433",           # decimal-encoded 127.0.0.1
    "0x7f000001",           # hex-encoded 127.0.0.1
    "localhost",
    "::1",
    "host.local",
    "svc.internal",
    "",                     # empty host
]

ALLOWED = [
    "8.8.8.8",
    "1.1.1.1",
    "9.9.9.9",
    "208.67.222.222",
]


@pytest.mark.parametrize("host", BLOCKED)
def test_internal_hosts_blocked(host):
    assert _is_internal_host(host) is True


@pytest.mark.parametrize("host", ALLOWED)
def test_public_ips_allowed(host):
    assert _is_internal_host(host) is False
