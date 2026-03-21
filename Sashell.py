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

import os, sys, subprocess, random, json, re, textwrap, shutil, base64, tempfile, time, threading
import urllib.request, urllib.error
import shutil as _shutil

try:
    import readline as _rl
    HAS_READLINE = True
except ImportError:
    _rl = None
    HAS_READLINE = False

VERSION = "1.0.0"

# ── Colours ───────────────────────────────────────────────────────────────────
RESET    = "\033[0m"
BOLD     = "\033[1m"
DIM      = "\033[2m"
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

# ── Themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "default": {"LIME":"154","MAGENTA":"198","CYAN":"51","AMBER":"214","LAVENDER":"183","GREEN":"82","GREY":"244","PINK":"213","ORANGE":"208"},
    "red":     {"LIME":"196","MAGENTA":"160","CYAN":"203","AMBER":"208","LAVENDER":"204","GREEN":"202","GREY":"244","PINK":"197","ORANGE":"202"},
    "blue":    {"LIME":"39", "MAGENTA":"63", "CYAN":"45", "AMBER":"75", "LAVENDER":"111","GREEN":"33", "GREY":"244","PINK":"69", "ORANGE":"67"},
    "pink":    {"LIME":"213","MAGENTA":"207","CYAN":"218","AMBER":"219","LAVENDER":"183","GREEN":"212","GREY":"244","PINK":"205","ORANGE":"211"},
    "gold":    {"LIME":"220","MAGENTA":"214","CYAN":"228","AMBER":"226","LAVENDER":"222","GREEN":"184","GREY":"244","PINK":"221","ORANGE":"214"},
    "purple":  {"LIME":"141","MAGENTA":"135","CYAN":"183","AMBER":"147","LAVENDER":"189","GREEN":"135","GREY":"244","PINK":"177","ORANGE":"141"},
    "matrix":  {"LIME":"46", "MAGENTA":"34", "CYAN":"40", "AMBER":"82", "LAVENDER":"28", "GREEN":"46", "GREY":"22", "PINK":"34", "ORANGE":"40"},
    "ocean":   {"LIME":"87", "MAGENTA":"51", "CYAN":"123","AMBER":"159","LAVENDER":"117","GREEN":"49", "GREY":"244","PINK":"122","ORANGE":"86"},
}
COLOUR_THEME = "default"

def apply_theme(name):
    global LIME, MAGENTA, CYAN, AMBER, LAVENDER, GREEN, GREY, PINK, ORANGE, COLOUR_THEME
    t = THEMES.get(name.lower())
    if not t:
        print(f"{RED}  Unknown theme: {name}. Available: {', '.join(THEMES)}{RESET}\n")
        return
    def c(n): return f"\033[38;5;{n}m"
    LIME, MAGENTA, CYAN  = c(t["LIME"]), c(t["MAGENTA"]), c(t["CYAN"])
    AMBER, LAVENDER      = c(t["AMBER"]), c(t["LAVENDER"])
    GREEN, GREY          = c(t["GREEN"]), c(t["GREY"])
    PINK, ORANGE         = c(t["PINK"]), c(t["ORANGE"])
    COLOUR_THEME         = name.lower()
    print(f"\n  {LIME}Theme: {BOLD}{name}{RESET}\n")

apply_theme("default")

# ── Global state ──────────────────────────────────────────────────────────────
SARVAM_API_KEY = "sk_v13x3ob5_TslaNd4aDKiufotX6jVHezQA"  # TODO: remove before push
TTS_ENABLED    = False
TTS_VOICE      = "anushka"
LAST_MESSAGE   = ""
SHELL_LANG     = "English"

# ── Config / paths ────────────────────────────────────────────────────────────
CONFIG_DIR  = os.path.expanduser("~/.sashell")
LOG_FILE    = os.path.join(CONFIG_DIR, "session.log")
NOTES_FILE  = os.path.join(CONFIG_DIR, "notes.txt")
os.makedirs(CONFIG_DIR, exist_ok=True)

LOG_ENABLED = False

