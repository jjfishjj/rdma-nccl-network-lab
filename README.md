# RDMA + NCCL Network Lab

比較 TCP Ethernet、RoCE、InfiniBand 與 GPUDirect RDMA 路徑的 AllReduce 效率。

## 執行

直接開啟 `index.html`，調整節點、GPU、梯度量與 fabric 即可估算 collective 時間。

## 實機延伸

依序使用 RDMA micro-benchmark、拓撲檢查與 `nccl-tests` 驗證模擬假設。

