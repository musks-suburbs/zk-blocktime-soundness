# README.md
# zk-blocktime-soundness

## Overview
**zk-blocktime-soundness** is a CLI analyzer that measures **average block time** and **gas utilization** across a specified range of blocks.  
It’s designed for developers working with zk-rollups like **Aztec** or **Zama**, where predictable block timing ensures **sound proof generation** and consistent network performance.

## Features
- ⏱️ Calculates average block time across a sample range  
- ⛽ Computes average gas utilization percentage  
- 🧮 Supports configurable sample sizes  
- 🌍 Compatible with any EVM-compatible RPC endpoint  
- 💾 JSON output for dashboards and automation  
- 🧩 Helps monitor network consistency for zk-proving environments  

## Installation
1. Requires Python 3.9+  
2. Install dependencies:
   pip install web3
3. Set RPC endpoint:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

## Usage
Check average block time over 5 blocks:
   python app.py --start-block 21000000

Increase sample size for better accuracy:
   python app.py --start-block 21000000 --samples 10

Use a custom RPC:
   python app.py --rpc https://arb1.arbitrum.io/rpc --start-block 21000000 --samples 6

Output results in JSON:
   python app.py --start-block 21000000 --json

Increase timeout for slower RPC nodes:
   python app.py --start-block 21000000 --timeout 60

Compare different chains:
   python app.py --rpc https://eth.llamarpc.com --start-block 19000000
   python app.py --rpc https://polygon-rpc.com --start-block 55000000

## Example Output
🕒 Timestamp: 2025-11-08T15:11:22.812Z  
🔧 zk-blocktime-soundness  
🔗 RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🧱 Start Block: 21000000  
📊 Sample Size: 5  
🧭 Range: 21000000 → 21000004  
⏱️ Average Block Time: 12.3 seconds  
⛽ Avg Gas Utilization: 82.45%  
⚖️ Normal block time detected.  
✅ Completed in 0.68s  

## Notes
- **Block Time Metric:** Indicates the average time between mined blocks.  
- **Gas Utilization:** Helps evaluate network congestion and miner performance.  
- **ZK Applications:** Stable block timing ensures consistent zk-proof batching and layer-2 sequencing.  
- **Cross-Network Analysis:** Compare L1 and L2 speeds to analyze finality soundness.  
- **CI/CD Friendly:** Use `--json` for integration with monitoring pipelines or alerts.  
- **Historical Tracking:** Run daily to record block interval statistics and detect slowdowns.  
- **Exit Codes:**  
  - `0` → Success  
  - `2` → RPC or block retrieval error.  
