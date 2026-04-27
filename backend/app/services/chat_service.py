"""
LegalSarthi - Chat Service
Orchestrates the full RAG chat flow:
  1. Rules engine retrieves matching legal rules (retrieval)
  2. Gemini AI generates personalized advice using matched rules as context (generation)
  3. Persist messages + advice_data to MongoDB
"""

from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId

from app.core.database import get_db
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    LegalAdvice,
    ConversationSummary,
    ConversationDetail,
    MessageOut,
)
from app.services.rules_engine import find_matching_rules
from app.services.ai_advisor import get_ai_advice


async def process_chat(user_id: str, request: ChatRequest) -> ChatResponse:
    """
    Main chat handler:
    - Creates or continues a conversation
    - Tries rules engine first, then AI
    - Saves both user message and assistant response
    """
    db = get_db()
    now = datetime.now(timezone.utc)

    # ── 1. Get or create conversation ──
    if request.conversation_id:
        convo = await db.conversations.find_one({
            "_id": ObjectId(request.conversation_id),
            "user_id": user_id,
        })
        if not convo:
            raise ValueError("Conversation not found")
        conversation_id = request.conversation_id
    else:
        # Create new conversation
        convo_doc = {
            "user_id": user_id,
            "title": request.message[:80] + ("..." if len(request.message) > 80 else ""),
            "category": "general",
            "message_count": 0,
            "created_at": now,
            "updated_at": now,
        }
        result = await db.conversations.insert_one(convo_doc)
        conversation_id = str(result.inserted_id)

    # ── 2. Save user message ──
    user_msg = {
        "conversation_id": conversation_id,
        "role": "user",
        "content": request.message,
        "created_at": now,
    }
    await db.messages.insert_one(user_msg)

    # ── 3. RETRIEVAL: Find matching legal rules ──
    # For follow-up messages, combine with recent conversation context
    # so "they took my license" after "police asking bribe" still matches
    query_for_matching = request.message
    if request.conversation_id:
        history = await _get_message_history(conversation_id, limit=4)
        user_messages = [m["content"] for m in history if m["role"] == "user"]
        if user_messages:
            query_for_matching = " ".join(user_messages[-3:]) + " " + request.message

    matched_rules = find_matching_rules(query_for_matching, top_n=3)

    # ── 4. GENERATION: Always call AI with matched rules as context ──
    conversation_history = await _get_message_history(conversation_id, limit=10)
    advice = await get_ai_advice(
        user_message=request.message,
        matched_rules=matched_rules,
        conversation_history=conversation_history,
    )
    category = advice.category

    # ── 5. Save assistant response ──
    assistant_content = _format_advice_for_storage(advice)
    assistant_msg = {
        "conversation_id": conversation_id,
        "role": "assistant",
        "content": assistant_content,
        "advice_data": advice.model_dump(),
        "created_at": datetime.now(timezone.utc),
    }
    result = await db.messages.insert_one(assistant_msg)
    message_id = str(result.inserted_id)

    # ── 6. Update conversation metadata ──
    await db.conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$set": {
                "category": category,
                "updated_at": datetime.now(timezone.utc),
            },
            "$inc": {"message_count": 2},  # user + assistant
        },
    )

    return ChatResponse(
        conversation_id=conversation_id,
        message_id=message_id,
        user_message=request.message,
        advice=advice,
        timestamp=now,
    )


async def get_conversations(user_id: str, skip: int = 0, limit: int = 20) -> list:
    """Get paginated conversation list for a user."""
    db = get_db()
    cursor = (
        db.conversations.find({"user_id": user_id})
        .sort("updated_at", -1)
        .skip(skip)
        .limit(limit)
    )

    conversations = []
    async for convo in cursor:
        conversations.append(
            ConversationSummary(
                id=str(convo["_id"]),
                title=convo.get("title", "Untitled"),
                category=convo.get("category", "general"),
                message_count=convo.get("message_count", 0),
                created_at=convo["created_at"],
                updated_at=convo["updated_at"],
            )
        )
    return conversations


async def get_conversation_detail(user_id: str, conversation_id: str) -> ConversationDetail:
    """Get full conversation with all messages."""
    db = get_db()

    convo = await db.conversations.find_one({
        "_id": ObjectId(conversation_id),
        "user_id": user_id,
    })
    if not convo:
        raise ValueError("Conversation not found")

    messages = []
    cursor = (
        db.messages.find({"conversation_id": conversation_id})
        .sort("created_at", 1)
    )
    async for msg in cursor:
        advice_data = None
        if msg["role"] == "assistant" and "advice_data" in msg:
            try:
                advice_data = LegalAdvice(**msg["advice_data"])
            except Exception:
                advice_data = None

        messages.append(
            MessageOut(
                id=str(msg["_id"]),
                role=msg["role"],
                content=msg["content"],
                advice=advice_data,
                timestamp=msg["created_at"],
            )
        )

    return ConversationDetail(
        id=str(convo["_id"]),
        title=convo.get("title", "Untitled"),
        category=convo.get("category", "general"),
        messages=messages,
        created_at=convo["created_at"],
        updated_at=convo["updated_at"],
    )


async def delete_conversation(user_id: str, conversation_id: str) -> bool:
    """Delete a conversation and all its messages."""
    db = get_db()

    result = await db.conversations.delete_one({
        "_id": ObjectId(conversation_id),
        "user_id": user_id,
    })

    if result.deleted_count == 0:
        return False

    await db.messages.delete_many({"conversation_id": conversation_id})
    return True


# ── Helpers ──

async def _get_message_history(conversation_id: str, limit: int = 10) -> list:
    """Fetch recent messages for AI context."""
    db = get_db()
    cursor = (
        db.messages.find({"conversation_id": conversation_id})
        .sort("created_at", -1)
        .limit(limit)
    )
    messages = []
    async for msg in cursor:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.reverse()  # chronological order
    return messages


def _format_advice_for_storage(advice: LegalAdvice) -> str:
    """Format advice as readable text for message storage."""
    lines = [
        f"📋 **{advice.category.upper()}**\n",
        f"{advice.summary}\n",
        "📌 **Steps to take:**",
    ]
    for i, step in enumerate(advice.steps, 1):
        lines.append(f"  {i}. {step}")

    if advice.relevant_laws:
        lines.append("\n📖 **Relevant Laws:**")
        for law in advice.relevant_laws:
            lines.append(f"  • {law}")

    lines.append(f"\n{advice.disclaimer}")
    return "\n".join(lines)
