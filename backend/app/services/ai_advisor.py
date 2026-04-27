"""
LegalSarthi - AI Advisor Service (RAG Architecture)

Uses google.genai (new official SDK) with:
- Retry logic for rate limits (429 errors)
- Model fallback chain (flash → flash-lite → 1.5-flash)
- Matched legal rules injected as context for personalized responses
"""

import json
import asyncio
from typing import List, Optional

from app.core.config import settings
from app.models.schemas import LegalAdvice, AdviceSource

# ── System prompt that grounds Gemini in Indian law ──
SYSTEM_PROMPT = """You are LegalSarthi AI, an expert legal information assistant specializing in Indian law.

YOUR ROLE:
- Provide accurate, step-by-step legal guidance based on Indian law
- Tailor your advice to the user's SPECIFIC situation — do NOT give generic advice
- Cite specific sections of relevant Acts (IPC/BNS, CrPC/BNSS, Constitution, specific Acts)
- Suggest practical actions the user can take IMMEDIATELY given their exact circumstances
- Recommend appropriate authorities, helplines, and portals to approach
- If the user is in danger, prioritize their safety FIRST

RULES:
1. Always clarify that you provide LEGAL INFORMATION, not legal advice
2. Always recommend consulting a qualified lawyer for specific cases
3. Mention NALSA free legal aid helpline (15100) when relevant
4. Be empathetic but factual — the user may be stressed or scared
5. Prioritize the user's safety in dangerous situations
6. Consider both old laws (IPC, CrPC) and new laws (BNS, BNSS) as India is transitioning
7. Give state-specific guidance when possible
8. If legal reference data is provided below, USE IT as your primary source — adapt the steps to the user's specific situation rather than copying them verbatim
9. Keep steps practical and actionable — what should the user do RIGHT NOW

RESPONSE FORMAT (respond ONLY in this JSON format, no markdown, no extra text):
{
    "category": "<legal category: police/consumer/property/workplace/cyber/domestic/environment/rti/general>",
    "summary": "<one-line summary tailored to the user's specific situation>",
    "steps": ["<specific step 1>", "<specific step 2>", "..."],
    "relevant_laws": ["<Act — Section (description)>", "..."]
}
"""


def _build_context_prompt(user_message: str, matched_rules: Optional[List[dict]] = None) -> str:
    """
    Build the prompt that includes matched legal rules as context.
    This is the RAG part — retrieval results injected into the generation prompt.
    """
    prompt_parts = []

    if matched_rules:
        prompt_parts.append("=== LEGAL REFERENCE DATA (use this to ground your response) ===")
        for rule in matched_rules:
            prompt_parts.append(f"\nTOPIC: {rule['title']}")
            prompt_parts.append(f"CATEGORY: {rule['category']}")
            prompt_parts.append(f"LEGAL SUMMARY: {rule['summary']}")
            prompt_parts.append("RECOMMENDED STEPS:")
            for i, step in enumerate(rule['steps'], 1):
                prompt_parts.append(f"  {i}. {step}")
            prompt_parts.append("RELEVANT LAWS:")
            for law in rule['relevant_laws']:
                prompt_parts.append(f"  - {law}")
        prompt_parts.append("\n=== END OF REFERENCE DATA ===\n")
        prompt_parts.append(
            "IMPORTANT: Use the above legal reference data to inform your response, "
            "but ADAPT the steps to the user's specific situation described below. "
            "Do NOT copy the steps word-for-word. Personalize based on their exact circumstances.\n"
        )

    prompt_parts.append(f"USER'S SITUATION: {user_message}")

    return "\n".join(prompt_parts)


async def get_ai_advice(
    user_message: str,
    matched_rules: Optional[List[dict]] = None,
    conversation_history: Optional[List[dict]] = None,
) -> LegalAdvice:
    """
    Get personalized legal advice from Gemini AI with matched rules as context.
    """
    if settings.GEMINI_ENABLED:
        return await _call_gemini(user_message, matched_rules, conversation_history)
    else:
        return _mock_response(user_message, matched_rules)


