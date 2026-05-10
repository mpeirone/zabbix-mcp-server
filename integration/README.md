# Integration Tests

Snapshot-based regression tests for the MCP protocol surface. A golden cassette records the `initialize` handshake, all tool schemas via `tools/list`, and error handling for core monitoring tools. CI verifies that every PR still matches. If a tool is renamed, removed, or has its schema changed, the diff shows exactly what broke.

Uses [mcp-recorder](https://github.com/devhelmhq/mcp-recorder) for recording and verification.

## What's tested

| Cassette | What it guards |
|---|---|
| `protocol_and_errors.json` | Protocol version, capabilities, all tool schemas, error responses for host\_get, hostgroup\_get, item\_get, trigger\_get, problem\_get, template\_get, and read-only enforcement via host\_create |

Tests run with `READ_ONLY=true` (the default). Read-only tools return a deterministic `ZABBIX_URL` error; write tools return a read-only mode error. No Zabbix server or credentials required.

## Setup

```bash
pip install -r integration/requirements.txt
uv sync
```

## Verify locally

Run from the repository root:

```bash
mcp-recorder verify \
  --cassette integration/cassettes/protocol_and_errors.json \
  --target-stdio "uv run python integration/run_server.py" \
  --verbose
```

All interactions should pass. No API key, Zabbix server, or Docker required.

## Update cassettes after intentional changes

When you've changed a tool schema or added a new tool, update the cassette:

```bash
mcp-recorder verify \
  --cassette integration/cassettes/protocol_and_errors.json \
  --target-stdio "uv run python integration/run_server.py" \
  --update
```

This replays the recorded requests, accepts the new responses, and writes them back to the cassette. Commit the updated cassette with your PR — the diff makes the schema change visible in review.

## Add new test scenarios

Edit `scenarios.yml` and re-record:

```bash
mcp-recorder record-scenarios integration/scenarios.yml \
  --output-dir integration/cassettes
```

See the [mcp-recorder docs](https://github.com/devhelmhq/mcp-recorder) for supported actions.

## Run with pytest

```bash
pytest integration/ --mcp-target-stdio "uv run python integration/run_server.py"
```
