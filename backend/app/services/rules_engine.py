"""
LegalSarthi - Rules Engine
Classifies user queries and matches them against the curated legal rules database.
Uses keyword matching with scoring to find the best matching rule.
"""

import re
from typing import Optional, Tuple, List
from app.data.legal_rules import LEGAL_RULES
from app.models.schemas import LegalAdvice, AdviceSource

# Threshold: minimum score to consider a rule match valid
MATCH_THRESHOLD = 2


def _normalize(text: str) -> str:
    """Lowercase and strip special chars for matching."""
    return re.sub(r"[^\w\s]", " ", text.lower())


def _stem(word: str) -> str:
    """Very basic suffix stripping for common English/Hindi-English endings."""
    for suffix in ("ing", "ed", "ment", "tion", "ness", "ally", "ly", "er", "est", "s"):
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def _score_rule(query_words: set, query_stems: set, rule: dict) -> int:
    """Score a rule by how many keywords match the query."""
    score = 0
    for keyword in rule["keywords"]:
        kw_parts = set(keyword.lower().split())
        kw_stems = {_stem(w) for w in kw_parts}

        # Full keyword phrase match → bonus points
        if kw_parts.issubset(query_words) or kw_stems.issubset(query_stems):
            score += len(kw_parts) + 1  # multi-word matches score higher
        # Partial single-word matches
        for part in kw_parts:
            if part in query_words or _stem(part) in query_stems:
                score += 1
    return score


def classify_and_match(user_message: str) -> Optional[Tuple[dict, int]]:
    """
    Find the best matching legal rule for a user query.
    Returns (rule, score) or None if no match above threshold.
    """
    normalized = _normalize(user_message)
    query_words = set(normalized.split())
    query_stems = {_stem(w) for w in query_words}

    best_rule = None
    best_score = 0

    for rule in LEGAL_RULES:
        score = _score_rule(query_words, query_stems, rule)
        if score > best_score:
            best_score = score
            best_rule = rule

    if best_rule and best_score >= MATCH_THRESHOLD:
        return best_rule, best_score

    return None


def find_matching_rules(user_message: str, top_n: int = 3) -> List[dict]:
    """
    Find the top N matching legal rules for a user query.
    Returns a list of rule dicts (without keywords) sorted by score, highest first.
    Used by the RAG pipeline to inject legal context into Gemini prompts.
    """
    normalized = _normalize(user_message)
    query_words = set(normalized.split())
    query_stems = {_stem(w) for w in query_words}

    scored_rules = []
    for rule in LEGAL_RULES:
        score = _score_rule(query_words, query_stems, rule)
        if score >= MATCH_THRESHOLD:
            scored_rules.append((rule, score))

    # Sort by score descending, take top N
    scored_rules.sort(key=lambda x: x[1], reverse=True)
    top_rules = scored_rules[:top_n]

    # Return rule dicts without keywords (Gemini doesn't need them)
    return [
        {k: v for k, v in rule.items() if k != "keywords"}
        for rule, score in top_rules
    ]


def build_advice_from_rule(rule: dict) -> LegalAdvice:
    """Convert a matched rule into a LegalAdvice response."""
    return LegalAdvice(
        category=rule["category"],
        summary=rule["summary"],
        steps=rule["steps"],
        relevant_laws=rule["relevant_laws"],
        disclaimer=(
            "⚠️ DISCLAIMER: This is general legal information based on Indian law, "
            "NOT professional legal advice. Every situation is unique. Please consult "
            "a qualified lawyer or legal aid service for advice specific to your case. "
            "For free legal aid, contact NALSA helpline: 15100."
        ),
        source=AdviceSource.RULES_ENGINE,
    )


def get_all_categories() -> list:
    """Return all unique categories in the rules database."""
    return list(set(rule["category"] for rule in LEGAL_RULES))


def get_rules_by_category(category: str) -> list:
    """Return all rules for a given category."""
    return [r for r in LEGAL_RULES if r["category"] == category]
