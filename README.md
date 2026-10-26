# RDMA + NCCL Network Lab

以真實 `nccl-tests`、InfiniBand 工具與 GPU topology 驗證 TCP／RoCE／InfiniBand／GPUDirect RDMA 路徑，並把 bus bandwidth 轉成效率與告警狀態。

## 快速驗證

```bash
python -m unittest discover -s tests -v
python src/nccl_analyzer.py tests/fixtures/all_reduce.txt --theoretical-gbps 200
```

## NVIDIA／IB 實機

```bash
export NCCL_TESTS_HOME=/opt/nccl-tests
export GPUS_PER_NODE=8
export THEORETICAL_GBPS=200
bash scripts/run_nccl_benchmark.sh network-report
```

腳本保存 topology、NCCL/UCX/CUDA 環境、IB 狀態、選用的 `ib_write_bw` 與 AllReduce 報告。自架 Runner 需具 `gpu`、`infiniband` labels。

## 驗收重點

先分離測量 RDMA link，再測 NCCL collective；避免把 PCIe、NUMA、GPUDirect、switch congestion 和 collective algorithm 混成單一問題。

