# CLAUDE.md – Ascended33 Dashboard

## Project Overview

**Ascended33** is a lightweight **Streamlit web application** serving as a dashboard template for the `hexstrike-ai` platform. It provides an interactive spiral visualization demo built with Python, demonstrating a clean, minimal architecture suitable for expanding into a full data dashboard.

- **Purpose**: Dashboard template for `hexstrike-ai` platform integration
- **Type**: Python Streamlit web app
- **Current Demo**: Interactive spiral visualization with real-time controls
- **Stack**: Python 3.11+, Streamlit, Altair (charting), Pandas, NumPy
- **Entry Point**: `streamlit_app.py`
- **Default Port**: 8501 (Streamlit standard)

---

## Codebase Structure

```
Ascended33/
├── streamlit_app.py              # Main app entry point (spiral visualization)
├── requirements.txt              # Python dependencies (altair, pandas, streamlit)
├── README.md                     # Basic usage instructions
├── LICENSE                       # Apache 2.0 license
├── .devcontainer/
│   └── devcontainer.json         # Local dev container config (Codespaces)
├── .github/
│   ├── .devcontainer/
│   │   └── devcontainer.json     # Build container config (CI/CD pipeline)
│   └── workflows/
│       └── devcontainer-build-and-push.yml  # GitHub Actions: build & push image
└── .git/                         # Git repository
```

### Key Files

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Application entry point; renders interactive spiral chart with Altair; implements `Number of points` and `Number of turns` sliders for real-time visualization control |
| `requirements.txt` | Minimal dependency list: `altair`, `pandas`, `streamlit` |
| `.devcontainer/devcontainer.json` | Codespaces/local container config; auto-opens README and app file; launches Streamlit on startup (port 8501) |
| `.github/.devcontainer/devcontainer.json` | CI build container config; Python 3.11 base; installs dependencies; includes VS Code extensions (Python, Pylance) |
| `.github/workflows/devcontainer-build-and-push.yml` | GitHub Actions workflow; builds and pushes dev container image to GHCR on `main` branch push or tags |

---

## Development Setup

### Local Development (No Container)

1. **Install Python 3.11+** (check with `python --version`)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```
   - Opens in browser at `http://localhost:8501`
   - Hot-reload enabled; changes to Python files auto-refresh the browser

### Development Container (Recommended)

The project includes dev container configurations for:

- **GitHub Codespaces**: Pre-configured `devcontainer.json` for instant cloud development
- **Local containers** (VS Code, Docker Desktop): Use `.devcontainer/devcontainer.json`

