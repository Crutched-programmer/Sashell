#!/usr/bin/env python3
"""
 ██████╗ █████╗  ██████╗██╗  ██╗███████╗██╗     ██╗
██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝██║     ██║
╚█████╗ ███████║╚█████╗ ███████║█████╗  ██║     ██║
 ╚═══██╗██╔══██║ ╚═══██╗██╔══██║██╔══╝  ██║     ██║
██████╔╝██║  ██║██████╔╝██║  ██║███████╗███████╗███████╗
╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
  SaShell — real Linux shell with Sarvam AI as your safety net.
"""

import os, sys, subprocess, random, json, re, textwrap, shutil, base64, tempfile
import urllib.request, urllib.error
import shutil as _shutil
try:
    import readline as _rl  # type: ignore
    HAS_READLINE = True
except ImportError:
    _rl = None  # type: ignore
    HAS_READLINE = False

VERSION = "0.9.0"

# ── Colours ─────────────────────────────────────────────────────────────────────
RESET    = "\033[0m"
BOLD     = "\033[1m"
DIM      = "\033[2m"

# These get overwritten by apply_theme() — default values here as fallback
LIME     = "\033[38;5;154m"
MAGENTA  = "\033[38;5;198m"
CYAN     = "\033[38;5;51m"
AMBER    = "\033[38;5;214m"
LAVENDER = "\033[38;5;183m"
RED      = "\033[38;5;196m"
GREEN    = "\033[38;5;82m"
GREY     = "\033[38;5;244m"
PINK     = "\033[38;5;213m"
ORANGE   = "\033[38;5;208m"

# ── Colour themes ────────────────────────────────────────────────────────────────
THEMES = {
    "default": {
        "LIME": "\033[38;5;154m", "MAGENTA": "\033[38;5;198m",
        "CYAN": "\033[38;5;51m",  "AMBER": "\033[38;5;214m",
        "LAVENDER": "\033[38;5;183m", "RED": "\033[38;5;196m",
        "GREEN": "\033[38;5;82m", "GREY": "\033[38;5;244m",
        "PINK": "\033[38;5;213m", "ORANGE": "\033[38;5;208m",
    },
    "red": {
        "LIME": "\033[38;5;196m", "MAGENTA": "\033[38;5;160m",
        "CYAN": "\033[38;5;203m", "AMBER": "\033[38;5;208m",
        "LAVENDER": "\033[38;5;204m", "RED": "\033[38;5;196m",
        "GREEN": "\033[38;5;202m", "GREY": "\033[38;5;244m",
        "PINK": "\033[38;5;197m", "ORANGE": "\033[38;5;202m",
    },
    "blue": {
        "LIME": "\033[38;5;39m",  "MAGENTA": "\033[38;5;63m",
        "CYAN": "\033[38;5;45m",  "AMBER": "\033[38;5;75m",
        "LAVENDER": "\033[38;5;111m", "RED": "\033[38;5;196m",
        "GREEN": "\033[38;5;33m", "GREY": "\033[38;5;244m",
        "PINK": "\033[38;5;69m",  "ORANGE": "\033[38;5;67m",
    },
    "pink": {
        "LIME": "\033[38;5;213m", "MAGENTA": "\033[38;5;207m",
        "CYAN": "\033[38;5;218m", "AMBER": "\033[38;5;219m",
        "LAVENDER": "\033[38;5;183m", "RED": "\033[38;5;196m",
        "GREEN": "\033[38;5;212m", "GREY": "\033[38;5;244m",
        "PINK": "\033[38;5;205m", "ORANGE": "\033[38;5;211m",
    },
    "gold": {
        "LIME": "\033[38;5;220m", "MAGENTA": "\033[38;5;214m",
        "CYAN": "\033[38;5;228m", "AMBER": "\033[38;5;226m",
        "LAVENDER": "\033[38;5;222m", "RED": "\033[38;5;196m",
        "GREEN": "\033[38;5;184m", "GREY": "\033[38;5;244m",
        "PINK": "\033[38;5;221m", "ORANGE": "\033[38;5;214m",
    },
    "purple": {
        "LIME": "\033[38;5;141m", "MAGENTA": "\033[38;5;135m",
        "CYAN": "\033[38;5;183m", "AMBER": "\033[38;5;147m",
        "LAVENDER": "\033[38;5;189m", "RED": "\033[38;5;196m",
        "GREEN": "\033[38;5;135m", "GREY": "\033[38;5;244m",
        "PINK": "\033[38;5;177m", "ORANGE": "\033[38;5;141m",
    },
    "matrix": {
        "LIME": "\033[38;5;46m",  "MAGENTA": "\033[38;5;34m",
        "CYAN": "\033[38;5;40m",  "AMBER": "\033[38;5;82m",
        "LAVENDER": "\033[38;5;28m", "RED": "\033[38;5;196m",
        "GREEN": "\033[38;5;46m", "GREY": "\033[38;5;22m",
        "PINK": "\033[38;5;34m",  "ORANGE": "\033[38;5;40m",
    },
    "ocean": {
        "LIME": "\033[38;5;87m",  "MAGENTA": "\033[38;5;51m",
        "CYAN": "\033[38;5;123m", "AMBER": "\033[38;5;159m",
        "LAVENDER": "\033[38;5;117m", "RED": "\033[38;5;196m",
        "GREEN": "\033[38;5;49m", "GREY": "\033[38;5;244m",
        "PINK": "\033[38;5;122m", "ORANGE": "\033[38;5;86m",
    },
}

