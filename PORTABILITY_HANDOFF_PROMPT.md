# Handoff prompt — paste this into each of the three Wagic-Profile sessions

Paste the block below (unchanged) into each session separately. Each session will produce its own `PORTABILITY_NOTES.md` in its own project folder. The notes from all four projects together form the brief for whoever does the tidy-up.

---

## PROMPT TO PASTE

I'm handing this project off to a different person (another Claude instance, another dev, or both) to do two things in sequence:

1. **Portability tidy-up** — rewrite hardcoded paths and machine-specific values so the project runs on any dev's setup, not just mine.
2. **Build / deploy work afterward** — they'll be running whatever build + deploy commands this project uses, so your notes need to double as a runbook.

Please write a single file called `PORTABILITY_NOTES.md` at the root of this project. Overwrite it if it already exists. Use this exact structure:

### 1. What this project is
One or two sentences. What does it do, who uses it, what does it produce. Mention which platforms it targets (web, Windows, Android, etc.).

### 2. Hardcoded-path hotspots
For every script / source file that has an absolute path, user name, drive letter, device serial, machine-specific location, or similar baked in — list the file, the constant / variable name, and what it currently points to. Mark each as either:
- **repo-relative** (derivable from where the project lives on disk)
- **machine-specific** (SDK, NDK, Python path, toolchain)
- **user-profile-specific** (home dir, credentials, keys)
- **device-specific** (serial number, SD card UUID, IP address)

Read every script, every config file, every notebook, every shell file. Don't skip tests or utility scripts. Grep for `C:\`, `M:\`, `G:\`, `/home/`, `/Users/`, `\Users\`, `Claude_projects`, `Wagic-Profile`, and the user's name.

### 3. Machine / device / user specifics to parameterise
Make a table of every distinct "my-machine-ism" — repo root path, user home, SDK locations, device serial, API keys, URLs, ports, login names, profile names, versioned filenames, passwords (including "safe" defaults like `android`), any hardcoded integer that's actually a config value. One row per thing, showing the current value and where it appears.

### 4. External inputs & outputs (paths OUTSIDE this project's folder)
If the project reads or writes files outside its own folder — e.g. pulls `collection.dat` from `G:\Wagic\…`, reads `mtg.txt` from the main wagic repo, writes somewhere under `%APPDATA%`, hits an Android device over ADB — list every such path and what the project does with it. Mark each as **read**, **write**, or **read+write**.

### 5. Cross-project dependencies
There are four related projects in my setup. They share data shapes (card IDs, `collection.dat` format, deck file format, `Wagic-core-0255.zip` name, `Maxglee` profile name). Explicitly list anything this project shares with the others:
- `M:\Claude_projects\wagic\` — main C++ game, produces APK + core zip
- `M:\Claude_projects\Wagic-Profile\<web-deck-builder>`
- `M:\Claude_projects\Wagic-Profile\<gemini-prompt-gen>`
- `M:\Claude_projects\Wagic-Profile\<collection-dedup>`

If this project reads/writes anything that another one touches, name the other project and the shared file / format / convention.

### 6. Build & run cheat-sheet
Step-by-step commands to build, run, test, and deploy this project as it currently stands. Include tool versions where they matter (Python version, Node version, browser for web app, etc.). Include any "first-time setup" steps (pip install, npm install, API keys to obtain).

The tidy-upper will run this after finishing the portability work, so it must actually work end-to-end.

### 7. Gotchas
Things that would cost the tidy-upper hours if they don't know them. Examples from neighbouring projects: MTP timestamps on Android don't update reliably; the game's core zip is named with a version (`Wagic-core-0255.zip`) not `core.zip`; SD card path is `/storage/<UUID>/` not `/sdcard/`; specific toolchain versions (`android-ndk-r22`) that newer versions break. List anything non-obvious about this project.

### 8. Suggested shape for parameterisation (non-binding)
Recommend how the tidy-upper should replace the hardcoded values. Options: `.env` + `python-dotenv`, `config.yaml`, `argparse` CLI args, a small `paths.py` module, env vars, a JSON config. Pick the option that fits the project best and say why — but note that the final decision is mine.

### 9. What's OUT of scope for tidy-up
Anything that should NOT be touched by a portability pass: generated artifacts, third-party vendored code, data files, open bugs currently being worked by another session, etc.

### 10. After tidy-up: build work
Assume the tidy-upper will run the build/deploy commands once portability is done. List any prerequisites they'll need to verify first (tool locations, device connectivity, API keys, network access, permissions). If any first-build step takes longer than a few seconds, warn them.

### Notes on how to write it

- Be specific. "Some paths in the scripts need fixing" is useless. "`patch_apk.py` line 18: `DEBUG_KEY = r'C:\Users\john\.android\debug.keystore'` — user-profile-specific" is useful.
- Don't include conversation history or session context. The tidy-upper won't read transcripts — they'll read this file.
- If something is truly portable already and doesn't need work, say so explicitly so they don't waste time checking it.
- If you're unsure whether something is a real dependency or just incidental, flag it with a "**verify before refactoring**" note rather than guessing.

Produce the file now. Don't ask for clarification — make reasonable inferences from what's actually in the project folder. If critical information is genuinely missing, list those gaps in a final "§11. Open questions for the user" section.

---

## END OF PROMPT

Drop the file in each project, paste the prompt, let each session produce its notes. Once all three are done + the one I've already written for the main wagic project, the tidy-upper has everything they need to start.