def log(line):
    if not LOG_ENABLED:
        return
    try:
        from datetime import datetime
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {line}\n")
    except Exception:
        pass

# ── Boot messages / fortunes ──────────────────────────────────────────────────
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
    "The best code is code you don't have to write.",
    "Premature optimisation is the root of all evil. — Knuth",
    "Any fool can write code a computer can understand. Good programmers write code humans can understand.",
    "The quieter you become, the more you can hear. — Ram Dass",
    "The obstacle is the path. — Zen proverb",
    "Before enlightenment, chop wood, carry water. After enlightenment, chop wood, carry water.",
    "You can't step in the same river twice. — Heraclitus",
    "The unexamined life is not worth living. — Socrates",
    "Man is condemned to be free. — Sartre",
    "Act without expectation. — Lao Tzu",
    "We suffer more in imagination than in reality. — Seneca",
    "Pain is inevitable. Suffering is optional. — Haruki Murakami",
    "Arise, awake, and stop not until the goal is reached. — Swami Vivekananda",
    "Be the change you wish to see in the world. — Gandhi",
    "You have the right to perform your actions, not to the fruits of your actions. — Bhagavad Gita",
    "Yogah karmasu kaushalam — Excellence in action is yoga. — Bhagavad Gita",
    "Truth alone triumphs. — Mundaka Upanishad",
    "Not all who wander are lost. — Tolkien (some are just lost in node_modules)",
    "One must imagine Sisyphus happy. — Camus (he was debugging)",
]

# ── Easter eggs ───────────────────────────────────────────────────────────────
LOCAL_EGGS = {
    "sudo make me a sandwich": f"{MAGENTA}🥪  Okay okay... *makes sandwich* ...but just this once.{RESET}",
    "what is love":            f"{MAGENTA}💘  Baby don't hurt me... don't hurt me... no more. (also: 42){RESET}",
    "meaning of life":         f"{LIME}✨  42. Obviously. Now go break something.{RESET}",
    "who are you":             f"{LIME}🤖  SaShell — real shell, Sarvam brain, zero chill.{RESET}",
    "why":                     f"{AMBER}🤔  Because entropy demands it.{RESET}",
    "hello":                   f"{CYAN}👋  Namaste! Ready to break something?{RESET}",
    "hi":                      f"{CYAN}👋  Hey. Let's do something dangerous together.{RESET}",
    "have you tried turning it off and on again": f"{LIME}💡  Step 1 of every IT certification.{RESET}",
    "git blame":               f"{AMBER}🫵  It was you. It's always you.{RESET}",
    "it works on my machine":  f"{MAGENTA}🚢  Then we'll ship your machine.{RESET}",
    "undefined is not a function": f"{RED}💀  JavaScript sends its regards.{RESET}",
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
    "yolo":                    f"{MAGENTA}🎲  git push --force --no-verify energy detected.{RESET}",
    "good morning":            f"{AMBER}☀️  Morning! Hope your cron jobs ran clean.{RESET}",
    "good night":              f"{LAVENDER}🌙  Sleep well. Your background processes won't.{RESET}",
    "thank you":               f"{LIME}💚  Just doing my job. Unlike your tests.{RESET}",
    "thanks":                  f"{LIME}💚  You're welcome. Now go write some docs.{RESET}",
    "rm -rf /":                f"{RED}🚨  Nice try, chaos agent. I have STANDARDS.{RESET}",
    "i am hungry":             "SAMOSA",
    "sudo i am hungry":        "SAMOSA",
    "it is what it is":        f"{GREY}🤷  Classic senior engineer response.{RESET}",
    "i am bored":              f"{LIME}😴  Have you tried rm -rf on your boredom? (don't){RESET}",
}

# ── Dangerous patterns ────────────────────────────────────────────────────────
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

# ── Sarvam API ────────────────────────────────────────────────────────────────
SARVAM_CHAT_URL = "https://api.sarvam.ai/v1/chat/completions"
SARVAM_TTS_URL  = "https://api.sarvam.ai/text-to-speech"
SARVAM_MODEL    = "sarvam-m"

