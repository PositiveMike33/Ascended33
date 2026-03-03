#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
#  HEXSTRIKE VAULT ↔ GITHUB SYNC SCRIPT
#  Operator: TH3_THIRTY3
#  Résout: ACL/droits, conflits, audit log
# ═══════════════════════════════════════════════════════════════════

set -euo pipefail

# ─── CONFIG ────────────────────────────────────────────────────────
VAULT_PATH="${VAULT_PATH:-/vault}"
REPO_URL="${GITHUB_REPO_URL:-}"          # ex: git@github.com:Th3Thirty3/hexstrike-vault.git
BRANCH="${GITHUB_BRANCH:-main}"
SYNC_LOG="${VAULT_PATH}/_LOGS/vault_sync_$(date +%Y%m%d).log"
GITIGNORE_PATH="${VAULT_PATH}/.gitignore"

# Couleurs terminal
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; DIM='\033[2m'; RESET='\033[0m'; BOLD='\033[1m'

# ─── HELPERS ───────────────────────────────────────────────────────
log() { echo -e "${DIM}[$(date '+%H:%M:%S')]${RESET} $*" | tee -a "$SYNC_LOG" 2>/dev/null || true; }
ok()  { echo -e "${GREEN}  ✓${RESET} $*" | tee -a "$SYNC_LOG" 2>/dev/null || true; }
err() { echo -e "${RED}  ✗${RESET} $*" | tee -a "$SYNC_LOG" 2>/dev/null || true; }
warn(){ echo -e "${YELLOW}  ⚠${RESET} $*" | tee -a "$SYNC_LOG" 2>/dev/null || true; }
info(){ echo -e "${CYAN}  ◈${RESET} $*" | tee -a "$SYNC_LOG" 2>/dev/null || true; }

header() {
  echo ""
  echo -e "${CYAN}╔══════════════════════════════════════════════════╗${RESET}"
  echo -e "${CYAN}║  $1$(printf '%*s' $((46 - ${#1})) '')║${RESET}"
  echo -e "${CYAN}╚══════════════════════════════════════════════════╝${RESET}"
  echo ""
}

# ─── STEP 1: PRE-FLIGHT CHECKS ─────────────────────────────────────
preflight_checks() {
  header "STEP 1/6 — PRE-FLIGHT CHECKS"

  # Vault path
  if [[ ! -d "$VAULT_PATH" ]]; then
    err "VAULT_PATH not found: $VAULT_PATH"
    exit 1
  fi
  ok "Vault path: $VAULT_PATH"

  # Git installed
  if ! command -v git &>/dev/null; then
    err "git not found — install with: apt install git"
    exit 1
  fi
  ok "Git: $(git --version)"

  # SSH key check
  if ssh-add -l &>/dev/null; then
    ok "SSH agent: keys loaded"
  else
    warn "SSH agent: no keys loaded — trying default ~/.ssh/id_ed25519"
    if [[ -f "$HOME/.ssh/id_ed25519" ]]; then
      ssh-add "$HOME/.ssh/id_ed25519" 2>/dev/null && ok "SSH key loaded" || warn "Could not add SSH key"
    else
      warn "No SSH key found — HTTPS auth will be used (requires token)"
    fi
  fi

  # REPO_URL
  if [[ -z "$REPO_URL" ]]; then
    warn "GITHUB_REPO_URL not set — attempting to read from git remote"
    if git -C "$VAULT_PATH" remote get-url origin &>/dev/null; then
      REPO_URL=$(git -C "$VAULT_PATH" remote get-url origin)
      ok "Remote detected: $REPO_URL"
    else
      err "No remote configured. Set GITHUB_REPO_URL env var."
      info "Example: export GITHUB_REPO_URL=git@github.com:Th3Thirty3/hexstrike-vault.git"
      exit 1
    fi
  fi

  ok "Repo: $REPO_URL"
  ok "Branch: $BRANCH"
}

