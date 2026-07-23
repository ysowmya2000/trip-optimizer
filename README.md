# 🌍 TripOptimizer - AI-Powered Budget-Aware Travel Planner

An intelligent multi-agent system that creates personalized, budget-optimized travel itineraries using RAG (Retrieval-Augmented Generation), Google Places API, and advanced AI orchestration.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

TripOptimizer is a sophisticated AI travel planning system that creates optimal itineraries based on your budget, interests, and travel dates. Unlike generic trip planners, it intelligently adjusts the number of attractions per day based on your budget and destination cost of living.

### Key Features

- **💰 Budget-Aware Planning**: Automatically adjusts attractions (1-5 per day) based on your budget
- **🌍 City Cost Intelligence**: Knows the cost of living in 90+ cities worldwide
- **💱 Multi-Currency Support**: Works with 49+ currencies with real-time conversion
- **📅 Seasonal Weather**: Provides season-specific packing advice for travel dates
- **🗺️ Route Optimization**: Uses TSP algorithm to minimize travel time between attractions
- **🎨 Smart Scheduling**: Places attractions at optimal times (morning gardens, evening viewpoints)
- **✅ Budget Validation**: Rejects trips with insufficient budget and suggests minimum required

## 🏗️ System Architecture

### Multi-Agent System

TripOptimizer uses 5 specialized AI agents coordinated by an orchestrator:
```
┌─────────────────────────────────────────────────────────┐
│                    Trip Orchestrator                     │
│         (Coordinates all agents & manages flow)          │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Research   │    │   Planning   │    │ Optimization │
│    Agent     │───▶│    Agent     │───▶│    Agent     │
└──────────────┘    └──────────────┘    └──────────────┘
                            │
                    ┌───────┴────────┐
                    ▼                ▼
            ┌──────────────┐  ┌──────────────┐
            │    Budget    │  │   Weather    │
            │    Agent     │  │    Agent     │
            └──────────────┘  └──────────────┘
```

### Agent Responsibilities

