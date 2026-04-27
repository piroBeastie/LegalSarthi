# ⚖️ LegalSarthi — Backend

FastAPI backend for LegalSarthi. Handles authentication, chat orchestration, a keyword-based rules engine, and Gemini AI integration.

---

## Stack

- **FastAPI** — async REST API
- **MongoDB** (Motor) — conversations, messages, users
- **Google Gemini** (`gemini-2.5-flash-lite`) — AI responses
- **JWT** (HS256) — authentication, 24-hour tokens
- **bcrypt** — password hashing

---

## Request Pipeline

```
POST /api/chat/ask
      │
      ├─ 1. Validate JWT → get current user
      ├─ 2. Create or load conversation (MongoDB)
      ├─ 3. Save user message (MongoDB)
      │
      ├─ 4. Rules Engine
      │      └─ Keyword score query against 30+ rules
      │         Combine last 3 user messages for follow-up context
      │         Return top-3 rules with score ≥ 2  (or empty list)
      │
      ├─ 5. Gemini AI  ← always called
      │      ├─ System prompt: Indian law expertise + JSON format
      │      ├─ Context: matched rules injected as grounding
      │      ├─ History: last 10 messages for multi-turn awareness
      │      └─ Fallback chain: flash-lite → flash → mock response
      │
      ├─ 6. Save assistant response (MongoDB)
      └─ 7. Update conversation metadata → return ChatResponse
```

---

## Setup

### 1. Install

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
```

Required variables:

| Variable         | Description                                   |
|------------------|-----------------------------------------------|
| `MONGODB_URL`    | MongoDB connection string (local or Atlas)    |
| `MONGODB_DB_NAME`| Database name (default: `legalsarthi`)        |
| `SECRET_KEY`     | JWT signing secret — generate below           |
| `GEMINI_API_KEY` | From [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

Generate a strong secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: **http://localhost:8000/docs**

---

## API Endpoints

### Auth

| Method | Endpoint              | Auth | Description           |
|--------|-----------------------|------|-----------------------|
| POST   | `/api/auth/register`  | No   | Create account        |
| POST   | `/api/auth/login`     | No   | Login, receive JWT    |
| GET    | `/api/auth/me`        | Yes  | Get current user info |

### Chat

| Method | Endpoint                        | Auth | Description                        |
|--------|---------------------------------|------|------------------------------------|
| POST   | `/api/chat/ask`                 | Yes  | Send message, get legal advice     |
| GET    | `/api/chat/conversations`       | Yes  | List conversations (paginated)     |
| GET    | `/api/chat/conversations/{id}`  | Yes  | Fetch conversation + messages      |
| DELETE | `/api/chat/conversations/{id}`  | Yes  | Delete conversation                |

### System

| Method | Endpoint       | Description  |
|--------|----------------|--------------|
| GET    | `/api/health`  | Health check |

---

## Response Format

Every chat response returns a structured `advice` object:

```json
{
  "conversation_id": "...",
  "message_id": "...",
  "user_message": "...",
  "advice": {
    "category": "police",
    "summary": "You should NOT pay the bribe...",
    "steps": ["Stay calm. Do not pay.", "Ask for officer's badge number.", "..."],
    "relevant_laws": ["Prevention of Corruption Act, 1988 — Section 7", "..."],
    "disclaimer": "⚠️ This is general information, not legal advice...",
    "source": "gemini_ai"
  },
  "timestamp": "2026-04-27T10:30:00Z"
}
```

`source` values: `gemini_ai` | `mock_ai`

---

## Database Schema

**users** — `{name, email, password_hash, created_at, updated_at}`

**conversations** — `{user_id, title, category, message_count, created_at, updated_at}`

**messages** — `{conversation_id, role, content, advice_data?, created_at}`

---

## Adding Legal Rules

Edit `app/data/legal_rules.py`:

```python
{
    "id": "unique_rule_id",
    "category": "police",           # police/consumer/property/workplace/cyber/domestic/environment/rti/general
    "keywords": ["keyword1", "multi word phrase"],
    "title": "Rule Title",
    "summary": "One-line legal summary.",
    "steps": ["Step 1", "Step 2"],
    "relevant_laws": ["Act Name — Section X (description)"],
}
```

Rules are matched via keyword scoring. Higher keyword specificity = higher match score.

---

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, lifespan
│   ├── core/
│   │   ├── config.py        # Settings via pydantic-settings
│   │   ├── database.py      # MongoDB connection (Motor)
│   │   └── security.py      # JWT create/verify, bcrypt
│   ├── data/
│   │   └── legal_rules.py   # 30+ curated Indian law rules
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response models
│   ├── routers/
│   │   ├── auth.py          # /api/auth/*
│   │   ├── chat.py          # /api/chat/*
│   │   └── health.py        # /api/health
│   └── services/
│       ├── ai_advisor.py    # Gemini integration + prompt construction
│       ├── chat_service.py  # Full pipeline orchestration
│       └── rules_engine.py  # Keyword matching + scoring
├── .env.example
└── requirements.txt
```

---

## Disclaimer

> ⚠️ LegalSarthi provides general legal information based on Indian law. It is not a substitute for professional legal advice. For free legal aid, call **NALSA: 15100**.
