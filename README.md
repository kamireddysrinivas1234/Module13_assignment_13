# FastAPI JWT Auth + Frontend + Playwright E2E + Pytest + Docker/CI

Includes:
- JWT auth endpoints: **POST /register**, **POST /login**
- Frontend pages: `/static/register.html`, `/static/login.html`
- Playwright E2E tests: `tests/e2e/*`
- Pytest API + unit tests: `tests/pytest/*`
- Docker Compose (Postgres + API)
- GitHub Actions CI: runs **pytest** + **Playwright**, then (on `main`) pushes to Docker Hub.

---

## Local run (VS Code) — SQLite
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:
Register: http://127.0.0.1:8000/static/register.html
Login: http://127.0.0.1:8000/static/login.html
API docs: http://127.0.0.1:8000/docs
Health: http://127.0.0.1:8000/health
---

## Run Pytest
```bash
pytest -q
```

(optional coverage)
```bash
pytest --cov=app --cov-report=term-missing
```

---

## Run Playwright E2E
Install Node.js LTS first.

```bash
npm install
npx playwright install
```

Start the API (uvicorn or docker compose), then:
```bash
npm run e2e
```

---

## Docker run (Postgres + API)
If your machine uses port 5432 already, Postgres is mapped to **55432** on host:
```bash
docker compose up --build
```

---

## CI/CD + Docker Hub
Workflow: `.github/workflows/ci.yml`

GitHub Secrets needed for pushing on `main`:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Docker Hub repo link (fill yours):
https://hub.docker.com/r/srinivaskamireddy/jwt-auth-fastapi-playwright


## If you see `ModuleNotFoundError: No module named 'app'`
Make sure you are running pytest from the **project root** (the folder that contains `app/`).

Use:
```bash
python -m pytest -q
```

For coverage:
```bash
python -m pytest --cov=app --cov-report=term-missing
```

```bash
python -m pytest
```

To see the detailed report:
```bash
python -m pytest --cov=app --cov-report=term-missing
```
