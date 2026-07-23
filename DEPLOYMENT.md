# Deployment

Backend deploys to Railway (Dockerfile), frontend to Vercel. This doc covers
what's already prepared in the repo and the exact steps left for you to run
- account login, secrets, and the actual deploy trigger aren't something run
on your behalf here.

## Backend (Railway)

**Prepared:**
- `backend/Dockerfile` - builds and runs the FastAPI app. Verified locally
  with `docker build` + `docker run`: starts cleanly, `/health` returns
  `{"status":"healthy","agents_active":5,"rag_enabled":true}`.
- `backend/railway.toml` - points Railway at the Dockerfile build, sets a
  health check against `/health`.

**ChromaDB persistence - the decision this needed, made explicit:** the
`travel_knowledge` corpus (`backend/data/chroma`) is copied into the image
at build time (`COPY data ./data` in the Dockerfile), not left to a runtime
volume. Two reasons: Railway's free tier doesn't guarantee a persistent
volume across redeploys unless you explicitly attach one, and re-seeding the
corpus needs live Google Places API calls, which aren't being made right now
(expired credits). Bundling at build time means the corpus is always present
regardless of volume support - the tradeoff is that any *future* corpus
update requires a rebuild+redeploy, not just a running-container write. If
you later want live updates without redeploying, attach a Railway volume
mounted at `/app/data/chroma` instead and drop the `COPY data` line - that's
the stronger option, just not the one bundled today given the constraint.

**Env vars to set in the Railway dashboard** (Settings -> Variables), exact
names from `backend/app/core/config.py`:

| Variable | Required | Notes |
|---|---|---|
| `GROQ_API_KEY` | Yes | Agent reasoning (Llama 3.3 70B via Groq) |
| `GOOGLE_PLACES_API_KEY` | Yes | Live attraction search. Falls back to mock data if unset/invalid. |
| `GOOGLE_DIRECTIONS_API_KEY` | Optional | Not `GOOGLE_MAPS_API_KEY` - that's what the spec said, but the actual code reads this name |
| `OPENWEATHER_API_KEY` | Optional | Weather agent has a seasonal-forecast fallback |
| `SECRET_KEY` | Recommended | Defaults to a placeholder string, set a real one |
| `DATABASE_URL`, `REDIS_URL` | No | Declared in config.py with working defaults; nothing in the current agent code actually connects to a real DB/Redis instance |

**Steps (yours to run):**
```bash
npm install -g @railway/cli
railway login                    # opens a browser auth flow
cd backend
railway init                     # or `railway link` if a project already exists
railway up                       # builds from the Dockerfile and deploys
railway variables set GROQ_API_KEY=... GOOGLE_PLACES_API_KEY=...
```
Railway assigns a public URL after the first deploy - find it under the
service's "Settings -> Networking" or `railway domain`.

## Frontend (Vercel)

**Prepared:**
- `frontend/vercel.json` - SPA rewrite so client-side routes (react-router-dom)
  don't 404 on refresh.
- `frontend/.env.example` - documents `VITE_API_BASE_URL`.
- `frontend/src/pages/Home.jsx` now reads `import.meta.env.VITE_API_BASE_URL`
  instead of a hardcoded `http://localhost:8000`, falling back to localhost
  for local dev. Verified with `npm run build` - builds clean.

**Steps (yours to run):**
```bash
npm install -g vercel
cd frontend
vercel login
vercel                           # first run links/creates the project
vercel env add VITE_API_BASE_URL production   # paste the Railway backend URL
vercel --prod
```

## After both are live

1. Open the Vercel URL, submit a real trip request, confirm it reaches the
   Railway backend and returns an itinerary.
2. Update this repo's README: add the live demo URL at the top, replace
   "configured for local development" in the Current Status section.
