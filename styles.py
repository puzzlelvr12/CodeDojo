"""
styles.py - Retro Arcade / Cyberpunk RPG Visual Engine for CodeDojo
Provides custom CSS injections, Google Web Fonts, glowing neon cards,
retro progress bars, CRT scanlines, and 8-bit Web Audio synth effects.
"""

def get_retro_css() -> str:
    return """
<style>
/* =========================================================================
   GOOGLE RETRO FONTS IMPORT
   ========================================================================= */
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Share+Tech+Mono&family=Chakra+Petch:ital,wght@0,400;0,600;0,700;1,400&family=VT323&display=swap');

/* =========================================================================
   CYBERPUNK THEME VARIABLES
   ========================================================================= */
:root {
    --bg-dark: #070913;
    --bg-surface: #0e1224;
    --bg-card: #131830;
    --bg-card-hover: #182040;
    --border-color: #1e2850;
    --neon-green: #00ff88;
    --neon-cyan: #00f0ff;
    --neon-pink: #ff007f;
    --neon-yellow: #ffe600;
    --neon-purple: #b5179e;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
}

/* Base Streamlit App Overrides */
.stApp {
    background-color: var(--bg-dark);
    color: var(--text-primary);
    font-family: 'Chakra Petch', sans-serif;
}

/* Header & Typography */
h1, h2, h3 {
    font-family: 'Chakra Petch', sans-serif;
    font-weight: 700;
    letter-spacing: 1px;
}

.pixel-font {
    font-family: 'Press Start 2P', cursive;
    letter-spacing: 1px;
}

.terminal-font {
    font-family: 'Share Tech Mono', monospace;
}

/* =========================================================================
   RETRO ARCADE HEADER & STATUS HUD
   ========================================================================= */
.arcade-header-container {
    background: linear-gradient(180deg, rgba(14, 18, 36, 0.95) 0%, rgba(7, 9, 19, 0.95) 100%);
    border: 1px solid var(--neon-cyan);
    border-radius: 8px;
    padding: 16px 24px;
    margin-bottom: 20px;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.2), inset 0 0 15px rgba(0, 240, 255, 0.08);
    position: relative;
    overflow: hidden;
}

.arcade-header-container::before {
    content: " ";
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--neon-pink), var(--neon-cyan), var(--neon-green));
}

.hud-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(19, 24, 48, 0.85);
    border: 1px solid rgba(0, 240, 255, 0.3);
    border-radius: 6px;
    padding: 6px 14px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 14px;
    color: #e2e8f0;
}

.hud-pill.highlight-cyan {
    border-color: var(--neon-cyan);
    box-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
}

.hud-pill.highlight-pink {
    border-color: var(--neon-pink);
    box-shadow: 0 0 8px rgba(255, 0, 127, 0.3);
}

.hud-pill.highlight-green {
    border-color: var(--neon-green);
    box-shadow: 0 0 8px rgba(0, 255, 136, 0.3);
}

.hud-pill.highlight-yellow {
    border-color: var(--neon-yellow);
    box-shadow: 0 0 8px rgba(255, 230, 0, 0.3);
}

/* Retro XP Progress Bar */
.xp-bar-container {
    width: 100%;
    background-color: #0b0e1b;
    border: 1px solid var(--neon-green);
    border-radius: 4px;
    height: 18px;
    margin: 8px 0;
    overflow: hidden;
    position: relative;
    box-shadow: 0 0 10px rgba(0, 255, 136, 0.2);
}

.xp-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #00b4d8 0%, var(--neon-green) 100%);
    transition: width 0.4s ease-in-out;
    box-shadow: 0 0 12px var(--neon-green);
}

.xp-bar-label {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    font-weight: bold;
    color: #ffffff;
    text-shadow: 0 0 4px #000;
}

/* =========================================================================
   GLOWING CARDS & PANELS
   ========================================================================= */
.cyber-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.25s ease;
}

.cyber-card:hover {
    border-color: var(--neon-cyan);
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.15);
}

.boss-card {
    background: linear-gradient(135deg, rgba(25, 15, 35, 0.9) 0%, rgba(14, 18, 36, 0.95) 100%);
    border: 1px solid var(--neon-pink);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 25px rgba(255, 0, 127, 0.25), inset 0 0 10px rgba(255, 0, 127, 0.1);
}

/* Cyber Terminal Box */
.terminal-window {
    background: #080a14;
    border: 1px solid rgba(0, 240, 255, 0.4);
    border-radius: 6px;
    padding: 16px;
    font-family: 'Share Tech Mono', monospace;
    color: #a7f3d0;
    box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.8), 0 0 10px rgba(0, 240, 255, 0.15);
}

.terminal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0, 240, 255, 0.2);
    padding-bottom: 8px;
    margin-bottom: 12px;
    font-size: 12px;
    color: var(--neon-cyan);
}

.terminal-bubble-user {
    background: rgba(0, 240, 255, 0.1);
    border-left: 3px solid var(--neon-cyan);
    padding: 10px 14px;
    border-radius: 4px;
    margin: 8px 0;
    font-size: 13px;
    color: #e2e8f0;
}

.terminal-bubble-sensei {
    background: rgba(181, 23, 158, 0.15);
    border-left: 3px solid var(--neon-pink);
    padding: 12px 14px;
    border-radius: 4px;
    margin: 8px 0;
    font-size: 13px;
    color: #f1f5f9;
}

/* =========================================================================
   STREAMLIT NATIVE COMPONENT OVERRIDES
   ========================================================================= */
/* Buttons */
.stButton > button {
    background: linear-gradient(180deg, #161f3d 0%, #0d1326 100%) !important;
    color: var(--neon-cyan) !important;
    border: 1px solid var(--neon-cyan) !important;
    border-radius: 6px !important;
    font-family: 'Chakra Petch', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 0 8px rgba(0, 240, 255, 0.2) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: var(--neon-cyan) !important;
    color: #070913 !important;
    box-shadow: 0 0 18px var(--neon-cyan) !important;
    transform: translateY(-1px) !important;
}

/* Action button with neon pink */
button[kind="primary"] {
    background: linear-gradient(180deg, #400d26 0%, #1f0714 100%) !important;
    color: var(--neon-pink) !important;
    border: 1px solid var(--neon-pink) !important;
    box-shadow: 0 0 10px rgba(255, 0, 127, 0.3) !important;
}

button[kind="primary"]:hover {
    background: var(--neon-pink) !important;
    color: #ffffff !important;
    box-shadow: 0 0 20px var(--neon-pink) !important;
}

/* Inputs, Textareas, and Selects */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #0c0f20 !important;
    color: #e2e8f0 !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.3) !important;
}

/* Streamlit Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #0a0d1c;
    border-bottom: 2px solid var(--border-color);
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Chakra Petch', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    padding: 10px 18px !important;
    border-radius: 4px 4px 0 0 !important;
}

.stTabs [aria-selected="true"] {
    background-color: #121832 !important;
    color: var(--neon-cyan) !important;
    border-bottom: 3px solid var(--neon-cyan) !important;
    box-shadow: inset 0 -2px 10px rgba(0, 240, 255, 0.2) !important;
}

/* Streamlit Metrics */
[data-testid="stMetricValue"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--neon-cyan) !important;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.3) !important;
}

/* Sidebar Customization */
section[data-testid="stSidebar"] {
    background-color: #090c18 !important;
    border-right: 1px solid var(--border-color) !important;
}

/* =========================================================================
   DIFFICULTY & RANK BADGES
   ========================================================================= */
.badge-easy {
    background: rgba(0, 255, 136, 0.15);
    color: var(--neon-green);
    border: 1px solid var(--neon-green);
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 700;
}

.badge-medium {
    background: rgba(255, 230, 0, 0.15);
    color: var(--neon-yellow);
    border: 1px solid var(--neon-yellow);
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 700;
}

.badge-hard {
    background: rgba(255, 0, 127, 0.15);
    color: var(--neon-pink);
    border: 1px solid var(--neon-pink);
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 700;
    box-shadow: 0 0 8px rgba(255, 0, 127, 0.3);
}

.pulse-glow {
    animation: pulseGlowAnim 2s infinite ease-in-out;
}

@keyframes pulseGlowAnim {
    0% { box-shadow: 0 0 8px rgba(0, 240, 255, 0.4); }
    50% { box-shadow: 0 0 20px rgba(0, 240, 255, 0.8); }
    100% { box-shadow: 0 0 8px rgba(0, 240, 255, 0.4); }
}

.pulse-boss-glow {
    animation: pulseBossGlowAnim 1.8s infinite ease-in-out;
}

@keyframes pulseBossGlowAnim {
    0% { box-shadow: 0 0 10px rgba(255, 0, 127, 0.4); }
    50% { box-shadow: 0 0 25px rgba(255, 0, 127, 0.9); }
    100% { box-shadow: 0 0 10px rgba(255, 0, 127, 0.4); }
}
</style>
"""