JUDGE_SYSTEM = """You are SaShell's command safety judge. The user typed a command into a real Linux shell.
Classify into exactly ONE category. Reply with ONLY that one word:
DANGEROUS  - could delete data, modify system, install software, kill processes
EASTER_EGG - joke, meme, or non-command phrase
TYPO       - looks like a real command but has a typo or syntax error
OK         - valid safe shell command"""

CHAT_SYSTEM = """You are SaShell's built-in AI companion — witty, helpful, slightly chaotic.
You live inside a real Linux terminal shell called SaShell, powered by Sarvam AI.
Answer anything: tech help, general knowledge, jokes, life advice, or just chat.
Keep answers concise. You support English and all Indian languages."""

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
    lang_note = f" Always respond in {SHELL_LANG}." if SHELL_LANG.lower() != "english" else ""
    system = CHAT_SYSTEM + lang_note
    return _call_sarvam([{"role": "system", "content": system}] + history, max_tokens=1024)

def fix_typo(cmd):
    result = _call_sarvam([
        {"role": "system", "content": "Fix the typo/syntax error in this shell command. Reply with ONLY the corrected command, no explanation, no backticks."},
        {"role": "user",   "content": cmd},
    ], max_tokens=64)
    return strip_think(result).strip("`' \n")

# ── TTS ───────────────────────────────────────────────────────────────────────
def _speak_pyttsx3(text):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except ImportError:
        print(f"{AMBER}  pyttsx3 not installed. Run: pip install pyttsx3{RESET}")
    except Exception as e:
        print(f"{RED}  pyttsx3 error: {e}{RESET}")

def speak(text):
    if not text.strip():
        return
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
        headers={"Content-Type": "application/json", "api-subscription-key": SARVAM_API_KEY},
        method="POST",
    )
    try:
        spinner_msg("🔊 generating audio...")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw_resp = resp.read()
        except urllib.error.HTTPError as e:
            clear_line()
            if e.code in (400, 401, 403):
                print(f"{AMBER}  🔊 Sarvam TTS unavailable — using offline voice.{RESET}")
                _speak_pyttsx3(clean)
            else:
                print(f"{RED}  TTS error {e.code}: {e.read().decode()}{RESET}")
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



# ── Spinning Donut (donut.c algorithm in Python) ─────────────────────────────
def _show_samosa():
    import math, sys
    R1, R2, K2 = 1.0, 2.0, 5.0
    W, H = 60, 28
    K1 = H * K2 * 3 / (8 * (R1 + R2))
    CHARS = ".,-~:;=!*#$@"
    A, B = 0.0, 0.0
    grad = [LIME, CYAN, AMBER, MAGENTA, LIME]
    sys.stdout.write("\033[?25l"); sys.stdout.flush()
    print()
    try:
        for frame in range(130):
            out  = [" "] * (W * H)
            zbuf = [0.0] * (W * H)
            sinA, cosA = math.sin(A), math.cos(A)
            sinB, cosB = math.sin(B), math.cos(B)
            t = 0.0
            while t < 6.2832:
                sT, cT = math.sin(t), math.cos(t)
                p = 0.0
                while p < 6.2832:
                    sP, cP = math.sin(p), math.cos(p)
                    cx = R2 + R1 * cT
                    cy = R1 * sT
                    x  = cx*(cosB*cP + sinA*sinB*sP) - cy*cosA*sinB
                    y  = cx*(sinB*cP - sinA*cosB*sP) + cy*cosA*cosB
                    z  = K2 + cosA*cx*sP + cy*sinA
                    iz = 1.0 / z
                    px = int(W/2 + K1*iz*x)
                    py = int(H/2 - K1*iz*y*0.5)
                    L  = (cP*cT*sinB - cosA*cT*sP - sinA*sT + cosB*(cosA*sT - cT*sinA*sP))
                    if 0 <= px < W and 0 <= py < H:
                        idx = py*W + px
                        if iz > zbuf[idx]:
                            zbuf[idx] = iz
                            li = int(L * 8)
                            out[idx] = CHARS[max(0, li)] if li >= 0 else "."
                    p += 0.07
                t += 0.07
            if frame > 0:
                sys.stdout.write(f"\033[{H+2}A")
            for row in range(H):
                line = ""
                for col in range(W):
                    ch = out[row*W + col]
                    if ch == " ":
                        line += " "
                    else:
                        ci = int(col / W * (len(grad)-1))
                        line += grad[ci] + ch + RESET
                sys.stdout.write("  " + line + "\n")
            sys.stdout.write("\n"); sys.stdout.flush()
            A += 0.07; B += 0.03
            time.sleep(0.033)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h"); sys.stdout.flush()
    print(f"\n  \U0001f369  {LIME}Here is a donut, bhai. You deserve it.{RESET}\n")