#### Using VS Code Dev Containers Locally

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Install [VS Code Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Open workspace in Dev Container: `Cmd/Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
4. Streamlit auto-launches on port 8501

#### Using GitHub Codespaces

1. Go to repository on GitHub
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Container builds automatically; Streamlit launches on port 8501

---

## Running the Application

### Standard Execution

```bash
streamlit run streamlit_app.py
```

- **Default URL**: `http://localhost:8501`
- **Config**: Disables CORS and CSRF in dev containers (see `.devcontainer/devcontainer.json`)

### Streamlit Configuration

The app runs with default Streamlit settings. To customize:
- Edit `streamlit run streamlit_app.py` commands in `.devcontainer/devcontainer.json`
- Create `.streamlit/config.toml` for persistent settings

---

## Key Conventions & Best Practices

### Python Style
- **Imports**: Standard library → third-party (altair, pandas, streamlit) → local code
- **Dependencies**: Minimal; only add to `requirements.txt` when necessary
- **Code**: Clear, readable; prioritize simplicity for dashboard templates

### Dependency Management
- **requirements.txt**: Pin major versions only (e.g., `streamlit`, not `streamlit==1.28.0`) for flexibility
- **No lock file**: Keep environment lightweight for dashboard use cases
- **Version compatibility**: Test with Python 3.11+ before updating

### Streamlit Patterns
- **Sliders & inputs**: Use `st.slider()`, `st.text_input()`, etc. for interactive controls
- **Charts**: Prefer Altair for composable, declarative visualizations
- **Data processing**: Use Pandas DataFrames for tabular data; NumPy for numerical operations
- **Performance**: Memoize expensive functions with `@st.cache_data`

---

## CI/CD & Deployment

### GitHub Actions Workflow

Trigger: `devcontainer-build-and-push.yml`

**When**:
- Manual trigger (`workflow_dispatch`)
- Push to `main` branch
- Tag push (version tags `v*.*.*`)
- Pull requests to `main`

**What it does**:
1. Checks out code
2. Logs into GHCR (GitHub Container Registry)
3. Builds dev container image from `.github/.devcontainer/devcontainer.json`
4. Pushes image to `ghcr.io/<repository>`

**Requirements**:
- `REGISTRY_TOKEN` secret in GitHub (PAT with `write:packages` scope)
- Sufficient GHCR quota

### Docker Image

- **Base**: `mcr.microsoft.com/devcontainers/python:1-3.11-bullseye`
- **Includes**: Python 3.11, pip, Streamlit, VS Code extensions (Python, Pylance)
- **Auto-install**: Dependencies from `requirements.txt` on container build

---

## AI Assistant Guidelines

### ✅ Do

- **Respect Streamlit patterns**: Use `st.slider()`, `st.chart()`, `@st.cache_data()` idioms
- **Enhance gradually**: Add new visualizations/features without breaking the spiral demo
- **Update requirements.txt**: List any new dependencies (keep minimal)
- **Test locally**: Run `streamlit run streamlit_app.py` before committing
- **Document changes**: Update this CLAUDE.md if adding new sections or conventions
- **Modularize code**: Extract reusable chart/data processing functions into separate Python files if the app grows beyond ~100 lines

### ❌ Don't

- **Break the spiral demo**: Keep `streamlit_app.py` functional; refactor without removing core visualization
- **Add heavy dependencies**: No complex ML frameworks, databases, or microservices without discussion
- **Hardcode secrets**: Never commit API keys, tokens, or credentials
- **Skip dev container testing**: Changes must work in both local and container environments
- **Ignore CI/CD**: Verify that image builds successfully before pushing to main
- **Change port 8501**: Streamlit port is hardcoded in configurations; changing requires updating all `.devcontainer/` files

### Development Workflow

1. **Branch**: Create feature branch from `main` (e.g., `feature/new-chart`)
2. **Local test**: Run app locally; verify slider interactions and chart rendering
3. **Update docs**: Add notes to CLAUDE.md if new patterns introduced
4. **Commit**: Clear message (e.g., "feat: add stock price dashboard widget")
5. **Push**: Triggers GitHub Actions; wait for dev container build to pass
6. **PR**: Create PR to `main`; include before/after screenshots of new features

---

## Known Limitations & Future Considerations

- **No database**: Currently stores no persistent data; suitable for real-time visualization only
- **Single user**: Streamlit is single-user by default; not suitable for multi-user dashboards without additional architecture
- **Deployment**: Not yet integrated with `hexstrike-ai` backend; awaiting API specification
- **Scalability**: Current spiral demo is O(n) performance; optimize data processing for large datasets when adding real data

---

## Useful Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run streamlit_app.py

# Build dev container locally (if Docker installed)
docker build -f .github/.devcontainer/Dockerfile -t ascended33:dev .

# Push to GHCR (requires REGISTRY_TOKEN secret)
git push origin main  # Triggers GitHub Actions workflow
```

---

## Links & References

- [Streamlit Docs](https://docs.streamlit.io)
- [Altair Documentation](https://altair-viz.github.io/)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [Dev Containers Spec](https://containers.dev/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Last Updated**: 2026-02-19  
**Maintained by**: Ascended33 Development Team  
**Related Project**: [hexstrike-ai](https://github.com/PositiveMike33/hexstrike-ai)
