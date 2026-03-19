FROM python:3.12-slim-bookworm

# System packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash coreutils grep sed findutils jq git curl ca-certificates ripgrep \
    && rm -rf /var/lib/apt/lists/*

# Python packages -- runtime only (lean image)
RUN pip install --no-cache-dir \
    anthropic>=0.45.0 \
    openai>=1.0.0 \
    typing_extensions>=4.0.0 \
    pyyaml>=6.0

# Runtime code -- opaque, not the user's concern
COPY runtime/ /opt/runtime/

# Viz server
COPY viz/ /opt/viz/

# Entry point
COPY entrypoint.py /opt/entrypoint.py

# Working directory is mounted by the user
WORKDIR /workspace

# Viz dashboard port
EXPOSE 8111

ENV PYTHONPATH=/opt
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

ENTRYPOINT ["python3", "/opt/entrypoint.py"]
