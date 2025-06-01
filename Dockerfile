# Multi-stage Dockerfile for WFRMLS Background Agent
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN groupadd -r wfrmls && useradd -r -g wfrmls wfrmls

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt ./

# Development stage
FROM base as development
# Copy dev requirements only for development
COPY requirements-dev.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt -r requirements-dev.txt

COPY . .
RUN pip install -e .

# Production stage
FROM base as production

# Install only production dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy source code
COPY wfrmls/ ./wfrmls/
COPY pyproject.toml README.md LICENSE ./

# Install the package
RUN pip install .

# Copy agent script
COPY agent/ ./agent/

# Change ownership to non-root user
RUN chown -R wfrmls:wfrmls /app

# Switch to non-root user
USER wfrmls

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import wfrmls; print('Health check passed')" || exit 1

# Default command runs the background agent
CMD ["python", "-m", "agent.main"] 