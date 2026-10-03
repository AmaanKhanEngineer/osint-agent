# ── 1. IMPORTS & SETUP ──────────────────────────────────────
import os
import json
from dotenv import load_dotenv

load_dotenv()

TARGET_LANGUAGES = {
    "arabic": "Arabic (Middle East: Saudi Arabia, UAE, Egypt, Syria, Iraq, Lebanon)",
    "persian": "Persian/Farsi (Iran, Afghanistan, Tajikistan)",
    "hebrew": "Hebrew (Israel)",
    "turkish": "Turkish (Turkey)",
    "russian": "Russian (Russia, Belarus, Kazakhstan, Ukraine)",
    "chinese_simplified": "Simplified Chinese (mainland China)",
    "chinese_traditional": "Traditional Chinese (Taiwan, Hong Kong)",
    "japanese": "Japanese (Japan)",
    "korean": "Korean (South Korea, North Korea)",
    "spanish": "Spanish (Spain, Latin America)",
    "french": "French (France, West Africa, parts of Europe)",
    "german": "German (Germany, Austria, Switzerland)",
    "portuguese": "Portuguese (Portugal, Brazil)",
    "italian": "Italian (Italy)",
    "ukrainian": "Ukrainian (Ukraine)",
    "hindi": "Hindi (India)",
}

REGION_MAP = {
    "middle_east": ["arabic", "persian", "hebrew", "turkish"],
    "east_asia": ["chinese_simplified", "chinese_traditional", "japanese", "korean"],
    "europe": ["russian", "french", "german", "spanish", "italian", "portuguese", "ukrainian"],
    "south_asia": ["hindi"],
}


def _get_translator_llm():
    """Lazily initialize the translation LLM with multi-provider fallback."""
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if anthropic_key and anthropic_key != "your_anthropic_key_here":
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0.0)
        except Exception:
            pass

    if groq_key and groq_key != "your_groq_key_here":
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.0)
        except Exception:
            pass

    if openai_key and openai_key != "your_openai_key_here":
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        except Exception:
            pass

    return None


# ── 3. LANGUAGE SELECTION ───────────────────────────────────
def _resolve_languages(regions: list) -> list:
    if not regions or "all" in regions:
        return list(TARGET_LANGUAGES.keys())
    languages = []
    for r in regions:
        languages.extend(REGION_MAP.get(r, []))
    return languages


# ── 4. TRANSLATION ──────────────────────────────────────────
def translate_target(target: str, regions: list = None) -> dict:
    """Translate a target name/topic into multiple languages, returning native-script versions."""
    languages_to_use = _resolve_languages(regions or ["all"])
    language_list = ", ".join(languages_to_use)

    llm = _get_translator_llm()
    if llm is None:
        # Fallback if no LLM key is configured yet
        return {
            lang: f"{target} ({lang})" for lang in languages_to_use
        }

    prompt = f"""Translate the target name or topic "{target}" into the following languages. Use the native script for each language (not romanized).

Languages needed: {language_list}

Rules:
1. For person names, transliterate phonetically into the native script of that language.
2. For common names with a known established native form (e.g. Chinese names, Russian politicians), use the established form.
3. For topics/organizations, translate the meaning where possible, otherwise transliterate.
4. If a translation is uncertain, provide your best guess.

Respond ONLY with valid JSON in this exact format:
{{
  "arabic": "...",
  "persian": "...",
  ...
}}

Only include the languages requested. No explanation, no markdown, just JSON."""

    try:
        response = llm.invoke(prompt)
        content = response.content.strip()

        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        return json.loads(content)
    except Exception as e:
        return {"error": f"Could not parse translations: {str(e)}"}


def translate_content_to_english(foreign_text: str, source_language: str = "auto") -> str:
    """Translate foreign-language content to English, preserving names, dates, and facts exactly."""
    if not foreign_text or len(foreign_text.strip()) < 10:
        return foreign_text

    llm = _get_translator_llm()
    if llm is None:
        return f"[Translation offline - LLM key required]\n{foreign_text}"

    prompt = f"""Translate the following text to English. Preserve all names, dates, numbers, and factual details exactly. Do not add commentary, just provide the English translation.

Source language: {source_language}

Text:
{foreign_text[:4000]}

English translation:"""

    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"[Translation error: {str(e)}]\n{foreign_text}"
