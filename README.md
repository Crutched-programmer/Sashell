<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SaShell v0.9.0 — README</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  :root {
    --lime:     #9deb3b;
    --magenta:  #ff2d78;
    --cyan:     #00eeff;
    --amber:    #ffb700;
    --lavender: #c4a3ff;
    --bg:       #0a0c0f;
    --bg2:      #111418;
    --bg3:      #181d22;
    --border:   #1e2530;
    --text:     #cdd6e0;
    --dim:      #5a6472;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Exo 2', sans-serif;
    font-size: 15px;
    line-height: 1.7;
    padding: 0 0 80px;
  }

  /* ── Hero ── */
  .hero {
    background: linear-gradient(135deg, #0a0c0f 0%, #0d1520 50%, #0a0c0f 100%);
    border-bottom: 1px solid var(--border);
    padding: 60px 40px 50px;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      0deg, transparent, transparent 39px,
      rgba(157,235,59,0.03) 39px, rgba(157,235,59,0.03) 40px
    ),
    repeating-linear-gradient(
      90deg, transparent, transparent 39px,
      rgba(157,235,59,0.03) 39px, rgba(157,235,59,0.03) 40px
    );
    pointer-events: none;
  }
  .ascii {
    font-family: 'Share Tech Mono', monospace;
    font-size: clamp(7px, 1.4vw, 13px);
    color: var(--lime);
    line-height: 1.2;
    white-space: pre;
    text-shadow: 0 0 20px rgba(157,235,59,0.4);
    margin-bottom: 24px;
  }
  .hero-sub {
    font-family: 'Share Tech Mono', monospace;
    color: var(--cyan);
    font-size: 14px;
    letter-spacing: 0.05em;
    margin-bottom: 20px;
  }
  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 16px;
  }
  .badge {
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 3px;
    border: 1px solid;
  }
  .badge-lime    { color: var(--lime);    border-color: var(--lime);    background: rgba(157,235,59,0.08); }
  .badge-cyan    { color: var(--cyan);    border-color: var(--cyan);    background: rgba(0,238,255,0.08); }
  .badge-amber   { color: var(--amber);   border-color: var(--amber);   background: rgba(255,183,0,0.08); }
  .badge-magenta { color: var(--magenta); border-color: var(--magenta); background: rgba(255,45,120,0.08); }

  /* ── Layout ── */
  .container { max-width: 900px; margin: 0 auto; padding: 0 32px; }

  /* ── Sections ── */
  .section { margin-top: 52px; }

  h2 {
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    font-weight: 400;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--lime);
    border-left: 3px solid var(--lime);
    padding-left: 14px;
    margin-bottom: 20px;
  }

  p { margin-bottom: 12px; color: var(--text); }

  /* ── Code blocks ── */
  pre, code {
    font-family: 'Share Tech Mono', monospace;
  }
  code {
    background: var(--bg3);
    color: var(--amber);
    padding: 2px 7px;
    border-radius: 3px;
    font-size: 13px;
    border: 1px solid var(--border);
  }
  pre {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--cyan);
    padding: 18px 22px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 13px;
    color: var(--cyan);
    margin: 16px 0;
    line-height: 1.6;
  }
  pre .prompt { color: var(--lavender); }
  pre .cmd    { color: var(--amber); }
  pre .comment{ color: var(--dim); }

  /* ── Tables ── */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 14px;
  }
  th {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--dim);
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
  }
  td {
    padding: 10px 14px;
    border-bottom: 1px solid rgba(30,37,48,0.6);
    vertical-align: top;
  }
  tr:hover td { background: rgba(157,235,59,0.03); }
  td:first-child {
    font-family: 'Share Tech Mono', monospace;
    color: var(--amber);
    white-space: nowrap;
    font-size: 13px;
    width: 35%;
  }
  td .danger {
    color: var(--magenta);
    font-size: 11px;
    margin-left: 6px;
    font-family: 'Share Tech Mono', monospace;
  }
  td .note {
    color: var(--dim);
    font-size: 12px;
    display: block;
    margin-top: 2px;
  }

  /* ── Cards ── */
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 16px;
    margin-top: 16px;
  }
  .card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
  }
  .card-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 12px;
  }
  .card-title.lime    { color: var(--lime); }
  .card-title.cyan    { color: var(--cyan); }
  .card-title.magenta { color: var(--magenta); }
  .card-title.amber   { color: var(--amber); }
  .card-title.lavender{ color: var(--lavender); }
  .card ul { list-style: none; }
  .card ul li {
    font-size: 13.5px;
    padding: 4px 0;
    border-bottom: 1px solid rgba(30,37,48,0.5);
    display: flex;
    align-items: baseline;
    gap: 8px;
  }
  .card ul li:last-child { border-bottom: none; }
  .card ul li::before { content: '›'; color: var(--dim); }
  .card ul li code { background: none; border: none; padding: 0; color: var(--amber); }

  /* ── Verdict pills ── */
  .verdict-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin: 16px 0; }
  .verdict-card {
    border-radius: 6px;
    padding: 16px;
    border: 1px solid;
  }
  .verdict-card.ok       { border-color: var(--lime);    background: rgba(157,235,59,0.06); }
  .verdict-card.danger   { border-color: var(--magenta); background: rgba(255,45,120,0.06); }
  .verdict-card.typo     { border-color: var(--amber);   background: rgba(255,183,0,0.06); }
  .verdict-card.egg      { border-color: var(--lavender);background: rgba(196,163,255,0.06); }
  .verdict-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
    font-weight: bold;
    margin-bottom: 6px;
  }
  .verdict-card.ok     .verdict-title { color: var(--lime); }
  .verdict-card.danger .verdict-title { color: var(--magenta); }
  .verdict-card.typo   .verdict-title { color: var(--amber); }
  .verdict-card.egg    .verdict-title { color: var(--lavender); }
  .verdict-desc { font-size: 13px; color: var(--text); }

  /* ── Divider ── */
  hr { border: none; border-top: 1px solid var(--border); margin: 48px 0; }

  /* ── Inline highlights ── */
  strong { color: var(--lime); font-weight: 600; }
  .cyan   { color: var(--cyan); }
  .amber  { color: var(--amber); }
  .magenta{ color: var(--magenta); }
  .lavender{color: var(--lavender); }
  .dim    { color: var(--dim); font-size: 13px; }

  /* ── Footer ── */
  footer {
    margin-top: 80px;
    padding: 32px 40px;
    border-top: 1px solid var(--border);
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    color: var(--dim);
    text-align: center;
  }
  footer span { color: var(--lime); }
