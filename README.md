# SaShell MK 2.0.4!!!

Real Linux shell with Sarvam AI as your safety net. Type real commands — AI only steps in when something looks dangerous, broken, or funny.
Go to the dist folder to find the .exe, download and enjoy! Or download the python file and run it in your terminal and enjoy!
---
<h3>Change log :
- A user can now type a command in plain english and the AI will translate that into actual linux commands which the user can select and run<br>
- Addded an ASCII analog vclock animation as an easter egg ( what is the time ) <br>
- A new Calculator feature where you can directly type simple arithmetic quistions like 16x8 and the terminal will answer that sum for you.<br>
 -Added a new demo mode to showcase the shell's capabilities... <br>
</h3>

<img src='https://github.com/user-attachments/assets/ec5cbb1b-6dac-40c1-9cf5-6ff3397445d5' />

---

## Tech Stack

| Component | Details |
|-----------|---------|
| Language | Python 3 — stdlib only for core |
| AI Model | sarvam-m via Sarvam API |
| TTS | Sarvam Bulbul v3 → pyttsx3 fallback |
| Shell executor | subprocess.run(shell=True) |
| History | readline — saved to ~/.pyshell_history |
| API key | Hardcoded or env var SARVAM_API_KEY |

---

## Installation

```bash
# Optional: install offline TTS fallback
pip install pyttsx3

# Run
python3 sashell.py
```

On first run, SaShell will ask for your Sarvam API key if not set in environment.
Get one free at: https://dashboard.sarvam.ai

---

## Startup Flags

| Flag | Description |
|------|-------------|
| `--help` | Show full command reference and exit |
| `--version` | Show version, model, TTS and language status |
| `--tts` | Boot with text-to-speech already enabled |
| `--no-ai` | Pure shell mode — zero Sarvam API calls |
| `--lang=Hindi` | AI responds in Hindi (or any Indian language) from boot |

```bash
python3 sashell.py --tts --lang=Tamil
python3 sashell.py --no-ai
```

---

## How It Works

Every command is silently judged by sarvam-m before running:

| Verdict | What happens |
|---------|-------------|
| `OK` | Runs immediately, no interruption |
| `DANGEROUS` | Asks y/N before running |
| `TYPO` | Suggests corrected command, asks y/N |
| `EASTER_EGG` | AI responds playfully instead of running |

If Sarvam is unreachable, the command runs anyway. It never blocks you.

---

## Shell Commands

SaShell runs every Linux command natively. Below is a reference.

### File & Directory

| Command | Description |
|---------|-------------|
| `ls -la` | List all files including hidden, with details |
| `cd <dir>` / `cd ..` / `cd ~` | Navigate directories |
| `pwd` | Print current directory |
| `mkdir -p a/b/c` | Create nested directories |
| `rm -rf <dir>` | Delete folder recursively ⚠ |
| `cp -r <src> <dst>` | Copy file or folder |
| `mv <src> <dst>` | Move or rename |
| `touch <file>` | Create empty file |
| `cat / less / head / tail <file>` | Read file contents |
| `tail -f <file>` | Follow file live (logs) |
| `wc -l <file>` | Count lines |
| `diff <f1> <f2>` | Compare two files |
| `find . -name "*.py"` | Find files by name pattern |
| `find . -size +100M` | Find files over 100MB |
| `du -ah . \| sort -rh \| head -10` | Top 10 biggest files |
| `stat <file>` | File metadata |
| `file <file>` | Detect file type |
| `ln -s <target> <link>` | Create symlink |
| `chmod +x <file>` | Make executable |
| `chown user:group <file>` | Change ownership ⚠ |

### Search & Text

| Command | Description |
|---------|-------------|
| `grep -rn "pattern" .` | Recursive search with line numbers |
| `grep -i "pattern" <file>` | Case-insensitive search |
| `awk '{print $1}' <file>` | Print first column |
| `sed 's/old/new/g' <file>` | Find and replace |
| `cut -d',' -f1 <file>` | Cut by delimiter |
| `sort -rn <file>` | Reverse numeric sort |
| `uniq <file>` | Remove duplicate lines |
| `tr 'a-z' 'A-Z'` | Transform characters |
| `xargs` | Pipe args to command |

### Pipes, Redirects & Chaining

| Syntax | Description |
|--------|-------------|
| `cmd1 \| cmd2` | Pipe output to next command |
| `cmd > file` | Redirect output to file (overwrite) |
| `cmd >> file` | Append output to file |
| `cmd 2> err.log` | Redirect stderr |
| `cmd &> all.log` | Redirect stdout + stderr |
| `cmd1 && cmd2` | Run cmd2 only if cmd1 succeeds |
| `cmd1 \|\| cmd2` | Run cmd2 only if cmd1 fails |
| `cmd &` | Run in background |
| `$(cmd)` | Command substitution |

### Processes & System

