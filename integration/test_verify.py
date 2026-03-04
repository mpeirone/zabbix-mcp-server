"""Regression test for Zabbix MCP Server protocol surface.

Run with:
    pytest integration/ --mcp-target-stdio "uv run python integration/run_server.py"

Or verify directly via CLI:
    mcp-recorder verify \
      --cassette integration/cassettes/protocol_and_errors.json \
      --target-stdio "uv run python integration/run_server.py"
"""

import pytest


@pytest.mark.mcp_cassette("cassettes/protocol_and_errors.json")
def test_no_regression(mcp_verify_result):
    """Verify MCP protocol surface hasn't regressed.

    Checks: initialize handshake, tool schemas, error responses for
    host_get, hostgroup_get, item_get, trigger_get, problem_get,
    template_get, and read-only enforcement via host_create.
    """
    assert mcp_verify_result.failed == 0, mcp_verify_result.results