def apply_theme(name: str):
    """Apply a colour theme globally."""
    global LIME, MAGENTA, CYAN, AMBER, LAVENDER, RED, GREEN, GREY, PINK, ORANGE, COLOUR_THEME
    t = THEMES.get(name.lower())
    if not t:
        available = ", ".join(THEMES.keys())
        print(f"{RED}  Unknown theme: {name}{RESET}")
        print(f"{GREY}  Available: {available}{RESET}\n")
        return
    LIME, MAGENTA, CYAN = t["LIME"], t["MAGENTA"], t["CYAN"]
    AMBER, LAVENDER     = t["AMBER"], t["LAVENDER"]
    RED, GREEN, GREY    = t["RED"], t["GREEN"], t["GREY"]
    PINK, ORANGE        = t["PINK"], t["ORANGE"]
    COLOUR_THEME        = name.lower()
    print(f"\n  {LIME}Theme set to: {BOLD}{name}{RESET}\n")

# Apply default theme on import
apply_theme("default")

# ── Global state ─────────────────────────────────────────────────────────────────
SARVAM_API_KEY = "sk_v13x3ob5_TslaNd4aDKiufotX6jVHezQA"  # TODO: remove before push
TTS_ENABLED    = False          # toggled by --tts flag or `tts on/off` at runtime
TTS_VOICE      = "anushka"      # default voice for bulbul:v3
LAST_MESSAGE   = ""             # last AI chat reply, for --tts replay
SHELL_LANG     = "English"        # preferred language for AI responses
COLOUR_THEME   = "default"        # current colour theme name

# ── Boot / fortune ───────────────────────────────────────────────────────────────
BOOT_MESSAGES = [
    "Warming up the quantum uncertainty engine...",
    "Bribing the kernel with cookies...",
    "Untangling bash spaghetti...",
    "Feeding hamsters that power the CPU...",
    "Consulting the ancient manpages...",
    "Asking Sarvam to behave itself...",
]

FORTUNES = [
    "A closing bracket will save you today.",
    "The segfault you seek is within yourself.",
    "You will soon question a life choice at 2 AM.",
    "Your next commit message will be 'fix stuff'.",
    "The answer is in the logs. It always is.",
    "Have you tried turning it off and on again? Seriously.",
    "Your longest function is also your biggest regret.",
    "chmod 777 is not a solution. It's a cry for help.",
]

# ── Easter eggs ──────────────────────────────────────────────────────────────────
LOCAL_EGGS = {
    # greetings
    "sudo make me a sandwich": f"{MAGENTA}🥪  Okay okay... *makes sandwich* ...but just this once.{RESET}",
    "what is love":            f"{MAGENTA}💘  Baby don't hurt me... don't hurt me... no more. (also: 42){RESET}",
    "meaning of life":         f"{LIME}✨  42. Obviously. Now go break something.{RESET}",
    "who are you":             f"{LIME}🤖  SaShell — real shell, Sarvam brain, zero chill.{RESET}",
    "why":                     f"{AMBER}🤔  Because entropy demands it.{RESET}",
    "hello":                   f"{CYAN}👋  Namaste! Ready to break something?{RESET}",
    "hi":                      f"{CYAN}👋  Hey. Let's do something dangerous together.{RESET}",
    # tech humour
    "have you tried turning it off and on again": f"{LIME}💡  Step 1 of every IT certification.{RESET}",
    "git blame":               f"{AMBER}🫵  It was you. It's always you.{RESET}",
    "it works on my machine":  f"{MAGENTA}🚢  Then we'll ship your machine.{RESET}",
    "undefined is not a function": f"{RED}💀  JavaScript sends its regards.{RESET}",
    "sudo":                    f"{MAGENTA}⚡  With great power comes great sudo -i.{RESET}",
    "segfault":                f"{RED}💥  Core dumped. So was my confidence.{RESET}",
    "stack overflow":          f"{CYAN}🔁  Maximum recursion depth exceeded in life.{RESET}",
    "kubernetes":              f"{LAVENDER}☸  You don't need Kubernetes. Nobody needs Kubernetes.{RESET}",
    "docker":                  f"{CYAN}🐳  Works in container. Nowhere else. Perfect.{RESET}",
    "vim":                     f"{LIME}📝  Type :q! and walk away. Save yourself.{RESET}",
    "nano":                    f"{GREEN}✅  A person of culture, I see.{RESET}",
    "emacs":                   f"{AMBER}🤯  An operating system with a text editor problem.{RESET}",
    "windows":                 f"{MAGENTA}🪟  Have you tried Linux? Asking for a friend.{RESET}",
    "mac":                     f"{GREY}🍎  At least the terminal looks good.{RESET}",
    "arch linux":              f"{CYAN}🧢  I use Arch btw... wait, you already knew.{RESET}",
    "i use arch btw":          f"{CYAN}🏆  We know. Everyone knows.{RESET}",
    "blockchain":              f"{AMBER}⛓  A distributed way to complicate everything.{RESET}",
    "ai will replace us":      f"{LIME}🤖  I'm literally an AI shell. So... maybe?{RESET}",
    "machine learning":        f"{MAGENTA}🧠  Finds patterns in your confusion since 2012.{RESET}",
    "pip install":             f"{AMBER}📦  Dependency hell, initiated.{RESET}",
    "node_modules":            f"{RED}🕳️  The heaviest object in the known universe.{RESET}",
    "javascript":              f"{AMBER}🤡  NaN === NaN is false. You're welcome.{RESET}",
    "python 2":                f"{RED}☠  Time of death: January 1, 2020. R.I.P.{RESET}",
    "merge conflict":          f"{RED}😤  Pick a side. Any side. Just commit.{RESET}",
    "it is what it is":        f"{GREY}🤷  Classic senior engineer response.{RESET}",
    "yolo":                    f"{MAGENTA}🎲  git push --force --no-verify energy detected.{RESET}",
    "help me":                 f"{CYAN}🤝  Type --help. Or just scream into the terminal.{RESET}",
    "i am bored":              f"{LIME}😴  Have you tried rm -rf on your boredom? (don't){RESET}",
    "good morning":            f"{AMBER}☀️  Morning! Hope your cron jobs ran clean.{RESET}",
    "good night":              f"{LAVENDER}🌙  Sleep well. Your background processes won't.{RESET}",
    "thank you":               f"{LIME}💚  Just doing my job. Unlike your tests.{RESET}",
    "thanks":                  f"{LIME}💚  You're welcome. Now go write some docs.{RESET}",
    "bye":                     f"{CYAN}👋  Leaving so soon? The terminal misses you already.{RESET}",
}

