"""
LegalSarthi - Health & Utility Router
Healthcheck, legal categories, and system info endpoints.
"""

from fastapi import APIRouter
from app.core.config import settings
from app.services.rules_engine import get_all_categories, get_rules_by_category

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check():
    """Application health check."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "gemini_enabled": settings.GEMINI_ENABLED,
    }


@router.get("/legal/categories")
async def list_categories():
    """List all legal categories available in the rules engine."""
    categories = get_all_categories()
    result = []
    for cat in sorted(categories):
        rules = get_rules_by_category(cat)
        result.append({
            "category": cat,
            "rule_count": len(rules),
            "topics": [r["title"] for r in rules],
        })
    return {"categories": result}
