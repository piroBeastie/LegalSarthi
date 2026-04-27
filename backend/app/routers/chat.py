"""
LegalSarthi - Chat Router
Handles chat messaging and conversation history endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationSummary,
    ConversationDetail,
)
from app.core.security import get_current_user
from app.services.chat_service import (
    process_chat,
    get_conversations,
    get_conversation_detail,
    delete_conversation,
)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/ask", response_model=ChatResponse)
async def ask_legal_question(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Ask a legal question.
    - Omit conversation_id to start a new conversation.
    - Pass conversation_id to continue an existing chat.

    The system first checks the rules engine for a match.
    If no match is found, it falls back to Gemini AI (or mock if not configured).
    """
    try:
        result = await process_chat(user_id=current_user["id"], request=request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong: {str(e)}",
        )


@router.get("/conversations", response_model=list[ConversationSummary])
async def list_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    """Get all conversations for the current user (paginated, newest first)."""
    return await get_conversations(current_user["id"], skip=skip, limit=limit)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Get a full conversation with all messages."""
    try:
        return await get_conversation_detail(current_user["id"], conversation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete a conversation and all its messages."""
    deleted = await delete_conversation(current_user["id"], conversation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
