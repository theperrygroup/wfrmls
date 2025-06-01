# WFRMLS Background Agent - Docker Deployment

This directory contains Docker configuration to run the WFRMLS Python client as a background agent in a containerized environment. The agent continuously monitors WFRMLS data and performs automated tasks.

## 🚀 Quick Start

### Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 1.29+)
- WFRMLS Bearer Token

### 1. Clone and Setup

```bash
# Clone the repository (if not already done)
git clone https://github.com/theperrygroup/wfrmls.git
cd wfrmls

# Make the management script executable
chmod +x run-agent.sh
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
# WFRMLS API Configuration
WFRMLS_BEARER_TOKEN=your_bearer_token_here

# Optional: Agent Configuration
WFRMLS_SYNC_INTERVAL=900        # 15 minutes (default)
WFRMLS_MONITOR_INTERVAL=300     # 5 minutes (default)
WFRMLS_LOG_LEVEL=INFO           # DEBUG, INFO, WARNING, ERROR
WFRMLS_ENABLE_ALERTS=true       # Enable/disable alerts
WFRMLS_WEBHOOK_URL=             # Optional webhook for notifications
```

### 3. Start the Agent

```bash
# Start the background agent
./run-agent.sh start

# Or using Docker Compose directly
docker-compose up -d wfrmls-agent
```

## 📋 Management Commands

The `run-agent.sh` script provides easy management of the background agent:

```bash
# Start the agent
./run-agent.sh start

# Stop the agent
./run-agent.sh stop

# Restart the agent
./run-agent.sh restart

# Check agent status and health
./run-agent.sh status

# View logs (last 50 lines)
./run-agent.sh logs

# Follow logs in real-time
./run-agent.sh logs -f

# Build the Docker image
./run-agent.sh build

# Open shell inside running container
./run-agent.sh shell

# Clean up (stop and remove containers/images)
./run-agent.sh clean

# Start with monitoring dashboard
./run-agent.sh dashboard
```

## 🏗️ Architecture

### Background Agent Components

The background agent consists of several modules:

- **Main Agent** (`agent/main.py`) - Orchestrates all background tasks
- **Data Processor** (`agent/data_processor.py`) - Processes WFRMLS data updates
- **Monitor** (`agent/monitor.py`) - Health checks and alerts
- **Scheduler** (`agent/scheduler.py`) - Periodic maintenance tasks
- **Config** (`agent/config.py`) - Configuration management

### Data Flow

```
WFRMLS API → Background Agent → Data Processor → Storage/Webhooks
     ↓              ↓               ↓
Health Monitor → Alerts → Notifications
     ↓
Scheduled Tasks → Cleanup/Reports
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WFRMLS_BEARER_TOKEN` | Required | WFRMLS API bearer token |
| `WFRMLS_SYNC_INTERVAL` | 900 | Data sync interval (seconds) |
| `WFRMLS_MONITOR_INTERVAL` | 300 | Monitoring check interval (seconds) |
| `WFRMLS_HEALTH_CHECK_INTERVAL` | 600 | Health check interval (seconds) |
| `WFRMLS_LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `WFRMLS_LOG_TO_FILE` | true | Whether to log to files |
| `WFRMLS_MAX_RETRIES` | 3 | Maximum retries for failed operations |
| `WFRMLS_BATCH_SIZE` | 200 | Records per batch for processing |
| `WFRMLS_ENABLE_ALERTS` | true | Enable alert notifications |
| `WFRMLS_WEBHOOK_URL` | None | Webhook URL for notifications |

### Volume Mounts

- `./logs:/app/logs` - Persistent logging directory
- `./agent-config:/app/config:ro` - Optional custom configuration

## 📊 Monitoring and Logging

### Log Files

Logs are stored in the `./logs` directory:

- `agent.log` - Main agent logs
- `daily_report_YYYYMMDD.json` - Daily activity reports
- Health check and error logs

### Health Checks

The agent includes built-in health checks:

- **API Connectivity** - Tests WFRMLS API connection
- **Data Quality** - Validates incoming data
- **Performance** - Monitors response times and error rates
- **Resource Usage** - Tracks memory and CPU usage

### Status Monitoring

```bash
# Check overall status
./run-agent.sh status

# View real-time logs
./run-agent.sh logs -f

