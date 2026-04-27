"""
LegalSarthi - Pydantic Schemas
Request/response models for all API endpoints.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ═══════════════════════════════════════════
# AUTH SCHEMAS
# ═══════════════════════════════════════════

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Rahul Sharma"])
    email: EmailStr = Field(..., examples=["rahul@example.com"])
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ═══════════════════════════════════════════
# CHAT SCHEMAS
# ═══════════════════════════════════════════

class AdviceSource(str, Enum):
    RULES_ENGINE = "rules_engine"
    GEMINI_AI = "gemini_ai"
    MOCK_AI = "mock_ai"


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        examples=["A traffic police stopped me and is asking for ₹500 bribe to let me go."],
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Pass existing conversation_id to continue a chat, or omit to start new.",
    )


class LegalAdvice(BaseModel):
    category: str  # e.g. "police", "consumer", "property"
    summary: str  # short 1-liner
    steps: List[str]  # step-by-step legal actions
    relevant_laws: List[str]  # IPC sections, Acts, etc.
    disclaimer: str
    source: AdviceSource  # whether rules_engine or AI answered


class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    user_message: str
    advice: LegalAdvice
    timestamp: datetime


# ═══════════════════════════════════════════
# CONVERSATION SCHEMAS
# ═══════════════════════════════════════════

class MessageOut(BaseModel):
    id: str
    role: str  # "user" or "assistant"
    content: str
    advice: Optional[LegalAdvice] = None  # present for assistant messages
    timestamp: datetime


class ConversationSummary(BaseModel):
    id: str
    title: str
    category: str
    message_count: int
    created_at: datetime
    updated_at: datetime


class ConversationDetail(BaseModel):
    id: str
    title: str
    category: str
    messages: List[MessageOut]
    created_at: datetime
    updated_at: datetime
