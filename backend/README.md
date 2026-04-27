# ⚖️ LegalSarthi

**Your AI-Powered Legal Guidance Companion for Indian Citizens**

LegalSarthi helps everyday citizens navigate legal situations with confidence. Describe your situation — whether it's a police officer demanding a bribe, a landlord illegally evicting you, or an online scam — and get step-by-step legal guidance with relevant Indian laws cited.

## Architecture

```
User Question
     │
     ▼
┌─────────────────┐
│  FastAPI Backend │
│  + JWT Auth      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐    Match found    ┌─────────────────────┐
│  Rules Engine    │ ───── YES ──────▶ │ Curated Legal Steps │
│  (keyword match  │                   │ + Relevant Sections │
│   + scoring)     │                   └─────────────────────┘
└──────┬──────────┘
       │ No match (complex/unusual case)
       ▼
┌─────────────────┐
│  Gemini AI       │ ← System prompt grounded in Indian law
│  (fallback)      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  MongoDB         │ ← Conversations, messages, users
└─────────────────┘
```

## Legal Categories Covered

| Category    | Topics                                              |
|-------------|-----------------------------------------------------|
| Police      | Bribery, FIR refusal, illegal detention/arrest       |
| Consumer    | Defective products, refunds, consumer fraud          |
| Property    | Illegal eviction, security deposit, tenant rights    |
| Workplace   | Harassment, POSH Act, wrongful termination           |
| Cyber       | Online fraud, hacking, identity theft, cyberbullying |
| Domestic    | Domestic violence, dowry harassment                  |
| Environment | Noise pollution, neighbourhood disturbance           |
| RTI         | Right to Information applications                    |

## Quick Start

### Prerequisites

- Python 3.10+
- MongoDB (local or Atlas)
- (Optional) Gemini API key

### 1. Clone & Install

```bash
cd legalsarthi
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your MongoDB URL and (optionally) Gemini API key
```

### 3. Start MongoDB

```bash
# If using local MongoDB:
mongod --dbpath /path/to/data

# Or use MongoDB Atlas (update MONGODB_URL in .env)
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: **http://localhost:8000/docs** for interactive API docs.

## API Endpoints

### Auth

| Method | Endpoint             | Description          |
|--------|----------------------|----------------------|
| POST   | `/api/auth/register` | Register new user    |
| POST   | `/api/auth/login`    | Login, get JWT token |
| GET    | `/api/auth/me`       | Get current profile  |

### Chat

| Method | Endpoint                                | Description                |
|--------|-----------------------------------------|----------------------------|
| POST   | `/api/chat/ask`                         | Ask a legal question       |
| GET    | `/api/chat/conversations`               | List all conversations     |
| GET    | `/api/chat/conversations/{id}`          | Get conversation + messages|
| DELETE | `/api/chat/conversations/{id}`          | Delete a conversation      |

### System

| Method | Endpoint               | Description              |
|--------|------------------------|--------------------------|
| GET    | `/api/health`          | Health check             |
| GET    | `/api/legal/categories`| List legal categories    |

## Usage Example

### 1. Register

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Rahul", "email": "rahul@example.com", "password": "secure123"}'
```

### 2. Ask a Legal Question

```bash
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"message": "A traffic police officer stopped me and is demanding ₹500 as bribe"}'
```

### 3. Continue the Conversation

```bash
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "message": "He is now threatening to impound my vehicle",
    "conversation_id": "<conversation-id-from-previous-response>"
  }'
```

## Adding Gemini AI

1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Add to your `.env` file:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```
3. Restart the server — Gemini auto-enables when the key is present

## Adding New Legal Rules

Edit `app/data/legal_rules.py` and add a new rule following this format:

```python
{
    "id": "unique_rule_id",
    "category": "category_name",
    "keywords": ["keyword1", "keyword2", "multi word keyword"],
    "title": "Rule Title",
    "summary": "One-line legal summary.",
    "steps": ["Step 1", "Step 2"],
    "relevant_laws": ["Act — Section X (description)"],
}
```

## Future Roadmap (v2+)

- [ ] 🌐 Multilingual support (Hindi, regional languages)
- [ ] 📎 Document upload (analyze legal documents)
- [ ] 📍 State-specific legal advice
- [ ] 🔔 Legal deadline reminders
- [ ] 👨‍⚖️ Connect with lawyers directory
- [ ] 📱 Mobile app (React Native)

## Disclaimer

> ⚠️ LegalSarthi provides **general legal information** based on Indian law.
> It is **NOT** a substitute for professional legal advice.
> Always consult a qualified lawyer for advice specific to your situation.
> For free legal aid, contact **NALSA helpline: 15100**.

## License

MIT