# ─── STEP 2: ACL AUDIT ─────────────────────────────────────────────
acl_audit() {
  header "STEP 2/6 — ACL / PERMISSIONS AUDIT"

  local issues=0

  # Vault directory permissions
  vault_perms=$(stat -c "%a" "$VAULT_PATH" 2>/dev/null || stat -f "%Lp" "$VAULT_PATH" 2>/dev/null)
  if [[ "$vault_perms" =~ ^7 ]]; then
    ok "Vault dir permissions: $vault_perms (owner RWX)"
  else
    warn "Vault dir permissions: $vault_perms — may block git operations"
    ((issues++))
  fi

  # .git directory
  if [[ -d "$VAULT_PATH/.git" ]]; then
    git_perms=$(stat -c "%a" "$VAULT_PATH/.git" 2>/dev/null || stat -f "%Lp" "$VAULT_PATH/.git" 2>/dev/null)
    ok ".git directory: exists (perms: $git_perms)"

    # Git config safe.directory
    if git config --global --get-all safe.directory 2>/dev/null | grep -q "$VAULT_PATH"; then
      ok "safe.directory: $VAULT_PATH registered"
    else
      warn "safe.directory not registered — adding..."
      git config --global --add safe.directory "$VAULT_PATH"
      ok "safe.directory: $VAULT_PATH added"
    fi
  else
    warn ".git not found — vault not initialized as git repo"
    info "Initializing git repo in vault..."
    git -C "$VAULT_PATH" init
    git -C "$VAULT_PATH" remote add origin "$REPO_URL"
    ok "Git repo initialized"
  fi

  # .gitignore check
  if [[ ! -f "$GITIGNORE_PATH" ]]; then
    warn ".gitignore missing — creating secure defaults..."
    create_gitignore
  else
    ok ".gitignore: present"
    # Verify sensitive paths are excluded
    for sensitive in ".obsidian/workspace" "*.log" "_PRIVATE/" "_KEYS/"; do
      if grep -q "$sensitive" "$GITIGNORE_PATH" 2>/dev/null; then
        ok ".gitignore covers: $sensitive"
      else
        warn ".gitignore missing rule for: $sensitive"
        echo "$sensitive" >> "$GITIGNORE_PATH"
        ok "Added: $sensitive"
        ((issues++))
      fi
    done
  fi

  # Check for accidentally tracked sensitive files
  if git -C "$VAULT_PATH" ls-files 2>/dev/null | grep -qiE "\.(key|pem|p12|pfx|secret|token|pass)$"; then
    err "CRITICAL: Sensitive file extensions tracked by git!"
    git -C "$VAULT_PATH" ls-files | grep -iE "\.(key|pem|p12|pfx|secret|token|pass)$" | while read f; do
      err "  → $f"
      warn "  Run: git rm --cached '$f' to untrack"
    done
    ((issues++))
  else
    ok "No sensitive file extensions tracked"
  fi

  if [[ $issues -eq 0 ]]; then
    ok "ACL audit: PASSED (0 issues)"
  else
    warn "ACL audit: $issues issue(s) found and auto-corrected where possible"
  fi
}

# ─── STEP 3: GITIGNORE ─────────────────────────────────────────────
create_gitignore() {
  cat > "$GITIGNORE_PATH" << 'GITEOF'
# ─── OBSIDIAN INTERNALS ───────────────────────────────
.obsidian/workspace
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/

# ─── SENSITIVE / PRIVATE ──────────────────────────────
_PRIVATE/
_KEYS/
_CREDENTIALS/
*.key
*.pem
*.p12
*.pfx
*.secret
*.token
*.pass
.env
.env.*

# ─── LOGS ─────────────────────────────────────────────
*.log
_LOGS/
vault_sync_*.log

# ─── OS ───────────────────────────────────────────────
.DS_Store
Thumbs.db
desktop.ini

# ─── TEMP ─────────────────────────────────────────────
*.tmp
*.bak
*~
GITEOF
  ok ".gitignore created with secure defaults"
}

# ─── STEP 4: PULL (fetch remote changes) ───────────────────────────
pull_remote() {
  header "STEP 3/6 — PULL REMOTE CHANGES"

  cd "$VAULT_PATH"

  # Stash any uncommitted changes
  if ! git diff --quiet HEAD 2>/dev/null; then
    warn "Uncommitted local changes detected — stashing..."
    git stash push -m "auto-stash before sync $(date +%Y%m%d_%H%M%S)"
    ok "Changes stashed"
    STASHED=true
  else
    STASHED=false
  fi

  # Fetch
  info "Fetching from remote..."
  if git fetch origin "$BRANCH" 2>&1 | tee -a "$SYNC_LOG"; then
    ok "Fetch: success"
  else
    err "Fetch failed — check SSH key / network / repo permissions"
    return 1
  fi

  # Check for conflicts before merge
  local_commits=$(git rev-list HEAD..origin/"$BRANCH" --count 2>/dev/null || echo 0)
  if [[ "$local_commits" -gt 0 ]]; then
    info "Remote has $local_commits new commit(s) — merging..."
    if git merge origin/"$BRANCH" --no-edit 2>&1 | tee -a "$SYNC_LOG"; then
      ok "Merge: success"
    else
      err "MERGE CONFLICT detected"
      warn "Conflicted files:"
      git diff --name-only --diff-filter=U | while read f; do warn "  → $f"; done
      info "To resolve: edit conflicted files, then run: git add . && git commit"
      info "Or abort:   git merge --abort"
      return 1
    fi
  else
    ok "Already up to date"
  fi

  # Restore stash
  if [[ "$STASHED" == "true" ]]; then
    info "Restoring stashed changes..."
    git stash pop && ok "Stash restored" || warn "Stash pop failed — run: git stash pop manually"
  fi
}

