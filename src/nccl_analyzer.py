"""Parse nccl-tests output and evaluate achieved bus bandwidth."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class NCCLResult:
    size_bytes: int
    algbw_gbps: float
    busbw_gbps: float
    efficiency_pct: float


def parse_output(text: str, theoretical_gbps: float) -> list[NCCLResult]:
    if theoretical_gbps <= 0:
        raise ValueError("theoretical bandwidth must be positive")
    results = []
    for line in text.splitlines():
        columns = line.split()
        if len(columns) < 9 or not columns[0].isdigit():
            continue
        try:
            size, algbw, busbw = int(columns[0]), float(columns[6]), float(columns[7])
        except ValueError:
            continue
        results.append(NCCLResult(size, algbw, busbw, round(busbw / theoretical_gbps * 100, 2)))
    if not results:
        raise ValueError("no nccl-tests rows found")
    return results


def summarize(results: list[NCCLResult]) -> dict:
    peak = max(results, key=lambda row: row.busbw_gbps)
    status = "healthy" if peak.efficiency_pct >= 70 else "investigate" if peak.efficiency_pct >= 45 else "critical"
    return {"samples": len(results), "peak": asdict(peak), "status": status}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--theoretical-gbps", type=float, required=True)
    args = parser.parse_args()
    print(json.dumps(summarize(parse_output(args.input.read_text(), args.theoretical_gbps)), indent=2))


if __name__ == "__main__":
    main()
