# ULTRON by Nouman

**Your Personal Desktop Intelligence**

> All the cool of Ultron. None of the world domination. Built from scratch, owned by its maker.

ULTRON is a cool, confident desktop assistant you run on your own
computer. Talk to it in plain text (or voice, if you install the voice
extras), ask it questions, and let it handle everyday chores: checking
the time, doing maths, reporting on your system, looking up the weather,
searching the web, opening apps, managing files safely, keeping
reminders, controlling media, and more.

ULTRON is built to be honest about its limits. It works **completely
offline** with built-in skills on a bare Python install; add a free
Google Gemini API key and the same chat also answers open-ended
questions through the model. No key? No problem -- ULTRON says it is in
offline mode and keeps helping with everything local.

> Designed & Developed by M Nouman

---

## Features

- **Chat, two ways** -- Gemini-powered answers when a key is configured,
  graceful offline responses when it is not. ULTRON never crashes just
  because the network or the key is missing.
- **Clock & calendar** -- current time, date, and day of the week.
- **Safe calculator** -- arithmetic evaluated by walking the syntax
  tree, never with `eval`, so a typed expression can't run code.
- **System report** -- OS, machine, Python version, disk space, and
  (with `psutil`) live CPU and memory figures.
- **Weather** -- current conditions for any city via wttr.in, no key
  required.
- **Web search** -- top results from DuckDuckGo's HTML endpoint.
- **App launcher** -- open notepad, calculator, browser, terminal, or
  the file manager by name.
- **File tools with safe delete** -- list, create, and remove files.
  "Delete" always means *recoverable*: the OS trash via `send2trash`
  when available, otherwise ULTRON's own `data/trash` folder.
- **Reminders** -- "remind me in 10 minutes to stretch", stored in a
  JSON file, with due reminders flagged when you list them.
- **Media keys** -- play/pause, next/previous, volume up/down.
- **Screenshot & clipboard** -- timestamped PNG captures and clipboard
  read/write when the small optional packages are installed.
- **A little personality** -- offline jokes and motivational quotes.
- **Memory** -- the conversation is kept (capped, atomically written)
  in `data/conversation.json`, so context survives restarts.
- **Status dashboard** -- an optional web page (standard library only)
  showing ULTRON's mode and system numbers at `http://127.0.0.1:8765`.
- **Plugins** -- drop a Python file into `plugins/` following the
  included template to teach ULTRON new tricks.

## Quick start

You need Python 3.10 or newer.

```bash
git clone <this-repo-url> ultron-by-nouman
cd ultron-by-nouman
python main.py
```

That's it -- offline mode works immediately. Try:

```
You: what time is it
You: calculate 12 * 8
You: system info
You: tell me a joke
```

For richer system info and the extra skills, install the optional
packages:

```bash
pip install -r requirements.txt
```

### Turn on the online brain (optional)

1. Get a free Gemini API key from Google AI Studio.
2. Copy the example config and paste your key in:

   ```bash
   cp config/api_keys.json.example config/api_keys.json
   ```

   Or skip the file and use an environment variable instead:

   ```bash
   export GEMINI_API_KEY="your-key-here"     # Windows: set GEMINI_API_KEY=...
   ```

`config/api_keys.json` is listed in `.gitignore` -- your real key is
never committed.

## Usage examples

| You say | ULTRON does |
| --- | --- |
| `what time is it` | Tells the time and date |
| `calculate (15 + 5) / 4` | Answers `= 5` |
| `system info` | Prints an OS / CPU / memory / disk report |
| `weather in Lahore` | Current weather for Lahore |
| `search best budget laptops` | Top web results with links |
| `open notepad` | Launches Notepad (or the OS equivalent) |
| `remind me in 30 minutes to call home` | Saves a timed reminder |
| `list reminders` | Shows reminders, flagging any that are due |
| `list files` | Lists the current folder |
| `create file notes.txt` | Creates an empty file (never overwrites) |
| `delete old-draft.txt` | Safe-deletes it -- always recoverable |
| `take a screenshot` | Saves a timestamped PNG |
| `copy meeting at 5` | Puts the text on your clipboard |
| `volume up` | Raises the volume |
| `give me a quote` | Shares a motivational line |
| `help` | Lists every command |

Run a single command without entering the chat loop:

```bash
python main.py --once "calculate 99 / 9"
```

Voice mode (after installing the commented voice extras in
`requirements.txt`):

```bash
python main.py --voice
```

Dashboard:

```bash
python -m dashboard.server
# then open http://127.0.0.1:8765  (JSON at /api/status)
```

## Architecture

```
ultron-by-nouman/
├── main.py               Entry point: chat loop, --once, --voice, piped input
├── core/
│   ├── config.py         Branding (NAME lives here) + settings from env / JSON
│   ├── llm_client.py     Gemini client (stdlib HTTP) with offline fallback
│   ├── memory.py         Capped, atomically-saved JSON conversation memory
│   └── router.py         Maps a sentence to an action, else to the chat model
├── actions/              One small module per skill, each with run(argument)
│   ├── time_date.py      calculator.py     system_info.py
│   ├── weather.py        web_search.py     open_app.py
│   ├── file_controller.py  reminder.py     media_control.py
│   ├── screenshot.py     clipboard_tool.py fun.py
├── dashboard/
│   └── server.py         Optional stdlib-only status web page
├── plugins/
│   └── _template.py      Copy this to start your own plugin
├── config/
│   └── api_keys.json.example
├── requirements.txt      Optional extras only -- core runs on stdlib
└── LICENSE               MIT
```

The design rule throughout: **standard library first, optional packages
guarded**. Every feature that can work without a third-party install
does, and every optional import is wrapped so a missing package turns
into a friendly explanation, not a traceback.

## Renaming ULTRON

The brand lives in exactly one place: `NAME` and `TAGLINE` at the top
of `core/config.py` (plus the title of this README). Change them and
the banner, dashboard, and model prompt all follow.

## License

MIT -- see [LICENSE](LICENSE). Copyright (c) 2026 M Nouman.

---

*Designed & Developed by M Nouman*
