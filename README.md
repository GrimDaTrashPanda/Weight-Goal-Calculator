# Weight Goal Calculator

A small desktop app that estimates your daily calorie needs and gives a
realistic timeline toward a weight goal. It has a pastel pink GUI, runs
fully offline, and stores nothing — no accounts, no tracking, no internet
connection required.

> **This tool is for entertainment and general informational purposes
> only.** It is not medical advice and is not a substitute for guidance
> from a registered dietitian, nutritionist, or physician. Always consult
> a qualified healthcare professional before making changes to your diet
> or exercise routine, especially if you have any underlying health
> conditions.

---

## Download

If you just want to run the app without installing Python, grab the latest pre-built Windows executable from the [Releases](https://github.com/GrimDaTrashPanda/Weight-Goal-Calculator/releases) page. No installation required, just download and run weight_calculator.exe.

The steps below are for building from source instead (needed for macOS/Linux, or if you want to inspect the code first).

---

## What this app does

- Calculates your **BMR** (Basal Metabolic Rate — calories burned at
  rest) using the **Mifflin-St Jeor** equation, which performs well
  across a wide range of body sizes.
- Optionally uses the **Katch-McArdle** formula instead, if you know
  your body fat percentage — this can be more accurate since it's based
  on lean body mass.
- Calculates your **TDEE** (Total Daily Energy Expenditure) by factoring
  in your activity level.
- Recommends a daily calorie target based on a weight gain or loss goal
  and a pace you choose (gentle, moderate, aggressive, or max
  recommended).
- Estimates how many weeks/months it will take to reach your goal at
  that pace.
- Warns you if the recommended calorie target drops below a commonly
  cited safe floor (1,200 kcal/day) for unsupervised dieting.
- Supports both **imperial** (lb/in) and **metric** (kg/cm) units.

---

## For the person setting this up: how to use this README

This README is written so you can paste it into an AI assistant (like
Claude, ChatGPT, or similar) along with the question **"walk me through
installing and running this"**, and the assistant should be able to
guide you step by step, even if you've never used Python before.

If you're doing it yourself without an AI assistant, just follow the
steps below in order. They are written for complete beginners — skip
ahead if you already know a step.

---

## Requirements

- **Python 3.8 or newer.** This app uses only Python's standard library
  (specifically `tkinter` for the GUI) — there is nothing to install via
  `pip` for the app itself.
- **Tkinter**, which usually comes bundled with Python, but on some Linux
  distributions it needs to be installed separately (see below).

There are no other dependencies, no API keys, and no internet connection
needed to run this app.

---

## Installation & Setup

### Step 1 — Check if Python is already installed

Open a terminal (Command Prompt or PowerShell on Windows, Terminal on
macOS/Linux) and run:

```bash
python3 --version
```

If that doesn't work on Windows, try:

```bash
python --version
```

You should see something like `Python 3.11.4`. If the version is **3.8
or higher**, you're good — skip to Step 3.

If you get an error like "command not found" or "not recognized," you
need to install Python first — go to Step 2.

### Step 2 — Install Python (if needed)

- **Windows:** Download the installer from
  [python.org/downloads](https://www.python.org/downloads/). During
  installation, **check the box that says "Add Python to PATH"** before
  clicking Install — this step trips up most beginners if skipped.
- **macOS:** Download the installer from
  [python.org/downloads](https://www.python.org/downloads/), or if you
  have [Homebrew](https://brew.sh) installed, run `brew install python`.
- **Linux (Debian/Ubuntu and derivatives):**
  ```bash
  sudo apt update
  sudo apt install python3 python3-tk
  ```
- **Linux (Fedora):**
  ```bash
  sudo dnf install python3 python3-tkinter
  ```
- **Linux (Arch):**
  ```bash
  sudo pacman -S python tk
  ```

After installing, close and reopen your terminal, then re-run the Step 1
check.

### Step 3 — Confirm tkinter is available

Run this command:

```bash
python3 -m tkinter
```

A tiny test window should pop up. If it does, close it — you're set. If
you get an error mentioning `tkinter` or `_tkinter`, install it for your
OS:

- **Windows/macOS official installer:** tkinter should already be
  included. If it's missing, reinstall Python from python.org and make
  sure you don't deselect "tcl/tk and IDLE" during install.
- **Debian/Ubuntu:** `sudo apt install python3-tk`
- **Fedora:** `sudo dnf install python3-tkinter`
- **Arch:** `sudo pacman -S tk`

### Step 4 — Get the project files

If you're cloning from GitHub:

```bash
git clone <this-repo-url>
cd <repo-folder-name>
```

Or if you downloaded a ZIP from GitHub, extract it and open a terminal
inside the extracted folder.

### Step 5 — (Optional) Create a virtual environment

Not required since there are no external dependencies, but it's good
practice if you plan to extend the app later:

```bash
python3 -m venv venv
```

Activate it:

- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Windows (cmd):** `venv\Scripts\activate.bat`
- **macOS/Linux:** `source venv/bin/activate`

### Step 6 — Install dependencies

```bash
pip install -r requirements.txt
```

This will complete instantly and do nothing, since the app has no
external dependencies — `requirements.txt` is included for completeness
and so the project plays nicely with standard tooling.

### Step 7 — Run the app

```bash
python3 weight_calculator.py
```

(On Windows, if `python3` doesn't work, use `python weight_calculator.py`
instead.)

A pastel pink window titled "Weight Goal Calculator" should open.

---

## How to use the app

1. Choose your unit system (Imperial or Metric) at the top.
2. Select your sex — this determines which BMR formula variables are
   used.
3. Enter your age, height, current weight, and goal weight.
4. **Optional:** enter your body fat percentage if you know it. If you
   leave this blank, the app uses the Mifflin-St Jeor formula. If you
   provide it, the app switches to Katch-McArdle, which can be more
   accurate since it accounts for lean body mass directly.
5. Select your activity level from the dropdown.
6. Select your target pace (how fast you want to gain or lose).
7. Click **Calculate**.
8. Your results — BMR, TDEE, recommended daily calories, and estimated
   timeline — will appear in the card below the button.

If your goal weight equals your current weight, the app will just
recommend a maintenance calorie target.

If the recommended calorie target falls below 1,200 kcal/day, the app
will flag this directly in the results and recommend consulting a
healthcare provider — this commonly cited threshold is a general
guideline, not a personalized medical limit.

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'tkinter'"**
Tkinter isn't installed for your Python. See Step 3 above for OS-specific
fixes.

**The window opens but looks tiny, cut off, or fonts look wrong**
This can happen on some Linux window managers or with display scaling.
Try resizing the window — it's resizable and scrollable. If text is
still cut off, your system's default font set may not include
"Verdana"; the app will fall back to a default system font automatically
on most platforms.

**"command not found: python3" on Windows**
Use `python` instead of `python3`. If neither works, Python wasn't added
to PATH during installation — reinstall Python and check the "Add Python
to PATH" box.

**Nothing happens when I click Calculate**
Make sure age, height, current weight, and goal weight are all filled in
with valid numbers (no letters or symbols). Body fat % is the only
optional field.

**I get a "Permission denied" error on macOS/Linux**
Try running with `python3 weight_calculator.py` rather than
`./weight_calculator.py`, or make the file executable first:
```bash
chmod +x weight_calculator.py
```

---

## The science, briefly

- **BMR (Mifflin-St Jeor):**
  - Men: `(10 × weight_kg) + (6.25 × height_cm) − (5 × age) + 5`
  - Women: `(10 × weight_kg) + (6.25 × height_cm) − (5 × age) − 161`
- **BMR (Katch-McArdle, used if body fat % is provided):**
  `370 + (21.6 × lean_mass_kg)`, where lean mass = weight × (1 − body
  fat % ÷ 100)
- **TDEE:** `BMR × activity multiplier` (1.2 to 1.9 depending on
  activity level)
- **Calorie target:** TDEE adjusted by a daily surplus/deficit derived
  from your chosen weekly pace, using the common approximation of
  ~7,700 kcal per kilogram of body weight change.

These are population-level estimates. Individual metabolism varies, and
actual results will differ from person to person — this is exactly why
the app is framed as informational rather than prescriptive.

---

## License

MIT — see `LICENSE`. Do whatever you want with it, just don't blame the
author if you ignore the disclaimer and something goes sideways.

---

## Disclaimer (again, because it matters)

This software provides general estimates for entertainment and
informational purposes only. It is **not** medical, dietary, or
nutritional advice. It does not account for individual medical
conditions, medications, metabolic disorders, pregnancy, eating disorder
history, or other factors that can significantly change safe and
appropriate calorie targets. Always consult a registered dietitian,
nutritionist, or physician before making changes to your diet, exercise,
or weight management plan.

