# ⚖️ LegalSarthi

**AI-Powered Legal Guidance for Indian Citizens**

Describe your legal situation — a police officer demanding a bribe, a landlord illegally evicting you, an online scam — and get step-by-step guidance with relevant Indian laws cited. Powered by Google Gemini with a curated rules engine for grounding.

---

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | React 18, Vite, Tailwind CSS, Axios |
| Backend   | FastAPI, Python 3.10+               |
| Database  | MongoDB (Motor async driver)        |
| AI        | Google Gemini 2.5 Flash Lite        |
| Auth      | JWT (HS256, 24-hour tokens)         |
| Deploy    | Vercel (experimentalServices)       |

---

## Architecture

```
User Message
      │
      ▼
┌─────────────────────────┐
│   FastAPI Backend        │
│   JWT Auth Required      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Rules Engine           │  Keyword scoring against 30+ curated rules
│   (always runs first)    │  Returns top-3 matched rules (or empty list)
└────────────┬────────────┘
             │  Matched rules injected as RAG context
             ▼
┌─────────────────────────┐
│   Gemini AI              │  Always called — rules used as grounding context
│   gemini-2.5-flash-lite  │  Prompt: system instructions + rules + user message
│   (+ fallback chain)     │  Responds with structured JSON
└────────────┬────────────┘
             │  If Gemini fails → mock response with NALSA helpline
             ▼
┌─────────────────────────┐
│   Structured Response    │
│   {category, summary,    │
│    steps, laws, source}  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   MongoDB                │  Saves conversation, user message, AI response
└─────────────────────────┘
```

The rules engine and Gemini work together — rules provide deterministic legal grounding, Gemini personalizes the response to the user's specific situation. Every response comes from Gemini; the source badge on each reply indicates whether matching rules were found (`gemini_ai`) or not.

---

## Legal Categories Covered

| Category    | Topics                                               |
|-------------|------------------------------------------------------|
| Police      | Bribery, FIR refusal, illegal detention/arrest       |
| Consumer    | Defective products, refunds, consumer fraud          |
| Property    | Illegal eviction, security deposit, tenant rights    |
| Workplace   | Harassment, POSH Act, wrongful termination           |
| Cyber       | Online fraud, hacking, identity theft, cyberbullying |
| Domestic    | Domestic violence, dowry harassment                  |
| Environment | Noise pollution, neighbourhood disturbance           |
| RTI         | Right to Information applications                    |

---

## Project Structure

```
LegalSarthi/
├── backend/          # FastAPI app
│   ├── app/
│   │   ├── core/     # Config, database, security (JWT)
│   │   ├── data/     # Curated legal rules database
│   │   ├── models/   # Pydantic schemas
│   │   ├── routers/  # auth, chat, health endpoints
│   │   └── services/ # Rules engine, AI advisor, chat orchestration
│   ├── .env.example
│   └── requirements.txt
├── frontend/         # React + Vite app
│   ├── src/
│   │   ├── api/      # Axios client
│   │   ├── components/
│   │   ├── context/  # AuthContext
│   │   ├── hooks/    # useChat, useAuth
│   │   └── pages/    # AuthPage, ChatPage
│   └── .env.example
└── vercel.json       # Vercel multi-service deployment config
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (local or Atlas)
- Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Fill in: MONGODB_URL, SECRET_KEY, GEMINI_API_KEY

uvicorn app.main:app --reload --port 8000
```

API docs at **http://localhost:8000/docs**

### Frontend

```bash
cd frontend
npm install

cp .env.example .env
# Set VITE_API_URL=http://localhost:8000

npm run dev
```

App at **http://localhost:5173**

---

## Deployment (Vercel)

Both services deploy from the same repo using `vercel.json`:

- Frontend → `/`
- Backend → `/_/backend`

Set these environment variables in the Vercel dashboard:

| Variable        | Where    | Value                          |
|-----------------|----------|--------------------------------|
| `MONGODB_URL`   | Backend  | Your Atlas connection string   |
| `MONGODB_DB_NAME` | Backend | `legalsarthi`                |
| `SECRET_KEY`    | Backend  | 32-char random hex             |
| `GEMINI_API_KEY`| Backend  | Your Gemini API key            |
| `VITE_API_URL`  | Frontend | `/_/backend`                   |

Generate `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Roadmap

- [ ] Multilingual support (Hindi, regional languages)
- [ ] Document upload and analysis
- [ ] State-specific legal advice
- [ ] Lawyer directory integration
- [ ] Mobile app (React Native)

---

## Disclaimer

> ⚠️ LegalSarthi provides **general legal information** based on Indian law. It is **not** a substitute for professional legal advice. Always consult a qualified lawyer for your specific situation. For free legal aid, call **NALSA helpline: 15100**.

---

## License

MIT
