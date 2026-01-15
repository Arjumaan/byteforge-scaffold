# Backend Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (Go, GCC, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    git \
    wget \
    libpQ-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Go (for security tools)
COPY --from=golang:1.21 /usr/local/go /usr/local/go
ENV PATH=$PATH:/usr/local/go/bin:/root/go/bin

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Security Tools
RUN go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/projectdiscovery/katana/cmd/katana@latest && \
    go install github.com/jaeles-project/gospider@latest

# Copy application code
COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]