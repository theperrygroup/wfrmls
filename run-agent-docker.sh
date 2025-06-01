#!/bin/bash

# WFRMLS Background Agent Docker Management Script (Pure Docker)
# This script uses pure Docker commands instead of Docker Compose

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CONTAINER_NAME="wfrmls-background-agent"
IMAGE_NAME="wfrmls-agent"
LOG_DIR="./logs"
NETWORK_NAME="wfrmls-network"

# Functions
print_usage() {
    echo "Usage: $0 {build|start|stop|restart|status|logs|clean|shell}"
    echo ""
    echo "Commands:"
    echo "  build    - Build the Docker image"
    echo "  start    - Start the WFRMLS background agent"
    echo "  stop     - Stop the WFRMLS background agent"
    echo "  restart  - Restart the WFRMLS background agent"
    echo "  status   - Show agent status and health"
    echo "  logs     - Show agent logs (use -f to follow)"
    echo "  clean    - Stop and remove containers and images"
    echo "  shell    - Open a shell inside the running container"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 start"
    echo "  $0 logs -f"
    echo "  $0 status"
}

check_dependencies() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        exit 1
    fi
}

create_log_dir() {
    if [ ! -d "$LOG_DIR" ]; then
        echo -e "${YELLOW}Creating log directory: $LOG_DIR${NC}"
        mkdir -p "$LOG_DIR"
    fi
}

create_network() {
    if ! docker network ls | grep -q "$NETWORK_NAME"; then
        echo -e "${YELLOW}Creating Docker network: $NETWORK_NAME${NC}"
        docker network create "$NETWORK_NAME"
    fi
}

build_image() {
    echo -e "${BLUE}Building WFRMLS Background Agent Docker image...${NC}"
    
    if docker build --target production -t "$IMAGE_NAME:latest" .; then
        echo -e "${GREEN}Docker image built successfully${NC}"
    else
        echo -e "${RED}Failed to build Docker image${NC}"
        exit 1
    fi
}

start_agent() {
    echo -e "${BLUE}Starting WFRMLS Background Agent...${NC}"
    create_log_dir
    create_network
    
    # Check if container already exists
    if docker ps -a --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        echo -e "${YELLOW}Container already exists. Removing...${NC}"
        docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
    fi
    
    # Get the bearer token from environment or use default
    BEARER_TOKEN=${WFRMLS_BEARER_TOKEN:-9d0243d7632d115b002acf3547d2d7ee}
    
    # Start the container
    if docker run -d \
        --name "$CONTAINER_NAME" \
        --network "$NETWORK_NAME" \
        --restart unless-stopped \
        -e WFRMLS_BEARER_TOKEN="$BEARER_TOKEN" \
        -e WFRMLS_SYNC_INTERVAL="${WFRMLS_SYNC_INTERVAL:-900}" \
        -e WFRMLS_MONITOR_INTERVAL="${WFRMLS_MONITOR_INTERVAL:-300}" \
        -e WFRMLS_HEALTH_CHECK_INTERVAL="${WFRMLS_HEALTH_CHECK_INTERVAL:-600}" \
        -e WFRMLS_LOG_LEVEL="${WFRMLS_LOG_LEVEL:-INFO}" \
        -e WFRMLS_LOG_TO_FILE="${WFRMLS_LOG_TO_FILE:-true}" \
        -e WFRMLS_MAX_RETRIES="${WFRMLS_MAX_RETRIES:-3}" \
        -e WFRMLS_BATCH_SIZE="${WFRMLS_BATCH_SIZE:-200}" \
        -e WFRMLS_ENABLE_ALERTS="${WFRMLS_ENABLE_ALERTS:-true}" \
        -e WFRMLS_WEBHOOK_URL="${WFRMLS_WEBHOOK_URL:-}" \
        -e PYTHONUNBUFFERED=1 \
        -e PYTHONDONTWRITEBYTECODE=1 \
        -v "$(pwd)/logs:/app/logs" \
        -p 8080:8080 \
        "$IMAGE_NAME:latest"; then
        
        echo -e "${GREEN}WFRMLS Background Agent started successfully${NC}"
        echo ""
        echo "Container ID: $(docker ps -q -f name=$CONTAINER_NAME)"
        echo "To view logs: $0 logs"
        echo "To check status: $0 status"
    else
        echo -e "${RED}Failed to start WFRMLS Background Agent${NC}"
        exit 1
    fi
}