# ── API key ───────────────────────────────────────────────────────────────────
def get_api_key():
    import getpass
    key = os.environ.get("SARVAM_API_KEY", "").strip()
    if key:
        print(f"{GREEN}  ✓ Key loaded from environment.{RESET}\n")
        return key
    print(f"{AMBER}  No SARVAM_API_KEY found.{RESET}")
    print(f"{GREY}  Get one free at: https://dashboard.sarvam.ai{RESET}")
    while not key:
        try:
            key = getpass.getpass(f"{CYAN}  Enter your Sarvam API key: {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{RED}  No key provided — exiting.{RESET}\n")
            sys.exit(1)
        if not key:
            print(f"{AMBER}  Key can't be empty.{RESET}")
    print(f"{GREEN}  ✓ Key accepted.{RESET}\n")
    return key

# ── Notes ─────────────────────────────────────────────────────────────────────
def open_notes():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("# SaShell Notes\n\n")
    editors = ["nano", "micro", "vim", "vi"]
    for ed in editors:
        if _shutil.which(ed):
            os.system(f"{ed} {NOTES_FILE}")
            return
    print(f"{AMBER}  No editor found. Notes at: {NOTES_FILE}{RESET}\n")

def note_cmd(tokens):
    sub = tokens[1].lower() if len(tokens) > 1 else "list"

    if sub in ("open", "edit"):
        open_notes()

    elif sub == "add":
        text = " ".join(tokens[2:])
        if not text:
            print(f"{AMBER}  Usage: note add <your note>{RESET}\n")
            return
        from datetime import datetime
        with open(NOTES_FILE, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {text}\n")
        print(f"{LIME}  ✓  Note saved.{RESET}\n")

    elif sub == "list":
        if not os.path.exists(NOTES_FILE):
            print(f"{GREY}  No notes yet. Use: note add <text>{RESET}\n")
            return
        with open(NOTES_FILE) as f:
            lines = f.readlines()
        notes = [l.rstrip() for l in lines if l.strip() and not l.startswith("#")]
        if not notes:
            print(f"{GREY}  No notes yet.{RESET}\n")
            return
        cols = shutil.get_terminal_size().columns
        bar = "─" * min(cols - 4, 56)
        print(f"\n{LAVENDER}{BOLD}  ┌{bar}┐{RESET}")
        print(f"{LAVENDER}{BOLD}  │{'  📝  NOTES':^{len(bar)}}│{RESET}")
        print(f"{LAVENDER}{BOLD}  ├{bar}┤{RESET}")
        for i, n in enumerate(notes[-20:], 1):
            display = f"  {i:2}. {n}"
            pad = max(0, len(bar) - len(display) - 1)
            truncated = display[:len(bar)-2]
            print(f"{LAVENDER}  │{RESET}{GREY}  {i:2}.{RESET} {n[:len(bar)-8]}{' '*pad}{LAVENDER}│{RESET}")
        print(f"{LAVENDER}{BOLD}  └{bar}┘{RESET}\n")

    elif sub == "clear":
        ans = input(f"{AMBER}  Clear all notes? [y/N]: {RESET}").strip().lower()
        if ans in ("y", "yes"):
            with open(NOTES_FILE, "w") as f:
                f.write("# SaShell Notes\n\n")
            print(f"{LIME}  ✓  Notes cleared.{RESET}\n")

    elif sub == "search":
        q = " ".join(tokens[2:]).lower()
        if not q:
            print(f"{AMBER}  Usage: note search <query>{RESET}\n")
            return
        if not os.path.exists(NOTES_FILE):
            print(f"{GREY}  No notes yet.{RESET}\n")
            return
        with open(NOTES_FILE) as f:
            matches = [l.rstrip() for l in f if q in l.lower() and l.strip()]
        if not matches:
            print(f"{GREY}  No notes matching '{q}'.{RESET}\n")
        else:
            for m in matches:
                print(f"  {LAVENDER}•{RESET} {m}")
            print()
    else:
        print(f"{GREY}  note add <text> | note list | note clear | note search <q> | note open{RESET}\n")

# ── Auto-suggest / readline ───────────────────────────────────────────────────
class AutoSuggestCompleter:
    def __init__(self):
        self.matches = []

    def complete(self, text, state):
        if state == 0:
            self.matches = []
            pass  # history search removed
        try:
            return self.matches[state]
        except IndexError:
            return None

def setup_readline():
    if not HAS_READLINE:
        return
    try:
        _rl.set_completer(AutoSuggestCompleter().complete)  # type: ignore
        _rl.parse_and_bind("tab: complete")                 # type: ignore
        _rl.parse_and_bind("set show-all-if-ambiguous on")  # type: ignore
        _rl.parse_and_bind("set completion-ignore-case on") # type: ignore
    except Exception:
        pass



# ── ASCII logo + gradient ─────────────────────────────────────────────────────
ASCII_LOGO = [
    " ██████╗ █████╗  ██████╗██╗  ██╗███████╗██╗     ██╗",
    "██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝██║     ██║",
    "╚█████╗ ███████║╚█████╗ ███████║█████╗  ██║     ██║",
    " ╚═══██╗██╔══██║ ╚═══██╗██╔══██║██╔══╝  ██║     ██║",
    "██████╔╝██║  ██║██████╔╝██║  ██║███████╗███████╗███████╗",
    "╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝",
]

GRAD_COLOURS = [
    "\033[38;5;154m", "\033[38;5;148m", "\033[38;5;118m",
    "\033[38;5;84m",  "\033[38;5;51m",  "\033[38;5;45m",
    "\033[38;5;39m",  "\033[38;5;198m",
]

def _gradient_line(line, offset):
    out = ""
    n = len(GRAD_COLOURS)
    for i, ch in enumerate(line):
        col = GRAD_COLOURS[(i // 6 + offset) % n]
        out += col + ch
    return out + RESET

def banner():
    os.system("clear")
    try:
        for frame in range(24):
            if frame > 0:
                print(f"\033[{len(ASCII_LOGO) + 1}A", end="")
            for line in ASCII_LOGO:
                print("  " + _gradient_line(line, frame))
            print()
            time.sleep(0.045)
    except Exception:
        for line in ASCII_LOGO:
            print(f"  {LIME}{line}{RESET}")
        print()

    print(f"  {GREY}Real Linux shell · Sarvam AI safety net · v{VERSION}{RESET}")
    print(f"  {GREY}{random.choice(BOOT_MESSAGES)}{RESET}\n")
    tts_status = f"{GREEN}ON ({TTS_VOICE}){RESET}" if TTS_ENABLED else f"{GREY}OFF{RESET}"
    lang_status = f"{CYAN}{SHELL_LANG}{RESET}"
    print(f"{DIM}  Type real Linux commands. AI watches for mistakes & danger.{RESET}")
    print(f"{DIM}  TTS: {tts_status}  │  Lang: {lang_status}  │  {BOLD}\"i wanna talk with you\"{RESET}{DIM} → chat  │  {BOLD}--help{RESET}{DIM} → guide{RESET}\n")

# ── Prompts ───────────────────────────────────────────────────────────────────
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

# ── Run command ───────────────────────────────────────────────────────────────
def run_command(cmd):
    log(f"RUN: {cmd}")
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print()
    except Exception as e:
        print(f"{RED}  error: {e}{RESET}")

# ── Chat reply box ────────────────────────────────────────────────────────────
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

# ── TTS controls ──────────────────────────────────────────────────────────────
def toggle_tts():
    global TTS_ENABLED
    TTS_ENABLED = not TTS_ENABLED
    state = f"{GREEN}ON 🔊{RESET}" if TTS_ENABLED else f"{GREY}OFF{RESET}"
    print(f"\n  TTS: {state}\n")

def handle_tts_command(tokens):
    global TTS_ENABLED, TTS_VOICE
    sub = tokens[1].lower() if len(tokens) > 1 else ""
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
            print(f"{AMBER}  Nothing to replay yet.{RESET}\n")
    elif sub == "say":
        text = " ".join(tokens[2:])
        if text:
            speak(text)
        else:
            print(f"{AMBER}  Usage: tts say <text>{RESET}\n")
    elif sub == "voice":
        voice = tokens[2] if len(tokens) > 2 else ""
        if voice:
            TTS_VOICE = voice
            print(f"\n  {CYAN}Voice: {BOLD}{TTS_VOICE}{RESET}\n")
        else:
            print(f"{AMBER}  Usage: tts voice <name>{RESET}\n")
    else:
        toggle_tts()

# ── Chat mode ─────────────────────────────────────────────────────────────────
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
    tts_hint = f"  {GREEN}🔊 TTS is ON.{RESET}" if TTS_ENABLED else ""
    print(f"{GREY}  type 'back' to return to shell{tts_hint}\n{RESET}")

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
        if msg.lower() in ("back", "exit chat", "shell", "exit"):
            print(f"\n{LIME}  ↩  Back to shell.{RESET}\n")
            break
        if msg.lower() in ("--tts", "tts"):
            toggle_tts()
            continue
        if msg.lower() in ("tts replay", "--tts replay"):
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
        print_chat_reply(reply)

# ── Help ──────────────────────────────────────────────────────────────────────
def show_help():
    tts = f"{GREEN}ON ({TTS_VOICE}){RESET}" if TTS_ENABLED else f"{GREY}OFF{RESET}"
    print(f"""
{LIME}{BOLD}  SaShell v{VERSION} — Full Command Reference{RESET}
{GREY}  ══════════════════════════════════════════════════════════════{RESET}

{CYAN}{BOLD}  SHELL{RESET} — all Linux commands work natively
  {GREY}  pipes · redirects · background jobs · wildcards · scripts{RESET}

{MAGENTA}{BOLD}  AI SAFETY NET{RESET} {GREY}(silent on every command){RESET}
  {GREY}────────────────────────────────────────────────────────────{RESET}
  Dangerous   → asks y/N before running
  Typos       → suggests fix, asks y/N
  Easter eggs → AI responds playfully
  Offline     → runs anyway, never blocks you

{PINK}{BOLD}  CHAT MODE{RESET}
  {GREY}────────────────────────────────────────────────────────────{RESET}
  {AMBER}i wanna talk with you{RESET}    open AI chat
  {AMBER}lets chat{RESET}                same
  {GREY}  inside chat → 'back' to return{RESET}

{ORANGE}{BOLD}  TTS{RESET}  Status: {tts}
  {GREY}────────────────────────────────────────────────────────────{RESET}
  {AMBER}tts on / off{RESET}             toggle
  {AMBER}tts say <text>{RESET}           speak text
  {AMBER}tts replay{RESET}               replay last reply
  {AMBER}tts voice <name>{RESET}         change voice
  {AMBER}--tts{RESET}                    quick toggle
  {GREY}  Voices: anushka aditya ritu priya neha rahul pooja rohan{RESET}
  {GREY}          simran kavya amit dev ishita shreya varun kabir{RESET}
  {GREY}  Falls back to pyttsx3 offline on error (pip install pyttsx3){RESET}

{LAVENDER}{BOLD}  NOTES{RESET}
  {GREY}────────────────────────────────────────────────────────────{RESET}
  {AMBER}note add <text>{RESET}          save a note
  {AMBER}note list{RESET}                show all notes
  {AMBER}note search <q>{RESET}          search notes
  {AMBER}note clear{RESET}               clear all notes
  {AMBER}note open{RESET}                open in nano/vim
  {AMBER}--notes{RESET}                  same as note open

{GREEN}{BOLD}  SESSION LOGGER{RESET}
  {GREY}────────────────────────────────────────────────────────────{RESET}
  {AMBER}log on{RESET}                   start logging to ~/.sashell/session.log
  {AMBER}log off{RESET}                  stop logging
  {AMBER}log open{RESET}                 open log in nano

{GREEN}{BOLD}  SASHELL BUILTINS{RESET}
  {GREY}────────────────────────────────────────────────────────────{RESET}
  {AMBER}help / --help{RESET}            this screen
  {AMBER}--version{RESET}                version info
  {AMBER}--tts{RESET}                    boot with TTS on
  {AMBER}--no-ai{RESET}                  pure shell, no AI
  {AMBER}--lang=Hindi{RESET}             AI responds in Hindi
  {AMBER}--colour=matrix{RESET}          set theme at boot
  {AMBER}lang <X>{RESET}                 change AI language
  {AMBER}theme / colour / color{RESET}   change theme
  {GREY}  Themes: default red blue pink gold purple matrix ocean{RESET}
  {AMBER}fortune{RESET}                  terminal wisdom 🔮
  {AMBER}clear{RESET}                    clear screen
  {AMBER}exit / quit{RESET}              leave SaShell

{GREY}  🥚 Easter eggs hidden throughout. Explore.{RESET}
{GREY}  ══════════════════════════════════════════════════════════════{RESET}
""")

def show_version():
    print(f"""
{LIME}{BOLD}  SaShell v{VERSION}{RESET}
  Model:   {CYAN}sarvam-m{RESET}
  TTS:     {CYAN}bulbul:v3 → pyttsx3 fallback{RESET}
  Voice:   {CYAN}{TTS_VOICE}{RESET}
  TTS on:  {GREEN if TTS_ENABLED else GREY}{TTS_ENABLED}{RESET}
  Lang:    {CYAN}{SHELL_LANG}{RESET}
  Theme:   {CYAN}{COLOUR_THEME}{RESET}
  Python:  {CYAN}{sys.version.split()[0]}{RESET}
""")

# ── cd builtin ────────────────────────────────────────────────────────────────
def do_cd(args):
    target = os.path.expandvars(os.path.expanduser(args[0] if args else "~"))
    try:
        os.chdir(target)
    except FileNotFoundError:
        print(f"{RED}  cd: no such directory: {target}{RESET}")
    except PermissionError:
        print(f"{RED}  cd: permission denied: {target}{RESET}")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    global SARVAM_API_KEY, TTS_ENABLED, SHELL_LANG, COLOUR_THEME, LOG_ENABLED

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
        print(f"SaShell v{VERSION}")
        sys.exit(0)
    if "--help" in args or "-h" in args:
        print(f"\n{LIME}{BOLD}SaShell v{VERSION}{RESET}")
        show_help()
        sys.exit(0)

    banner()
    setup_readline()

    if no_ai:
        print(f"{AMBER}  ⚡ --no-ai mode. Pure shell.{RESET}\n")
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

        log(f"INPUT: {user_input}")
        lower  = user_input.lower().strip("!?.~ ")
        tokens = user_input.split()

        # ── Builtins ──────────────────────────────────────────────────────
        if lower in ("exit", "quit", "q"):
            print(f"\n{LIME}  ✌  Later. May your paths always resolve.{RESET}\n")
            break

        if lower in ("--help", "help", "?"):
            show_help(); continue

        if lower == "--version":
            show_version(); continue

        if lower == "clear":
            os.system("clear"); continue

        if tokens[0] == "cd":
            do_cd(tokens[1:]); continue

        if lower in CHAT_TRIGGERS or lower.startswith("i wanna talk") or lower.startswith("i want to talk"):
            chat_mode(); continue

        if any(w in lower for w in ("fortune", "predict my future")):
            msg = random.choice(FORTUNES)
            print(f"\n{MAGENTA}  🔮  {msg}{RESET}\n")
            if TTS_ENABLED: speak(msg)
            continue

        # ── Lang ──────────────────────────────────────────────────────────
        if tokens[0].lower() == "lang":
            if len(tokens) > 1:
                SHELL_LANG = " ".join(tokens[1:])
                print(f"\n  {CYAN}Language: {BOLD}{SHELL_LANG}{RESET}\n")
            else:
                print(f"\n  {CYAN}Language: {BOLD}{SHELL_LANG}{RESET}\n")
            continue

        # ── Theme ─────────────────────────────────────────────────────────
        if tokens[0].lower() in ("theme", "colour", "color"):
            if len(tokens) > 1:
                apply_theme(tokens[1])
            else:
                print(f"\n  {CYAN}Theme: {BOLD}{COLOUR_THEME}{RESET}")
                print(f"  {GREY}Available: {', '.join(THEMES)}{RESET}\n")
            continue

        # ── TTS ───────────────────────────────────────────────────────────
        if tokens[0].lower() == "tts":
            handle_tts_command(tokens); continue

        if lower == "--tts":
            toggle_tts(); continue

        # ── Notes ─────────────────────────────────────────────────────────
        if tokens[0].lower() in ("note", "notes") or lower == "--notes":
            if lower == "--notes":
                open_notes()
            else:
                note_cmd(tokens)
            continue

        # ── Logger ────────────────────────────────────────────────────────
        if lower in ("log on", "log start"):
            LOG_ENABLED = True
            print(f"  {LIME}Logging ON → {LOG_FILE}{RESET}\n"); continue
        if lower in ("log off", "log stop"):
            LOG_ENABLED = False
            print(f"  {GREY}Logging OFF{RESET}\n"); continue
        if lower == "log open":
            os.system(f"nano {LOG_FILE}"); continue

        # ── Local easter eggs ─────────────────────────────────────────────
        if lower in LOCAL_EGGS:
            msg = LOCAL_EGGS[lower]
            if msg == "SAMOSA":
                _show_samosa()
                if TTS_ENABLED: speak("Here is a donut bhai. You deserve it.")
            else:
                print(f"\n{msg}\n")
                if TTS_ENABLED: speak(re.sub(r"\033\[[0-9;]*m", "", msg))
            continue

        # ── No-AI mode ────────────────────────────────────────────────────
        if no_ai:
            run_command(user_input); print(); continue

        # ── AI judge ──────────────────────────────────────────────────────
        spinner_msg("checking...")
        try:
            verdict = judge_command(user_input)
        except Exception:
            verdict = "OK"
        clear_line()

        if verdict == "EASTER_EGG":
            spinner_msg("SaShell has something to say...")
            try:
                reply = ask_sarvam_chat([{"role": "user", "content": user_input}])
            except Exception:
                reply = "🥚 Easter egg detected. No further comment."
            clear_line()
            print(f"\n{MAGENTA}  🥚  {reply}{RESET}\n")
            if TTS_ENABLED: speak(reply)
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
                ans = input(f"{AMBER}  Run fixed? [Y/n]: {RESET}").strip().lower()
                run_command(fixed if ans not in ("n", "no") else user_input)
            else:
                run_command(user_input)
            print(); continue

        if verdict == "DANGEROUS":
            print(f"\n{RED}  ⚠  Dangerous command:{RESET} {BOLD}{user_input}{RESET}")
            ans = input(f"{AMBER}  Run it? [y/N]: {RESET}").strip().lower()
            if ans not in ("y", "yes"):
                print(f"{GREY}  Aborted.{RESET}\n"); continue
            print()

        run_command(user_input)
        print()

if __name__ == "__main__":
    main()
