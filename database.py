"""
database.py - CodeDojo Gamification Engine
Manages XP, user levels, streaks, problem solving records, quiz history, and achievements using SQLite.
"""

import sqlite3
import datetime
from typing import Dict, List, Optional, Tuple

DB_PATH = "progress.db"

RANKS = [
    {"name": "Bronze Ninja", "tier": "Bronze", "min_level": 1, "max_level": 4, "icon": "🥉", "color": "#cd7f32"},
    {"name": "Silver Ronin", "tier": "Silver", "min_level": 5, "max_level": 9, "icon": "🥈", "color": "#c0c0c0"},
    {"name": "Gold Samurai", "tier": "Gold", "min_level": 10, "max_level": 14, "icon": "🥇", "color": "#ffd700"},
    {"name": "Diamond Shogun", "tier": "Diamond", "min_level": 15, "max_level": 19, "icon": "💎", "color": "#00f0ff"},
    {"name": "Master Boss (Kage)", "tier": "Master", "min_level": 20, "max_level": 999, "icon": "👑", "color": "#ff007f"},
]

ACHIEVEMENT_DEFINITIONS = [
    {
        "id": "first_blood",
        "name": "First Blood",
        "description": "Solved your very first coding challenge in the Dojo.",
        "icon": "🗡️",
        "xp_reward": 50,
    },
    {
        "id": "triple_threat",
        "name": "Triple Combo",
        "description": "Solved 3 coding problems in total.",
        "icon": "⚡",
        "xp_reward": 75,
    },
    {
        "id": "ten_strike",
        "name": "Deca-Decimator",
        "description": "Solved 10 coding problems across the Dojo.",
        "icon": "🔥",
        "xp_reward": 150,
    },
    {
        "id": "boss_slayer_1",
        "name": "Boss Vanquisher",
        "description": "Defeated your first Hard / Boss-Level interview killer problem.",
        "icon": "👹",
        "xp_reward": 200,
    },
    {
        "id": "boss_slayer_all",
        "name": "Grandmaster Slayer",
        "description": "Conquered all 7 Hard / Boss-Level killer problems.",
        "icon": "👑",
        "xp_reward": 500,
    },
    {
        "id": "speed_demon",
        "name": "Speed Demon",
        "description": "Successfully completed a Timed Quiz with time to spare.",
        "icon": "⏱️",
        "xp_reward": 100,
    },
    {
        "id": "streak_master",
        "name": "Daily Discipline",
        "description": "Maintained a daily coding streak of 3 or more days.",
        "icon": "🥋",
        "xp_reward": 120,
    },
    {
        "id": "pure_mind",
        "name": "Pure Mind (No Crutches)",
        "description": "Solved a Medium or Hard problem without taking any AI Sensei hints.",
        "icon": "🧘",
        "xp_reward": 100,
    },
    {
        "id": "gold_rank",
        "name": "Ascended Samurai",
        "description": "Reached Level 10 and unlocked the Gold Samurai rank.",
        "icon": "⚔️",
        "xp_reward": 250,
    },
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL DEFAULT 'CyberNinja',
        xp INTEGER NOT NULL DEFAULT 0,
        level INTEGER NOT NULL DEFAULT 1,
        streak INTEGER NOT NULL DEFAULT 1,
        highest_streak INTEGER NOT NULL DEFAULT 1,
        last_active_date TEXT NOT NULL,
        hints_taken INTEGER NOT NULL DEFAULT 0,
        quizzes_passed INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS solved_problems (
        problem_id TEXT PRIMARY KEY,
        problem_title TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        category TEXT NOT NULL,
        solved_at TEXT NOT NULL,
        xp_earned INTEGER NOT NULL,
        attempts INTEGER NOT NULL DEFAULT 1,
        hints_used INTEGER NOT NULL DEFAULT 0,
        best_code TEXT NOT NULL DEFAULT ''
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id TEXT NOT NULL,
        problem_title TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        time_limit_sec INTEGER NOT NULL,
        time_taken_sec INTEGER NOT NULL,
        passed INTEGER NOT NULL,
        xp_change INTEGER NOT NULL,
        completed_at TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        achievement_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        icon TEXT NOT NULL,
        unlocked_at TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id TEXT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        xp_cost INTEGER NOT NULL DEFAULT 0,
        timestamp TEXT NOT NULL
    );
    """)

    # Ensure initial profile exists
    cursor.execute("SELECT COUNT(*) as count FROM user_profile")
    if cursor.fetchone()["count"] == 0:
        today_str = datetime.date.today().isoformat()
        cursor.execute("""
        INSERT INTO user_profile (id, username, xp, level, streak, highest_streak, last_active_date, hints_taken, quizzes_passed, created_at)
        VALUES (1, 'CyberNinja', 0, 1, 1, 1, ?, 0, 0, ?)
        """, (today_str, datetime.datetime.now().isoformat()))

    conn.commit()
    conn.close()


def calculate_level_from_xp(xp: int) -> int:
    """
    Progressive leveling curve:
    Level 1: 0 XP
    Level 2: 150 XP
    Level 3: 350 XP
    Level 4: 600 XP
    Formula: Level = 1 + int((XP / 120) ** 0.65)
    """
    if xp <= 0:
        return 1
    lvl = 1 + int((xp / 120) ** 0.65)
    return max(1, lvl)


def xp_for_level(lvl: int) -> int:
    """Calculate minimum XP required to achieve level `lvl`."""
    if lvl <= 1:
        return 0
    return int(120 * ((lvl - 1) ** (1 / 0.65)))


def get_rank_info(level: int) -> Dict:
    for rank in RANKS:
        if rank["min_level"] <= level <= rank["max_level"]:
            return rank
    return RANKS[-1]


def get_user_profile() -> Dict:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile WHERE id = 1")
    row = cursor.fetchone()

    today = datetime.date.today()
    today_str = today.isoformat()

    # Calculate streak updates
    streak = row["streak"]
    highest_streak = row["highest_streak"]
    last_active = datetime.date.fromisoformat(row["last_active_date"])
    diff_days = (today - last_active).days

    if diff_days == 1:
        streak += 1
        highest_streak = max(highest_streak, streak)
        cursor.execute("UPDATE user_profile SET streak = ?, highest_streak = ?, last_active_date = ? WHERE id = 1",
                       (streak, highest_streak, today_str))
        conn.commit()
    elif diff_days > 1:
        streak = 1
        cursor.execute("UPDATE user_profile SET streak = 1, last_active_date = ? WHERE id = 1", (today_str,))
        conn.commit()

    xp = row["xp"]
    level = calculate_level_from_xp(xp)
    current_level_min_xp = xp_for_level(level)
    next_level_xp = xp_for_level(level + 1)
    progress_xp = xp - current_level_min_xp
    span_xp = max(1, next_level_xp - current_level_min_xp)
    progress_pct = min(100, max(0, int((progress_xp / span_xp) * 100)))

    rank_info = get_rank_info(level)

    # Get total solved
    cursor.execute("SELECT COUNT(*) as solved_count FROM solved_problems")
    total_solved = cursor.fetchone()["solved_count"]

    conn.close()

    return {
        "username": row["username"],
        "xp": xp,
        "level": level,
        "current_level_min_xp": current_level_min_xp,
        "next_level_xp": next_level_xp,
        "progress_pct": progress_pct,
        "streak": streak,
        "highest_streak": highest_streak,
        "hints_taken": row["hints_taken"],
        "quizzes_passed": row["quizzes_passed"],
        "total_solved": total_solved,
        "rank_name": rank_info["name"],
        "rank_tier": rank_info["tier"],
        "rank_icon": rank_info["icon"],
        "rank_color": rank_info["color"],
    }


def add_xp(amount: int) -> Tuple[int, bool]:
    """
    Adjusts user's XP by `amount` (can be positive or negative for penalties).
    Returns (new_xp, level_up_occurred)
    """
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT xp, level FROM user_profile WHERE id = 1")
    row = cursor.fetchone()
    old_xp = row["xp"]
    old_lvl = row["level"]

    new_xp = max(0, old_xp + amount)
    new_lvl = calculate_level_from_xp(new_xp)
    level_up = new_lvl > old_lvl

    cursor.execute("UPDATE user_profile SET xp = ?, level = ? WHERE id = 1", (new_xp, new_lvl))
    conn.commit()
    conn.close()

    if level_up:
        check_and_unlock_achievements()

    return new_xp, level_up


def deduct_xp_for_hint(xp_cost: int) -> int:
    """Deduct XP for using an AI Sensei hint."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT xp, hints_taken FROM user_profile WHERE id = 1")
    row = cursor.fetchone()
    old_xp = row["xp"]
    hints_taken = row["hints_taken"] + 1

    new_xp = max(0, old_xp - xp_cost)
    new_lvl = calculate_level_from_xp(new_xp)

    cursor.execute("UPDATE user_profile SET xp = ?, level = ?, hints_taken = ? WHERE id = 1",
                   (new_xp, new_lvl, hints_taken))
    conn.commit()
    conn.close()
    return new_xp


