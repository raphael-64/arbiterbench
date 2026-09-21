# Judge environment. Everything the harness needs is baked in: Harbor's agent adapters
# shell out to node/npm/curl/procps at setup, and doing that over apt on every trial is
# both slow and a failure mode when the mirror is unreachable.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
    curl ca-certificates git procps jq \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages pytest

WORKDIR /root
RUN mkdir -p /root/workspace
COPY . /root/workspace/
RUN rm -f /root/workspace/Dockerfile
