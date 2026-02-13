# TripOptimizer

AI-powered travel itinerary planner with real-time optimization using multi-agent systems.

## Features
- Multi-agent AI system for intelligent trip planning
- Real-time itinerary adaptation (weather, budget, energy)
- Constraint optimization for best travel experience
- Integration with Google Places, Weather APIs

## Tech Stack
- **Backend**: FastAPI, LangGraph, LangChain
- **AI/ML**: OpenAI GPT-4, Multi-agent orchestration
- **Database**: SQLite (dev), PostgreSQL (production)
- **APIs**: Google Places, Google Directions, OpenWeather

## Setup (Mac)

### Prerequisites
- Python 3.12
- Git

### Installation

1. Clone repository:
```bash
git clone https://github.com/YOUR_USERNAME/trip-optimizer.git
cd trip-optimizer
```

2. Create virtual environment:
```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. Run the server:
```bash
python -m uvicorn app.main:app --reload
```

## Development Status
🚧 Currently in development

## Project Structure
```
trip-optimizer/
├── backend/
│   ├── app/
│   │   ├── agents/       # Multi-agent system
│   │   ├── api/          # FastAPI endpoints
│   │   ├── core/         # Core logic
│   │   ├── db/           # Database models
│   │   ├── external/     # External API wrappers
│   │   └── schemas/      # Pydantic models
│   └── tests/
└── README.md
```

## Author
Sowmya Yerraguntla - Columbia University MS Data Science

## License
MIT