</style>
</head>
<body>

<!-- ── HERO ── -->
<div class="hero">
  <div class="container">
    <div class="ascii"> ██████╗ █████╗  ██████╗██╗  ██╗███████╗██╗     ██╗
██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝██║     ██║
╚█████╗ ███████║╚█████╗ ███████║█████╗  ██║     ██║
 ╚═══██╗██╔══██║ ╚═══██╗██╔══██║██╔══╝  ██║     ██║
██████╔╝██║  ██║██████╔╝██║  ██║███████╗███████╗███████╗
╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝</div>
    <div class="hero-sub">Real Linux shell · Sarvam AI safety net · TTS · Chat mode</div>
    <div class="badges">
      <span class="badge badge-lime">v0.9.0</span>
      <span class="badge badge-cyan">Python 3</span>
      <span class="badge badge-amber">sarvam-m</span>
      <span class="badge badge-magenta">bulbul:v3 TTS</span>
      <span class="badge badge-lime">Linux / macOS / Git Bash</span>
    </div>
  </div>
</div>

<div class="container">

  <!-- ── WHAT IS IT ── -->
  <div class="section">
    <h2>What is SaShell?</h2>
    <p>
      SaShell is a <strong>real Linux shell written in Python</strong> — every command you type runs directly through bash, exactly like a normal terminal.
      The difference: <strong>Sarvam AI watches silently in the background</strong>, stepping in only when something looks dangerous, broken, or funny.
    </p>
    <p>
      It also includes a full <strong>AI chat mode</strong>, <strong>text-to-speech</strong> powered by Sarvam Bulbul v3, multi-language support, and a collection of easter eggs.
    </p>
  </div>

  <!-- ── INSTALL ── -->
  <div class="section">
    <h2>Installation &amp; Setup</h2>
    <pre><span class="comment"># 1. Clone or download sashell.py