# Check Docker container health
docker inspect wfrmls-background-agent | jq '.[0].State.Health'
```

## 🔔 Alerts and Notifications

The agent can send alerts for various conditions:

- API connectivity issues
- High error rates (>10%)
- Slow response times (>15s)
- Data quality problems
- Resource constraints

### Webhook Notifications

Configure webhook notifications by setting `WFRMLS_WEBHOOK_URL`:

```bash
WFRMLS_WEBHOOK_URL=https://your-webhook-endpoint.com/alerts
```

Webhook payload format:
```json
{
  "event_type": "alert",
  "alert": {
    "timestamp": "2024-01-15T10:30:00Z",
    "type": "api_error",
    "message": "API health check failed",
    "severity": "error",
    "agent_id": "wfrmls-agent"
  }
}
```

## 🔧 Development and Customization

### Building Custom Images

```bash
# Build production image
docker build --target production -t wfrmls-agent:latest .

# Build development image with dev dependencies
docker build --target development -t wfrmls-agent:dev .
```

### Custom Data Processing

Extend the `DataProcessor` class in `agent/data_processor.py`:

```python
async def _process_single_property(self, property_data: Dict[str, Any]) -> None:
    # Add your custom processing logic here
    listing_id = property_data.get("ListingId")
    
    # Example: Save to database
    await self.save_to_database(property_data)
    
    # Example: Send to external API
    await self.send_to_external_api(property_data)
    
    # Example: Generate alerts
    if property_data.get("ListPrice", 0) > 5000000:
        await self.create_alert("high_value_property", 
                              f"High value property listed: {listing_id}")
```

### Adding Custom Scheduled Tasks

Add tasks in `TaskScheduler.__init__()`:

```python
# Custom cleanup task every 2 hours
self.add_task(
    "custom_cleanup",
    self._custom_cleanup_task,
    interval=7200  # 2 hours
)
```

## 🚦 Production Deployment

### Resource Requirements

**Minimum:**
- CPU: 0.25 cores
- Memory: 256MB
- Storage: 1GB (for logs)

**Recommended:**
- CPU: 0.5 cores
- Memory: 512MB
- Storage: 5GB (for logs and data)

### Security Considerations

1. **API Key Security**: Store bearer token securely
2. **Network Security**: Use firewalls and private networks
3. **Container Security**: Run as non-root user (already configured)
4. **Log Security**: Rotate and secure log files

### High Availability

For production deployments:

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  wfrmls-agent:
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
```

### Backup and Recovery

```bash
# Backup logs and data
tar -czf wfrmls-backup-$(date +%Y%m%d).tar.gz logs/

# Restore from backup
tar -xzf wfrmls-backup-YYYYMMDD.tar.gz
```

## 🐛 Troubleshooting

### Common Issues

**1. Agent won't start**
```bash
# Check logs
./run-agent.sh logs

# Verify bearer token
docker exec wfrmls-background-agent python -c "import os; print('Token:', os.getenv('WFRMLS_BEARER_TOKEN')[:10] + '...')"
```

**2. API connectivity issues**
```bash
# Test API from container
docker exec wfrmls-background-agent python -c "
from wfrmls import WFRMLSClient
client = WFRMLSClient()
print(client.property.get_properties(top=1))
"
```

**3. High memory usage**
```bash
# Check container stats
docker stats wfrmls-background-agent

# Reduce batch size
# Set WFRMLS_BATCH_SIZE=50 in environment
```

**4. Logs not persisting**
```bash
# Check volume mounts
docker inspect wfrmls-background-agent | jq '.[0].Mounts'

# Ensure logs directory exists and has proper permissions
mkdir -p logs
chmod 755 logs
```

### Debug Mode

Enable debug logging:

```bash
# Set debug level
export WFRMLS_LOG_LEVEL=DEBUG

# Restart agent
./run-agent.sh restart

# Follow debug logs
./run-agent.sh logs -f
```

## 📝 Integration with Cursor

To use this as a background agent in Cursor:

1. **Start the agent in the background:**
   ```bash
   ./run-agent.sh start
   ```

2. **Monitor from Cursor terminal:**
   ```bash
   # Check status
   ./run-agent.sh status
   
   # View logs
   ./run-agent.sh logs
   ```

3. **Integrate with your development workflow:**
   - The agent runs independently of your development environment
   - Logs are available in `./logs/` directory
   - Agent status can be checked anytime with the management script

## 🔗 Additional Resources

- [WFRMLS API Documentation](https://docs.utahrealestate.com)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

## 📄 License

This Docker configuration is part of the WFRMLS Python client and follows the same MIT License. 