def record_solved_problem(problem_id: str, title: str, difficulty: str, category: str, xp_earned: int, hints_used: int, code: str) -> bool:
    """
    Records a problem as solved. Returns True if this is the first time solving it.
    """
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT problem_id, attempts FROM solved_problems WHERE problem_id = ?", (problem_id,))
    row = cursor.fetchone()

    is_first_time = row is None
    now_str = datetime.datetime.now().isoformat()

    if is_first_time:
        cursor.execute("""
        INSERT INTO solved_problems (problem_id, problem_title, difficulty, category, solved_at, xp_earned, attempts, hints_used, best_code)
        VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (problem_id, title, difficulty, category, now_str, xp_earned, hints_used, code))
        add_xp(xp_earned)
    else:
        cursor.execute("""
        UPDATE solved_problems
        SET attempts = attempts + 1, solved_at = ?, best_code = ?
        WHERE problem_id = ?
        """, (now_str, code, problem_id))

    conn.commit()
    conn.close()

    check_and_unlock_achievements()
    return is_first_time


def is_problem_solved(problem_id: str) -> bool:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM solved_problems WHERE problem_id = ?", (problem_id,))
    solved = cursor.fetchone() is not None
    conn.close()
    return solved


def get_all_solved_problem_ids() -> List[str]:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT problem_id FROM solved_problems")
    rows = cursor.fetchall()
    conn.close()
    return [r["problem_id"] for r in rows]


def record_quiz_result(problem_id: str, title: str, difficulty: str, time_limit: int, time_taken: int, passed: bool, xp_change: int):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO quiz_history (problem_id, problem_title, difficulty, time_limit_sec, time_taken_sec, passed, xp_change, completed_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (problem_id, title, difficulty, time_limit, time_taken, 1 if passed else 0, xp_change, now_str))

    if passed:
        cursor.execute("UPDATE user_profile SET quizzes_passed = quizzes_passed + 1 WHERE id = 1")

    conn.commit()
    conn.close()

    add_xp(xp_change)
    check_and_unlock_achievements()


def get_quiz_history(limit: int = 15) -> List[Dict]:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM quiz_history ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_solved_problems_detailed() -> List[Dict]:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM solved_problems ORDER BY solved_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def check_and_unlock_achievements() -> List[Dict]:
    """Evaluates user progress against all achievements and unlocks newly met ones."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_profile WHERE id = 1")
    profile = cursor.fetchone()

    cursor.execute("SELECT problem_id, difficulty FROM solved_problems")
    solved_rows = cursor.fetchall()
    solved_ids = {r["problem_id"] for r in solved_rows}
    hard_solved_count = sum(1 for r in solved_rows if r["difficulty"] == "Hard")

    cursor.execute("SELECT achievement_id FROM achievements")
    already_unlocked = {r["achievement_id"] for r in cursor.fetchall()}

    cursor.execute("SELECT COUNT(*) as passed_count FROM quiz_history WHERE passed = 1")
    quizzes_passed = cursor.fetchone()["passed_count"]

    newly_unlocked = []
    now_str = datetime.datetime.now().isoformat()

    BOSS_KILLER_IDS = {
        "trapping_rain_water",
        "merge_k_sorted_lists",
        "minimum_window_substring",
        "median_from_data_stream",
        "word_ladder_ii",
        "max_profit_job_scheduling",
        "alien_dictionary"
    }

    for ach in ACHIEVEMENT_DEFINITIONS:
        ach_id = ach["id"]
        if ach_id in already_unlocked:
            continue

        should_unlock = False

        if ach_id == "first_blood" and len(solved_ids) >= 1:
            should_unlock = True
        elif ach_id == "triple_threat" and len(solved_ids) >= 3:
            should_unlock = True
        elif ach_id == "ten_strike" and len(solved_ids) >= 10:
            should_unlock = True
        elif ach_id == "boss_slayer_1" and hard_solved_count >= 1:
            should_unlock = True
        elif ach_id == "boss_slayer_all" and BOSS_KILLER_IDS.issubset(solved_ids):
            should_unlock = True
        elif ach_id == "speed_demon" and quizzes_passed >= 1:
            should_unlock = True
        elif ach_id == "streak_master" and profile["streak"] >= 3:
            should_unlock = True
        elif ach_id == "gold_rank" and profile["level"] >= 10:
            should_unlock = True
        elif ach_id == "pure_mind":
            cursor.execute("SELECT COUNT(*) as count FROM solved_problems WHERE difficulty IN ('Medium', 'Hard') AND hints_used = 0")
            if cursor.fetchone()["count"] >= 1:
                should_unlock = True

        if should_unlock:
            cursor.execute("""
            INSERT INTO achievements (achievement_id, name, description, icon, unlocked_at)
            VALUES (?, ?, ?, ?, ?)
            """, (ach_id, ach["name"], ach["description"], ach["icon"], now_str))
            newly_unlocked.append(ach)

    conn.commit()
    conn.close()

    # Award bonus XP for unlocked achievements
    for ach in newly_unlocked:
        add_xp(ach["xp_reward"])

    return newly_unlocked


