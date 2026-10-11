# ⚔️ CodeDojo: Retro Arcade Coding Interview Academy

[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini%20API-google--genai-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-00f0ff?style=for-the-badge)](#license)

> **"Step into the cyber matrix, train under Cyber Sensei, and conquer the most ruthless coding interview bosses in existence."**

**CodeDojo** is a complete, highly polished, gamified offline coding interview preparation web app built with **Streamlit**, **Python**, and **SQLite**, with AI mentorship powered by the **Google Gemini API** (`google-genai` SDK). Designed with a **Retro Arcade / Cyberpunk RPG** visual identity, CodeDojo transforms repetitive algorithmic grind into an exhilarating quest for rank, XP, and algorithmic mastery.

---

## 🕹️ Visual Identity & Architecture (Retro Arcade RPG)

- **Aesthetic:** Dark cyberpunk background palette (`#070913`, `#0e1224`, `#131830`) illuminated by vibrant neon accents (Neon Green `#00ff88`, Electric Cyan `#00f0ff`, Hot Pink `#ff007f`, Arcade Yellow `#ffe600`).
- **Typography:** Pixel headers using Google Fonts (`Press Start 2P`, `VT323`, `Chakra Petch`, and `Share Tech Mono`).
- **Web Audio 8-bit Sound Synthesizer:** Real-time synthesized retro arcade chimes for clicks, test passes, level-ups, and penalty deductions via HTML5 Web Audio API.
- **Wide Split Layout:**
  - **Left Side (Workspace):** Interactive workspace hosting the structured **Code School Curriculum**, **Practice Dojo** with embedded Ace code editor, **Timed Countdown Trials**, and **Hall of Fame Stats**.
  - **Right Side (AI Assistant NPC Box):** Cyber Sensei companion powered by Google Gemini with multi-tier hint penalties and offline vault wisdom.

---

## 🥋 Rank Tiers & Leveling Curve

| Rank Icon | Rank Tier | Level Span | XP Requirement | Aesthetic Color |
| :---: | :---: | :---: | :---: | :---: |
| 🥉 | **Bronze Ninja** | Lvl 1 – 4 | 0 – 599 XP | `#cd7f32` (Bronze) |
| 🥈 | **Silver Ronin** | Lvl 5 – 9 | 600 – 1,499 XP | `#c0c0c0` (Silver) |
| 🥇 | **Gold Samurai** | Lvl 10 – 14 | 1,500 – 2,999 XP | `#ffd700` (Gold) |
| 💎 | **Diamond Shogun** | Lvl 15 – 19 | 3,000 – 4,999 XP | `#00f0ff` (Cyan) |
| 👑 | **Master Boss (Kage)** | Lvl 20+ | 5,000+ XP | `#ff007f` (Neon Pink) |

### ⚡ Gamification Mechanics:
- **XP Rewards:** Easy (+100 XP), Medium (+250 XP), Hard / Boss (+500 XP).
- **Speed Bonus:** Earn up to +100 bonus XP for beating timed trials before the countdown expires.
- **Daily Discipline:** Daily coding streak tracking powered by a local SQLite engine (`progress.db`).
- **XP Penalty Mechanic:** Consulting Cyber Sensei costs hard-earned XP to incentivize independent problem solving:
  - 💡 **Subconscious Nudge:** `-10 XP` (Socratic invariant hint, no code).
  - 🔍 **Algorithmic Blueprint:** `-25 XP` (Step-by-step logic, Big-O, edge cases).
  - ⚔️ **Master Scroll:** `-60 XP` (Full canonical reference solution and line analysis).
  - ⏱️ **Timed Trial Timeout / Abandon:** `-30 XP`.

---

## 📚 The Code School Curriculum

CodeDojo acts as a full data structures and algorithms academy with deep-dive markdown explanations, Big-O complexity matrices, universal templates, and the 5 deadly interview trap patterns across 9 categories:

1. **Arrays, Strings & Two Pointers:** Pointer collision, fast & slow pointers, prefix-suffix scans.
2. **Hash Maps & Sets Engine:** Amortized $\mathcal{O}(1)$ lookups, frequency counters, space-time tradeoffs.
3. **Sliding Window Paradigms:** Fixed vs dynamic windows, shrinkage conditions, $\mathcal{O}(N)$ bounds.
4. **Linked Lists & Pointer Surgery:** Sentinel nodes, Floyd's cycle detection, in-place reversals.
5. **Binary Search & Monotonic Predicates:** Boundary templates, rotated sorted arrays, binary search on answer spaces.
6. **Trees, Graphs & Topological Sort:** BFS layer queues, DFS backtracking, Kahn's algorithm for DAGs.
7. **Heaps & Priority Queues:** Min-heaps, top-$k$ elements, dual balancing heaps.
8. **Dynamic Programming (1D & 2D):** State definition, transitions, base cases, tabulation.
9. **Boss-Level Killer Patterns:** Synthesizing orthogonal algorithmic paradigms.

---

## 👹 The Problem Bank & The 7 LeetCode Hard Boss Killers

CodeDojo includes exhaustive coverage from Easy warm-ups to Medium core patterns to the **7 notorious LeetCode Hard interview killers**:

| Difficulty | Problem Title | Category | Boss Persona |
| :--- | :--- | :--- | :--- |
| **Easy** | Two Sum | Arrays & Hash Maps | Minion 1: The Binary Sentinels |
| **Easy** | Valid Anagram | Strings & Hash Maps | Minion 2: The Cipher Decrypter |
| **Easy** | Valid Palindrome | Two Pointers | Minion 3: The Mirror Monolith |
| **Easy** | Best Time to Buy and Sell Stock | Arrays & DP | Minion 4: The Market Speculator |
| **Easy** | Binary Search | Binary Search | Minion 5: The Monotonic Scanner |
| **Medium** | Longest Substring Without Repeating Characters | Sliding Window | Sentinel 1: The Unique Buffer |
| **Medium** | 3Sum | Two Pointers & Sorting | Sentinel 2: The Triad Alignment |
| **Medium** | Search in Rotated Sorted Array | Binary Search | Sentinel 3: The Fractured Axis |
| **Medium** | Binary Tree Level Order Traversal | Trees (BFS) | Sentinel 4: The Hierarchical Scanner |
| **Medium** | Combination Sum | Backtracking | Sentinel 5: The Energy Synthesis |
| **Medium** | Top K Frequent Elements | Heaps & Hash Maps | Sentinel 6: The Signal Spectrum |
| **Medium** | Coin Change | Dynamic Programming | Sentinel 7: The Currency Matrix |
| **Hard (Boss)** | **Trapping Rain Water** | Arrays & Two Pointers | 👹 **BOSS 1: The Leviathan Rainmaker** |
| **Hard (Boss)** | **Merge k Sorted Lists** | Heaps & Linked Lists | 👹 **BOSS 2: The Multi-Headed Hydra** |
| **Hard (Boss)** | **Minimum Window Substring** | Sliding Window | 👹 **BOSS 3: The Quantum Sieve** |
| **Hard (Boss)** | **Median from Data Stream** | Dual Balancing Heaps | 👹 **BOSS 4: The Dynamic Gyroscope** |
| **Hard (Boss)** | **Word Ladder II** | Layered BFS + DFS | 👹 **BOSS 5: The Morphing Polyglot** |
| **Hard (Boss)** | **Maximum Profit in Job Scheduling** | DP + Binary Search | 👹 **BOSS 6: The Chrono Mercenary** |
| **Hard (Boss)** | **Alien Dictionary** | Topological Sort | 👹 **BOSS 7: The Extraterrestrial Oracle** |

---

## 🤖 Cyber Sensei AI Mentorship (Google Gemini API)

Cyber Sensei is powered by the official `google-genai` SDK:
- **Free Key Support:** Enter your free Google AI Studio API key directly in the sidebar or set `GEMINI_API_KEY`.
- **Context-Aware:** Sensei analyzes the active problem statement, difficulty, and your current code in the editor.
- **100% Offline Vault Mode:** If no key is entered or the network is offline, Cyber Sensei automatically serves curated offline architectural advice and solutions!

---

## 🚀 Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/puzzlelvr12/CodeDojo.git
cd CodeDojo
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the App
```bash
streamlit run app.py
```

### 4. (Optional) Activate Gemini AI
Paste your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey) into the sidebar input field, or export it in your environment:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## 📁 Repository Structure

```text
CodeDojo/
├── app.py              # Main Streamlit web app with retro HUD, layout & modes
├── database.py         # SQLite gamification engine (XP, streaks, achievements)
├── problems.py         # Comprehensive problem bank with 7 Boss killers & test cases
├── lessons.py          # Structured Code School curriculum with Big-O & templates
├── test_runner.py      # Automated sandboxed Python evaluation & timeout engine
├── gemini_npc.py       # Cyber Sensei AI assistant powered by google-genai SDK
├── styles.py           # Retro Arcade / Cyberpunk custom CSS & 8-bit Web Audio synth
├── requirements.txt    # Python package dependencies
├── .gitignore          # Standard repository ignore configuration
└── README.md           # Documentation & guides
```

---

## 📜 License
MIT License. Built for aspiring software engineers preparing for top-tier technical coding interviews.
