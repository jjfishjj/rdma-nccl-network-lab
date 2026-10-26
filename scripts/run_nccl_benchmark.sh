#!/usr/bin/env bash
set -euo pipefail
: "${NCCL_TESTS_HOME:?Set NCCL_TESTS_HOME to the compiled nccl-tests directory}"
output_dir="${1:-network-report}"
mkdir -p "$output_dir"
nvidia-smi topo -m > "$output_dir/topology.txt"
env | grep -E '^(NCCL|UCX|CUDA)_' | sort > "$output_dir/environment.txt" || true
if command -v ibstat >/dev/null 2>&1; then ibstat > "$output_dir/ibstat.txt"; fi
if command -v ib_write_bw >/dev/null 2>&1; then timeout 30 ib_write_bw --report_gbits > "$output_dir/ib-write-bw.txt" || true; fi
"$NCCL_TESTS_HOME/build/all_reduce_perf" -b 1M -e 1G -f 2 -g "${GPUS_PER_NODE:-8}" | tee "$output_dir/all-reduce.txt"
python3 src/nccl_analyzer.py "$output_dir/all-reduce.txt" --theoretical-gbps "${THEORETICAL_GBPS:-200}" > "$output_dir/summary.json"