| Command | Description |
|---------|-------------|
| `ps aux --sort=-%cpu \| head -10` | Top CPU hogs |
| `top` / `htop` | Live process monitor |
| `kill <pid>` / `killall <name>` | Kill process ⚠ |
| `jobs` / `bg` / `fg` | Job control |
| `nohup cmd &` | Run immune to hangup |
| `uptime` | System uptime and load averages |
| `uname -a` | Full system info |
| `whoami` / `who` / `id` | User info |
| `env` / `export VAR=val` | Environment variables |
| `history \| tail -20` | Last 20 commands |
| `watch -n 2 <cmd>` | Repeat command every 2 seconds |
| `time <cmd>` | Measure command runtime |

### Disk & Memory

| Command | Description |
|---------|-------------|
| `df -h` | Disk usage |
| `free -h` | RAM and swap usage |
| `lsblk` | List block devices |
| `du -sh <dir>` | Size of a directory |

### Network

| Command | Description |
|---------|-------------|
| `ip addr show` | Network interfaces and IPs |
| `ss -tuln` | Open ports |
| `ping <host>` | Ping a host |
| `curl -O <url>` | Download a file |
| `wget <url>` | Download a file |
| `ssh user@host` | SSH into remote machine |
| `scp file user@host:/path` | Copy file to remote |
| `rsync -av src/ dst/` | Sync folders |
| `dig <domain>` | DNS lookup |
| `traceroute <host>` | Trace network path |

### Archives & Compression

| Command | Description |
|---------|-------------|
| `tar -czf out.tar.gz dir/` | Compress folder to .tar.gz |
| `tar -xzf file.tar.gz` | Extract .tar.gz |
| `zip -r out.zip dir/` | Zip a folder |
| `unzip file.zip` | Extract zip |
| `gzip` / `gunzip` | Compress / decompress |

### Git

| Command | Description |
|---------|-------------|
| `git init` / `git clone <url>` | Init or clone repo |
| `git status` / `git diff` | Check changes |
| `git add . && git commit -m "msg"` | Stage and commit |
| `git push` / `git pull` | Sync with remote |
| `git log --oneline` | Compact history |
| `git checkout -b <branch>` | Create and switch branch |
| `git stash` | Stash uncommitted changes |

### Package Managers ⚠ all ask y/N

| Command | Description |
|---------|-------------|
| `apt install / remove <pkg>` | Debian/Ubuntu packages |
| `apt update && apt upgrade` | Update system |
| `pip install <pkg>` | Python packages |
| `pip list` / `pip show <pkg>` | Inspect packages |
| `npm install <pkg>` | Node packages |

### Services — systemctl ⚠ ask y/N

| Command | Description |
|---------|-------------|
| `systemctl status <svc>` | Check service status |
| `systemctl start/stop/restart <svc>` | Control service |
| `systemctl enable <svc>` | Enable on boot |
| `journalctl -f` | Follow system logs |

---

## Chat Mode

Say any of these to open a full AI conversation:

- `i wanna talk with you`
- `i want to talk with you`
- `lets chat`
- `chat mode`
- `talk to me`

Type `back` to return to the shell.
Chat keeps memory across the session. TTS auto-speaks replies when enabled.

---

## Text to Speech

Uses Sarvam Bulbul v3. Falls back to pyttsx3 (offline) if unavailable.

| Command | Description |
|---------|-------------|
| `tts on` | Enable TTS — 🔊 shows in prompt |
| `tts off` | Disable TTS |
| `tts say <text>` | Speak any text immediately |
| `tts replay` | Replay last chat reply |
| `tts voice <name>` | Change voice |
| `--tts` | Quick toggle on/off |

**Available voices:**
Shubh (default), Aditya, Ritu, Priya, Neha, Rahul, Pooja, Rohan, Simran, Kavya, Amit, Dev, Ishita, Shreya, Varun, Kabir

```bash
pip install pyttsx3   # for offline fallback
```

---

## Language Support

| Method | Example |
|--------|---------|
| At boot | `python3 sashell.py --lang=Hindi` |
| While running | `lang Tamil` |
| Check current | `lang` |

Supported: Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, Marathi, Punjabi, and more.

---

## SaShell Builtins

| Command | Description |
|---------|-------------|
| `help` / `--help` | Full command reference |
| `--version` | Version and status info |
| `lang <X>` | Change AI response language |
| `tts <subcommand>` | TTS controls |
| `fortune` | Random terminal wisdom 🔮 |
| `clear` | Clear screen |
| `exit` / `quit` | Leave SaShell |

---

## Easter Eggs 🥚

| Phrase | Hint |
|--------|------|
| `sudo make me a sandwich` | Classic |
| `what is love` | Baby don't hurt me |
| `meaning of life` | 42 |
| `who are you` | SaShell introduces itself |
| `why` | Philosophy |
| `hello` / `hi` | Greeting with attitude |
| `fortune` | Random terminal wisdom |
| `rm -rf /` | Nice try |

More are hidden. Explore.

---

*SaShell MK 2.0.4*
