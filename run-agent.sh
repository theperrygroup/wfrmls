#!/bin/bash

# WFRMLS Background Agent Management Script
# This script provides easy commands to manage the WFRMLS background agent

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CONTAINER_NAME="wfrmls-background-agent"
COMPOSE_FILE="docker-compose.yml"
LOG_DIR="./logs"

# Docker Compose command (use newer syntax if available)
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    DOCKER_COMPOSE_CMD="docker compose"
fi

# Functions
print_usage() {
    echo "Usage: $0 {start|stop|restart|status|logs|build|clean|shell}"
    echo ""
    echo "Commands:"
    echo "  start    - Start the WFRMLS background agent"
    echo "  stop     - Stop the WFRMLS background agent"
    echo "  restart  - Restart the WFRMLS background agent"
    echo "  status   - Show agent status and health"
    echo "  logs     - Show agent logs (use -f to follow)"
    echo "  build    - Build the Docker image"
    echo "  clean    - Stop and remove containers and images"
    echo "  shell    - Open a shell inside the running container"
    echo "  dashboard - Start with monitoring dashboard"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs -f"
    echo "  $0 status"
}

check_dependencies() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}Error: Docker Compose is not installed${NC}"
        exit 1
    fi
}

create_log_dir() {
    if [ ! -d "$LOG_DIR" ]; then
        echo -e "${YELLOW}Creating log directory: $LOG_DIR${NC}"
        mkdir -p "$LOG_DIR"
    fi
}

start_agent() {
    echo -e "${BLUE}Starting WFRMLS Background Agent...${NC}"
    create_log_dir
    
    if $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" up -d wfrmls-agent; then
        echo -e "${GREEN}WFRMLS Background Agent started successfully${NC}"
        echo ""
        echo "To view logs: $0 logs"
        echo "To check status: $0 status"
    else
        echo -e "${RED}Failed to start WFRMLS Background Agent${NC}"
        exit 1
    fi
}

start_with_dashboard() {
    echo -e "${BLUE}Starting WFRMLS Background Agent with Dashboard...${NC}"
    create_log_dir
    
    if $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" --profile dashboard up -d; then
        echo -e "${GREEN}WFRMLS Background Agent and Dashboard started successfully${NC}"
        echo ""
        echo "Agent logs: $0 logs"
        echo "Dashboard: http://localhost:3000"
        echo "Agent status: $0 status"
    else
        echo -e "${RED}Failed to start WFRMLS Background Agent with Dashboard${NC}"
        exit 1
    fi
}

stop_agent() {
    echo -e "${BLUE}Stopping WFRMLS Background Agent...${NC}"
    
    if $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" down; then
        echo -e "${GREEN}WFRMLS Background Agent stopped${NC}"
    else
        echo -e "${RED}Failed to stop WFRMLS Background Agent${NC}"
        exit 1
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
    health_status=$(docker inspect --format='{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "unknown")
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
    if ! docker ps -a --format "{{.Names}}" | grep -q "$CONTAINER_NAME"; then
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

build_image() {
    echo -e "${BLUE}Building WFRMLS Background Agent Docker image...${NC}"
    
    if $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" build; then
        echo -e "${GREEN}Docker image built successfully${NC}"
    else
        echo -e "${RED}Failed to build Docker image${NC}"
        exit 1
    fi
}

clean_environment() {
    echo -e "${YELLOW}Cleaning up WFRMLS Background Agent environment...${NC}"
    
    # Stop and remove containers
    $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" down --remove-orphans
    
    # Remove images
    if docker images | grep -q "wfrmls"; then
        echo "Removing WFRMLS Docker images..."
        docker images | grep "wfrmls" | awk '{print $3}' | xargs docker rmi -f
    fi
    
    echo -e "${GREEN}Environment cleaned${NC}"
}

open_shell() {
    echo -e "${BLUE}Opening shell in WFRMLS Background Agent container...${NC}"
    
    if docker ps --format "{{.Names}}" | grep -q "$CONTAINER_NAME"; then
        docker exec -it "$CONTAINER_NAME" /bin/bash
    else
        echo -e "${RED}Container $CONTAINER_NAME is not running${NC}"
        exit 1
    fi
}

# Main script logic
case "$1" in
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
    build)
        check_dependencies
        build_image
        ;;
    clean)
        check_dependencies
        clean_environment
        ;;
    shell)
        check_dependencies
        open_shell
        ;;
    dashboard)
        check_dependencies
        start_with_dashboard
        ;;
    *)
        print_usage
        exit 1
        ;;
esac 