# 2. Install optional dependency for offline TTS</span>
<span class="cmd">pip install pyttsx3</span>

<span class="comment"># 3. Run it</span>
<span class="cmd">python3 sashell.py</span></pre>

    <p>On first run, SaShell will ask for your <strong>Sarvam API key</strong> if not already set.<br>
    Get one free at <code>dashboard.sarvam.ai</code></p>

    <table>
      <thead><tr><th>Flag</th><th>What it does</th></tr></thead>
      <tbody>
        <tr><td>--help</td><td>Show full command reference and exit</td></tr>
        <tr><td>--version</td><td>Show version, model, TTS and language status</td></tr>
        <tr><td>--tts</td><td>Boot with text-to-speech already enabled</td></tr>
        <tr><td>--no-ai</td><td>Pure shell mode — zero Sarvam API calls</td></tr>
        <tr><td>--lang=Hindi</td><td>AI responds in Hindi (or any Indian language) from boot</td></tr>
      </tbody>
    </table>

    <pre><span class="comment"># Examples</span>
<span class="cmd">python3 sashell.py --tts --lang=Tamil</span>
<span class="cmd">python3 sashell.py --no-ai</span>
<span class="cmd">python3 sashell.py --help</span></pre>
  </div>

  <!-- ── AI SAFETY NET ── -->
  <div class="section">
    <h2>AI Safety Net</h2>
    <p>Every command is silently judged by <strong>sarvam-m</strong> before running. It classifies into one of four verdicts:</p>

    <div class="verdict-grid">
      <div class="verdict-card ok">
        <div class="verdict-title">OK</div>
        <div class="verdict-desc">Valid, safe command — runs immediately, no interruption.</div>
      </div>
      <div class="verdict-card danger">
        <div class="verdict-title">⚠ DANGEROUS</div>
        <div class="verdict-desc">Destructive or system-level command — asks <strong>y/N</strong> before running.</div>
      </div>
      <div class="verdict-card typo">
        <div class="verdict-title">✏ TYPO</div>
        <div class="verdict-desc">Spotted a mistake — suggests the corrected command and asks to run it.</div>
      </div>
      <div class="verdict-card egg">
        <div class="verdict-title">🥚 EASTER EGG</div>
        <div class="verdict-desc">Detected a joke phrase — AI responds playfully instead of running it.</div>
      </div>
    </div>

    <p class="dim">If Sarvam is unreachable, SaShell runs the command anyway — it never blocks you.</p>
  </div>

  <!-- ── SHELL COMMANDS ── -->
  <div class="section">
    <h2>Shell Commands</h2>
    <p>SaShell runs <strong>every Linux command</strong> natively. Below is a reference of common ones.</p>

    <br><strong>File &amp; Directory</strong>
    <table>
      <thead><tr><th>Command</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td>ls -la</td><td>List all files including hidden, with details</td></tr>
        <tr><td>cd &lt;dir&gt; / cd .. / cd ~</td><td>Navigate directories</td></tr>
        <tr><td>pwd</td><td>Print current directory</td></tr>
        <tr><td>mkdir -p a/b/c</td><td>Create nested directories</td></tr>
        <tr><td>rm -rf &lt;dir&gt;</td><td>Delete folder recursively <span class="danger">⚠ danger</span></td></tr>
        <tr><td>cp -r &lt;src&gt; &lt;dst&gt;</td><td>Copy file or folder</td></tr>
        <tr><td>mv &lt;src&gt; &lt;dst&gt;</td><td>Move or rename</td></tr>
        <tr><td>find . -name "*.py"</td><td>Find files by name pattern</td></tr>
        <tr><td>find . -size +100M</td><td>Find files over 100MB</td></tr>
        <tr><td>du -ah . | sort -rh | head -10</td><td>Top 10 biggest files</td></tr>
        <tr><td>chmod +x &lt;file&gt;</td><td>Make file executable</td></tr>
        <tr><td>chown user:group &lt;file&gt;</td><td>Change ownership <span class="danger">⚠ danger</span></td></tr>
      </tbody>
    </table>

    <br><strong>Search &amp; Text</strong>
    <table>
      <thead><tr><th>Command</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td>grep -rn "pattern" .</td><td>Recursive search with line numbers</td></tr>
        <tr><td>grep -i "pattern" &lt;file&gt;</td><td>Case-insensitive search</td></tr>
        <tr><td>awk '{print $1}' &lt;file&gt;</td><td>Print first column</td></tr>
        <tr><td>sed 's/old/new/g' &lt;file&gt;</td><td>Find and replace</td></tr>
        <tr><td>sort -rn &lt;file&gt;</td><td>Reverse numeric sort</td></tr>
        <tr><td>uniq &lt;file&gt;</td><td>Remove duplicate lines</td></tr>
        <tr><td>wc -l &lt;file&gt;</td><td>Count lines</td></tr>
      </tbody>
    </table>

    <br><strong>Pipes, Redirects &amp; Chaining</strong>
    <table>
      <thead><tr><th>Syntax</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td>cmd1 | cmd2</td><td>Pipe output to next command</td></tr>
        <tr><td>cmd &gt; file</td><td>Redirect output to file (overwrite)</td></tr>
        <tr><td>cmd &gt;&gt; file</td><td>Append output to file</td></tr>
        <tr><td>cmd 2&gt; err.log</td><td>Redirect stderr</td></tr>
        <tr><td>cmd1 &amp;&amp; cmd2</td><td>Run cmd2 only if cmd1 succeeds</td></tr>
        <tr><td>cmd1 || cmd2</td><td>Run cmd2 only if cmd1 fails</td></tr>
        <tr><td>cmd &amp;</td><td>Run in background</td></tr>
        <tr><td>$(cmd)</td><td>Command substitution</td></tr>
      </tbody>
    </table>

    <br><strong>Processes &amp; System</strong>
    <table>
      <thead><tr><th>Command</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td>ps aux --sort=-%cpu</td><td>All processes sorted by CPU</td></tr>
        <tr><td>top / htop</td><td>Live process monitor</td></tr>
        <tr><td>kill &lt;pid&gt; / killall &lt;name&gt;</td><td>Kill process <span class="danger">⚠ danger</span></td></tr>
        <tr><td>uptime</td><td>System uptime and load averages</td></tr>
        <tr><td>uname -a</td><td>Full system info</td></tr>
        <tr><td>whoami / who / id</td><td>User info</td></tr>
        <tr><td>env / export VAR=val</td><td>Environment variables</td></tr>
        <tr><td>watch -n 2 &lt;cmd&gt;</td><td>Repeat command every 2 seconds</td></tr>
        <tr><td>history | tail -20</td><td>Last 20 commands</td></tr>
      </tbody>
    </table>

    <br><strong>Network</strong>
    <table>
      <thead><tr><th>Command</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td>ip addr show</td><td>Network interfaces and IPs</td></tr>
        <tr><td>ss -tuln</td><td>Open ports</td></tr>
        <tr><td>ping &lt;host&gt;</td><td>Ping a host</td></tr>
        <tr><td>curl -O &lt;url&gt;</td><td>Download a file</td></tr>
        <tr><td>ssh user@host</td><td>SSH into remote machine</td></tr>
        <tr><td>rsync -av src/ dst/</td><td>Sync folders</td></tr>
        <tr><td>dig &lt;domain&gt;</td><td>DNS lookup</td></tr>
      </tbody>
    </table>

    <br><strong>Git</strong>
    <table>
      <thead><tr><th>Command</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td>git init / clone &lt;url&gt;</td><td>Init or clone repo</td></tr>
        <tr><td>git status / diff</td><td>Check changes</td></tr>
        <tr><td>git add . &amp;&amp; git commit -m "msg"</td><td>Stage and commit</td></tr>
        <tr><td>git push / pull</td><td>Sync with remote</td></tr>
        <tr><td>git log --oneline</td><td>Compact history</td></tr>
        <tr><td>git checkout -b &lt;branch&gt;</td><td>Create and switch branch</td></tr>
        <tr><td>git stash</td><td>Stash uncommitted changes</td></tr>
      </tbody>
    </table>
  </div>

  <!-- ── CHAT MODE ── -->
  <div class="section">
    <h2>Chat Mode</h2>
    <p>Switch to a full AI conversation with <strong>Sarvam</strong> without leaving the shell.</p>

    <table>
      <thead><tr><th>Trigger phrase</th><th>Action</th></tr></thead>
      <tbody>
        <tr><td>i wanna talk with you</td><td>Opens chat mode</td></tr>
        <tr><td>lets chat</td><td>Opens chat mode</td></tr>
        <tr><td>talk to me</td><td>Opens chat mode</td></tr>
        <tr><td>chat mode</td><td>Opens chat mode</td></tr>
        <tr><td>back</td><td>Returns to shell (from inside chat)</td></tr>
      </tbody>
    </table>

    <p>Chat keeps <strong>full memory across the session</strong> — Sarvam remembers what you said earlier in the conversation.<br>
    When TTS is enabled, every AI reply is spoken aloud automatically.</p>
  </div>

  <!-- ── TTS ── -->
  <div class="section">
    <h2>Text to Speech</h2>
    <p>SaShell uses <strong>Sarvam Bulbul v3</strong> for TTS. If your API key doesn't have TTS access (403), it automatically falls back to <strong>pyttsx3</strong> (offline, free).</p>

    <table>
      <thead><tr><th>Command</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td>tts on</td><td>Enable TTS — 🔊 badge appears in prompt</td></tr>
        <tr><td>tts off</td><td>Disable TTS</td></tr>
        <tr><td>tts say &lt;text&gt;</td><td>Speak any text immediately</td></tr>
        <tr><td>tts replay</td><td>Replay last chat reply</td></tr>
        <tr><td>tts voice &lt;name&gt;</td><td>Change voice</td></tr>
        <tr><td>--tts</td><td>Quick toggle on/off while running</td></tr>
      </tbody>
    </table>

    <br><strong>Available Voices (Bulbul v3)</strong><br><br>
    <div class="card-grid">
      <div class="card">
        <div class="card-title amber">Female</div>
        <ul>
          <li><code>Ritu</code></li>
          <li><code>Priya</code></li>
          <li><code>Neha</code></li>
          <li><code>Pooja</code></li>
          <li><code>Simran</code></li>
          <li><code>Kavya</code></li>
          <li><code>Ishita</code></li>
          <li><code>Shreya</code></li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title cyan">Male</div>
        <ul>
          <li><code>Shubh</code> <span style="color:var(--dim);font-size:11px">(default)</span></li>
          <li><code>Aditya</code></li>
          <li><code>Rahul</code></li>
          <li><code>Rohan</code></li>
          <li><code>Amit</code></li>
          <li><code>Dev</code></li>
          <li><code>Varun</code></li>
          <li><code>Kabir</code></li>
        </ul>
      </div>
    </div>

    <pre><span class="comment"># Install offline fallback</span>
