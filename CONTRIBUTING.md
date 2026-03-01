# Contributing to iVDrive

Thank you for your interest in contributing to iVDrive. Most users [use iVDrive online](https://ivdrive.eu) — no setup required. This guide is for anyone who wants to contribute code, docs, or run the stack locally (e.g. for development or self-hosting).

## How to contribute

- Report bugs and issues
- Suggest new features or improvements
- Improve documentation
- Submit code changes and fixes
- Test the application and report feedback

## Quick start

### 1. Fork and clone

```bash
git clone https://github.com/YOUR_USERNAME/iVDrive.git
cd iVDrive

git remote add upstream https://github.com/m7xlab/iVDrive.git
```

### 2. Set up your environment

- Copy `.env.example` to `.env` and set the required variables (see [.env.example](.env.example)):
  - `POSTGRES_PASSWORD`, `VALKEY_PASSWORD`, `JWT_SECRET_KEY`, `ENCRYPTION_KEY`
  - For local dev, `CORS_ORIGINS` can stay as `["http://localhost:3000"]` or include your frontend origin.

### 3. Create a branch

```bash
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b fix/your-bug-description
```

## Development setup

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- (Optional) Node.js and npm for frontend-only work; Python 3.12+ for backend-only work

### Run the stack

```bash
docker compose up -d
```

- Web UI: http://localhost:3035 (or the port mapped in `docker-compose.yml`)
- API: http://localhost:8000
- API docs: http://localhost:8000/docs

### Frontend (optional local dev)

```bash
cd frontend
npm install
npm run dev
```

Use the same `.env` (or set `NEXT_PUBLIC_API_URL` if the API runs elsewhere).

### Backend (optional local dev)

Use a virtual environment, install from `backend/requirements.txt`, and point `DATABASE_URL` and `VALKEY_URL` to your running Postgres and Valkey (e.g. from Docker).

## Contribution guidelines

### Code style

- **Python**: Prefer [Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/) for formatting and imports. Follow [PEP 8](https://peps.python.org/pep-0008/) where applicable.
- **Frontend (TypeScript/React)**: Match existing style; use the project’s lint/format setup if present.

### Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): short description

[optional body]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**

- `feat(api): add endpoint for charging history`
- `fix(frontend): correct trip chart date range`
- `docs: update getting started for Docker`

### Pull requests

1. Keep PRs focused — one feature or fix per PR.
2. Use the [pull request template](.github/pull_request_template.md): fill in the summary and check at least one “Type of change”.
3. Ensure the backend runs and any existing tests pass; the frontend builds (e.g. `npm run build` in `frontend/`).
4. Update documentation if you change behaviour or add options.

### Security

Do **not** report security vulnerabilities in public issues or PRs. See [SECURITY.md](SECURITY.md) for how to report them privately.

## Bug reports

When opening an issue for a bug, please include:

- A clear description of the problem
- Steps to reproduce
- What you expected vs what actually happened
- Your environment (OS, Docker version, how you run iVDrive)
- Relevant logs or screenshots if helpful

## Feature requests

For feature ideas:

- Describe the feature and the use case
- Explain why it would help you or other users
- Optionally, outline a possible implementation

## Getting help

- Open a [GitHub Discussion](https://github.com/m7xlab/iVDrive/discussions) for questions.
- Use [GitHub Issues](https://github.com/m7xlab/iVDrive/issues) for bugs and feature requests.

Thank you for contributing to iVDrive.
