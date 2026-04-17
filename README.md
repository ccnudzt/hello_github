# hello_github
first repository for testing

- good job
- hello

# the second operation

I edit the readme file, and I will commit changes.

---

## GitHub 当月热榜 Top 3

本仓库提供一个脚本，自动抓取 [GitHub Trending](https://github.com/trending?since=monthly)（This month · All languages）前 3 名仓库，并将结果写入 [`docs/trending-monthly-top3.md`](docs/trending-monthly-top3.md)。

### 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行脚本（结果写入 docs/trending-monthly-top3.md）
python scripts/fetch_trending.py
```

### 自动更新

仓库已配置 GitHub Actions（`.github/workflows/update-trending.yml`），每周一 00:00 UTC 自动运行脚本并提交更新结果。也可在 Actions 页面手动触发（`workflow_dispatch`）。