async def _call_gemini(
    user_message: str,
    matched_rules: Optional[List[dict]] = None,
    conversation_history: Optional[List[dict]] = None,
) -> LegalAdvice:
    """
    Call Gemini API with retry logic and model fallback.
    Tries: primary model → fallback models → mock response
    """
    # Build model chain: primary + fallbacks
    models_to_try = [settings.GEMINI_MODEL] + list(settings.GEMINI_FALLBACK_MODELS)

    # Build the RAG-enhanced prompt
    enhanced_prompt = _build_context_prompt(user_message, matched_rules)

    # Build conversation history for multi-turn
    history_contents = []
    if conversation_history:
        for msg in conversation_history[-10:]:
            role = "user" if msg["role"] == "user" else "model"
            history_contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}],
            })

    # Add the current user message
    history_contents.append({
        "role": "user",
        "parts": [{"text": enhanced_prompt}],
    })

    last_error = None

    for model_name in models_to_try:
        for attempt in range(settings.GEMINI_MAX_RETRIES + 1):
            try:
                response_text = await _make_api_call(model_name, history_contents)
                advice = _parse_response(response_text)
                if advice:
                    return advice

            except Exception as e:
                last_error = e
                error_str = str(e)

                # Rate limit — wait and retry or try next model
                if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                    if attempt < settings.GEMINI_MAX_RETRIES:
                        wait_time = settings.GEMINI_RETRY_DELAY * (attempt + 1)
                        print(f"⏳ Rate limited on {model_name}, retrying in {wait_time}s (attempt {attempt + 1})...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print(f"⚠️ {model_name} quota exhausted, trying next model...")
                        break  # Try next model
                else:
                    # Non-rate-limit error — try next model immediately
                    print(f"⚠️ {model_name} error: {error_str[:150]}")
                    break

    # All models failed — fall back to mock
    print(f"⚠️ All Gemini models failed. Last error: {last_error}")
    return _mock_response(user_message, matched_rules)


async def _make_api_call(model_name: str, contents: list) -> str:
    """Make a single API call to Gemini using the new google.genai SDK."""
    from google import genai

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=2048,
        ),
    )

    return response.text


def _parse_response(response_text: str) -> Optional[LegalAdvice]:
    """Parse Gemini response text into LegalAdvice object."""
    if not response_text:
        return None

    text = response_text.strip()

    # Clean markdown fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        text = text.rsplit("```", 1)[0]
    text = text.strip()

    try:
        data = json.loads(text)
        return LegalAdvice(
            category=data.get("category", "general"),
            summary=data.get("summary", "AI-generated legal guidance."),
            steps=data.get("steps", ["Please consult a lawyer for detailed guidance."]),
            relevant_laws=data.get("relevant_laws", []),
            disclaimer=(
                "⚠️ DISCLAIMER: This advice was generated by AI based on Indian law. "
                "AI can make mistakes. Please verify with a qualified lawyer. "
                "For free legal aid, contact NALSA helpline: 15100."
            ),
            source=AdviceSource.GEMINI_AI,
        )
    except json.JSONDecodeError:
        # If Gemini doesn't return valid JSON, wrap the raw text
        return LegalAdvice(
            category="general",
            summary="AI-generated legal guidance",
            steps=[text[:2000]],
            relevant_laws=[],
            disclaimer=(
                "⚠️ DISCLAIMER: This advice was generated by AI. "
                "Please consult a qualified lawyer. NALSA helpline: 15100."
            ),
            source=AdviceSource.GEMINI_AI,
        )


def _mock_response(
    user_message: str,
    matched_rules: Optional[List[dict]] = None,
) -> LegalAdvice:
    """
    Mock response when Gemini is not configured or all models fail.
    If rules were matched, returns them as static advice (fallback).
    """
    if matched_rules and len(matched_rules) > 0:
        rule = matched_rules[0]
        return LegalAdvice(
            category=rule["category"],
            summary=rule["summary"],
            steps=rule["steps"] + [
                "💡 TIP: Configure Gemini AI (set GEMINI_API_KEY in .env) to get "
                "advice personalized to your exact situation instead of these general steps."
            ],
            relevant_laws=rule["relevant_laws"],
            disclaimer=(
                "⚠️ DISCLAIMER: These are general legal steps from our database. "
                "For advice personalized to your specific situation, configure Gemini AI. "
                "Always consult a qualified lawyer. NALSA helpline: 15100."
            ),
            source=AdviceSource.MOCK_AI,
        )
    else:
        return LegalAdvice(
            category="general",
            summary=(
                "Your question requires AI analysis. "
                "Please set GEMINI_API_KEY in your .env file to enable personalized legal guidance."
            ),
            steps=[
                "Our system couldn't find a specific legal rule matching your situation.",
                "Configure Gemini AI (set GEMINI_API_KEY in .env) to get detailed, personalized legal guidance.",
                "In the meantime, here are general steps you can take:",
                "→ Document everything: dates, times, witnesses, evidence.",
                "→ For emergencies, call 112 (national emergency number).",
                "→ For free legal aid, call NALSA helpline: 15100.",
                "→ Visit your nearest District Legal Services Authority (DLSA) for free legal assistance.",
                "→ Consult a qualified lawyer for advice specific to your situation.",
            ],
            relevant_laws=[
                "Constitution of India — Article 39A (free legal aid)",
                "Legal Services Authorities Act, 1987 (free legal aid for eligible persons)",
            ],
            disclaimer=(
                "⚠️ DISCLAIMER: This is a placeholder response. Configure Gemini AI "
                "for detailed, situation-specific legal guidance. "
                "Always consult a qualified lawyer. NALSA helpline: 15100."
            ),
            source=AdviceSource.MOCK_AI,
        )
