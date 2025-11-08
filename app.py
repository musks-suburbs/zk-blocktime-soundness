# app.py
import os
import sys
import json
import time
import argparse
from datetime import datetime
from web3 import Web3
from statistics import mean

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

def get_average_block_time(w3: Web3, start_block: int, sample_size: int = 5) -> dict:
    """
    Calculates the average block time and gas utilization across a range of blocks.
    """
    if sample_size <= 0:
        raise ValueError("Sample size must be positive.")

    times = []
    gas_ratios = []

    for i in range(start_block, start_block + sample_size):
        try:
            block = w3.eth.get_block(i)
            prev_block = w3.eth.get_block(i - 1)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch block {i}: {e}")

        time_diff = block.timestamp - prev_block.timestamp
        gas_ratio = block.gasUsed / block.gasLimit if block.gasLimit else 0
        times.append(time_diff)
        gas_ratios.append(gas_ratio)

    avg_time = mean(times)
    avg_gas = mean(gas_ratios) * 100
    return {
        "start_block": start_block,
        "end_block": start_block + sample_size - 1,
        "avg_block_time": round(avg_time, 2),
        "avg_gas_utilization": round(avg_gas, 2),
        "sample_size": sample_size
    }

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-blocktime-soundness — analyze average block time and gas utilization across recent blocks."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM RPC URL (default from RPC_URL)")
    p.add_argument("--start-block", type=int, required=True, help="Starting block number")
    p.add_argument("--samples", type=int, default=5, help="Number of blocks to average (default: 5)")
    p.add_argument("--json", action="store_true", help="Output results as JSON")
    p.add_argument("--timeout", type=int, default=30, help="RPC timeout (default: 30 seconds)")
    return p.parse_args()

def main() -> None:
    start = time.time()
    args = parse_args()

    if not args.rpc.startswith("http"):
        print("❌ Invalid RPC URL. It must start with 'http' or 'https'.")
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": args.timeout}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check RPC_URL or --rpc argument.")
        sys.exit(1)

    print(f"🕒 Timestamp: {datetime.utcnow().isoformat()}Z")
    print("🔧 zk-blocktime-soundness")
    print(f"🔗 RPC: {args.rpc}")
    print(f"🧱 Start Block: {args.start_block}")
    print(f"📊 Sample Size: {args.samples}")

    try:
        data = get_average_block_time(w3, args.start_block, args.samples)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(2)

    print(f"🧭 Range: {data['start_block']} → {data['end_block']}")
    print(f"⏱️ Average Block Time: {data['avg_block_time']} seconds")
    print(f"⛽ Avg Gas Utilization: {data['avg_gas_utilization']}%")

    if data["avg_block_time"] > 20:
        print("🐢 Slow network — high latency between blocks.")
    elif data["avg_block_time"] < 8:
        print("⚡ Fast block production — optimal performance.")
    else:
        print("⚖️ Normal block time detected.")
        # ✅ New: Add block time stability summary
    try:
        # Fetch timestamps for analysis of variation
        diffs = []
        for i in range(args.start_block, args.start_block + args.samples):
            b = w3.eth.get_block(i)
            p = w3.eth.get_block(i - 1)
            diffs.append(b.timestamp - p.timestamp)
        variation = max(diffs) - min(diffs)
        if variation < 2:
            print("🟢 Network Stability: Stable block production ⏱️")
        elif variation < 5:
            print("🟡 Network Stability: Slightly variable timing ⚖️")
        else:
            print("🔴 Network Stability: Volatile timing ⚠️")
    except Exception:
        print("⚠️ Could not compute stability analysis.")

    elapsed = round(time.time() - start, 2)
    print(f"✅ Completed in {elapsed:.2f}s")

    if args.json:
        data.update(
            {
                "rpc": args.rpc,
                "timestamp_utc": datetime.utcnow().isoformat() + "Z",
                "elapsed_seconds": elapsed
            }
        )
        print(json.dumps(data, ensure_ascii=False, indent=2))

    sys.exit(0)

if __name__ == "__main__":
    main()
