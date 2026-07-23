# Deployment

Backend deploys to Render (Dockerfile), frontend to Netlify. This doc covers
what's already prepared in the repo and the exact steps left for you to run
- account login, secrets, and the actual deploy trigger aren't something run
on your behalf here.

(Originally targeted Railway + Vercel, per the spec's "Railway or Render" /
Vercel options - switched after both of those hit expired free-trial
billing during setup. Render + Netlify don't require a paid trial to start.)

## Backend (Render)

**Prepared:**
- `backend/Dockerfile` - builds and runs the FastAPI app. Verified locally
  with `docker build` + `docker run`: starts cleanly, `/health` returns
  `{"status":"healthy","agents_active":5,"rag_enabled":true}`.
- `render.yaml` (repo root) - a Render "Blueprint" that points at the
  Dockerfile, sets the free plan, and declares the env vars below as
  `sync: false` (meaning Render will prompt you to fill them in rather than
  expecting a value in the file - so no secrets live in git).

**ChromaDB persistence - the decision this needed, made explicit:** the
`travel_knowledge` corpus (`backend/data/chroma`) is copied into the image
at build time (`COPY data ./data` in the Dockerfile), not left to a runtime
volume/disk. Render's free web service plan doesn't include a persistent
disk at all (that's a paid-plan feature), and re-seeding the corpus needs
live Google Places API calls, which aren't being made right now (expired
credits). Bundling at build time sidesteps both constraints - the tradeoff
is that any *future* corpus update requires a rebuild+redeploy, not just a
running-container write. If you later upgrade to a paid Render plan and want
live updates without redeploying, attach a persistent disk mounted at
`/app/data/chroma` instead and drop the `COPY data` line.

**Env vars to set** (Render will prompt for these on first deploy from the
Blueprint, or set them under the service's Environment tab), exact names
from `backend/app/core/config.py`:

| Variable | Required | Notes |
|---|---|---|
| `GROQ_API_KEY` | Yes | Agent reasoning (Llama 3.3 70B via Groq) |
| `GOOGLE_PLACES_API_KEY` | Yes | Live attraction search. Falls back to mock data if unset/invalid. |
| `GOOGLE_DIRECTIONS_API_KEY` | Optional | Not `GOOGLE_MAPS_API_KEY` - that's what the spec said, but the actual code reads this name |
| `OPENWEATHER_API_KEY` | Optional | Weather agent has a seasonal-forecast fallback |
| `SECRET_KEY` | Auto-generated | `render.yaml` sets `generateValue: true`, Render creates one |
| `DATABASE_URL`, `REDIS_URL` | No | Declared in config.py with working defaults; nothing in the current agent code actually connects to a real DB/Redis instance |

**Steps (yours to run - Render deploys via GitHub connection + dashboard,
there's no CLI push flow like Railway's):**
1. Go to [dashboard.render.com](https://dashboard.render.com) and sign in
   (or create an account - free, no trial/card required for the free plan).
2. **New +** -> **Blueprint** -> connect the `ysowmya2000/trip-optimizer`
   GitHub repo. Render reads `render.yaml` automatically and proposes the
   `trip-optimizer-backend` service.
3. Fill in `GROQ_API_KEY` and `GOOGLE_PLACES_API_KEY` when prompted (the
   other two are optional, leave blank to skip).
4. Deploy. First build takes a few minutes (installs `torch`,
   `sentence-transformers`, etc.). Render assigns a public URL like
   `https://trip-optimizer-backend.onrender.com`.

**Free-tier tradeoff to know about:** Render's free web services spin down
after ~15 minutes of inactivity and cold-start (30s-1min) on the next
request. Fine for a demo/portfolio link, not for anything needing instant
response after idle time.

## Frontend (Netlify)

**Prepared:**
- `frontend/netlify.toml` - build command, publish directory, and an SPA
  redirect rule so client-side routes (react-router-dom) don't 404 on
  refresh.
- `frontend/.env.example` - documents `VITE_API_BASE_URL`.
- `frontend/src/pages/Home.jsx` now reads `import.meta.env.VITE_API_BASE_URL`
  instead of a hardcoded `http://localhost:8000`, falling back to localhost
  for local dev. Verified with `npm run build` - builds clean.

**Steps (yours to run):**
```bash
npm install -g netlify-cli    # already installed in this environment
cd frontend
netlify login                 # opens a browser auth flow
netlify init                  # links/creates the site, reads netlify.toml
netlify env:set VITE_API_BASE_URL https://trip-optimizer-backend.onrender.com
netlify deploy --prod
```
Netlify assigns a URL like `https://<site-name>.netlify.app` - find it in
the CLI output after `--prod`, or in the Netlify dashboard.

## After both are live

1. Open the Netlify URL, submit a real trip request, confirm it reaches the
   Render backend and returns an itinerary (allow for the cold-start delay
   if the backend has been idle).
2. Update this repo's README: add the live demo URL at the top, replace
   "configured for local development" in the Current Status section.
