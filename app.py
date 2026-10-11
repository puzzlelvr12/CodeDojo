"""
app.py - CodeDojo: Gamified Offline Coding Interview Preparation Web App
Built with Streamlit, Python, Google Gemini API, and SQLite.
"""

import datetime
import html
import time
from typing import Any, Dict, List, Optional

import streamlit as st

import database
import gemini_npc
import lessons
import problems
import styles
import test_runner

# =========================================================================
# STREAMLIT CONFIGURATION
# =========================================================================
st.set_page_config(
    page_title="CodeDojo // Retro Arcade Interview Academy",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database
database.init_db()

# Inject Retro Arcade CSS & Audio Synth
st.markdown(styles.get_retro_css(), unsafe_allow_html=True)
st.markdown(styles.get_retro_audio_synth_script(), unsafe_allow_html=True)


# =========================================================================
# SESSION STATE INITIALIZATION
# =========================================================================
if "active_problem_id" not in st.session_state:
    st.session_state["active_problem_id"] = "two_sum"

if "active_lesson_id" not in st.session_state:
    st.session_state["active_lesson_id"] = "arrays_two_pointers"

if "app_mode" not in st.session_state:
    st.session_state["app_mode"] = "⚔️ Practice Dojo"

if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = ""

if "editor_type" not in st.session_state:
    st.session_state["editor_type"] = "Arcade Ace Editor"

if "last_test_results" not in st.session_state:
    st.session_state["last_test_results"] = None

# Timed Quiz State
if "quiz_active" not in st.session_state:
    st.session_state["quiz_active"] = False
if "quiz_start_time" not in st.session_state:
    st.session_state["quiz_start_time"] = None
if "quiz_time_limit_sec" not in st.session_state:
    st.session_state["quiz_time_limit_sec"] = 600
if "quiz_problem_id" not in st.session_state:
    st.session_state["quiz_problem_id"] = "trapping_rain_water"
if "quiz_status_msg" not in st.session_state:
    st.session_state["quiz_status_msg"] = None

# Level-up & Victory banners
if "level_up_alert" not in st.session_state:
    st.session_state["level_up_alert"] = None
if "new_achievement_alert" not in st.session_state:
    st.session_state["new_achievement_alert"] = []


# =========================================================================
# HELPER FUNCTIONS
# =========================================================================
def get_user_code(problem_id: str, default_code: str) -> str:
    key = f"code_buffer_{problem_id}"
    if key not in st.session_state or not st.session_state[key]:
        st.session_state[key] = default_code
    return st.session_state[key]


def set_user_code(problem_id: str, code: str):
    key = f"code_buffer_{problem_id}"
    st.session_state[key] = code


def trigger_audio(event_type: str):
    """Triggers synthesized 8-bit Web Audio in browser."""
    script = f"<script>if(window.CodeDojoAudio) window.CodeDojoAudio.{event_type}();</script>"
    st.markdown(script, unsafe_allow_html=True)


# =========================================================================
# SIDEBAR: PLAYER PROFILE, NAVIGATION & SETTINGS
# =========================================================================
profile = database.get_user_profile()

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 16px 0;">
        <span class="pixel-font" style="font-size: 20px; color: var(--neon-cyan); text-shadow: 0 0 12px var(--neon-cyan);">
            ⚔️ CODEDOJO
        </span>
        <div style="font-size: 11px; color: var(--neon-pink); letter-spacing: 2px; margin-top: 4px;">
            // RETRO ARCADE ACADEMY //
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Player Rank & Level Badge
    st.markdown(f"""
    <div class="cyber-card" style="padding: 14px; text-align: center; border-color: {profile['rank_color']};">
        <div style="font-size: 28px; margin-bottom: 4px;">{profile['rank_icon']}</div>
        <div class="pixel-font" style="font-size: 13px; color: {profile['rank_color']}; margin-bottom: 4px;">
            {profile['rank_name']}
        </div>
        <div style="font-size: 13px; color: var(--text-secondary);">
            Rank Tier: <b style="color: #fff;">{profile['rank_tier']}</b> | Level: <b style="color: var(--neon-cyan);">{profile['level']}</b>
        </div>
        <div class="xp-bar-container">
            <div class="xp-bar-fill" style="width: {profile['progress_pct']}%;"></div>
            <div class="xp-bar-label">{profile['xp']} XP / {profile['next_level_xp']} XP</div>
        </div>
        <div style="display: flex; justify-content: space-around; font-size: 12px; margin-top: 8px;">
            <span>🔥 Streak: <b>{profile['streak']}d</b></span>
            <span>⚔️ Solved: <b>{profile['total_solved']}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Modes
    st.markdown("### 🕹️ Mission Mode")
    app_modes = [
        "⚔️ Practice Dojo",
        "📚 Code School Curriculum",
        "⏱️ Timed Trials (Pressure)",
        "📊 Hall of Fame & Stats",
    ]
    selected_mode = st.radio(
        "Choose Mode:",
        app_modes,
        index=app_modes.index(st.session_state["app_mode"]) if st.session_state["app_mode"] in app_modes else 0,
        label_visibility="collapsed",
    )
    if selected_mode != st.session_state["app_mode"]:
        st.session_state["app_mode"] = selected_mode
        st.rerun()

    st.markdown("---")

    # Cyber Sensei API Configuration
    st.markdown("### 🤖 Cyber Sensei AI Link")
    api_key_input = st.text_input(
        "Google AI Studio Key:",
        value=st.session_state["gemini_api_key"],
        type="password",
        placeholder="Paste AI Studio API key...",
        help="Free Google Gemini API key. Enables live dynamic neural mentorship. If blank, offline curated wisdom is used.",
    )
    if api_key_input != st.session_state["gemini_api_key"]:
        st.session_state["gemini_api_key"] = api_key_input

    if st.session_state["gemini_api_key"]:
        st.markdown("""
        <div style="font-size: 11px; color: var(--neon-green); margin-top: -6px;">
            ● Gemini 2.5 Flash Online (Live Neural Link)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-size: 11px; color: var(--neon-yellow); margin-top: -6px;">
            ● Offline Vault Active (<a href="https://aistudio.google.com/app/apikey" target="_blank" style="color: var(--neon-cyan);">Get free key</a>)
        </div>
        """, unsafe_allow_html=True)

    # Editor Preferences
    st.markdown("### ⚙️ Dojo Settings")
    st.session_state["editor_type"] = st.selectbox(
        "Code Editor Engine:",
        ["Arcade Ace Editor", "Classic Monospace Editor"],
        index=0 if st.session_state["editor_type"] == "Arcade Ace Editor" else 1,
    )

    if st.button("🗑️ Reset All Progress", help="Wipes local database progress and restarts from Level 1."):
        database.reset_user_progress()
        st.success("Progress wiped! Restarting Dojo...")
        time.sleep(1)
        st.rerun()


# =========================================================================
# TOP HEADER HUD (ARCADE MARQUEE)
# =========================================================================
current_problem = problems.get_problem_by_id(st.session_state["active_problem_id"])

st.markdown(f"""
<div class="arcade-header-container">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
            <span class="pixel-font" style="font-size: 16px; color: var(--neon-cyan);">
                CODEDOJO
            </span>
            <span style="color: var(--neon-pink); font-weight: bold; margin: 0 8px;">//</span>
            <span style="font-size: 15px; font-weight: 600; color: #f8fafc;">
                {st.session_state["app_mode"]}
            </span>
        </div>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <div class="hud-pill highlight-cyan">
                <span>{profile['rank_icon']} {profile['rank_name']} (Lvl {profile['level']})</span>
            </div>
            <div class="hud-pill highlight-green">
                <span>⚡ {profile['xp']} XP</span>
            </div>
            <div class="hud-pill highlight-yellow">
                <span>🔥 {profile['streak']} Day Streak</span>
            </div>
            <div class="hud-pill highlight-pink">
                <span>🎯 Target: {current_problem['title']}</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Level Up & Achievement Notifications
if st.session_state.get("level_up_alert"):
    st.balloons()
    trigger_audio("levelup")
    st.markdown(f"""
    <div class="cyber-card pulse-glow" style="border-color: var(--neon-yellow); background: rgba(255, 230, 0, 0.15); text-align: center;">
        <span class="pixel-font" style="font-size: 18px; color: var(--neon-yellow);">
            ⚡ LEVEL UP! YOU ARE NOW LEVEL {st.session_state['level_up_alert']}! ⚡
        </span>
        <div style="margin-top: 6px; font-size: 14px;">Your algorithmic potency expands across the Dojo matrix!</div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state["level_up_alert"] = None

if st.session_state.get("new_achievement_alert"):
    for ach in st.session_state["new_achievement_alert"]:
        st.markdown(f"""
        <div class="cyber-card" style="border-color: var(--neon-green); background: rgba(0, 255, 136, 0.15);">
            <b style="color: var(--neon-green); font-size: 16px;">🏆 ACHIEVEMENT UNLOCKED: {ach['icon']} {ach['name']}</b>
            <div style="font-size: 13px; color: #e2e8f0; margin-top: 4px;">{ach['description']} (+{ach['xp_reward']} Bonus XP)</div>
        </div>
        """, unsafe_allow_html=True)
    st.session_state["new_achievement_alert"] = []


# =========================================================================
# SPLIT WORKSPACE: LEFT (MAIN WORKSPACE) vs RIGHT (CYBER SENSEI NPC)
# =========================================================================
col_workspace, col_npc = st.columns([68, 32], gap="large")


# =========================================================================
# RIGHT COLUMN: CYBER SENSEI NPC & HINT BOX
# =========================================================================
with col_npc:
    is_boss = current_problem["difficulty"] == "Hard"
    card_glow = "pulse-boss-glow" if is_boss else "pulse-glow"
    card_border = "var(--neon-pink)" if is_boss else "var(--neon-cyan)"

    st.markdown(f"""
    <div class="cyber-card {card_glow}" style="border-color: {card_border}; padding: 16px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 34px;">🤖</div>
            <div>
                <div class="pixel-font" style="font-size: 13px; color: var(--neon-cyan);">
                    CYBER SENSEI NPC
                </div>
                <div style="font-size: 11px; color: var(--neon-green); letter-spacing: 1px;">
                    ● STATUS: ONLINE // INTEL READY
                </div>
            </div>
        </div>
        <div style="margin-top: 10px; font-size: 12px; color: var(--text-secondary); line-height: 1.4;">
            <i>"The matrix rewards independent grit. Seeking divine intervention costs XP bounty!"</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # XP Penalty Tier Actions
    st.markdown("#### ⚡ Request Tactical Intel")
    st.markdown("""
    <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 8px;">
        Each tier of assistance deducts XP to encourage self-reliance:
    </div>
    """, unsafe_allow_html=True)

    c_hint1, c_hint2, c_hint3 = st.columns(3)
    user_current_code = get_user_code(current_problem["id"], current_problem["starter_code"])

    with c_hint1:
        if st.button("💡 Nudge\n(-10 XP)", help="Subconscious intuition clue without code (-10 XP)", use_container_width=True):
            if profile["xp"] < 10:
                st.warning("Insufficient XP to spend on a nudge!")
            else:
                trigger_audio("hint")
                new_xp = database.deduct_xp_for_hint(10)
                resp, _ = gemini_npc.generate_sensei_response(
                    mode="nudge",
                    problem_meta=current_problem,
                    user_code=user_current_code,
                    api_key=st.session_state["gemini_api_key"],
                    player_rank=profile["rank_name"],
                    player_level=profile["level"],
                )
                database.add_chat_message(current_problem["id"], "User", "Requested: Subconscious Nudge", 10)
                database.add_chat_message(current_problem["id"], "Sensei", resp, 0)
                st.rerun()

    with c_hint2:
        if st.button("🔍 Blueprint\n(-25 XP)", help="Algorithmic steps, Big-O, and edge cases (-25 XP)", use_container_width=True):
            if profile["xp"] < 25:
                st.warning("Insufficient XP to spend on a blueprint!")
            else:
                trigger_audio("hint")
                new_xp = database.deduct_xp_for_hint(25)
                resp, _ = gemini_npc.generate_sensei_response(
                    mode="blueprint",
                    problem_meta=current_problem,
                    user_code=user_current_code,
                    api_key=st.session_state["gemini_api_key"],
                    player_rank=profile["rank_name"],
                    player_level=profile["level"],
                )
                database.add_chat_message(current_problem["id"], "User", "Requested: Algorithmic Blueprint", 25)
                database.add_chat_message(current_problem["id"], "Sensei", resp, 0)
                st.rerun()

    with c_hint3:
        if st.button("⚔️ Scroll\n(-60 XP)", help="Full canonical reference code and line explanation (-60 XP)", use_container_width=True):
            if profile["xp"] < 60:
                st.warning("Insufficient XP to spend on the Master Scroll!")
            else:
                trigger_audio("hint")
                new_xp = database.deduct_xp_for_hint(60)
                resp, _ = gemini_npc.generate_sensei_response(
                    mode="master_scroll",
                    problem_meta=current_problem,
                    user_code=user_current_code,
                    api_key=st.session_state["gemini_api_key"],
                    player_rank=profile["rank_name"],
                    player_level=profile["level"],
                )
                database.add_chat_message(current_problem["id"], "User", "Requested: Master Scroll (Full Solution)", 60)
                database.add_chat_message(current_problem["id"], "Sensei", resp, 0)
                st.rerun()

    st.markdown("---")

    # Terminal Chat Transcript
    st.markdown(f"""
    <div class="terminal-header">
        <span>COMM_LINK: {current_problem['id']}</span>
        <span>ACTIVE BUFFER</span>
    </div>
    """, unsafe_allow_html=True)

    chat_history = database.get_chat_history(problem_id=current_problem["id"], limit=12)

    terminal_html = '<div class="terminal-window" style="max-height: 380px; overflow-y: auto; margin-bottom: 12px;">'
    if not chat_history:
        terminal_html += f"""
        <div style="font-size: 12px; color: var(--text-muted); text-align: center; padding: 20px 0;">
            [TERMINAL IDLE]<br>
            Awaiting transmissions regarding <b>{current_problem['title']}</b>.<br>
            Request a hint above or transmit a custom query below.
        </div>
        """
    else:
        for msg in chat_history:
            if msg["role"] == "User":
                cost_tag = f" <span style='color: var(--neon-pink);'>(-{msg['xp_cost']} XP)</span>" if msg["xp_cost"] > 0 else ""
                escaped_text = html.escape(msg['content']).replace('\n', '<br>')
                terminal_html += f"""
                <div class="terminal-bubble-user">
                    <b>INITIATE:</b>{cost_tag}<br>{escaped_text}
                </div>
                """
            else:
                # Sensei message
                clean_text = msg["content"].replace("\n", "<br>")
                terminal_html += f"""
                <div class="terminal-bubble-sensei">
                    <b>CYBER SENSEI:</b><br>{clean_text}
                </div>
                """
    terminal_html += '</div>'
    st.markdown(terminal_html, unsafe_allow_html=True)

    # Chat Input
    with st.form("sensei_chat_form", clear_on_submit=True):
        chat_query = st.text_input(
            "Transmit to Cyber Sensei (Free 0 XP):",
            placeholder="e.g. Why is my solution timing out?",
            label_visibility="collapsed",
        )
        submitted_chat = st.form_submit_button("⚡ Transmit Query")
        if submitted_chat and chat_query.strip():
            trigger_audio("click")
            resp, _ = gemini_npc.generate_sensei_response(
                mode="chat",
                problem_meta=current_problem,
                user_code=user_current_code,
                user_query=chat_query.strip(),
                api_key=st.session_state["gemini_api_key"],
                player_rank=profile["rank_name"],
                player_level=profile["level"],
            )
            database.add_chat_message(current_problem["id"], "User", chat_query.strip(), 0)
            database.add_chat_message(current_problem["id"], "Sensei", resp, 0)
            st.rerun()


# =========================================================================
# LEFT COLUMN: MAIN WORKSPACE (PRACTICE, CURRICULUM, TIMED QUIZ, STATS)
# =========================================================================
with col_workspace:

    # ---------------------------------------------------------------------
    # MODE 1: PRACTICE DOJO
    # ---------------------------------------------------------------------
    if st.session_state["app_mode"] == "⚔️ Practice Dojo":
        # Problem Filter Controls
        f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 3])
        with f_col1:
            diff_filter = st.selectbox("Difficulty:", ["All", "Easy", "Medium", "Hard"])
        with f_col2:
            all_cats = ["All"] + sorted(list({p["category"] for p in problems.get_all_problems()}))
            cat_filter = st.selectbox("Category:", all_cats)

        # Filter problem list
        candidate_problems = problems.get_all_problems()
        if diff_filter != "All":
            candidate_problems = [p for p in candidate_problems if p["difficulty"] == diff_filter]
        if cat_filter != "All":
            candidate_problems = [p for p in candidate_problems if p["category"] == cat_filter]

        solved_ids = set(database.get_all_solved_problem_ids())

        # Select Problem
        problem_options = {}
        for p in candidate_problems:
            status_icon = "✅" if p["id"] in solved_ids else ("👹" if p["difficulty"] == "Hard" else "⚔️")
            problem_options[f"{status_icon} {p['title']} ({p['difficulty']})"] = p["id"]

        with f_col3:
            current_choice_idx = 0
            for idx, (lbl, pid) in enumerate(problem_options.items()):
                if pid == st.session_state["active_problem_id"]:
                    current_choice_idx = idx
                    break

            chosen_label = st.selectbox(
                "Select Dojo Challenge:",
                list(problem_options.keys()),
                index=current_choice_idx if current_choice_idx < len(problem_options) else 0,
            )
            if chosen_label:
                selected_pid = problem_options[chosen_label]
                if selected_pid != st.session_state["active_problem_id"]:
                    st.session_state["active_problem_id"] = selected_pid
                    st.session_state["last_test_results"] = None
                    st.rerun()

        prob = problems.get_problem_by_id(st.session_state["active_problem_id"])
        is_solved = prob["id"] in solved_ids
        diff_badge = f"badge-{prob['difficulty'].lower()}"

        # Problem Header Card
        st.markdown(f"""
        <div class="cyber-card" style="margin-top: 10px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span class="pixel-font" style="font-size: 15px; color: var(--neon-cyan);">
                        {prob['boss_title']}
                    </span>
                    <h2 style="margin: 4px 0 0 0; font-size: 24px; color: #ffffff;">
                        {prob['title']}
                    </h2>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span class="{diff_badge}">{prob['difficulty']}</span>
                    <span class="hud-pill" style="font-size: 12px;">📁 {prob['category']}</span>
                    <span class="hud-pill highlight-yellow" style="font-size: 12px;">💰 +{prob['xp']} XP</span>
                    {'<span class="hud-pill highlight-green">✅ SOLVED</span>' if is_solved else '<span class="hud-pill">⏳ UNSOLVED</span>'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Tabs for Problem Details vs Solution vs Test Cases
        p_tab1, p_tab2, p_tab3 = st.tabs(["🎯 Problem Statement", "📜 Official Solution Guide", "🧪 Visible Test Cases"])

        with p_tab1:
            st.markdown(prob["description"])

        with p_tab2:
            if is_solved or st.session_state.get(f"unlocked_sol_{prob['id']}"):
                st.markdown(prob["solution_explanation"])
                st.code(prob["solution_code"], language="python")
            else:
                st.info("🔒 Solve this problem or consult Cyber Sensei's Master Scroll to view the official solution breakdown.")
                if st.button("🔓 Unlock Solution Now (-60 XP)", key=f"unlock_sol_btn_{prob['id']}"):
                    if profile["xp"] < 60:
                        st.warning("Insufficient XP!")
                    else:
                        database.deduct_xp_for_hint(60)
                        st.session_state[f"unlocked_sol_{prob['id']}"] = True
                        st.rerun()

        with p_tab3:
            st.markdown("### 🧪 Visible Sample Test Cases")
            for idx, tc in enumerate(prob["sample_tests"]):
                st.markdown(f"**Test Case {idx + 1}:**")
                st.code(f"Input: {tc.get('display_input', tc['input'])}\nExpected Output: {tc['expected']}", language="python")

        st.markdown("---")

        # Code Editor Section
        st.markdown("### 💻 Cyberpunk Code Editor")
        current_code = get_user_code(prob["id"], prob["starter_code"])

        # Editor rendering
        if st.session_state["editor_type"] == "Arcade Ace Editor":
            try:
                from code_editor import code_editor
                custom_btns = [
                    {
                        "name": "Reset",
                        "feather": "RotateCcw",
                        "primary": False,
                        "hasText": True,
                        "showWithIcon": True,
                        "commands": ["submit"],
                        "style": {"bottom": "0.44rem", "right": "0.44rem"},
                    }
                ]
                editor_response = code_editor(
                    current_code,
                    lang="python",
                    theme="monokai",
                    height=22,
                    key=f"editor_component_{prob['id']}",
                )
                if editor_response and isinstance(editor_response, dict) and editor_response.get("text"):
                    set_user_code(prob["id"], editor_response["text"])
                    current_code = editor_response["text"]
            except Exception:
                # Fallback to text_area
                current_code = st.text_area(
                    "Python Code:",
                    value=current_code,
                    height=320,
                    key=f"code_ta_{prob['id']}",
                    label_visibility="collapsed",
                )
                set_user_code(prob["id"], current_code)
        else:
            current_code = st.text_area(
                "Python Code:",
                value=current_code,
                height=320,
                key=f"code_ta_{prob['id']}",
                label_visibility="collapsed",
            )
            set_user_code(prob["id"], current_code)

        # Editor Action Bar
        act_col1, act_col2, act_col3 = st.columns([1.5, 2, 1.5])
        with act_col1:
            run_sample_btn = st.button("▶️ Run Tests (Visible)", use_container_width=True)
        with act_col2:
            submit_btn = st.button("🚀 Submit Solution (Full Suite)", type="primary", use_container_width=True)
        with act_col3:
            if st.button("🔄 Reset Code", use_container_width=True):
                set_user_code(prob["id"], prob["starter_code"])
                st.session_state["last_test_results"] = None
                st.rerun()

        # Handle Run Tests
        if run_sample_btn:
            trigger_audio("click")
            with st.spinner("Evaluating against visible test cases..."):
                results = test_runner.run_all_tests(current_code, prob, only_visible=True)
                st.session_state["last_test_results"] = results
                if results["all_passed"]:
                    trigger_audio("pass")
                else:
                    trigger_audio("fail")

        # Handle Submit Solution
        if submit_btn:
            trigger_audio("click")
            with st.spinner("Executing full test suite against hidden edge cases..."):
                results = test_runner.run_all_tests(current_code, prob, only_visible=False)
                st.session_state["last_test_results"] = results

                if results["all_passed"]:
                    trigger_audio("pass")
                    # Award XP & Record in database
                    is_first = database.record_solved_problem(
                        problem_id=prob["id"],
                        title=prob["title"],
                        difficulty=prob["difficulty"],
                        category=prob["category"],
                        xp_earned=prob["xp"],
                        hints_used=0,
                        code=current_code,
                    )
                    new_xp, level_up = database.add_xp(prob["xp"])
                    if level_up:
                        st.session_state["level_up_alert"] = database.calculate_level_from_xp(new_xp)

                    unlocked = database.check_and_unlock_achievements()
                    if unlocked:
                        st.session_state["new_achievement_alert"] = unlocked

                    st.balloons()
                    st.success(f"🎉 VICTORY! All {results['total_count']} tests passed! +{prob['xp']} XP awarded!")
                else:
                    trigger_audio("fail")
                    st.error(f"❌ Submission Failed! Passed {results['passed_count']}/{results['total_count']} tests.")

        # Render Test Results Table
        if st.session_state["last_test_results"]:
            res = st.session_state["last_test_results"]
            st.markdown("### 📊 Test Case Results")

            summary_color = "var(--neon-green)" if res["all_passed"] else "var(--neon-pink)"
            status_text = "ALL TESTS PASSED" if res["all_passed"] else f"FAILED ({res['passed_count']}/{res['total_count']} Passed)"

            st.markdown(f"""
            <div style="background: rgba(14, 18, 36, 0.9); border: 1px solid {summary_color}; border-radius: 6px; padding: 12px 18px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: {summary_color}; font-weight: bold; font-size: 16px;">
                    {status_text}
                </span>
                <span class="terminal-font" style="font-size: 13px; color: var(--text-secondary);">
                    Total Runtime: {res['total_time_ms']} ms
                </span>
            </div>
            """, unsafe_allow_html=True)

            # Details
            for r in res["results"]:
                t_status_color = "var(--neon-green)" if r["passed"] else "var(--neon-pink)"
                t_badge = "✅ PASSED" if r["passed"] else "❌ FAILED"
                if r["status"] == "ERROR":
                    t_badge = "⚠️ ERROR"
                elif r["status"] == "TIMEOUT":
                    t_badge = "⏱️ TIMEOUT"

                with st.expander(f"Test #{r['test_num']}: {t_badge} ({r['time_ms']} ms)", expanded=not r["passed"]):
                    st.markdown(f"**Input:** `{r['input_repr']}`")
                    st.markdown(f"**Expected:** `{r['expected']}`")
                    st.markdown(f"**Actual Output:** `{r['actual']}`")
                    if r.get("stdout"):
                        st.markdown(f"**Stdout Log:**\n```\n{r['stdout']}\n```")
                    if r.get("error"):
                        st.markdown(f"**Error Traceback:**\n```\n{r['error']}\n```")

    # ---------------------------------------------------------------------
    # MODE 2: CODE SCHOOL CURRICULUM
    # ---------------------------------------------------------------------
    elif st.session_state["app_mode"] == "📚 Code School Curriculum":
        st.markdown("""
        <div class="cyber-card" style="margin-bottom: 16px;">
            <div class="pixel-font" style="font-size: 15px; color: var(--neon-cyan);">
                CODEDOJO ACADEMY // DEEP-DIVE CURRICULUM
            </div>
            <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
                Internalize the core mental models, Big-O tables, and common interview trap patterns before battle.
            </div>
        </div>
        """, unsafe_allow_html=True)

        all_lessons_list = lessons.get_all_lessons()
        lesson_titles = [f"{l['icon']} {l['title']}" for l in all_lessons_list]
        lesson_ids = [l["id"] for l in all_lessons_list]

        curr_lesson_idx = 0
        if st.session_state["active_lesson_id"] in lesson_ids:
            curr_lesson_idx = lesson_ids.index(st.session_state["active_lesson_id"])

        chosen_lesson_title = st.selectbox(
            "Select Curriculum Topic:",
            lesson_titles,
            index=curr_lesson_idx,
        )
        selected_lesson_id = lesson_ids[lesson_titles.index(chosen_lesson_title)]
        if selected_lesson_id != st.session_state["active_lesson_id"]:
            st.session_state["active_lesson_id"] = selected_lesson_id
            st.rerun()

        active_lesson = lessons.get_lesson_by_id(st.session_state["active_lesson_id"])

        # Display lesson content
        st.markdown(active_lesson["content"])

        # Related Dojo Challenges quick links
        st.markdown("---")
        st.markdown("### ⚔️ Practice Challenges for this Topic:")
        rel_cols = st.columns(len(active_lesson.get("related_problems", [])) or 1)
        for idx, pid in enumerate(active_lesson.get("related_problems", [])):
            rel_prob = problems.get_problem_by_id(pid)
            with rel_cols[idx]:
                if st.button(f"Jump to: {rel_prob['title']} ({rel_prob['difficulty']})", key=f"jump_{pid}", use_container_width=True):
                    st.session_state["active_problem_id"] = pid
                    st.session_state["app_mode"] = "⚔️ Practice Dojo"
                    st.rerun()

    # ---------------------------------------------------------------------
    # MODE 3: TIMED CODING QUIZZES (PRESSURE / COUNTDOWN)
    # ---------------------------------------------------------------------
    elif st.session_state["app_mode"] == "⏱️ Timed Trials (Pressure)":
        st.markdown("""
        <div class="cyber-card" style="margin-bottom: 16px; border-color: var(--neon-pink);">
            <div class="pixel-font" style="font-size: 15px; color: var(--neon-pink);">
                ⏱️ TIMED TRIAL // BOSS RUSH UNDER PRESSURE
            </div>
            <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
                Simulate real technical interview time constraints. Solve before the countdown expires!
                <br><b>Rule:</b> Passing within time grants +Speed Run Multiplier. Running out of time deducts -30 XP!
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quiz Setup / Active State
        if not st.session_state["quiz_active"]:
            q_col1, q_col2, q_col3 = st.columns([2, 2, 2])
            with q_col1:
                quiz_prob_choice = st.selectbox(
                    "Challenge to Speedrun:",
                    [f"{p['title']} ({p['difficulty']})" for p in problems.get_all_problems()],
                    index=0,
                )
                chosen_q_title = quiz_prob_choice.split(" (")[0]
                q_prob = [p for p in problems.get_all_problems() if p["title"] == chosen_q_title][0]
                st.session_state["quiz_problem_id"] = q_prob["id"]

            with q_col2:
                time_choice = st.selectbox(
                    "Time Constraint:",
                    ["5 Minutes (Sprint)", "10 Minutes (Standard)", "15 Minutes (Boss)", "20 Minutes (Marathon)"],
                    index=1,
                )
                mins = int(time_choice.split(" ")[0])
                st.session_state["quiz_time_limit_sec"] = mins * 60

            with q_col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔥 START TIMED TRIAL", type="primary", use_container_width=True):
                    trigger_audio("pass")
                    st.session_state["quiz_active"] = True
                    st.session_state["quiz_start_time"] = time.time()
                    st.session_state["active_problem_id"] = q_prob["id"]
                    st.rerun()

        else:
            # Active Quiz Countdown Loop
            q_prob = problems.get_problem_by_id(st.session_state["quiz_problem_id"])
            elapsed = time.time() - st.session_state["quiz_start_time"]
            remaining = max(0, int(st.session_state["quiz_time_limit_sec"] - elapsed))

            mins_left = remaining // 60
            secs_left = remaining % 60
            timer_color = "var(--neon-green)" if remaining > 120 else ("var(--neon-yellow)" if remaining > 60 else "var(--neon-pink)")
            timer_glow = "pulse-boss-glow" if remaining <= 60 else ""

            # Prominent Countdown Clock Display
            st.markdown(f"""
            <div class="cyber-card {timer_glow}" style="border-color: {timer_color}; text-align: center; padding: 18px; margin-bottom: 16px;">
                <div style="font-size: 13px; color: var(--text-secondary); letter-spacing: 2px;">
                    MISSION TIME REMAINING
                </div>
                <div class="terminal-font" style="font-size: 48px; font-weight: bold; color: {timer_color}; text-shadow: 0 0 15px {timer_color};">
                    {mins_left:02d}:{secs_left:02d}
                </div>
                <div style="font-size: 14px; color: #e2e8f0; margin-top: 4px;">
                    Target: <b>{q_prob['title']}</b> ({q_prob['difficulty']})
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Check for Timeout
            if remaining <= 0:
                trigger_audio("fail")
                st.session_state["quiz_active"] = False
                database.record_quiz_result(
                    problem_id=q_prob["id"],
                    title=q_prob["title"],
                    difficulty=q_prob["difficulty"],
                    time_limit=st.session_state["quiz_time_limit_sec"],
                    time_taken=st.session_state["quiz_time_limit_sec"],
                    passed=False,
                    xp_change=-30,
                )
                st.error("💀 TIME OVER! MISSION FAILED. -30 XP Penalty deducted from your record.")
                time.sleep(2)
                st.rerun()

            # Active Quiz Code Editor
            q_code = get_user_code(q_prob["id"], q_prob["starter_code"])
            q_code = st.text_area(
                "Submit Solution Under Pressure:",
                value=q_code,
                height=300,
                key=f"quiz_code_ta_{q_prob['id']}",
            )
            set_user_code(q_prob["id"], q_code)

            sub_col1, sub_col2 = st.columns([2, 1])
            with sub_col1:
                if st.button("🚀 SUBMIT TRIAL SOLUTION", type="primary", use_container_width=True):
                    trigger_audio("click")
                    results = test_runner.run_all_tests(q_code, q_prob, only_visible=False)
                    time_taken = int(time.time() - st.session_state["quiz_start_time"])

                    if results["all_passed"]:
                        trigger_audio("pass")
                        st.session_state["quiz_active"] = False
                        # Calculate Speed Bonus XP
                        time_left_pct = remaining / st.session_state["quiz_time_limit_sec"]
                        speed_bonus = int(100 * time_left_pct)
                        total_xp = q_prob["xp"] + speed_bonus

                        database.record_quiz_result(
                            problem_id=q_prob["id"],
                            title=q_prob["title"],
                            difficulty=q_prob["difficulty"],
                            time_limit=st.session_state["quiz_time_limit_sec"],
                            time_taken=time_taken,
                            passed=True,
                            xp_change=total_xp,
                        )
                        database.record_solved_problem(
                            problem_id=q_prob["id"],
                            title=q_prob["title"],
                            difficulty=q_prob["difficulty"],
                            category=q_prob["category"],
                            xp_earned=total_xp,
                            hints_used=0,
                            code=q_code,
                        )
                        st.balloons()
                        st.success(f"🏆 MISSION ACCOMPLISHED in {time_taken}s! +{q_prob['xp']} Base XP + {speed_bonus} Speed Bonus XP!")
                        time.sleep(2)
                        st.rerun()
                    else:
                        trigger_audio("fail")
                        st.error(f"❌ Incorrect solution: Passed {results['passed_count']}/{results['total_count']} tests. Timer still running!")

            with sub_col2:
                if st.button("🏳️ Abandon Trial (-30 XP)", use_container_width=True):
                    trigger_audio("fail")
                    st.session_state["quiz_active"] = False
                    database.record_quiz_result(
                        problem_id=q_prob["id"],
                        title=q_prob["title"],
                        difficulty=q_prob["difficulty"],
                        time_limit=st.session_state["quiz_time_limit_sec"],
                        time_taken=int(time.time() - st.session_state["quiz_start_time"]),
                        passed=False,
                        xp_change=-30,
                    )
                    st.warning("Trial abandoned. -30 XP deducted.")
                    time.sleep(1)
                    st.rerun()

    # ---------------------------------------------------------------------
    # MODE 4: HALL OF FAME & STATS
    # ---------------------------------------------------------------------
    elif st.session_state["app_mode"] == "📊 Hall of Fame & Stats":
        st.markdown("""
        <div class="cyber-card" style="margin-bottom: 16px;">
            <div class="pixel-font" style="font-size: 15px; color: var(--neon-cyan);">
                DOJO HALL OF FAME & COMBAT METRICS
            </div>
            <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
                Review your battle history, unlocked achievement trophies, and mastery across algorithmic categories.
            </div>
        </div>
        """, unsafe_allow_html=True)

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Total XP", profile["xp"])
        with m_col2:
            st.metric("Player Level", profile["level"])
        with m_col3:
            st.metric("Daily Streak", f"{profile['streak']} Days")
        with m_col4:
            st.metric("Problems Conquered", profile["total_solved"])

        st.markdown("### 🏆 Achievement Trophy Room")
        all_ach = database.get_all_achievements()

        ach_cols = st.columns(3)
        for idx, ach in enumerate(all_ach):
            with ach_cols[idx % 3]:
                if ach["unlocked"]:
                    st.markdown(f"""
                    <div class="cyber-card" style="border-color: var(--neon-green); padding: 14px; text-align: center;">
                        <div style="font-size: 32px;">{ach['icon']}</div>
                        <div class="pixel-font" style="font-size: 12px; color: var(--neon-green); margin: 6px 0;">
                            {ach['name']}
                        </div>
                        <div style="font-size: 12px; color: #e2e8f0;">{ach['description']}</div>
                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 6px;">
                            Unlocked: {ach['unlocked_at'][:10]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="cyber-card" style="border-color: #2a3456; opacity: 0.6; padding: 14px; text-align: center;">
                        <div style="font-size: 32px; filter: grayscale(100%);">🔒</div>
                        <div class="pixel-font" style="font-size: 12px; color: var(--text-muted); margin: 6px 0;">
                            {ach['name']}
                        </div>
                        <div style="font-size: 12px; color: var(--text-muted);">{ach['description']}</div>
                        <div style="font-size: 11px; color: var(--neon-yellow); margin-top: 6px;">
                            +{ach['xp_reward']} XP Bounty
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ⏱️ Timed Trial Quiz History")
        quiz_hist = database.get_quiz_history(limit=10)
        if quiz_hist:
            for q in quiz_hist:
                status_icon = "✅ PASSED" if q["passed"] else "❌ FAILED"
                st.markdown(f"- **{q['problem_title']}** ({q['difficulty']}): {status_icon} | Time: {q['time_taken_sec']}s / {q['time_limit_sec']}s | XP: `{q['xp_change']:+d}` | Date: `{q['completed_at'][:19]}`")
        else:
            st.info("No timed trials recorded yet. Enter '⏱️ Timed Trials' mode to test your speed!")

        st.markdown("---")
        st.markdown("### 📜 Solved Problems Log")
        solved_details = database.get_solved_problems_detailed()
        if solved_details:
            for s in solved_details:
                st.markdown(f"- **{s['problem_title']}** ({s['difficulty']}) - *{s['category']}* | Earned: `+{s['xp_earned']} XP` | Solved: `{s['solved_at'][:19]}`")
        else:
            st.info("No problems solved yet. Enter the Practice Dojo to conquer your first problem!")
