"""
gemini_npc.py - AI Assistant "Cyber Sensei" NPC Box
Powered by Google Gemini API (using google-genai SDK) with offline fallback intelligence,
custom prompt engineering, and XP deduction integration.
"""

import os
from typing import Any, Dict, Optional, Tuple

HINT_COSTS = {
    "nudge": 10,
    "blueprint": 25,
    "master_scroll": 60,
    "chat": 0,
}

SYSTEM_INSTRUCTION = """You are CYBER SENSEI, an elite arcade grandmaster NPC in the retro cyberpunk coding dojo 'CodeDojo'.
Your mission is to forge the user into an unstoppable technical interview ninja.
You speak with a cool, sharp cyberpunk mentor persona (drawing subtle metaphors from cyberspace, matrix, scrolls, bytecode, dojos, and martial discipline).
Keep answers punchy, well-structured, formatted in clear markdown, and concise (interviewers value clarity and conciseness).

Strict Hint Guidelines based on requested mode:
1. Subconscious Nudge: DO NOT write code. DO NOT reveal the direct formula. Ask a provocative question or point out an invariant to trigger an aha moment.
2. Algorithmic Blueprint: Give step-by-step logical bullet points, Big-O trade-offs, and critical edge cases. Do NOT write full code blocks.
3. Master Scroll: Provide the clean, battle-tested reference Python code with concise annotations and line-by-line insight.
4. General Chat / Debugging: Help the user analyze their thought process, spot bugs in their submitted code, or explain Big-O concepts.
"""


def get_gemini_client(api_key: Optional[str] = None):
    """
    Creates a Google GenAI client using the provided key, environment variable, or secrets.
    """
    effective_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not effective_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=effective_key)
        return client
    except Exception:
        return None


def generate_sensei_response(
    mode: str,
    problem_meta: Optional[Dict[str, Any]],
    user_code: str = "",
    user_query: str = "",
    api_key: Optional[str] = None,
    player_rank: str = "Bronze Ninja",
    player_level: int = 1,
) -> Tuple[str, int]:
    """
    Generates a response from Cyber Sensei using Gemini API (or curated offline wisdom fallback).
    Returns (response_text, xp_cost).
    """
    xp_cost = HINT_COSTS.get(mode, 0)
    p_title = problem_meta.get("title", "Unknown Challenge") if problem_meta else "General Dojo Inquiry"
    p_diff = problem_meta.get("difficulty", "Core") if problem_meta else "General"
    p_category = problem_meta.get("category", "Algorithms") if problem_meta else "General"

    # Check for live Gemini API client
    client = get_gemini_client(api_key)

    if client:
        try:
            from google.genai import types

            if mode == "nudge":
                user_prompt = f"""[MODE: Subconscious Nudge]
Player Rank: {player_rank} (Level {player_level})
Active Problem: {p_title} ({p_diff} - {p_category})
User's Current Code:
```python
{user_code.strip() or '# No code written yet'}
```
Give me a subtle Socratic nudge or question to guide my intuition without revealing the solution or code."""

            elif mode == "blueprint":
                user_prompt = f"""[MODE: Algorithmic Blueprint]
Player Rank: {player_rank} (Level {player_level})
Active Problem: {p_title} ({p_diff} - {p_category})
User's Current Code:
```python
{user_code.strip() or '# No code written yet'}
```
Provide the algorithmic blueprint in clean bullet points: data structures to use, step-by-step logic, Time/Space Big-O, and edge cases to watch for. No full code."""

            elif mode == "master_scroll":
                user_prompt = f"""[MODE: Master Scroll]
Player Rank: {player_rank} (Level {player_level})
Active Problem: {p_title} ({p_diff} - {p_category})
Reveal the canonical Master Scroll Python solution for this problem with an annotated walkthrough of why it achieves optimal Big-O."""

            else:
                user_prompt = f"""[MODE: Cyber Sensei Terminal Chat]
Player Rank: {player_rank} (Level {player_level})
Active Problem: {p_title} ({p_diff} - {p_category})
User's Code in Editor:
```python
{user_code.strip() or '# Empty'}
```
User's Query:
{user_query}
Provide direct, razor-sharp advice."""

            # Attempt Gemini generation with 2.5-flash / fallback
            model_name = "gemini-2.5-flash"
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    ),
                )
                if response and response.text:
                    return response.text, xp_cost
            except Exception:
                # Fallback to gemini-2.0-flash if 2.5 unavailable
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    ),
                )
                if response and response.text:
                    return response.text, xp_cost

        except Exception as e:
            # Fall back to offline engine with notice
            offline_text = get_offline_fallback(mode, problem_meta, user_query)
            return f"*(Live telemetry degraded: {str(e)[:60]}... Switched to Offline Cyber Vault)*\n\n{offline_text}", xp_cost

    # Offline Mode Fallback
    offline_text = get_offline_fallback(mode, problem_meta, user_query)
    return offline_text, xp_cost


def get_offline_fallback(mode: str, problem_meta: Optional[Dict[str, Any]], user_query: str = "") -> str:
    """Provides curated offline advice from problem database when offline or API key absent."""
    if not problem_meta:
        return """🤖 **Cyber Sensei:** "Welcome to the CodeDojo mainframe, initiate! Select any challenge from the problem bank or practice dojo to begin training your algorithmic instincts." """

    hints = problem_meta.get("hints", {})
    title = problem_meta.get("title", "")
    diff = problem_meta.get("difficulty", "")

    if mode == "nudge":
        nudge_content = hints.get("nudge", "Focus on identifying the invariant property that remains constant as you process elements.")
        return f"""🤖 **CYBER SENSEI [SUBCONSCIOUS NUDGE]**
*Target: {title} ({diff})*

> 🧠 **Sensei's Whisper:**
> "{nudge_content}"

*💡 Tip: Ponder this invariant before touching the editor. What state must hold true at every single loop iteration?*"""

    elif mode == "blueprint":
        blueprint_content = hints.get("blueprint", "Break down the problem: define your state representation, evaluate monotonic conditions, and establish clean termination rules.")
        return f"""🤖 **CYBER SENSEI [ALGORITHMIC BLUEPRINT]**
*Target: {title} ({diff})*

### 📐 Tactical Blueprint
{blueprint_content}

### ⚠️ Pitfalls to Avoid:
- Be vigilant of boundary conditions (empty inputs, single elements, negative coordinates).
- Ensure your space complexity does not unintentionally blow up due to memory copying.
"""

    elif mode == "master_scroll":
        master_content = hints.get("master_scroll", "Examine the reference solution and internalize how the pointers or dynamic programming tables interact.")
        ref_code = problem_meta.get("solution_code", "")
        return f"""🤖 **CYBER SENSEI [MASTER SCROLL DEPLOYED]**
*Target: {title} ({diff})*

### 📜 Master Scroll Code:
```python
{ref_code.strip()}
```

### 🧠 Tactical Deconstruction:
{master_content}
"""

    else:
        return f"""🤖 **CYBER SENSEI [OFFLINE VAULT]**
You asked: *"{user_query}"*

I am currently running in **Offline Vault Mode**. To activate live, dynamic neural dialog with me for customized code reviews and line-by-line debugging, provide a free Google AI Studio key in the panel above!

In the meantime, consider:
- Are there redundant recalculations you can cache?
- Can you sort the input first to unlock two-pointer or binary search access?
- Is there an invariant that lets you discard half the candidates at each step?
"""