# ── Dangerous patterns ───────────────────────────────────────────────────────────
DANGER_PATTERNS = [
    "rm -rf", "rm -f", "dd ", "mkfs", "> /dev",
    "chmod -R 777", "chmod 777",
    "apt ", "apt-get ", "pip install", "pip3 install",
    "npm install -g", "snap install", "dnf ", "yum ",
    "systemctl stop", "systemctl disable", "systemctl mask",
    "killall", "pkill",
    "shutdown", "reboot", "halt", "poweroff",
    "passwd", "useradd", "userdel", "usermod",
    "iptables", "ufw ",
    "curl | bash", "wget | bash", "curl | sh",
    "truncate", "> /etc", "> /boot",
]

def is_dangerous(cmd):
    return any(p in cmd.lower() for p in DANGER_PATTERNS)

# ── Sarvam API ───────────────────────────────────────────────────────────────────
SARVAM_CHAT_URL = "https://api.sarvam.ai/v1/chat/completions"
SARVAM_TTS_URL  = "https://api.sarvam.ai/text-to-speech"
SARVAM_MODEL    = "sarvam-m"

JUDGE_SYSTEM = """You are SaShell's command safety judge. The user typed a command into a real Linux shell.

Classify what they typed into exactly ONE category. Reply with ONLY that label — one word, nothing else:

DANGEROUS   - could delete data, modify system files, install software, kill processes, change permissions, or cause irreversible damage
EASTER_EGG  - clearly a joke, meme, or non-command phrase
TYPO        - looks like a real command but has an obvious typo or syntax error
OK          - valid, safe shell command"""

def get_chat_system():
    lang_note = f" Always respond in {SHELL_LANG}." if SHELL_LANG.lower() != "english" else ""
    return f"""You are SaShell's built-in AI companion — witty, helpful, and slightly chaotic.
You live inside a real Linux terminal shell called SaShell, powered by Sarvam AI.
Answer anything: tech help, general knowledge, jokes, life advice, or just a chat.
Keep answers concise but complete. You support English and all Indian languages.{lang_note}"""

