"""
╔═══════════════════════════════════════════════════════════╗
║                    ⚖️  LegalSarthi  ⚖️                    ║
║         Your AI-Powered Legal Guidance Companion          ║
║                                                           ║
║   Rules-first, AI-fallback legal advice for Indian law    ║
╚═══════════════════════════════════════════════════════════╝
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import connect_db, close_db
from app.routers import auth, chat, health


# ── Lifespan: startup/shutdown ──
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    print(f"""
    ⚖️  {settings.APP_NAME} v{settings.APP_VERSION} is running!
    📡 Gemini AI: {"✅ Enabled" if settings.GEMINI_ENABLED else "❌ Disabled (set GEMINI_API_KEY in .env)"}
    🗄️  MongoDB:   {settings.MONGODB_URL}/{settings.MONGODB_DB_NAME}
    📖 Docs:      http://localhost:8000/docs
    """)
    yield
    await close_db()


# ── Create app ──
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "⚖️ LegalSarthi — AI-powered legal guidance for Indian citizens. "
        "Ask about your rights, get step-by-step legal actions, and know "
        "the relevant laws. Powered by a curated rules engine with Gemini AI fallback."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── CORS (allow frontend origins) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # React dev
        "http://localhost:5173",    # Vite dev
        "http://localhost:8080",    # Vue dev
        "*",                        # TODO: restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Register routers ──
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


# ── Root endpoint ──
@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "⚖️ Welcome to LegalSarthi! Visit /docs for API documentation.",
        "endpoints": {
            "docs": "/docs",
            "register": "/api/auth/register",
            "login": "/api/auth/login",
            "ask": "/api/chat/ask",
            "conversations": "/api/chat/conversations",
            "categories": "/api/legal/categories",
            "health": "/api/health",
        },
    }
