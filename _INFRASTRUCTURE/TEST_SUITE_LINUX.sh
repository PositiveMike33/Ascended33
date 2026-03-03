#!/bin/bash

# ============================================================================
# TEST SUITE AUTOMATISÉE - HexStrike Ascended33
# Valide tous les conteneurs Docker, connexions, volumes, et APIs
# ============================================================================

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
COMPOSE_FILE_V2="$PROJECT_ROOT/docker-compose-v2.yml"
VAULT_PATH="${VAULT_PATH:-/mnt/vault}"
RESULTS_LOG="$SCRIPT_DIR/test-results-$(date +%Y-%m-%d_%H%M%S).log"

# Couleurs ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[1;35m'
NC='\033[0m' # No Color

# Compteurs
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_WARNING=0

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

write_header() {
    echo -e "\n${MAGENTA}╔════════════════════════════════════════╗${NC}"
    printf "${MAGENTA}║ %-36s ║${NC}\n" "$1"
    echo -e "${MAGENTA}╚════════════════════════════════════════╝${NC}\n"
}

write_test_info() {
    echo -e "${CYAN}[ÉTAPE $1]${NC} $2"
}

write_success() {
    echo -e "${GREEN}✓ SUCCÈS:${NC} $1"
    echo "✓ $1" >> "$RESULTS_LOG"
    ((TESTS_PASSED++))
}

write_failure() {
    echo -e "${RED}✗ ÉCHEC:${NC} $1"
    echo "✗ $1" >> "$RESULTS_LOG"
    ((TESTS_FAILED++))
}

write_warning() {
    echo -e "${YELLOW}⚠ ATTENTION:${NC} $1"
    echo "⚠ $1" >> "$RESULTS_LOG"
    ((TESTS_WARNING++))
}

get_container_status() {
    docker inspect -f '{{.State.Status}}' "$1" 2>/dev/null || echo "unknown"
}

test_endpoint() {
    local url="$1"
    local description="$2"
    
    if curl -s -m 5 "$url" &>/dev/null; then
        write_success "$description - Status 200"
        return 0
    else
        write_failure "$description - No response"
        return 1
    fi
}

docker_exec_test() {
    local container="$1"
    local command="$2"
    local description="$3"
    
    if docker exec "$container" sh -c "$command" &>/dev/null; then
        write_success "$description"
        return 0
    else
        write_failure "$description"
        return 1
    fi
}

# ============================================================================
# TESTS
# ============================================================================

write_header "DÉMARRAGE SUITE DE TESTS - HexStrike Ascended33"
echo "=== TEST SUITE STARTED $(date) ===" > "$RESULTS_LOG"

# ============================================================================
# PHASE 1 : VÉRIFICATION INFRASTRUCTURE
# ============================================================================

write_header "PHASE 1 - Vérification Infrastructure Docker"

write_test_info "1.1" "Vérifier l'état des conteneurs Docker"
containers=("th3-hexstrike" "th3-tor" "th3-kali" "th3-hackergpt" "th3-streamlit")

for container in "${containers[@]}"; do
    status=$(get_container_status "$container")
    if [ "$status" = "running" ]; then
        write_success "Conteneur $container est UP"
    elif [ "$status" = "exited" ]; then
        write_failure "Conteneur $container est STOPPED"
    else
        write_warning "Conteneur $container status: $status"
    fi
done

write_test_info "1.2" "Afficher le format détaillé des conteneurs"
ps_output=$(docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}")
echo "$ps_output"
echo "Docker PS Output:" >> "$RESULTS_LOG"
echo "$ps_output" >> "$RESULTS_LOG"

# ============================================================================
# PHASE 2 : CONNEXIONS INTERNES
# ============================================================================

write_header "PHASE 2 - Tests de Connexion Interne"

write_test_info "2.1" "Test santé Hexstrike (port 8001)"
if docker exec th3-hexstrike curl -s http://localhost:8001/health &>/dev/null; then
    write_success "HexStrike Health Check"
else
    write_failure "HexStrike Health Check"
fi

write_test_info "2.2" "Test ping Redis depuis Hexstrike"
if docker exec th3-hexstrike redis-cli -h redis ping &>/dev/null; then
    write_success "Redis ping test"
else
    write_warning "Redis pas accessible (optionnel)"
fi

write_test_info "2.3" "Test connectivité réseau Docker"
network_info=$(docker network inspect ascended33-network 2>/dev/null | grep -A 20 "Containers" || echo "Network not found")
if [ ! -z "$network_info" ]; then
    write_success "Réseau ascended33-network accessible"
    echo "$network_info"
else
    write_warning "Réseau ascended33-network non trouvé"
fi

# ============================================================================
# PHASE 3 : TESTS APPLICATIFS
# ============================================================================

write_header "PHASE 3 - Tests Applicatifs"

write_test_info "3.1" "Test volume Vault monté"
if [ -d "$VAULT_PATH" ]; then
    write_success "Volume Vault accessible: $VAULT_PATH"
    vault_size=$(du -sh "$VAULT_PATH" 2>/dev/null | cut -f1)
    echo "  Taille totale: $vault_size"
else
    write_failure "Volume Vault INACCESSIBLE: $VAULT_PATH"
fi

write_test_info "3.2" "Tester création fichier dans volume"
if [ -d "$VAULT_PATH" ]; then
    test_file="$VAULT_PATH/test_$(date +%s).txt"
    if echo "Test write at $(date)" > "$test_file" 2>/dev/null; then
        write_success "Fichier créé: $test_file"
        rm -f "$test_file"
    else
        write_failure "Impossible d'écrire dans Vault"
    fi