def get_retro_audio_synth_script() -> str:
    """
    Returns an HTML snippet with synthesized Web Audio API sounds.
    Supports click, pass, fail, levelup, and hint audio triggers directly in browser!
    """
    return """
<script>
window.CodeDojoAudio = {
    ctx: null,
    init: function() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) this.ctx = new AudioContext();
        }
    },
    playTone: function(freq, type, duration, delay=0) {
        this.init();
        if (!this.ctx) return;
        setTimeout(() => {
            try {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
                gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + duration);
            } catch(e) {}
        }, delay * 1000);
    },
    click: function() {
        this.playTone(600, 'square', 0.05);
    },
    pass: function() {
        this.playTone(523.25, 'triangle', 0.1, 0.0);
        this.playTone(659.25, 'triangle', 0.1, 0.08);
        this.playTone(783.99, 'triangle', 0.15, 0.16);
        this.playTone(1046.50, 'triangle', 0.3, 0.24);
    },
    fail: function() {
        this.playTone(250, 'sawtooth', 0.15, 0.0);
        this.playTone(180, 'sawtooth', 0.25, 0.12);
    },
    levelup: function() {
        this.playTone(440, 'sine', 0.1, 0.0);
        this.playTone(554, 'sine', 0.1, 0.08);
        this.playTone(659, 'sine', 0.1, 0.16);
        this.playTone(880, 'sine', 0.35, 0.24);
    },
    hint: function() {
        this.playTone(400, 'sine', 0.08, 0.0);
        this.playTone(300, 'sine', 0.15, 0.08);
    }
};
</script>
"""
