**繁體中文** | [English](demo-sessions.md)

# Demo Sessions

其他貢獻者可先安裝開發相依套件，再直接執行內建的 demo 測試：

```bash
pip install -e ".[dev]"
```

- `nox -s demo-10-shards`：將 `demo/demo_tests/` 分成 10 個 shard 執行，並產生合併後的 Allure 報告。
- `nox -s demo-3-shards-parallel`：將 `demo/demo30_tests/` 以 3 個平行 shard 執行，產生清楚的 Timeline 範例。
- `nox -s demo-duration-comparison`：對 `demo/demo_duration_tests/` 做兩次執行，比較 round-robin 與 duration-based balancing。
- `nox -s demo-xdist-group-hash`：以 `--shard-mode=hash` 將 `demo/demo_xdist_group_tests/` 分成 3 個平行 shard 執行，示範 `xdist_group` 同 shard 保證。產生報告後執行 `allure open allure-report-xdist-group`，在 Timeline 中可以看到相同 group 的所有測試都出現在同一條執行緒上。
- `nox -s demo-xdist-group-hash-balanced`：以 `--shard-mode=hash-balanced` 執行同一組測試。示範 LPT bin-packing 如何避免多個大型 group 碰撞到同一個 shard，可與純 `hash` 的報告對比 Timeline，觀察負載分配改善的效果。

凡是需要產生報告的 demo session，都需要系統上的 `PATH` 可找到 `allure` CLI。

完整的報告流程與截圖請參考 [Allure Report 整合指南](allure-integration.zh-TW.md)。
