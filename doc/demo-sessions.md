[繁體中文](demo-sessions.zh-TW.md) | **English**

# Demo Sessions

Contributors can run the bundled demo suites locally after installing the development dependencies:

```bash
pip install -e ".[dev]"
```

- `nox -s demo-10-shards`: runs `demo/demo_tests/` across 10 shards and builds a merged Allure report.
- `nox -s demo-3-shards-parallel`: runs `demo/demo30_tests/` across 3 parallel shards and produces a clear Timeline example.
- `nox -s demo-duration-comparison`: runs `demo/demo_duration_tests/` twice to compare round-robin versus duration-based balancing.
- `nox -s demo-xdist-group-hash`: runs `demo/demo_xdist_group_tests/` across 3 parallel shards with `--shard-mode=hash`. Demonstrates the `xdist_group` co-location guarantee — open the generated `allure-report-xdist-group` and check the Timeline to see that all tests in the same group appear on the same shard thread.
- `nox -s demo-xdist-group-hash-balanced`: runs the same suite with `--shard-mode=hash-balanced`. Shows that LPT bin-packing prevents multiple large groups from colliding on the same shard — compare the Timeline with the plain `hash` report to see the load distribution improvement.

The demo sessions that generate reports require the `allure` CLI to be available on `PATH`.

For the full report workflow and screenshots, see [Allure Report Integration](allure-integration.md).
