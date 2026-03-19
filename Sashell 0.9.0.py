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

VERSION = "1.0.0"

# ── Colours ─────────────────────────────────────────────────────────────────────
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

# ── Global state ─────────────────────────────────────────────────────────────────
SARVAM_API_KEY = "sk_v13x3ob5_TslaNd4aDKiufotX6jVHezQA"  # TODO: remove before push
TTS_ENABLED    = False          # toggled by --tts flag or `tts on/off` at runtime
TTS_VOICE      = "Shubh"        # default voice for bulbul:v3
LAST_MESSAGE   = ""             # last AI chat reply, for --tts replay
SHELL_LANG     = "English"        # preferred language for AI responses

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
    "sudo make me a sandwich": f"{MAGENTA}🥪  Okay okay... *makes sandwich* ...but just this once.{RESET}",
    "what is love":            f"{MAGENTA}💘  Baby don't hurt me... don't hurt me... no more. (also: 42){RESET}",
    "meaning of life":         f"{LIME}✨  42. Obviously. Now go break something.{RESET}",
    "who are you":             f"{LIME}🤖  SaShell — real shell, Sarvam brain, zero chill.{RESET}",
    "why":                     f"{AMBER}🤔  Because entropy demands it.{RESET}",
    "hello":                   f"{CYAN}👋  Namaste! Ready to break something?{RESET}",
    "hi":                      f"{CYAN}👋  Hey. Let's do something dangerous together.{RESET}",
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
        "speaker": TTS_VOICE,
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
            if http_err.code in (403, 401):
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

# ── UI helpers ───────────────────────────────────────────────────────────────────
def banner():
    print(f"\n{LIME}{BOLD}", end="")
    print(__doc__, end="")
    print(RESET)
    print(f"{GREY}  {random.choice(BOOT_MESSAGES)}{RESET}\n")
    print(f"{DIM}  Type real Linux commands. AI watches for mistakes & danger.{RESET}")
    tts_status = f"{GREEN}ON ({TTS_VOICE}){RESET}" if TTS_ENABLED else f"{GREY}OFF{RESET}"
    lang_status = f"{CYAN}{SHELL_LANG}{RESET}"
    print(f"{DIM}  TTS: {tts_status}  │  Lang: {lang_status}  │  Say {BOLD}\"i wanna talk with you\"{RESET}{DIM} for chat.  {BOLD}--help{RESET}{DIM} for guide.{RESET}\n")

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
{LIME}{BOLD}  SaShell v{VERSION} — Command Reference{RESET}
{GREY}  ══════════════════════════════════════════════════════{RESET}

{CYAN}{BOLD}  SHELL MODE{RESET} {GREY}(default — just type Linux commands){RESET}
  {GREY}────────────────────────────────────────────────────{RESET}
  {AMBER}ls -la{RESET}                    list files with details
  {AMBER}cd <dir>{RESET}                  change directory
  {AMBER}cat <file>{RESET}                print file contents
  {AMBER}grep <pattern> <file>{RESET}     search inside files
  {AMBER}find . -name "*.py"{RESET}       find files by pattern
  {AMBER}ps aux{RESET}                    show running processes
  {AMBER}df -h{RESET}                     disk usage
  {AMBER}free -h{RESET}                   memory usage
  {AMBER}top / htop{RESET}                live process monitor
  {AMBER}uname -r{RESET}                  kernel version
  {AMBER}ip addr show{RESET}              network interfaces
  {AMBER}ss -tuln{RESET}                  open ports
  {AMBER}uptime{RESET}                    system uptime
  {AMBER}who{RESET}                       who is logged in
  {AMBER}env{RESET}                       environment variables
  {AMBER}history{RESET}                   command history
  {AMBER}tar -czf out.tar.gz dir/{RESET}  compress a folder
  {AMBER}curl <url>{RESET}                fetch a URL
  {AMBER}ping <host>{RESET}               ping a host
  {AMBER}du -ah . | sort -rh | head -5{RESET}  top 5 biggest files
  {AMBER}chmod +x script.sh{RESET}        make script executable
  {AMBER}tail -f /var/log/syslog{RESET}   follow a log file

{MAGENTA}{BOLD}  AI SAFETY NET{RESET} {GREY}(runs silently on every command){RESET}
  {GREY}────────────────────────────────────────────────────{RESET}
  Dangerous commands     → asks {BOLD}y/N{RESET} before running
  Typos / syntax errors  → suggests the fix, asks to run
  Easter egg phrases     → plays the egg 🥚

{PINK}{BOLD}  CHAT MODE{RESET}
  {GREY}────────────────────────────────────────────────────{RESET}
  {AMBER}i wanna talk with you{RESET}     open AI chat
  {AMBER}lets chat{RESET}                 same thing
  {GREY}inside chat: type 'back' to return to shell{RESET}

{ORANGE}{BOLD}  TTS — TEXT TO SPEECH{RESET} {GREY}(Sarvam Bulbul v3){RESET}  Status: {tts}
  {GREY}────────────────────────────────────────────────────{RESET}
  {AMBER}tts on{RESET}                    enable TTS globally
  {AMBER}tts off{RESET}                   disable TTS
  {AMBER}tts replay{RESET}                replay last chat message
  {AMBER}tts say <text>{RESET}            speak any text aloud
  {AMBER}tts voice <name>{RESET}          change voice (e.g. Ritu, Priya, Rahul)
  {GREY}In chat mode: every AI reply is auto-spoken when TTS is ON{RESET}
  {GREY}Available voices: Anushka Ritu Priya Neha Rahul Pooja{RESET}
  {GREY}                  Rohan Simran Kavya Amit Dev Ishita{RESET}
  {GREY}Requires: aplay (Linux) or afplay (Mac){RESET}

{GREEN}{BOLD}  SASHELL BUILTINS{RESET}
  {GREY}────────────────────────────────────────────────────{RESET}
  {AMBER}--help{RESET}  or  {AMBER}help{RESET}          this screen
  {AMBER}--version{RESET}                 show version info
  {AMBER}--lang=Hindi{RESET}              set AI response language at boot
  {AMBER}lang Hindi{RESET}                change AI language while running
  {AMBER}lang{RESET}                      show current language
  {AMBER}fortune{RESET}                   get a terminal fortune 🔮
  {AMBER}clear{RESET}                     clear screen
  {AMBER}exit{RESET}  /  {AMBER}quit{RESET}            leave SaShell

{GREY}  🥚 Easter eggs hidden throughout. Explore.{RESET}
{GREY}  ══════════════════════════════════════════════════════{RESET}
""")

def show_version():
    print(f"""
{LIME}{BOLD}  SaShell v{VERSION}{RESET}
  {GREY}Real Linux shell + Sarvam AI safety net{RESET}
  Model:   {CYAN}sarvam-m{RESET}
  TTS:     {CYAN}bulbul:v3{RESET}  ({TTS_VOICE})
  TTS on:  {GREEN if TTS_ENABLED else GREY}{TTS_ENABLED}{RESET}
  Lang:    {CYAN}{SHELL_LANG}{RESET}
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
    global SARVAM_API_KEY, TTS_ENABLED, SHELL_LANG

    # ── parse CLI args ──
    args = sys.argv[1:]
    no_ai = "--no-ai" in args
    if "--tts" in args:
        TTS_ENABLED = True
    for a in args:
        if a.startswith("--lang="):
            SHELL_LANG = a.split("=", 1)[1].strip()
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