#### 1. **Research Agent** 🔍
- **Purpose**: Discovers attractions using RAG + Google Places API
- **Capabilities**:
  - Hybrid retrieval (BM25 keyword search + ChromaDB semantic search, fused
    with Reciprocal Rank Fusion) over the local knowledge base, reranked with
    a cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) - a standard
    two-stage retrieval pattern: retrieve broad with hybrid search, rerank
    precise with a cross-encoder. See [Evaluation Results](#-evaluation-results)
    for before/after retrieval numbers.
  - Fetches top-rated attractions from Google Places
  - Combines RAG results with live API data
  - Selects `trip_duration × 5` attractions for variety
- **Output**: Curated list of attractions with ratings, coordinates, prices

#### 2. **Planning Agent** 📅
- **Purpose**: Creates day-by-day itineraries with budget awareness
- **Capabilities**:
  - Calculates optimal attractions per day based on budget
  - Uses city cost multipliers (Bangkok ×0.4, Paris ×1.5, etc.)
  - Categorizes attractions by best time (morning/evening/night)
  - Creates 7-slot daily schedule (9 AM - 11 PM)
  - Estimates costs with city-adjusted pricing
- **Budget Tiers**:
  - **Ultra Budget**: 1 attraction/day, street food
  - **Budget**: 2 attractions/day, casual cafes
  - **Standard**: 3 attractions/day, local restaurants
  - **Comfortable**: 4 attractions/day, nice restaurants
  - **Luxury**: 5 attractions/day, fine dining
- **Output**: Complete itinerary with activities, times, costs

#### 3. **Optimization Agent** 🎯
- **Purpose**: Analyzes itinerary efficiency
- **Capabilities**:
  - Calculates total travel distance using Haversine formula
  - Estimates time savings from route optimization
  - Provides efficiency metrics
- **Note**: Does NOT reorder attractions (preserves time-based scheduling)
- **Output**: Optimization statistics and metrics

#### 4. **Budget Agent** 💰
- **Purpose**: Analyzes costs and provides budget status
- **Capabilities**:
  - Converts costs between currencies
  - Compares trip cost vs user budget
  - Calculates over/under budget amounts
  - Provides dual currency display
- **Output**: Budget analysis with status (under/on/over budget)

#### 5. **Weather Agent** 🌤️
- **Purpose**: Provides seasonal weather forecasts
- **Capabilities**:
  - Knows seasonal patterns for major cities
  - Provides temperature ranges and conditions
  - Gives packing advice based on season
- **Coverage**: Bangkok, Paris, London, Tokyo (expandable)
- **Output**: Seasonal forecast with packing recommendations

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104
- **AI/ML**: 
  - Groq API (Llama 3.3 70B) for agent intelligence
  - ChromaDB for vector database & RAG
  - Hybrid retrieval: BM25 (`rank_bm25`) + semantic search, fused with
    Reciprocal Rank Fusion, reranked with a cross-encoder
    (`cross-encoder/ms-marco-MiniLM-L-6-v2` via `sentence-transformers`)
- **APIs**:
  - Google Places API (attraction discovery)
  - Google Maps API (route visualization)
- **Language**: Python 3.12
- **Key Libraries**:
  - `chromadb` - Vector database
  - `rank_bm25` - Keyword retrieval
  - `groq` - LLM API client
  - `pydantic` - Data validation
  - `httpx` - Async HTTP client

### Frontend
- **Framework**: React 18.3 + Vite
- **Styling**: Tailwind CSS 3.4
- **UI Components**: 
  - Lucide React (icons)
  - Recharts (budget visualization)
  - @react-google-maps/api (maps)
- **Routing**: React Router DOM 6.22

### Infrastructure
- **Vector DB**: ChromaDB (local persistent storage)
- **Algorithms**: TSP optimization, Haversine distance
- **Deployment**: Netlify (frontend) + Render (backend)

## 🚀 Getting Started

### Prerequisites
```bash
# Required
- Python 3.12+
- Node.js 18+
- npm or yarn

# API Keys Needed
- Groq API Key (free tier available)
- Google Places API Key
- Google Maps API Key
```

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/ysowmya2000/trip-optimizer.git
cd trip-optimizer
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_PLACES_API_KEY=your_google_places_key_here
EOF

# Initialize ChromaDB (first time only)
python -c "from app.db.vector_store import travel_kb; print('✅ ChromaDB initialized')"
```

#### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# No .env needed (API keys handled by backend)
```

### Running the Application

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

**Access**: http://localhost:5173

## 💡 How It Works

### Example: Bangkok 5 Days with ₹50,000 INR

1. **User Input**:
   - Destination: Bangkok
   - Duration: 5 days
   - Budget: ₹50,000 INR
   - Currency: Indian Rupee
   - Interests: Culture, Food, Nature
   - Start Date: March 20, 2026

2. **Backend Processing**:

   **Step 1: Budget Validation**
   - Converts ₹50,000 → $601 USD
   - Checks minimum: Bangkok needs ~$160 for 5 days
   - ✅ Budget sufficient

   **Step 2: City Cost Analysis**
   - Bangkok multiplier: ×0.4 (very affordable)
   - Daily budget: $601 ÷ 5 = $120/day
   - With ×0.4 multiplier: effectively $300/day purchasing power
   - **Tier**: Comfortable (4 attractions/day)

   **Step 3: Research (RAG + Google Places)**
   - Queries ChromaDB: "temples, street food, parks in Bangkok"
   - Fetches Google Places: Top-rated attractions
   - Combines: 25 attractions total
   - Examples: Wat Pho, Grand Palace, Chatuchak Market, etc.

   **Step 4: Planning**
   - Creates 5 days × 4 attractions = 20 activities
   - Categorizes by time:
     - Morning: Wat Pho (temple, cooler hours)
     - Afternoon: Grand Palace, Jim Thompson House
     - Evening: Asiatique (riverside, sunset)
     - Night: Khao San Road (nightlife)
   - Estimates costs:
     - Meals: $35/day (× 0.4 = $14/day actual)
     - Attractions: 4 × $30 = $120 (× 0.4 = $48 actual)
     - Transport: $10 (× 0.4 = $4 actual)
     - **Daily**: ~$66 USD = ₹5,488 INR
     - **Total**: ~$330 USD = ₹27,436 INR

   **Step 5: Optimization**
   - Calculates distances between attractions
   - Estimates 300 min time saved vs random order

   **Step 6: Budget Analysis**
   - Trip cost: ₹27,436 INR
   - Your budget: ₹50,000 INR
   - **Status**: ✅ Under budget by ₹22,564

   **Step 7: Weather**
   - March in Bangkok: Hot Season
   - Temperature: 28-35°C
   - Advice: Pack light, breathable clothes. Stay hydrated.

3. **Frontend Display**:
```
   Budget: ₹50,000 INR
   Trip Cost: ₹27,436 INR (≈ ฿11,820 THB)
   ✅ Under Budget

   Day 1: 4 attractions (₹5,487 INR)
   - 9:00 AM: Wat Pho
   - 12:00 PM: Lunch
   - 1:30 PM: Grand Palace
   - 4:00 PM: Jim Thompson House
   - 7:00 PM: Dinner
   - 8:30 PM: Asiatique

   Weather: Hot Season • 28-35°C
   Pack: Light clothes, sunscreen
```

### Budget Comparison: Same Budget, Different Cities

| City | Budget | Multiplier | Tier | Attractions/Day | Total Cost |
|------|--------|------------|------|----------------|------------|
| Bangkok | ₹50,000 | ×0.4 | Comfortable | 4 | ₹27,436 ✅ |
| Prague | ₹50,000 | ×0.8 | Standard | 3 | ₹45,200 ✅ |
| Paris | ₹50,000 | ×1.5 | Budget | 2 | ₹48,900 ✅ |
| London | ₹50,000 | ×1.6 | Budget | 1-2 | ₹51,200 ⚠️ |

## 📊 City Cost Database

### Expensive Cities (×1.4 - ×1.8)
- Paris (×1.5), London (×1.6), Tokyo (×1.7)
- Zurich (×1.8), Geneva (×1.7), Dubai (×1.8)
- Singapore (×1.4), Hong Kong (×1.5), Sydney (×1.5)

### Moderate Cities (×0.8 - ×1.2)
- Barcelona (×1.1), Madrid (×1.0), Rome (×1.1)
- Prague (×0.8), Budapest (×0.7), Lisbon (×0.9)
- Seoul (×1.0), Taipei (×0.9), Shanghai (×1.0)

### Budget-Friendly Cities (×0.3 - ×0.7)
- Bangkok (×0.4), Bali (×0.3), Hanoi (×0.4)
- Mumbai (×0.4), Delhi (×0.4), Manila (×0.5)
- Mexico City (×0.5), Lima (×0.5), Cairo (×0.4)

**Total**: 90+ cities with cost data

## 💱 Supported Currencies

49 currencies including:
- 🇺🇸 USD, 🇪🇺 EUR, 🇬🇧 GBP, 🇯🇵 JPY, 🇮🇳 INR
- 🇦🇺 AUD, 🇨🇦 CAD, 🇨🇭 CHF, 🇨🇳 CNY, 🇸🇬 SGD
- 🇹🇭 THB, 🇻🇳 VND, 🇮🇩 IDR, 🇲🇾 MYR, 🇵🇭 PHP
- And 34 more...

## 🎨 Features Showcase

### 1. Budget Validation
```
User enters ₹10,000 for 5-day Bangkok trip
❌ "Budget too low! Minimum needed: ₹21,000 INR"
```

### 2. Dual Currency Display
```
Your Budget: ₹50,000 INR
Trip Cost: ₹27,436 INR (≈ ฿11,820 THB)
Day 1: ₹5,487 INR (≈ ฿2,364 THB)
```

### 3. Seasonal Weather
```
Season: Hot Season (March)
Temperature: 28-35°C
Condition: Hot & Humid
What to Pack: Light, breathable clothes. Stay hydrated.
```

### 4. Smart Time Scheduling
```
9:00 AM  - Temple (cooler morning hours)
12:00 PM - Lunch
4:00 PM  - Museum (afternoon)
7:00 PM  - Dinner
8:30 PM  - Rooftop bar (sunset/evening)
10:00 PM - Night market (nightlife)
```

## 📁 Project Structure
```
trip-optimizer/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── research_agent.py      # RAG + Google Places
│   │   │   ├── planning_agent.py      # Budget-aware scheduling
│   │   │   ├── optimization_agent.py  # Route optimization
│   │   │   ├── budget_agent.py        # Cost analysis
│   │   │   ├── weather_agent.py       # Seasonal forecasts
│   │   │   └── orchestrator.py        # Agent coordination
│   │   ├── api/
│   │   │   └── trips.py               # FastAPI endpoints
│   │   ├── db/
│   │   │   └── vector_store.py        # ChromaDB setup
│   │   ├── schemas/
│   │   │   └── trip.py                # Pydantic models
│   │   ├── utils/
│   │   │   ├── budget_calculator.py   # Budget tier logic
│   │   │   ├── city_costs.py          # City multipliers
│   │   │   └── currency_converter.py  # Currency conversion
│   │   └── main.py                    # FastAPI app
│   ├── data/
│   │   └── chroma/                    # ChromaDB storage
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx               # Trip input form
│   │   │   └── Results.jsx            # Itinerary display
│   │   ├── components/
│   │   │   ├── TripMap.jsx            # Google Maps
│   │   │   ├── BudgetChart.jsx        # Cost visualization
│   │   │   ├── DestinationHero.jsx    # Hero section
│   │   │   └── ProTips.jsx            # Travel tips
│   │   └── App.jsx
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## 🔧 API Endpoints

### POST `/api/trips/create`

**Request**:
```json
{
  "destination": "Bangkok",
  "trip_duration": 5,
  "budget": 50000,
  "currency": "INR",
  "interests": ["culture", "food", "nature"],
  "start_date": "2026-03-20"
}
```

**Response**:
```json
{
  "success": true,
  "itinerary": {
    "destination": "Bangkok",
    "trip_duration": 5,
    "days": [...],
    "estimated_total_cost": 27436.50
  },
  "budget_analysis": {
    "user_budget": 50000,
    "estimated_cost_user": 27436.50,
    "status": "under_budget"
  },
  "weather_forecast": {
    "season": "Hot Season",
    "temperature": "28-35°C"
  },
  "currency_info": {
    "user_currency": "INR",
    "destination_currency": "THB"
  }
}
```

## 🧪 Testing

Automated eval harness: `backend/eval/` (see
[Evaluation Results](#-evaluation-results) above). Run with
`python -m eval.run_budget_eval`, `run_quality_eval`, or `run_retrieval_eval
--mode {semantic,hybrid,reranked}` from `backend/`.

### Manual Testing Scenarios

1. **Budget Rejection**:
   - Bangkok, 5 days, ₹10,000 → Should reject with minimum amount

2. **Budget Tiers**:
   - Bangkok, 5 days, ₹25,000 → 2 attractions/day
   - Bangkok, 5 days, ₹50,000 → 4 attractions/day
   - Bangkok, 5 days, ₹2,00,000 → 5 attractions/day

3. **City Costs**:
   - Same budget (₹50,000) should give:
     - Bangkok: 4 attractions/day (cheap)
     - Prague: 3 attractions/day (moderate)
     - Paris: 1-2 attractions/day (expensive)

4. **Seasonal Weather**:
   - Bangkok March → Hot Season
   - Paris March → Spring
   - London December → Winter

## 📊 Evaluation Results

Quantitative eval harness in `backend/eval/`, run against the real agent
pipeline (not a mocked simplification) - see `backend/eval/results/` for the
full per-case JSON reports.

### Budget / Tier Accuracy

44 synthetic test cases spanning the three city-cost tiers (expensive,
moderate, budget) and budget levels, including boundary cases at tier
cutoffs. Expected values are computed directly from `budget_calculator`'s
actual logic, not hand-guessed.

| Metric | Score |
|---|---|
| Tier assignment accuracy | 100% |
| Attractions-per-day accuracy | 100% |
| Budget status accuracy | 0%* |
| Cost estimate mean deviation | 25.7% (n=11 hand-verified subset) |

\* This isn't a harness bug - it's a real finding. `planning_agent`'s actual
cost formula runs 25-40% cheaper than the tier-selection formula in
`budget_calculator` predicts, so the pipeline reports "under budget" far
more often than the tier math alone would suggest. The two formulas were
never reconciled with each other; the eval surfaced the gap rather than
papering over it.

### Itinerary Quality

Three rule-based dimensions scored per generated itinerary (44 cases):

| Dimension | Score |
|---|---|
| Time-slot appropriateness | 97.4/100 |
| Attraction diversity | 57.7/100 |
| Interest-match rate | 100/100** |

\*\* Sitting flat at 100 reflects a real methodology limit worth naming: the
interest-to-category keyword map is broad enough (e.g. "sightseeing" maps to
generic Places types like `point_of_interest`) that most attractions
trivially match, so this metric currently has weak discriminative power.

### RAG Retrieval: Semantic → Hybrid → Reranked

20 manually labeled queries (ground truth = real ChromaDB corpus documents
tagged with matching destination+category, not LLM-generated labels).
Precision@5 at each stage of the retrieval pipeline:

| Stage | Precision@5 |
|---|---|
| Semantic search only (baseline) | 0.89 |
| + BM25 hybrid (RRF fusion, no rerank) | 0.89 |
| + Cross-encoder reranking | 1.00 |

Adding hybrid retrieval on its own didn't move the needle - Reciprocal Rank
Fusion just re-orders two already-decent rankings without adding new
judgment. The cross-encoder reranker is what closed the gap: it scores each
(query, candidate) pair directly instead of aggregating rank positions, and
that's what fixed cases like "temples in Bangkok," where the semantic-only
baseline mixed in a Hanoi temple and an unrelated Bangkok nightlife bar.
Ground truth here is coarse (destination+category match, not a strict top-5
ranking), so a perfect reranked score reflects a well-separated corpus at
that granularity, not that ranking within a category is fully solved.

**Note on the live deployment:** the numbers above measure the full
hybrid+reranked pipeline as implemented. The deployed instance runs with
reranking disabled (`ENABLE_RERANKING=false`) because the reranker's
PyTorch dependency pushed the container over Render's free-tier memory
limit - see `DEPLOYMENT.md` for the full investigation. The live demo
therefore reflects hybrid retrieval without reranking (0.89 precision@5),
not the 1.00 figure above.

## 🚀 Deployment

### Current Status

Deployment artifacts are prepared and locally verified but **not yet live**:
a `backend/Dockerfile` builds and runs cleanly (`docker build` + `docker run`
tested locally, `/health` returns healthy with the RAG corpus loaded), and
the frontend no longer hardcodes `localhost:8000` - it reads
`VITE_API_BASE_URL`. See [`DEPLOYMENT.md`](./DEPLOYMENT.md) for the full env
var checklist and exact deploy commands. Going live requires account setup
on Render/Netlify and pasting in API keys, which are manual steps.

### Deployment Plan

- **Frontend**: Netlify (`frontend/netlify.toml` prepared for build + SPA routing)
- **Backend**: Render, via the Dockerfile (`render.yaml` Blueprint prepared)
- **ChromaDB persistence**: bundled into the backend image at build time
  rather than a runtime disk (Render's free plan doesn't include one) -
  see `DEPLOYMENT.md` for why.

Originally targeted Railway + Vercel per the spec; switched to Render +
Netlify after both hit expired free-trial billing during setup.

## 📈 Future Enhancements

- [ ] Flight booking integration
- [ ] Hotel recommendations
- [ ] Multi-city trips
- [ ] Collaborative planning (share with friends)
- [ ] Real-time pricing updates
- [ ] Premium experiences for high budgets
- [ ] Visa requirement checker
- [ ] Travel insurance recommendations
- [ ] Local SIM card suggestions
- [ ] Restaurant reservations

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Sowmya Yerraguntla**

- LinkedIn: [Sowmya Yerraguntla](https://www.linkedin.com/in/sowmyayerraguntla/)

## 📊 Project Stats

- **Lines of Code**: ~8,000+
- **Agents**: 5 specialized AI agents
- **Cities Supported**: 90+
- **Currencies**: 49
- **API Integrations**: 3 (Groq, Google Places, Google Maps)
- **Development Time**: 4 weeks

---

**Built with ❤️ for travelers who want to maximize experiences within their budget**