fi

write_test_info "3.3" "Vérifier structure REPORT"
report_path="$VAULT_PATH/REPORT/Classified"
if [ -d "$report_path" ]; then
    write_success "Dossier REPORT/Classified existe"
    file_count=$(find "$report_path" -type f 2>/dev/null | wc -l)
    echo "  Fichiers présents: $file_count"
else
    write_warning "Dossier REPORT/Classified n'existe pas encore"
fi

# ============================================================================
# PHASE 4 : TESTS API EXTERNES
# ============================================================================

write_header "PHASE 4 - Tests API Externes"

write_test_info "4.1" "Test HexStrike API (port 8001)"
test_endpoint "http://localhost:8001/health" "HexStrike Health Endpoint"

write_test_info "4.2" "Test HackerGPT API (port 8000)"
test_endpoint "http://localhost:8000/health" "HackerGPT Health Endpoint"

write_test_info "4.3" "Test Streamlit Dashboard (port 8501)"
test_endpoint "http://localhost:8501/_stcore/health" "Streamlit Health Endpoint"

write_test_info "4.4" "Test Kali Labs API (port 5000)"
test_endpoint "http://localhost:5000/health" "Kali Labs Health Endpoint"

write_test_info "4.5" "Test Audit API (port 8002)"
test_endpoint "http://localhost:8002/health" "Audit API Health Endpoint"

write_test_info "4.6" "Test Vault Indexer (port 8004)"
test_endpoint "http://localhost:8004/health" "Vault Indexer Health Endpoint"

write_test_info "4.7" "Test Report Generator (port 8005)"
test_endpoint "http://localhost:8005/health" "Report Generator Health Endpoint"

# ============================================================================
# PHASE 5 : TESTS TOR / ANONYMITÉ
# ============================================================================

write_header "PHASE 5 - Tests Tor & Anonymité"

write_test_info "5.1" "Vérifier Tor SOCKS5 (port 9050)"
if docker exec th3-tor curl -s --socks5 localhost:9050 https://check.torproject.org/api/ip 2>/dev/null | grep -q "isTor"; then
    write_success "Tor SOCKS5 est fonctionnel"
else
    write_failure "Tor SOCKS5 ne répond pas correctement"
fi

write_test_info "5.2" "Vérifier Tor control port (9051)"
if docker exec th3-tor sh -c "echo 'GETINFO version' | nc localhost 9051" &>/dev/null; then
    write_success "Tor Control Port est accessible"
else
    write_warning "Tor Control Port non accessible"
fi

# ============================================================================
# PHASE 6 : TESTS PERSISTANCE ET LOGGING
# ============================================================================

write_header "PHASE 6 - Tests Persistance & Logging"

write_test_info "6.1" "Vérifier logs Hexstrike"
echo "Derniers logs Hexstrike (20 lignes):"
docker logs th3-hexstrike 2>&1 | tail -20

write_test_info "6.2" "Vérifier logs Tor"
echo "Derniers logs Tor (10 lignes):"
docker logs th3-tor 2>&1 | tail -10

write_test_info "6.3" "Vérifier volumes Docker"
volumes=$(docker volume ls --format "table {{.Name}}\t{{.Driver}}")
echo "$volumes"
echo "Docker Volumes:" >> "$RESULTS_LOG"
echo "$volumes" >> "$RESULTS_LOG"

# ============================================================================
# PHASE 7 : TESTS INTEGRATION PIECES OS & MCP
# ============================================================================

write_header "PHASE 7 - Tests Intégration Pieces OS & MCP"

write_test_info "7.1" "Vérifier Pieces OS (port 39300)"
test_endpoint "http://localhost:39300/health" "Pieces OS Health"

write_test_info "7.2" "Vérifier Obsidian API (port 3123)"
test_endpoint "http://127.0.0.1:3123/health" "Obsidian API Health"

write_test_info "7.3" "Vérifier HexStrike MCP"
if [ -f "$SCRIPT_DIR/Ascended33/hexstrike-mcp.py" ]; then
    write_success "HexStrike MCP script trouvé"
else
    write_warning "HexStrike MCP script non trouvé"
fi

# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================

write_header "RÉSUMÉ DES TESTS"

total_tests=$((TESTS_PASSED + TESTS_FAILED + TESTS_WARNING))
if [ $total_tests -gt 0 ]; then
    success_rate=$((TESTS_PASSED * 100 / total_tests))
else
    success_rate=0
fi

echo -e "Total Tests: $total_tests"
echo -e "${GREEN}✓ Succès: $TESTS_PASSED${NC}"
echo -e "${RED}✗ Échecs: $TESTS_FAILED${NC}"
echo -e "${YELLOW}⚠ Avertissements: $TESTS_WARNING${NC}"
echo "Taux de réussite: $success_rate%"

echo ""
echo "Résultats sauvegardés dans: $RESULTS_LOG"

# ============================================================================
# NETTOYAGE (OPTIONNEL)
# ============================================================================

write_header "Options de Nettoyage"

echo -e "Pour nettoyer les ressources Docker:"
echo -e "${YELLOW}  docker system prune -a --volumes${NC}"
echo ""
echo -e "Pour redémarrer tous les services:"
echo -e "${YELLOW}  docker-compose -f docker-compose-v2.yml down && docker-compose -f docker-compose-v2.yml up -d${NC}"

echo "" >> "$RESULTS_LOG"
echo "=== TEST SUITE COMPLETED $(date) ===" >> "$RESULTS_LOG"

echo -e "\n${GREEN}✓ Suite de tests terminée !${NC}\n"
