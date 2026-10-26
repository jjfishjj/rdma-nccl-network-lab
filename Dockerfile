ARG CUDA_DL_IMAGE=nvcr.io/nvidia/cuda-dl-base:26.08-cuda13.4-devel-ubuntu24.04
FROM ${CUDA_DL_IMAGE}
ARG NCCL_TESTS_COMMIT=afd59abab774a6a4b492eb344bd0c845a0b7bb4d
RUN apt-get update && apt-get install -y --no-install-recommends git make python3 infiniband-diags perftest && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/NVIDIA/nccl-tests.git /opt/nccl-tests && cd /opt/nccl-tests && git checkout ${NCCL_TESTS_COMMIT} && make -j"$(nproc)"
WORKDIR /workspace
COPY src/ src/
COPY scripts/ scripts/
ENV NCCL_TESTS_HOME=/opt/nccl-tests
CMD ["bash", "scripts/run_nccl_benchmark.sh", "network-report"]
