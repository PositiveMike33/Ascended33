#!/bin/bash

# ============================================================================
# HexStrike Ascended33 - TEST SUITE LAUNCHER
# Multiplatform test orchestration for Docker infrastructure
# ============================================================================

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$SCRIPT_DIR/test_orchestrator.py"
BASH_SCRIPT="$SCRIPT_DIR/TEST_SUITE_LINUX.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[1;35m'
NC='\033[0m' # No Color

# ============================================================================
# BANNER
# ============================================================================

clear
echo ""
echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║       HexStrike Ascended33 - TEST SUITE LAUNCHER          ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# CHECK PREREQUISITES
# ============================================================================

echo -e "${CYAN}[CHECKING PREREQUISITES]${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found${NC}"
    echo ""
    echo "Please install Docker:"
    echo "  macOS: brew install docker"
    echo "  Linux: sudo apt-get install docker.io"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}"

# Check Python
if command -v python3 &> /dev/null; then
    HAS_PYTHON=1
    PYTHON_CMD="python3"
    echo -e "${GREEN}✓ Python 3 found${NC}"
elif command -v python &> /dev/null; then
    HAS_PYTHON=1
    PYTHON_CMD="python"
    echo -e "${GREEN}✓ Python found${NC}"
else
    HAS_PYTHON=0
    echo -e "${YELLOW}⚠ Python not found (using Bash instead)${NC}"
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose not found${NC}"
    echo ""
    echo "Please install Docker Compose:"
    echo "  macOS: brew install docker-compose"
    echo "  Linux: sudo apt-get install docker-compose"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose found${NC}"

echo ""

# ============================================================================
# MENU
# ============================================================================

while true; do
    echo -e "${MAGENTA}Select test execution method:${NC}"
    echo ""
    
    if [ $HAS_PYTHON -eq 1 ]; then
        echo -e "  ${CYAN}[1]${NC} Python - Full featured (recommended)"
        echo -e "  ${CYAN}[2]${NC} Bash - Simple and fast"
    else
        echo -e "  ${CYAN}[1]${NC} Bash - Simple and fast"
    fi
    
    echo -e "  ${CYAN}[3]${NC} Docker PS - Quick container check"
    echo -e "  ${CYAN}[4]${NC} Docker Logs - View service logs"
    echo -e "  ${CYAN}[5]${NC} Docker Network - Inspect network"
    echo -e "  ${CYAN}[6]${NC} System Cleanup - Clean Docker resources"
    echo -e "  ${CYAN}[7]${NC} Exit"
    echo ""
    
    read -p "Choose option (1-7): " CHOICE
    
    case $CHOICE in
        1)
            if [ $HAS_PYTHON -eq 1 ]; then
                run_python_tests
            else
                run_bash_tests
            fi
            ;;
        2)
            if [ $HAS_PYTHON -eq 1 ]; then
                run_bash_tests
            else
                echo -e "${RED}Invalid choice${NC}"
            fi
            ;;
        3)
            quick_container_check
            ;;
        4)
            view_logs
            ;;
        5)
            inspect_network
            ;;
        6)
            cleanup_docker
            ;;
        7)
            exit_script
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            echo ""
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    clear
done

# ============================================================================
# FUNCTIONS
# ============================================================================

run_python_tests() {
    clear
    echo ""
    echo -e "${CYAN}[RUNNING PYTHON TEST SUITE]${NC}"
    echo ""
    $PYTHON_CMD "$PYTHON_SCRIPT"
}

run_bash_tests() {
    clear
    echo ""
    echo -e "${CYAN}[RUNNING BASH TEST SUITE]${NC}"
    echo ""
    bash "$BASH_SCRIPT"
}

quick_container_check() {
    clear
    echo ""
    echo -e "${CYAN}[DOCKER CONTAINER STATUS]${NC}"
    echo ""
    docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
}

view_logs() {
    clear
    echo ""
    echo -e "${CYAN}[SELECT CONTAINER FOR LOGS]${NC}"
    echo ""
    echo -e "  ${CYAN}[1]${NC} th3-hexstrike"
    echo -e "  ${CYAN}[2]${NC} th3-tor"
    echo -e "  ${CYAN}[3]${NC} th3-kali"
    echo -e "  ${CYAN}[4]${NC} th3-hackergpt"
    echo -e "  ${CYAN}[5]${NC} th3-streamlit"
    echo -e "  ${CYAN}[6]${NC} All (last 20 lines each)"
    echo ""
    
    read -p "Choose container (1-6): " LOG_CHOICE
    
    case $LOG_CHOICE in
        1) docker logs --tail=50 th3-hexstrike ;;
        2) docker logs --tail=50 th3-tor ;;
        3) docker logs --tail=50 th3-kali ;;
        4) docker logs --tail=50 th3-hackergpt ;;
        5) docker logs --tail=50 th3-streamlit ;;
        6)
            for container in th3-hexstrike th3-tor th3-kali th3-hackergpt th3-streamlit; do
                echo ""
                echo -e "${CYAN}--- Logs for $container ---${NC}"
                docker logs --tail=20 "$container" 2>&1 || echo "(No logs available)"
            done
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
    
    echo ""
}

inspect_network() {
    clear
    echo ""
    echo -e "${CYAN}[DOCKER NETWORK INSPECTION]${NC}"
    echo ""
    docker network inspect ascended33-network 2>/dev/null || {
        echo -e "${YELLOW}Network 'ascended33-network' not found${NC}"
        echo ""
        echo "Available networks:"
        docker network ls
    }
    echo ""
}

cleanup_docker() {
    clear
    echo ""
    echo -e "${YELLOW}[CLEANUP OPTIONS]${NC}"
    echo ""
    echo -e "  ${CYAN}[1]${NC} Remove stopped containers"
    echo -e "  ${CYAN}[2]${NC} Remove dangling images"
    echo -e "  ${CYAN}[3]${NC} Remove unused volumes"
    echo -e "  ${CYAN}[4]${NC} Full cleanup (containers, images, volumes)"
    echo -e "  ${CYAN}[5]${NC} Back to menu"
    echo ""
    
    read -p "Choose option (1-5): " CLEANUP_CHOICE
    
    case $CLEANUP_CHOICE in
        1)
            echo -e "${CYAN}Removing stopped containers...${NC}"
            docker container prune -f
            echo -e "${GREEN}✓ Done${NC}"
            ;;
        2)
            echo -e "${CYAN}Removing dangling images...${NC}"
            docker image prune -f
            echo -e "${GREEN}✓ Done${NC}"
            ;;
        3)
            echo -e "${CYAN}Removing unused volumes...${NC}"
            docker volume prune -f
            echo -e "${GREEN}✓ Done${NC}"
            ;;
        4)
            echo -e "${RED}WARNING: This will remove all Docker resources not in use!${NC}"
            read -p "Continue? (y/N): " CONFIRM
            if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
                echo -e "${CYAN}Running full cleanup...${NC}"
                docker system prune -a --volumes -f
                echo -e "${GREEN}✓ Cleanup complete${NC}"
            else
                echo -e "${YELLOW}Cleanup cancelled${NC}"
            fi
            ;;
        5)
            return
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
    
    echo ""
}

exit_script() {
    clear
    echo ""
    echo -e "${GREEN}Goodbye!${NC}"
    echo ""
    exit 0
}