<span class="cmd">pip install pyttsx3</span></pre>
  </div>

  <!-- ── LANGUAGE ── -->
  <div class="section">
    <h2>Language Support</h2>
    <p>SaShell's AI can respond in <strong>any Indian language</strong>. Set it at boot or switch live.</p>

    <table>
      <thead><tr><th>Method</th><th>Example</th></tr></thead>
      <tbody>
        <tr><td>At boot</td><td><code>python3 sashell.py --lang=Hindi</code></td></tr>
        <tr><td>While running</td><td><code>lang Tamil</code></td></tr>
        <tr><td>Check current</td><td><code>lang</code></td></tr>
      </tbody>
    </table>

    <p class="dim">Works for: Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, Marathi, Punjabi, and more.</p>
  </div>

  <!-- ── BUILTINS ── -->
  <div class="section">
    <h2>SaShell Builtins</h2>

    <div class="card-grid">
      <div class="card">
        <div class="card-title lime">Shell Builtins</div>
        <ul>
          <li><code>cd</code> true directory change</li>
          <li><code>clear</code> clear the screen</li>
          <li><code>history</code> command history</li>
          <li><code>exit</code> / <code>quit</code> leave SaShell</li>
          <li><code>fortune</code> terminal wisdom 🔮</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title magenta">Info &amp; Config</div>
        <ul>
          <li><code>help</code> / <code>--help</code> full reference</li>
          <li><code>--version</code> version &amp; status</li>
          <li><code>lang &lt;X&gt;</code> change AI language</li>
          <li><code>tts &lt;cmd&gt;</code> TTS controls</li>
          <li><code>--no-ai</code> disable AI entirely</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- ── EASTER EGGS ── -->
  <div class="section">
    <h2>Easter Eggs 🥚</h2>
    <p>Type these phrases to discover hidden responses. More are scattered throughout — explore.</p>

    <table>
      <thead><tr><th>Phrase</th><th>Hint</th></tr></thead>
      <tbody>
        <tr><td>sudo make me a sandwich</td><td>Classic.</td></tr>
        <tr><td>what is love</td><td>Baby don't hurt me.</td></tr>
        <tr><td>meaning of life</td><td>42.</td></tr>
        <tr><td>who are you</td><td>SaShell introduces itself.</td></tr>
        <tr><td>why</td><td>Philosophy.</td></tr>
        <tr><td>hello / hi</td><td>Greeting with attitude.</td></tr>
        <tr><td>fortune</td><td>Random terminal wisdom 🔮</td></tr>
        <tr><td>rm -rf /</td><td>Nice try.</td></tr>
      </tbody>
    </table>
  </div>

  <!-- ── TECH STACK ── -->
  <div class="section">
    <h2>Tech Stack</h2>
    <table>
      <thead><tr><th>Component</th><th>Details</th></tr></thead>
      <tbody>
        <tr><td>Language</td><td>Python 3 — stdlib only (no pip needed for core)</td></tr>
        <tr><td>AI Model</td><td>sarvam-m via Sarvam API</td></tr>
        <tr><td>TTS Engine</td><td>Sarvam Bulbul v3 → pyttsx3 fallback</td></tr>
        <tr><td>Shell executor</td><td>subprocess.run(shell=True) — native bash</td></tr>
        <tr><td>History</td><td>readline — saved to ~/.pyshell_history</td></tr>
        <tr><td>Key storage</td><td>Hardcoded / env var SARVAM_API_KEY</td></tr>
      </tbody>
    </table>
  </div>

  <hr>

</div>

<footer>
  <span>SaShell v0.9.0</span> &nbsp;·&nbsp; Powered by Sarvam AI &nbsp;·&nbsp; Built with Python &nbsp;·&nbsp; <span>Stay chaotic. 🌀</span>
</footer>

</body>
</html>