# ─── STEP 5: COMMIT + PUSH ─────────────────────────────────────────
push_changes() {
  header "STEP 4/6 — COMMIT & PUSH"

  cd "$VAULT_PATH"

  # Count changes
  changed=$(git status --porcelain | wc -l | tr -d ' ')
  if [[ "$changed" -eq 0 ]]; then
    ok "Nothing to commit — vault is clean"
    return 0
  fi

  info "Staging $changed changed file(s)..."
  git add -A

  # Build commit message
  added=$(git diff --cached --name-only --diff-filter=A | wc -l | tr -d ' ')
  modified=$(git diff --cached --name-only --diff-filter=M | wc -l | tr -d ' ')
  deleted=$(git diff --cached --name-only --diff-filter=D | wc -l | tr -d ' ')

  commit_msg="vault: sync $(date '+%Y-%m-%d %H:%M') [+${added} ~${modified} -${deleted}]"

  git commit -m "$commit_msg"
  ok "Committed: $commit_msg"

  info "Pushing to $REPO_URL ($BRANCH)..."
  if git push origin "$BRANCH" 2>&1 | tee -a "$SYNC_LOG"; then
    ok "Push: SUCCESS"
  else
    err "Push FAILED"
    warn "Common causes:"
    warn "  • SSH key not authorized on GitHub → check Settings > SSH keys"
    warn "  • Branch protection rules blocking push → check repo Settings"
    warn "  • Token expired (HTTPS) → refresh PAT in GitHub Settings"
    warn "  • Diverged history → run pull_remote() first"
    return 1
  fi
}

# ─── STEP 6: AUDIT REPORT ──────────────────────────────────────────
sync_report() {
  header "STEP 5/6 — SYNC REPORT"

  cd "$VAULT_PATH"

  local last_commit=$(git log -1 --format="%H %s (%cr)" 2>/dev/null || echo "N/A")
  local total_files=$(git ls-files 2>/dev/null | wc -l | tr -d ' ')
  local total_commits=$(git rev-list --count HEAD 2>/dev/null || echo "N/A")
  local remote_url=$(git remote get-url origin 2>/dev/null || echo "N/A")

  echo -e "${CYAN}  ┌──────────────────────────────────────────────┐${RESET}"
  echo -e "${CYAN}  │ SYNC STATUS REPORT                           │${RESET}"
  echo -e "${CYAN}  ├──────────────────────────────────────────────┤${RESET}"
  printf "${CYAN}  │${RESET} %-18s %-27s ${CYAN}│${RESET}\n" "Remote:" "$remote_url"
  printf "${CYAN}  │${RESET} %-18s %-27s ${CYAN}│${RESET}\n" "Branch:" "$BRANCH"
  printf "${CYAN}  │${RESET} %-18s %-27s ${CYAN}│${RESET}\n" "Last commit:" "${last_commit:0:40}"
  printf "${CYAN}  │${RESET} %-18s %-27s ${CYAN}│${RESET}\n" "Tracked files:" "$total_files"
  printf "${CYAN}  │${RESET} %-18s %-27s ${CYAN}│${RESET}\n" "Total commits:" "$total_commits"
  printf "${CYAN}  │${RESET} %-18s %-27s ${CYAN}│${RESET}\n" "Sync log:" "$SYNC_LOG"
  echo -e "${CYAN}  └──────────────────────────────────────────────┘${RESET}"
}

# ─── MAIN ──────────────────────────────────────────────────────────
main() {
  mkdir -p "$(dirname "$SYNC_LOG")" 2>/dev/null || true

  echo ""
  echo -e "${GREEN}⬡ HEXSTRIKE VAULT SYNC — $(date '+%Y-%m-%d %H:%M:%S')${RESET}"
  echo ""

  preflight_checks
  acl_audit
  pull_remote
  push_changes
  sync_report

  header "STEP 6/6 — COMPLETE"
  ok "Vault sync completed successfully"
  echo ""
}

# Run
main "$@"
