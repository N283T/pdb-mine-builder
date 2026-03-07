FROM python:3.12-slim

WORKDIR /app

# Install rsync for data synchronization
RUN apt-get update && apt-get install -y --no-install-recommends \
    rsync \
    && rm -rf /var/lib/apt/lists/*

# Install Python package
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/
RUN pip install --no-cache-dir .

# Default config location
VOLUME ["/app/config", "/data"]

ENTRYPOINT ["pmb"]
CMD ["--help"]
