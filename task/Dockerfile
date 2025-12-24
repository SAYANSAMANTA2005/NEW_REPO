FROM python:3.10-slim

WORKDIR /app

# Install basic tools
RUN apt-get update && apt-get install -y \
    bash \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p network_map tests

# Copy project files
COPY . .

# Set permissions
RUN chmod +x run-tests.sh solution.sh generate_data.py

# Generate data initially
RUN python3 generate_data.py

CMD ["/bin/bash"]