def get_all_achievements() -> List[Dict]:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM achievements")
    unlocked = {r["achievement_id"]: r["unlocked_at"] for r in cursor.fetchall()}
    conn.close()

    result = []
    for defn in ACHIEVEMENT_DEFINITIONS:
        item = dict(defn)
        item["unlocked"] = defn["id"] in unlocked
        item["unlocked_at"] = unlocked.get(defn["id"])
        result.append(item)
    return result


def add_chat_message(problem_id: Optional[str], role: str, content: str, xp_cost: int = 0):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO chat_history (problem_id, role, content, xp_cost, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (problem_id, role, content, xp_cost, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_chat_history(problem_id: Optional[str] = None, limit: int = 20) -> List[Dict]:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    if problem_id:
        cursor.execute("""
        SELECT * FROM chat_history WHERE problem_id = ? OR problem_id IS NULL ORDER BY id ASC LIMIT ?
        """, (problem_id, limit))
    else:
        cursor.execute("""
        SELECT * FROM chat_history ORDER BY id ASC LIMIT ?
        """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def reset_user_progress():
    """Resets all player progress back to clean state."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM solved_problems")
    cursor.execute("DELETE FROM quiz_history")
    cursor.execute("DELETE FROM achievements")
    cursor.execute("DELETE FROM chat_history")
    today_str = datetime.date.today().isoformat()
    cursor.execute("""
    UPDATE user_profile
    SET xp = 0, level = 1, streak = 1, highest_streak = 1, last_active_date = ?, hints_taken = 0, quizzes_passed = 0
    WHERE id = 1
    """, (today_str,))
    conn.commit()
    conn.close()