stop_agent() {
    echo -e "${BLUE}Stopping WFRMLS Background Agent...${NC}"
    
    if docker ps --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        if docker stop "$CONTAINER_NAME"; then
            echo -e "${GREEN}WFRMLS Background Agent stopped${NC}"
        else
            echo -e "${RED}Failed to stop WFRMLS Background Agent${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Container is not running${NC}"
    fi
}

restart_agent() {
    echo -e "${BLUE}Restarting WFRMLS Background Agent...${NC}"
    stop_agent
    sleep 2
    start_agent
}

show_status() {
    echo -e "${BLUE}WFRMLS Background Agent Status:${NC}"
    echo ""
    
    # Check if container is running
    if docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q "$CONTAINER_NAME"; then
        echo -e "${GREEN}✓ Container Status: Running${NC}"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep "$CONTAINER_NAME"
    else
        echo -e "${RED}✗ Container Status: Stopped${NC}"
        return 1
    fi
    
    echo ""
    
    # Check health status
    health_status=$(docker inspect --format='{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "no-healthcheck")
    case $health_status in
        "healthy")
            echo -e "${GREEN}✓ Health Status: Healthy${NC}"
            ;;
        "unhealthy")
            echo -e "${RED}✗ Health Status: Unhealthy${NC}"
            ;;
        "starting")
            echo -e "${YELLOW}⚠ Health Status: Starting${NC}"
            ;;
        "no-healthcheck")
            echo -e "${YELLOW}? Health Status: No health check configured${NC}"
            ;;
        *)
            echo -e "${YELLOW}? Health Status: Unknown${NC}"
            ;;
    esac
    
    # Show resource usage
    echo ""
    echo -e "${BLUE}Resource Usage:${NC}"
    docker stats "$CONTAINER_NAME" --no-stream --format "table {{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" 2>/dev/null || echo "Resource stats unavailable"
}

show_logs() {
    echo -e "${BLUE}WFRMLS Background Agent Logs:${NC}"
    echo ""
    
    # Check if container exists
    if ! docker ps -a --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        echo -e "${RED}Container $CONTAINER_NAME not found${NC}"
        exit 1
    fi
    
    # Show logs with optional follow flag
    if [ "$1" == "-f" ]; then
        docker logs -f "$CONTAINER_NAME"
    else
        docker logs "$CONTAINER_NAME" | tail -50
    fi
}

clean_environment() {
    echo -e "${YELLOW}Cleaning up WFRMLS Background Agent environment...${NC}"
    
    # Stop and remove container
    if docker ps -a --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        echo "Stopping and removing container..."
        docker rm -f "$CONTAINER_NAME"
    fi
    
    # Remove image
    if docker images --format "{{.Repository}}" | grep -q "^${IMAGE_NAME}$"; then
        echo "Removing Docker image..."
        docker rmi -f "$IMAGE_NAME:latest"
    fi
    
    # Remove network
    if docker network ls | grep -q "$NETWORK_NAME"; then
        echo "Removing Docker network..."
        docker network rm "$NETWORK_NAME" 2>/dev/null || true
    fi
    
    echo -e "${GREEN}Environment cleaned${NC}"
}

open_shell() {
    echo -e "${BLUE}Opening shell in WFRMLS Background Agent container...${NC}"
    
    if docker ps --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        docker exec -it "$CONTAINER_NAME" /bin/bash
    else
        echo -e "${RED}Container $CONTAINER_NAME is not running${NC}"
        exit 1
    fi
}

# Main script logic
case "$1" in
    build)
        check_dependencies
        build_image
        ;;
    start)
        check_dependencies
        start_agent
        ;;
    stop)
        check_dependencies
        stop_agent
        ;;
    restart)
        check_dependencies
        restart_agent
        ;;
    status)
        check_dependencies
        show_status
        ;;
    logs)
        check_dependencies
        show_logs "$2"
        ;;
    clean)
        check_dependencies
        clean_environment
        ;;
    shell)
        check_dependencies
        open_shell
        ;;
    *)
        print_usage
        exit 1
        ;;
esac 