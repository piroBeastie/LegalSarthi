# ⚖️ LegalSarthi — Frontend

React + Vite frontend for LegalSarthi. Provides authentication and a multi-turn legal chat interface that displays structured AI responses.

---

## Stack

- **React 18** — UI
- **Vite** — build tooling and dev server
- **Tailwind CSS** — styling
- **Axios** — API client with JWT interceptors
- **React Router** — client-side routing
- **Lucide React** — icons

---

## Setup

### 1. Install

```bash
npm install
```

### 2. Configure

```bash
cp .env.example .env
```

| Variable       | Description                                |
|----------------|--------------------------------------------|
| `VITE_API_URL` | Backend base URL (no trailing slash)       |

Local dev:
```
VITE_API_URL=http://localhost:8000
```

Production (Vercel):
```
VITE_API_URL=/_/backend
```

### 3. Run

```bash
npm run dev       # dev server at http://localhost:5173
npm run build     # production build → dist/
npm run preview   # preview production build locally
```

---

## Pages & Routes

| Route    | Component  | Description                                       |
|----------|------------|---------------------------------------------------|
| `/`      | RootRoute  | Redirects to `/chat` if authenticated, else `/login` |
| `/login` | AuthPage   | Login and registration (toggled in one page)      |
| `/chat`  | ChatPage   | Main chat interface (protected)                   |

---

## App Flow

```
User visits /
      │
      ├─ Authenticated? → /chat
      └─ Not authenticated? → /login
             │
             ├─ Register: POST /api/auth/register
             └─ Login:    POST /api/auth/login
                               │
                               └─ Store JWT in localStorage
                                  Redirect → /chat

/chat
  ├─ Sidebar: list conversations (GET /api/chat/conversations)
  ├─ Click conversation: load messages (GET /api/chat/conversations/{id})
  ├─ Send message: POST /api/chat/ask
  │    └─ Optimistic UI: show user message immediately
  │       On response: render AdviceBubble with structured advice
  └─ Delete conversation: DELETE /api/chat/conversations/{id}
```

---

## Key Components

| Component       | Description                                                  |
|-----------------|--------------------------------------------------------------|
| `AuthPage`      | Dual login/register form with validation                     |
| `ChatPage`      | Main layout: sidebar + chat area                             |
| `ChatSidebar`   | Conversation list, new chat button, delete option            |
| `ChatInput`     | Auto-resizing textarea, 2000 char limit, Enter to send       |
| `ChatMessages`  | Scrollable message history with typing indicator             |
| `AdviceBubble`  | Renders AI response: category, summary, steps, laws          |
| `UserBubble`    | Simple bubble for user messages                              |
| `CategoryBadge` | Color-coded legal category label                             |
| `SourceBadge`   | Shows response source (`Gemini AI` or `Mock AI`)             |

---

## Auth & API

**JWT storage**: `localStorage['legalsarthi_token']`

**Auto-attach**: every request gets `Authorization: Bearer <token>` via axios interceptor.

**Auto-logout**: 401 responses clear localStorage and redirect to `/login`.

---

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.js          # Axios instance with interceptors
│   ├── components/
│   │   ├── AdviceBubble.jsx   # Structured advice renderer
│   │   ├── CategoryBadge.jsx
│   │   ├── ChatInput.jsx
│   │   ├── ChatMessages.jsx
│   │   ├── ChatSidebar.jsx
│   │   ├── SourceBadge.jsx
│   │   ├── TypingIndicator.jsx
│   │   └── UserBubble.jsx
│   ├── context/
│   │   └── AuthContext.jsx    # Auth state, login/logout/register
│   ├── hooks/
│   │   ├── useAuth.js
│   │   └── useChat.js         # Conversation state, send, load, delete
│   ├── pages/
│   │   ├── AuthPage.jsx
│   │   └── ChatPage.jsx
│   ├── utils/
│   │   └── constants.js       # Category color mappings
│   ├── App.jsx                # Routes
│   └── main.jsx
├── .env.example
├── index.html
└── vite.config.js
```
