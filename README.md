# Todo List App (Python + Vue)

Modern, dark-mode-first To Do List web app with full **CRUD** for tasks (description + deadline).

## Features

- **Task CRUD**: create, read (list), update, delete
- **Fields**: description + deadline (date/time)
- **Dark mode first** + toggle (persisted in browser)
- **Responsive UI**: works well on mobile + desktop

## Tech stack

- **Frontend**: Vue 3 + Vite + Tailwind CSS
- **Backend**: FastAPI + SQLModel (SQLite locally, Postgres-ready for hosting)

---

## Local development

### Prerequisites

- **Node.js**: 18+ recommended
- **Python**: 3.11+ recommended

### Backend (FastAPI)

From the repo root:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Create a local env file:

- Copy `backend/env.example` to `backend/.env`
- Keep default `DATABASE_URL=sqlite:///./todo.db`

Run the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Apply database migrations (Alembic):

```bash
alembic upgrade head
```

API will be at `http://localhost:8000`.

### Frontend (Vue)

From the repo root:

```bash
cd frontend
npm install
```

Create a local env file:

- Copy `frontend/env.example` to `frontend/.env`
- Ensure:
  - `VITE_API_BASE_URL=http://localhost:8000`

Run the web app:

```bash
npm run dev
```

Open the app at `http://localhost:5173`.

---

## API endpoints

- `GET /health` → health check
- `GET /tasks` → list tasks (sorted by deadline ascending)
- `POST /tasks` → create task
- `GET /tasks/{id}` → get one task
- `PUT /tasks/{id}` → update task
- `DELETE /tasks/{id}` → delete task

### Task JSON shape

```json
{
  "id": 1,
  "description": "Pay rent",
  "deadline": "2026-01-30T18:00:00.000Z",
  "created_at": "2026-01-21T09:30:00.000Z",
  "updated_at": "2026-01-21T09:30:00.000Z"
}
```

---

## Deploy online (free hosting)

Recommended free stack:

- **Database**: Supabase (free Postgres)
- **Backend**: Render (free web service)
- **Frontend**: Netlify (free static hosting)

### 1) Create a free Postgres database (Supabase)

1. Create a project in Supabase.
2. Copy the **connection string** (it looks like `postgresql://...`).
3. Make sure SSL is enabled. If the string doesn’t include it, append:
   - `?sslmode=require`

You’ll use this as `DATABASE_URL` on Render.

### 2) Deploy the backend (Render)

1. Push this repo to GitHub.
2. In Render, create a **New Web Service** from your GitHub repo.
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**:
     - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables:
   - **DATABASE_URL**: your Supabase connection string
   - **FRONTEND_ORIGIN**: your Netlify site URL (example: `https://your-site.netlify.app`)
5. Deploy.

After deploy, note your backend URL (example: `https://your-backend.onrender.com`).

### 3) Deploy the frontend (Netlify)

This repo includes `frontend/netlify.toml` so Netlify builds the Vue app correctly.

1. In Netlify, create a **New site from Git**.
2. Select this repo.
3. Set environment variables:
   - **VITE_API_BASE_URL**: your Render backend URL (example: `https://your-backend.onrender.com`)
4. Deploy.

### 4) Final CORS check

If the web app can’t call the API in production, re-check:

- Netlify env var `VITE_API_BASE_URL` is correct
- Render env var `FRONTEND_ORIGIN` matches your Netlify URL exactly

---

## Notes

- Local dev uses SQLite (`backend/todo.db`). Production hosting should use Postgres (Supabase) so data persists reliably.