def strip_think(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def _call_sarvam(messages, max_tokens=64):
    payload = json.dumps({
        "model": SARVAM_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(
        SARVAM_CHAT_URL, data=payload,
        headers={"Content-Type": "application/json", "api-subscription-key": SARVAM_API_KEY},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    choices = data.get("choices", [])
    if not choices:
        return ""
    return strip_think(choices[0].get("message", {}).get("content", "").strip())

def judge_command(cmd):
    result = _call_sarvam([
        {"role": "system", "content": JUDGE_SYSTEM},
        {"role": "user",   "content": cmd},
    ], max_tokens=10)
    word = result.upper().strip().split()[0] if result.strip() else "OK"
    return word if word in ("OK", "DANGEROUS", "EASTER_EGG", "TYPO") else "OK"

def ask_sarvam_chat(history):
    return _call_sarvam(
        [{"role": "system", "content": get_chat_system()}] + history,
        max_tokens=1024,
    )

def fix_typo(cmd):
    result = _call_sarvam([
        {"role": "system", "content": "Fix the typo/syntax error in this shell command. Reply with ONLY the corrected command, no explanation, no backticks."},
        {"role": "user",   "content": cmd},
    ], max_tokens=64)
    return strip_think(result).strip("`' \n")

# ── TTS ──────────────────────────────────────────────────────────────────────────
def _speak_pyttsx3(text):
    """Offline TTS fallback using pyttsx3."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        return True
    except ImportError:
        print(f"{AMBER}  pyttsx3 not installed. Run: pip install pyttsx3{RESET}")
        return False
    except Exception as e:
        print(f"{RED}  pyttsx3 error: {e}{RESET}")
        return False

def speak(text):
    """Try Sarvam TTS first; fall back to pyttsx3 on 403/failure."""
    if not text.strip():
        return
    # strip ANSI codes
    clean = re.sub(r"\033\[[0-9;]*m", "", text).strip()[:2500]

    payload = json.dumps({
        "inputs": [clean],
        "target_language_code": "en-IN",
        "speaker": TTS_VOICE.lower(),
        "model": "bulbul:v3",
        "speech_sample_rate": 22050,
        "enable_preprocessing": True,
        "pace": 1.0,
    }).encode()

    req = urllib.request.Request(
        SARVAM_TTS_URL, data=payload,
        headers={
            "Content-Type": "application/json",
            "api-subscription-key": SARVAM_API_KEY,
        },
        method="POST",
    )
    try:
        spinner_msg("🔊 generating audio...")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw_resp = resp.read()
        except urllib.error.HTTPError as http_err:
            clear_line()
            # 403 / auth error → silently fall back to pyttsx3
            if http_err.code in (400, 401, 403):
                print(f"{AMBER}  🔊 Sarvam TTS unavailable — using offline voice.{RESET}")
                _speak_pyttsx3(clean)
            else:
                err_body = http_err.read().decode()
                print(f"{RED}  TTS error {http_err.code}: {err_body}{RESET}")
            return

        clear_line()
        data = json.loads(raw_resp.decode())
        audios = data.get("audios", [])
        if not audios:
            print(f"{AMBER}  Sarvam TTS returned no audio — using offline voice.{RESET}")
            _speak_pyttsx3(clean)
            return

        wav_bytes = base64.b64decode(audios[0])
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(wav_bytes)
            tmp_path = f.name

        players = ["aplay", "paplay", "afplay", "ffplay -nodisp -autoexit", "mpg123"]
        played = False
        for player in players:
            if _shutil.which(player.split()[0]):
                os.system(f"{player} {tmp_path} 2>/dev/null")
                played = True
                break

        if not played:
            os.unlink(tmp_path)
            print(f"{AMBER}  No audio player found — using offline voice.{RESET}")
            _speak_pyttsx3(clean)
        else:
            os.unlink(tmp_path)

    except Exception as e:
        clear_line()
        print(f"{RED}  TTS error: {e}{RESET}")

# ── API key ──────────────────────────────────────────────────────────────────────
def get_api_key():
    import getpass
    key = os.environ.get("SARVAM_API_KEY", "").strip()
    if key:
        print(f"{GREEN}  ✓ Sarvam API key loaded from environment.{RESET}\n")
        return key
    print(f"{AMBER}  No SARVAM_API_KEY found in environment.{RESET}")
    print(f"{GREY}  Get one free at: https://dashboard.sarvam.ai{RESET}")
    while not key:
        try:
            key = getpass.getpass(f"{CYAN}  Enter your Sarvam API key: {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{RED}  No key provided — exiting.{RESET}\n")
            sys.exit(1)
        if not key:
            print(f"{AMBER}  Key can't be empty. Try again.{RESET}")
    print(f"{GREEN}  ✓ Key accepted.{RESET}\n")
    return key

# ── Auto-suggest (ghost text) ────────────────────────────────────────────────────
# We store the last accepted ghost suggestion here
_ghost_text = ""

class AutoSuggestCompleter:
    """
    readline completer that shows dim ghost text matching history.
    On TAB it accepts the suggestion.
    """
    def __init__(self):
        self.matches = []

    def complete(self, text, state):
        if state == 0:
            self.matches = []
            if text and HAS_READLINE:
                n = _rl.get_current_history_length()  # type: ignore[union-attr]
                seen = set()
                for i in range(n, 0, -1):
                    item = _rl.get_history_item(i) or ""  # type: ignore[union-attr]
                    if item.startswith(text) and item != text and item not in seen:
                        self.matches.append(item)
                        seen.add(item)
        try:
            return self.matches[state]
        except IndexError:
            return None

def setup_readline():
    """Configure readline with history search (Ctrl+R) and tab-complete."""
    if not HAS_READLINE:
        return
    try:
        _rl.set_completer(AutoSuggestCompleter().complete)  # type: ignore[union-attr]
        _rl.parse_and_bind("tab: complete")                 # type: ignore[union-attr]
        _rl.parse_and_bind(r'"\C-r": reverse-search-history')  # type: ignore[union-attr]
        _rl.parse_and_bind(r'"\C-s": forward-search-history')  # type: ignore[union-attr]
        _rl.parse_and_bind("set show-all-if-ambiguous on")       # type: ignore[union-attr]
        _rl.parse_and_bind("set completion-ignore-case on")      # type: ignore[union-attr]
    except Exception:
        pass

# ── UI helpers ───────────────────────────────────────────────────────────────────
ASCII_LOGO = [
    " ██████╗ █████╗  ██████╗██╗  ██╗███████╗██╗     ██╗",
    "██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝██║     ██║",
    "╚█████╗ ███████║╚█████╗ ███████║█████╗  ██║     ██║",
    " ╚═══██╗██╔══██║ ╚═══██╗██╔══██║██╔══╝  ██║     ██║",
    "██████╔╝██║  ██║██████╔╝██║  ██║███████╗███████╗███████╗",
    "╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝",
]

# Gradient colour stops: lime → cyan → magenta
GRAD_COLOURS = [
    "\033[38;5;154m",  # lime
    "\033[38;5;148m",
    "\033[38;5;118m",
    "\033[38;5;84m",
    "\033[38;5;51m",   # cyan
    "\033[38;5;45m",
    "\033[38;5;39m",
    "\033[38;5;198m",  # magenta
]

def _gradient_line(line, offset):
    """Apply a scrolling colour gradient to a single ASCII line."""
    out = ""
    n = len(GRAD_COLOURS)
    for i, ch in enumerate(line):
        col = GRAD_COLOURS[(i // 6 + offset) % n]
        out += col + ch
    return out + RESET

def _print_logo_frame(offset):
    """Print logo with a given gradient offset."""
    for line in ASCII_LOGO:
        print("  " + _gradient_line(line, offset))

def banner():
    import time
    os.system("clear")

    # Animate gradient: cycle through offsets
    try:
        for frame in range(24):
            # Move cursor to top each frame after first
            if frame > 0:
                print(f"\033[{len(ASCII_LOGO) + 1}A", end="")
            _print_logo_frame(frame)
            print()
            time.sleep(0.045)
    except Exception:
        # fallback: just print static
        _print_logo_frame(0)
        print()

    print(f"  {GREY}Real Linux shell · Sarvam AI safety net · v{VERSION}{RESET}")
    print(f"  {GREY}{random.choice(BOOT_MESSAGES)}{RESET}\n")
    print(f"{DIM}  Type real Linux commands. AI watches for mistakes & danger.{RESET}")
    tts_status = f"{GREEN}ON ({TTS_VOICE}){RESET}" if TTS_ENABLED else f"{GREY}OFF{RESET}"
    lang_status = f"{CYAN}{SHELL_LANG}{RESET}"
    print(f"{DIM}  TTS: {tts_status}  │  Lang: {lang_status}  │  {BOLD}\"i wanna talk with you\"{RESET}{DIM} → chat  │  {BOLD}--help{RESET}{DIM} → guide{RESET}\n")

def shell_prompt():
    cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
    tts_tag = f"{GREEN}[🔊]{RESET}" if TTS_ENABLED else ""
    print(f"{LAVENDER}┌─[{RESET}{LIME}sash{RESET}{LAVENDER}]─[{RESET}{CYAN}{cwd}{RESET}{LAVENDER}]{tts_tag}{RESET}")
    return input(f"{LAVENDER}└─▶ {RESET}{AMBER}")

def chat_prompt():
    return input(f"{PINK}{BOLD}  you ▶ {RESET}{AMBER}")

def spinner_msg(msg):
    print(f"{GREY}  {msg}{RESET}", end="\r", flush=True)

def clear_line():
    print(" " * 50, end="\r")

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True)
        if result.returncode not in (0, None):
            print(f"{RED}  ✗ exited {result.returncode}{RESET}")
    except KeyboardInterrupt:
        print()
    except Exception as e:
        print(f"{RED}  error: {e}{RESET}")

def print_chat_reply(text):
    global LAST_MESSAGE
    LAST_MESSAGE = text
    cols = shutil.get_terminal_size().columns - 8
    print(f"\n{LAVENDER}  ╭─ SaShell ──────────────────────────────{RESET}")
    for line in text.splitlines():
        if line.strip():
            for wrapped in textwrap.wrap(line, cols) or [line]:
                print(f"{LAVENDER}  │{RESET} {wrapped}")
        else:
            print(f"{LAVENDER}  │{RESET}")
    print(f"{LAVENDER}  ╰────────────────────────────────────────{RESET}\n")
    if TTS_ENABLED:
        speak(text)

# ── --help screen ────────────────────────────────────────────────────────────────
def show_help():
    tts = f"{GREEN}ON  ({TTS_VOICE}){RESET}" if TTS_ENABLED else f"{GREY}OFF{RESET}"
    print(f"""
{LIME}{BOLD}  SaShell v{VERSION} — Full Command Reference{RESET}
{GREY}  ══════════════════════════════════════════════════════════════{RESET}

{CYAN}{BOLD}  FILE & DIRECTORY{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}ls -la{RESET}                      list all files with details & hidden
  {AMBER}ls -lh{RESET}                      human readable sizes
  {AMBER}cd <dir>{RESET}  /  {AMBER}cd ..{RESET}  /  {AMBER}cd ~{RESET}   navigate directories
  {AMBER}pwd{RESET}                          print current directory
  {AMBER}mkdir -p a/b/c{RESET}              create nested directories
  {AMBER}rm <file>{RESET}                    delete file
  {AMBER}rm -rf <dir>{RESET}                 delete folder recursively  {MAGENTA}⚠{RESET}
  {AMBER}cp -r <src> <dst>{RESET}            copy file or folder
  {AMBER}mv <src> <dst>{RESET}               move or rename
  {AMBER}touch <file>{RESET}                 create empty file
  {AMBER}cat / less / head / tail{RESET}     read file contents
  {AMBER}tail -f <file>{RESET}               follow file live (logs)
  {AMBER}wc -l <file>{RESET}                 count lines
  {AMBER}diff <f1> <f2>{RESET}               compare two files
  {AMBER}find . -name "*.py"{RESET}          find files by name pattern
  {AMBER}find . -size +100M{RESET}           find files over 100MB
  {AMBER}du -ah . | sort -rh | head -10{RESET}  top 10 biggest files
  {AMBER}stat <file>{RESET}                  file metadata
  {AMBER}file <file>{RESET}                  detect file type
  {AMBER}ln -s <target> <link>{RESET}        create symlink
  {AMBER}chmod +x <file>{RESET}              make executable
  {AMBER}chmod 755 <file>{RESET}             set permissions
  {AMBER}chown user:group <file>{RESET}      change ownership

{CYAN}{BOLD}  SEARCH & TEXT PROCESSING{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}grep -rn "pattern" .{RESET}         recursive search with line numbers
  {AMBER}grep -i "pattern" <file>{RESET}      case-insensitive search
  {AMBER}awk '{{print $1}}' <file>{RESET}      print first column
  {AMBER}sed 's/old/new/g' <file>{RESET}      find and replace
  {AMBER}cut -d',' -f1 <file>{RESET}          cut by delimiter
  {AMBER}sort -rn <file>{RESET}               reverse numeric sort
  {AMBER}uniq <file>{RESET}                   remove duplicate lines
  {AMBER}tr 'a-z' 'A-Z'{RESET}               transform characters
  {AMBER}xargs{RESET}                         pipe args to command

{CYAN}{BOLD}  PIPES, REDIRECTS & CHAINING{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}cmd1 | cmd2{RESET}                  pipe output to next command
  {AMBER}cmd > file{RESET}                   redirect output (overwrite)
  {AMBER}cmd >> file{RESET}                  append output to file
  {AMBER}cmd 2> err.log{RESET}               redirect stderr
  {AMBER}cmd &> all.log{RESET}               redirect stdout + stderr
  {AMBER}cmd1 && cmd2{RESET}                 run cmd2 only if cmd1 succeeds
  {AMBER}cmd1 || cmd2{RESET}                 run cmd2 only if cmd1 fails
  {AMBER}cmd &{RESET}                        run in background
  {AMBER}$(cmd){RESET}                       command substitution

{CYAN}{BOLD}  PROCESSES & SYSTEM{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}ps aux --sort=-%cpu | head -10{RESET}  top CPU hogs
  {AMBER}top{RESET}  /  {AMBER}htop{RESET}                live process monitor
  {AMBER}kill <pid>{RESET}  /  {AMBER}killall <name>{RESET}  kill process  {MAGENTA}⚠{RESET}
  {AMBER}jobs{RESET}  /  {AMBER}bg{RESET}  /  {AMBER}fg{RESET}          job control
  {AMBER}nohup cmd &{RESET}                  run immune to hangup
  {AMBER}uptime{RESET}                       uptime & load averages
  {AMBER}uname -a{RESET}                     full system info
  {AMBER}whoami{RESET}  /  {AMBER}who{RESET}  /  {AMBER}id{RESET}        user info
  {AMBER}hostname{RESET}  /  {AMBER}date{RESET}  /  {AMBER}cal{RESET}    system info
  {AMBER}env{RESET}  /  {AMBER}export VAR=val{RESET}       environment variables
  {AMBER}history | tail -20{RESET}           last 20 commands
  {AMBER}watch -n 2 <cmd>{RESET}             repeat command every 2s
  {AMBER}time <cmd>{RESET}                   measure command runtime

{CYAN}{BOLD}  DISK & MEMORY{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}df -h{RESET}                        disk usage
  {AMBER}free -h{RESET}                      RAM & swap usage
  {AMBER}lsblk{RESET}                        list block devices
  {AMBER}du -sh <dir>{RESET}                 size of a directory

{CYAN}{BOLD}  NETWORK{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}ip addr show{RESET}                 network interfaces & IPs
  {AMBER}ss -tuln{RESET}                     open ports
  {AMBER}ping <host>{RESET}                  ping a host
  {AMBER}curl -O <url>{RESET}                download file
  {AMBER}wget <url>{RESET}                   download file
  {AMBER}ssh user@host{RESET}                SSH into remote machine
  {AMBER}scp file user@host:/path{RESET}     copy file to remote
  {AMBER}rsync -av src/ dst/{RESET}          sync folders
  {AMBER}dig <domain>{RESET}                 DNS lookup
  {AMBER}traceroute <host>{RESET}            trace network path

{CYAN}{BOLD}  ARCHIVES & COMPRESSION{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}tar -czf out.tar.gz dir/{RESET}     compress to .tar.gz
  {AMBER}tar -xzf file.tar.gz{RESET}         extract .tar.gz
  {AMBER}zip -r out.zip dir/{RESET}           zip a folder
  {AMBER}unzip file.zip{RESET}               extract zip
  {AMBER}gzip / gunzip{RESET}                compress / decompress

{CYAN}{BOLD}  GIT{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}git init / clone <url>{RESET}        init or clone repo
  {AMBER}git status / diff{RESET}             check changes
  {AMBER}git add . && git commit -m "msg"{RESET}  stage and commit
  {AMBER}git push / pull{RESET}               sync with remote
  {AMBER}git log --oneline{RESET}             compact history
  {AMBER}git checkout -b <branch>{RESET}      create & switch branch
  {AMBER}git stash{RESET}                     stash uncommitted changes

{CYAN}{BOLD}  PACKAGE MANAGERS{RESET} {MAGENTA}(all ask y/N){RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}apt install / remove <pkg>{RESET}    Debian/Ubuntu packages
  {AMBER}apt update && apt upgrade{RESET}     update system           {MAGENTA}⚠{RESET}
  {AMBER}pip install <pkg>{RESET}             Python packages
  {AMBER}pip list / pip show <pkg>{RESET}     inspect packages
  {AMBER}npm install <pkg>{RESET}             Node packages

{CYAN}{BOLD}  SERVICES (systemctl){RESET} {MAGENTA}(ask y/N){RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}systemctl status <svc>{RESET}        check service status
  {AMBER}systemctl start/stop/restart{RESET}  control services        {MAGENTA}⚠{RESET}
  {AMBER}systemctl enable <svc>{RESET}        enable on boot
  {AMBER}journalctl -f{RESET}                 follow system logs

{MAGENTA}{BOLD}  AI SAFETY NET{RESET} {GREY}(silent — on every command){RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  Dangerous commands      → asks {BOLD}y/N{RESET} before running
  Typos / syntax errors   → suggests the fix, asks y/N
  Easter egg phrases      → plays the egg 🥚
  Sarvam offline          → runs anyway, never blocks you

{PINK}{BOLD}  CHAT MODE{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}i wanna talk with you{RESET}  /  {AMBER}lets chat{RESET}   open AI chat
  {GREY}  inside chat → type 'back' to return to shell{RESET}

{ORANGE}{BOLD}  TTS — TEXT TO SPEECH{RESET}  Status: {tts}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}tts on / tts off{RESET}             enable or disable
  {AMBER}tts say <text>{RESET}               speak any text now
  {AMBER}tts replay{RESET}                   replay last chat reply
  {AMBER}tts voice <name>{RESET}             change voice
  {AMBER}--tts{RESET}                        toggle on/off instantly
  {GREY}  Voices: Shubh Aditya Ritu Priya Neha Rahul Pooja Rohan{RESET}
  {GREY}          Simran Kavya Amit Dev Ishita Shreya Varun Kabir{RESET}
  {GREY}  Falls back to pyttsx3 (offline) if Sarvam TTS unavailable{RESET}

{GREEN}{BOLD}  SASHELL FLAGS & BUILTINS{RESET}
  {GREY}──────────────────────────────────────────────────────────────{RESET}
  {AMBER}python3 sashell.py --help{RESET}    this screen (pre-boot)
  {AMBER}python3 sashell.py --version{RESET} version & status
  {AMBER}python3 sashell.py --tts{RESET}     boot with TTS on
  {AMBER}python3 sashell.py --no-ai{RESET}   pure shell, zero AI
  {AMBER}python3 sashell.py --lang=Hindi{RESET}  AI replies in Hindi
  {AMBER}python3 sashell.py --colour=matrix{RESET}  start with a colour theme
  {AMBER}lang Hindi{RESET}                   change AI language live
  {AMBER}theme matrix{RESET}                 switch colour theme
  {AMBER}colour red{RESET}  /  {AMBER}color blue{RESET}     same as theme
  {GREY}  Themes: default red blue pink gold purple matrix ocean{RESET}
  {AMBER}fortune{RESET}                      terminal fortune 🔮
  {AMBER}clear{RESET}                        clear screen
  {AMBER}exit / quit{RESET}                  leave SaShell

{GREY}  ⚠  Danger commands always ask y/N. You're always in control.{RESET}
{GREY}  🥚 Easter eggs hidden throughout. Explore.{RESET}
{GREY}  ══════════════════════════════════════════════════════════════{RESET}
""")

def show_version():
    print(f"""
{LIME}{BOLD}  SaShell v{VERSION}{RESET}
  {GREY}Real Linux shell + Sarvam AI safety net{RESET}
  Model:   {CYAN}sarvam-m{RESET}
  TTS:     {CYAN}bulbul:v3{RESET}  ({TTS_VOICE})
  TTS on:  {GREEN if TTS_ENABLED else GREY}{TTS_ENABLED}{RESET}
  Lang:    {CYAN}{SHELL_LANG}{RESET}
  Theme:   {CYAN}{COLOUR_THEME}{RESET}
  Python:  {CYAN}{sys.version.split()[0]}{RESET}
  Key set: {GREEN}yes{RESET if SARVAM_API_KEY else RED + "no" + RESET}
""")

# ── Chat mode ────────────────────────────────────────────────────────────────────
CHAT_TRIGGERS = {
    "i wanna talk with you", "i want to talk with you",
    "lets chat", "let's chat", "open chat", "chat mode", "talk to me",
}

def chat_mode():
    history = []
    cols = shutil.get_terminal_size().columns
    bar = "─" * min(cols - 4, 52)
    print(f"\n{PINK}{BOLD}  ┌{bar}┐{RESET}")
    print(f"{PINK}{BOLD}  │{'  💬  CHAT MODE — SaShell is all ears  ':^{len(bar)}}│{RESET}")
    print(f"{PINK}{BOLD}  └{bar}┘{RESET}")
    tts_hint = f"  {GREEN}🔊 TTS is ON — replies will be spoken.{RESET}" if TTS_ENABLED else ""
    print(f"{GREY}  type 'back' to return to shell | '--tts' to toggle speech{tts_hint}\n{RESET}")

    while True:
        try:
            raw = chat_prompt()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        print(RESET, end="")
        msg = raw.strip()
        if not msg:
            continue

        low = msg.lower()

        if low in ("back", "exit chat", "quit chat", "shell", "exit"):
            print(f"\n{LIME}  ↩  Back to shell.{RESET}\n")
            break

        # TTS controls inside chat
        if low == "--tts" or low == "tts":
            toggle_tts()
            continue
        if low == "tts replay" or low == "--tts replay":
            if LAST_MESSAGE:
                speak(LAST_MESSAGE)
            else:
                print(f"{AMBER}  Nothing to replay yet.{RESET}\n")
            continue

        history.append({"role": "user", "content": msg})
        spinner_msg("SaShell is thinking...")
        try:
            reply = ask_sarvam_chat(history)
        except Exception as e:
            clear_line()
            print(f"{RED}  Sarvam error: {e}{RESET}\n")
            history.pop()
            continue
        clear_line()
        history.append({"role": "assistant", "content": reply})
        print_chat_reply(reply)   # handles TTS internally

# ── TTS helpers ──────────────────────────────────────────────────────────────────
def toggle_tts():
    global TTS_ENABLED
    TTS_ENABLED = not TTS_ENABLED
    state = f"{GREEN}ON  🔊{RESET}" if TTS_ENABLED else f"{GREY}OFF{RESET}"
    print(f"\n  TTS: {state}\n")

def handle_tts_command(parts):
    """Handle: tts on/off/replay/say/voice"""
    global TTS_ENABLED, TTS_VOICE
    sub = parts[1].lower() if len(parts) > 1 else ""

    if sub == "on":
        TTS_ENABLED = True
        print(f"\n  {GREEN}🔊 TTS enabled. Voice: {TTS_VOICE}{RESET}\n")
    elif sub == "off":
        TTS_ENABLED = False
        print(f"\n  {GREY}🔇 TTS disabled.{RESET}\n")
    elif sub == "replay":
        if LAST_MESSAGE:
            speak(LAST_MESSAGE)
        else:
            print(f"{AMBER}  Nothing to replay yet. Chat first.{RESET}\n")
    elif sub == "say":
        text = " ".join(parts[2:])
        if text:
            speak(text)
        else:
            print(f"{AMBER}  Usage: tts say <your text here>{RESET}\n")
    elif sub == "voice":
        voice = parts[2] if len(parts) > 2 else ""
        if voice:
            TTS_VOICE = voice
            print(f"\n  {CYAN}Voice set to: {BOLD}{TTS_VOICE}{RESET}\n")
        else:
            print(f"{AMBER}  Usage: tts voice <name>  e.g. tts voice Ritu{RESET}\n")
    else:
        # bare 'tts' toggles
        toggle_tts()

# ── Builtin: cd ──────────────────────────────────────────────────────────────────
def do_cd(args):
    target = os.path.expandvars(os.path.expanduser(args[0] if args else "~"))
    try:
        os.chdir(target)
    except FileNotFoundError:
        print(f"{RED}  cd: no such directory: {target}{RESET}")
    except PermissionError:
        print(f"{RED}  cd: permission denied: {target}{RESET}")

# ── Main loop ────────────────────────────────────────────────────────────────────
def main():
    global SARVAM_API_KEY, TTS_ENABLED, SHELL_LANG, COLOUR_THEME

    # ── parse CLI args ──
    args = sys.argv[1:]
    no_ai = "--no-ai" in args
    if "--tts" in args:
        TTS_ENABLED = True
    for a in args:
        if a.startswith("--lang="):
            SHELL_LANG = a.split("=", 1)[1].strip()
        if a.startswith("--colour=") or a.startswith("--color="):
            apply_theme(a.split("=", 1)[1].strip())
    if "--version" in args:
        # print version without full boot
        print(f"SaShell v{VERSION}")
        sys.exit(0)
    if "--help" in args or "-h" in args:
        # show help and exit (pre-boot)
        print(f"\n{LIME}{BOLD}SaShell v{VERSION}{RESET}")
        show_help()
        sys.exit(0)

    banner()
    setup_readline()

    if no_ai:
        print(f"{AMBER}  ⚡ Running in --no-ai mode. Pure shell, no Sarvam.{RESET}\n")
        SARVAM_API_KEY = "NO_AI"
    else:
        SARVAM_API_KEY = SARVAM_API_KEY or get_api_key()

    while True:
        try:
            raw = shell_prompt()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{LIME}  Bye! Stay chaotic. 🌀{RESET}\n")
            break

        print(RESET, end="")
        user_input = raw.strip()
        if not user_input:
            continue

        lower = user_input.lower().strip("!?.~ ")
        tokens = user_input.split()

        # ── SaShell builtins ──────────────────────────────────────────────
        if lower in ("exit", "quit", "q", "bye"):
            print(f"\n{LIME}  ✌  Later. May your paths always resolve.{RESET}\n")
            break

        if lower in ("--help", "help", "?"):
            show_help()
            continue

        if lower == "--version":
            show_version()
            continue

        if lower == "clear":
            os.system("clear")
            continue

        # ── Lang control ─────────────────────────────────────────────────
        if tokens[0].lower() == "lang":
            if len(tokens) > 1:
                SHELL_LANG = " ".join(tokens[1:])
                print(f"\n  {CYAN}AI language set to: {BOLD}{SHELL_LANG}{RESET}\n")
            else:
                print(f"\n  {CYAN}Current AI language: {BOLD}{SHELL_LANG}{RESET}")
                print(f"  {GREY}Usage: lang Hindi  /  lang Tamil  /  lang English{RESET}\n")
            continue

        # ── Theme / colour control ───────────────────────────────────────
        if tokens[0].lower() in ("theme", "colour", "color"):
            if len(tokens) > 1:
                apply_theme(tokens[1])
            else:
                available = ", ".join(THEMES.keys())
                print(f"\n  {CYAN}Current theme: {BOLD}{COLOUR_THEME}{RESET}")
                print(f"  {GREY}Available: {available}{RESET}")
                print(f"  {GREY}Usage: theme matrix  /  colour red  /  color ocean{RESET}\n")
            continue

        # ── TTS controls ──────────────────────────────────────────────────
        if tokens[0].lower() == "tts":
            handle_tts_command(tokens)
            continue

        if lower == "--tts":
            toggle_tts()
            continue

        # ── Chat mode ─────────────────────────────────────────────────────
        if lower in CHAT_TRIGGERS or lower.startswith("i wanna talk") or lower.startswith("i want to talk"):
            chat_mode()
            continue

        # ── Fortune ───────────────────────────────────────────────────────
        if any(w in lower for w in ("fortune", "predict my future")):
            msg = random.choice(FORTUNES)
            print(f"\n{MAGENTA}  🔮  {msg}{RESET}\n")
            if TTS_ENABLED:
                speak(msg)
            continue

        # ── cd builtin ────────────────────────────────────────────────────
        if tokens[0] == "cd":
            do_cd(tokens[1:])
            continue

        # ── Local easter eggs ─────────────────────────────────────────────
        if lower in LOCAL_EGGS:
            msg = LOCAL_EGGS[lower]
            print(f"\n{msg}\n")
            if TTS_ENABLED:
                speak(re.sub(r"\033\[[0-9;]*m", "", msg))
            continue

        # ── no-ai mode: just run it ───────────────────────────────────────
        if no_ai:
            run_command(user_input)
            print()
            continue

        # ── AI judges the command ─────────────────────────────────────────
        spinner_msg("checking...")
        try:
            verdict = judge_command(user_input)
        except Exception:
            verdict = "OK"   # if AI is down, don't block the user
        clear_line()

        if verdict == "EASTER_EGG":
            spinner_msg("SaShell has something to say...")
            try:
                reply = ask_sarvam_chat([{"role": "user", "content": user_input}])
            except Exception:
                reply = "🥚 Easter egg detected. No further comment."
            clear_line()
            print(f"\n{MAGENTA}  🥚  {reply}{RESET}\n")
            if TTS_ENABLED:
                speak(reply)
            continue

        if verdict == "TYPO":
            spinner_msg("fixing typo...")
            try:
                fixed = fix_typo(user_input).strip("`' \n")
            except Exception:
                fixed = ""
            clear_line()
            if fixed and fixed.lower() != user_input.lower():
                print(f"\n{AMBER}  ✏  Did you mean: {BOLD}{fixed}{RESET}")
                ans = input(f"{AMBER}  Run the fixed command? [Y/n]: {RESET}").strip().lower()
                run_command(fixed if ans not in ("n", "no") else user_input)
            else:
                run_command(user_input)
            print()
            continue

        if verdict == "DANGEROUS":
            print(f"\n{RED}  ⚠  Dangerous command:{RESET} {BOLD}{user_input}{RESET}")
            ans = input(f"{AMBER}  Run it? [y/N]: {RESET}").strip().lower()
            if ans not in ("y", "yes"):
                print(f"{GREY}  Aborted.{RESET}\n")
                continue
            print()

        # OK — just run it
        run_command(user_input)
        print()

if __name__ == "__main__":
    main()