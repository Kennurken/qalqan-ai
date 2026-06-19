"""Community crowd-block threshold tests (pure decision function)."""
import pytest

from api.utils.supabase import community_auto_block


@pytest.mark.parametrize("reports,confirms,disputes,ips,expected", [
    (0, 5, 0, 5, True),    # 5 confirms / 5 IPs
    (3, 2, 0, 4, True),    # mixed reports + confirms
    (10, 0, 0, 3, True),   # reports-only still blocks
    (0, 5, 0, 2, False),   # Sybil: only 2 distinct IPs
    (0, 5, 5, 10, False),  # contested (confirms == disputes)
    (0, 5, 3, 8, True),    # confirms beat disputes
    (0, 4, 0, 4, False),   # below signal threshold
])
def test_auto_block_decision(reports, confirms, disputes, ips, expected):
    assert community_auto_block(reports, confirms, disputes, ips) is expected
