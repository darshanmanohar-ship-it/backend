# Synnovatify User API

A small **FastAPI** service that accepts user details and stores them in
**Supabase**. Designed to deploy on **Render** and be served from
`api.synnovatify.com`.

## Endpoints

| Method | Path         | Description                          |
|--------|--------------|--------------------------------------|
| GET    | `/`          | Service info                         |
| GET    | `/health`    | Health check (used by Render)        |
| POST   | `/api/users` | Create a user (saved to Supabase)    |
| GET    | `/api/users` | List recent users (newest first)     |

Interactive docs are available at `/docs` once running.

### Example request

```bash
curl -X POST https://api.synnovatify.com/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada Lovelace","email":"ada@example.com","phone":"+1-555-0100","message":"Hello"}'
```

## Project layout

```
app/
  __init__.py
  config.py     # env-driven settings (pydantic-settings)
  db.py         # cached Supabase client (service_role key)
  models.py     # UserCreate / UserRead schemas
  main.py       # FastAPI app + routes
requirements.txt
render.yaml       # Render blueprint
supabase_schema.sql
.env.example
```

## Local development

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in SUPABASE_URL and SUPABASE_SERVICE_KEY
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

---

## Deployment guide (do these 3 dashboard steps)

### 1. Supabase — create the project + table

1. Go to <https://supabase.com/dashboard> → **New project**.
2. Once ready, open **SQL Editor** → **New query**, paste the contents of
   [`supabase_schema.sql`](./supabase_schema.sql), and click **Run**.
3. Go to **Project Settings → API** and copy:
   - **Project URL** → this is `SUPABASE_URL`
   - **service_role** key (under *Project API keys*) → this is `SUPABASE_SERVICE_KEY`
     > Keep the service_role key secret — it bypasses row-level security.

### 2. Render — deploy the API

**Option A (Blueprint, recommended):**
1. Push this repo to GitHub (see below).
2. Go to <https://dashboard.render.com> → **New → Blueprint**, connect the repo.
   Render reads `render.yaml` automatically.
3. When prompted, set the two secret env vars:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
4. Click **Apply** / **Deploy**.

**Option B (manual Web Service):**
- New → **Web Service** → connect repo
- Runtime: **Python 3**
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`
- Add env vars: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_TABLE=users`,
  `CORS_ALLOW_ORIGINS=https://synnovatify.com,https://www.synnovatify.com`

After deploy, test the live URL Render gives you (e.g.
`https://synnovatify-user-api.onrender.com/health`).

### 3. Map the domain — `api.synnovatify.com`

1. In Render: your service → **Settings → Custom Domains → Add Custom Domain**
   → enter `api.synnovatify.com`. Render shows a target hostname like
   `synnovatify-user-api.onrender.com`.
2. In your DNS provider for **synnovatify.com**, add a record:

   | Type  | Name | Value                                   |
   |-------|------|-----------------------------------------|
   | CNAME | api  | `synnovatify-user-api.onrender.com`     |

3. Wait for DNS to propagate; Render auto-issues a TLS certificate.
   Your API is then live at `https://api.synnovatify.com`.

> Using a subdomain (`api.`) keeps your main website on the root domain
> untouched. Root domains can't use CNAME — a subdomain is the clean choice.

## Environment variables

| Variable                | Required | Default                                                       |
|-------------------------|----------|---------------------------------------------------------------|
| `SUPABASE_URL`          | yes      | —                                                             |
| `SUPABASE_SERVICE_KEY`  | yes      | —                                                             |
| `SUPABASE_TABLE`        | no       | `users`                                                       |
| `CORS_ALLOW_ORIGINS`    | no       | `https://synnovatify.com,https://www.synnovatify.com`         |
