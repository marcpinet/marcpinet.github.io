+++
title = "Doublage"
description = "🎬 Dub your favorite scenes from any video in any language, online and with your friends! Everything works right in the browser, no installation required for your friends. Smart handling of every edge case. Includes tons of features and options for you to explore!"
date = "2026-06-04"
weight = 1

[extra]
remote_image = "/doublage/img.gif"
github_link = "https://github.com/marcpinet/doublage"
pinned = false
category = "personal"
+++

<style>
/* GitHub Alert Styles */
.github-alert {
    border-radius: 6px;
    margin: 16px 0;
    padding: 12px 16px;
    border-left: 4px solid;
}

.github-alert-note {
    background-color: #ddf4ff;
    border-color: #0969da;
}

.github-alert-tip {
    background-color: #dcfce7;
    border-color: #1a7f37;
}

.github-alert-important {
    background-color: #f3e8ff;
    border-color: #8250df;
}

.github-alert-warning {
    background-color: #fff8dc;
    border-color: #d1242f;
}

.github-alert-caution {
    background-color: #ffebee;
    border-color: #d1242f;
}

/* Table Wrapper */
.table-wrapper {
    overflow-x: auto;
    margin: 16px 0;
}

.table-wrapper table {
    width: 100%;
    border-collapse: collapse;
}

.table-wrapper th,
.table-wrapper td {
    border: 1px solid #d1d5da;
    padding: 8px 12px;
    text-align: left;
}

.table-wrapper th {
    font-weight: 600;
}

/* Video Styles */
video {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 16px 0;
}

/* Code Block Styles */
pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    margin: 16px 0;
}

code {
    background-color: #f6f8fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'SFMono-Regular', 'Monaco', 'Inconsolata', 'Liberation Mono', 'Consolas', monospace;
    font-size: 85%;
    color: #24292f;
}

pre code {
    background-color: transparent;
    padding: 0;
}

/* Dark mode support for inline code */
@media (prefers-color-scheme: dark) {
    pre {
        background-color: #161b22;
        color: #f0f6fc;
    }
    
    code {
        background-color: #21262d;
        color: #f0f6fc;
    }
    
    pre code {
        background-color: transparent;
        color: inherit;
    }
}
</style>

# 🎬 Doublage

<p align="center">
  <img src="readme_assets/dubbling_example.png" alt="Dubbing a scene live in the browser — the video plays while a rhythmo band scrolls the line word by word" width="100%">
</p>

> 🌍 **Works in any language.** The screenshots here show French dubs, but nothing is French-specific — Doublage works with content in **any language**: use the video's existing subtitles (any language), or auto-generate them with Whisper (multilingual, ~100 languages). Voice/background separation, speaker diarization, recording and assembly are all language-independent.

Dub your favorite scenes with friends, straight from the browser. **You** (the host) pick a video, prepare the scene and host the game. **Your friends** open a link in their browser (zero install) and dub a character. Everything is then assembled into a final video.

Voices go through an external voice channel (Discord or anything else): the game does not transmit audio, it only synchronizes the recording.

```
  YOU (host)                RELAY (small server)            YOUR FRIENDS
  preprocess + assembly <-> rooms + WebSocket + storage  <-> browser (0 install)
  Python + GPU + ffmpeg                                      (click the link)
```

The host app runs locally. The relay can run on any always-on server (a Raspberry Pi is plenty, but any machine works): see "Hosting the relay" below.

## Two game modes

- **Live Take**: a single, synchronized take. The host starts the recording, everyone plays at the same time (3-2-1 countdown), the host can pause and resume. A "one shot" vibe.
- **Pro Take**: everyone at their own pace. Each player records their lines one by one (with a 3-2-1 countdown before each line), several takes possible (configurable limit, or unlimited), picks their best take and tunes the timing. A banner shows who is done; once everyone is finished, the host wraps up and moves on to assembly.

## For your friends (nothing to install)

1. Open the invite link (e.g. `https://your-relay/?room=ABC12`) or enter the code.
2. Pick a nickname, then a character in the lobby (the host can also assign roles at random).
3. Headphones recommended, otherwise the scene's sound leaks back into the mic. On Bluetooth, calibrate your mic delay (popup at the start, ~15 s) so your voice lands on beat.
4. Play: the video rolls and a **rhythmo band** (dubbing-studio style) scrolls your lines word by word; your text is highlighted when it's your turn.

![The lobby — share the invite link, pick a character (or let the host randomize), calibrate your audio delay, and the host picks the mode and starts the game](readme_assets/lobby.png)

## For you (the host)

### 1. Install (once)

- `ffmpeg` on the PATH (an NVIDIA GPU is used automatically for encoding when `h264_nvenc` is available, otherwise it falls back to CPU `libx264`).
- Python 3.10+ then:
  ```
  python -m venv .venv
  .venv\Scripts\activate            # Windows, or: source .venv/bin/activate
  pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124   # GPU recommended
  pip install -r requirements.txt
  ```
- Copy `.env.example` to `.env` and fill in at least:
  - `HUGGINGFACE_TOKEN` for pyannote diarization (first accept the terms of the `pyannote/speaker-diarization-3.1` model on huggingface.co).
  - `RELAY_URL`: the address of the relay the host targets (defaults to `http://127.0.0.1:21826`, i.e. a relay launched locally).

### 2. Launch the host app

```
python -m dubbing.host        # http://127.0.0.1:8765
```

### 3. Prepare the scene (everything in the app)

Enter your nickname, then "New scene":

- **Source**: browse to a video (mp4/mkv), set the range to keep (timeline, `HH:MM:SS` fields, "at cursor"), check the tracks (the VFF is pre-selected, never the VFQ nor forced/SDH tracks). Subtitles come from the embedded track by default; if the video has no usable one, tick **"Generate subtitles automatically"** (local Whisper large-v3 transcription). Then run preprocessing.
- **Preprocessing**: voice/background separation (Demucs), diarization (pyannote) and word-level forced alignment (for the karaoke rhythmo band), assembled into a `project.json`.
- **Editing**: fix who speaks, the text, the timestamps (start/end per line), rename or merge the detected voices, split a line with two speakers, listen to excerpts. The word-level karaoke is re-aligned automatically when you edit a text.
- **Game**: choose the mode and the number of takes.
- **Host**: the scene is transcoded (H.264 720p, browser-playable) and sent to the relay. You get a code and a link to share.

![Source screen — set the crop, pick the audio/subtitle tracks (smart auto-pick prefers VFF and skips VFQ/forced/SDH), or auto-generate subtitles with Whisper (here: a French example, but the language is configurable)](readme_assets/preprocess_subtitles.png)

![Editor — fix who speaks, the text and the per-line timestamps; rename or merge the detected voices and play samples (French example)](readme_assets/subtitles_editing_example.png)

Diarization tip: for 2-3 characters with similar voices, set "Num speakers" = the real count + 1, then merge the extra clusters in the editor. Setting this number enables embedding-based diarization (one embedding per line), far more robust than overlap for close voices.

From the command line, without the UI:

```
python -m dubbing.pipeline --input film.mkv --output output_bundles/out_film --start 37:06 --end 39:30 --num-speakers 3
python -m dubbing.host --bundle output_bundles/out_film
```

Useful pipeline options: `--list-tracks` (list the tracks and exit), `--auto-subs` (Whisper subtitles instead of the embedded track), `--resume` (resume by skipping stages already produced), `--skip-separation` / `--skip-diarization` / `--skip-alignment`, `--num-speakers` / `--min-speakers` / `--max-speakers`. `python -m dubbing.pipeline -h` lists everything.

### 4. Play then assemble

- Lobby, "Start the game". In Live you drive the recording; in Pro everyone records their lines. Each take is automatically compensated for its player's measured mic delay (calibration).
- "Finish" opens the assembly screen: each player's kept takes are pre-selected, you can re-choose, re-time, trim/split a take, set the background/voice levels and a per-character latency adjustment. Audio mix choice:
  - **separated** (default): the Demucs background (music/SFX without voices) everywhere.
  - **OWS**: the original audio everywhere, except during dubbed lines (where it switches to background + the take).
- Choose mp4/mkv (re-encode to H.264 ticked by default), then "Assemble" and download the final video.

![Assembly screen — a per-take timeline (drag to retime, scissors to split), background/voice levels, container + re-encode, and per-character timing correction (French example)](readme_assets/timeline_editing_assembling_example.png)

## Hosting the relay

The relay is standalone (`relay/server.py`, light dependencies, no ffmpeg and no ML). On the server:

```
pip install -r relay/requirements.txt
python relay/server.py
```

It is configured via the `.env` at the root (see `.env.example`): `HOST`, `PORT`, `STORAGE_DIR`, `ROOM_TTL_MIN`, `EMPTY_ROOM_GRACE_MIN`, `MAX_ROOM_MB`, `ALLOWED_ORIGINS`, and `PUBLIC_URL` (used for the Open Graph link preview). The defaults are fine (port 21826, ephemeral rooms purged after inactivity and shortly after everyone has left).

For a production setup: a reverse proxy (Caddy, nginx) for TLS, and a systemd service to restart the relay automatically (`doublage.service` + `update.bat` templates to adapt to your server).

## Structure

| Path | Role |
|---|---|
| `dubbing/pipeline.py` | Preprocessing orchestration (CLI `python -m dubbing.pipeline`) |
| `dubbing/extract.py` | ffmpeg extraction: muted video, WAV audio, SRT subtitles |
| `dubbing/tracks.py` | ffprobe probing + track selection (prefers VFF, excludes VFQ/forced/SDH) |
| `dubbing/subtitles.py` | Subtitle parsing + splitting of multi-speaker cues |
| `dubbing/transcribe.py` | Auto subtitles (Whisper large-v3, local) for `--auto-subs` |
| `dubbing/separate.py` | Voice/background separation (Demucs) |
| `dubbing/diarize.py` | pyannote diarization (overlap, or per-line embedding when `--num-speakers`) |
| `dubbing/align.py` | Assigning lines to characters, merging lines |
| `dubbing/align_words.py` | Word-level forced alignment (torchaudio MMS_FA) for the rhythmo band |
| `dubbing/models.py` + `dubbing/bundle.py` | Bundle dataclasses + reading/writing `project.json` |
| `dubbing/gpu.py` + `dubbing/ffmpeg_gpu.py` | VRAM management + GPU-accelerated encoding (NVENC, CPU `libx264` fallback) |
| `dubbing/preprocess_app.py` + `dubbing/web/preprocess.html` | Local preprocessing UI (file pick, crop, preview) |
| `dubbing/host.py` | Local host app: editing, hosting, collection, final assembly |
| `dubbing/distribute.py` | Lightweight distribution bundle (H.264 720p video, AAC audio) |
| `dubbing/export.py` | Mix/mux helpers for the final export |
| `dubbing/merge_archives.py` | Multi-player assembly (mix + mux, `separated`/`ows` modes) |
| `dubbing/web/index.html` | Single web app (landing, lobby, game, rhythmo band, assembly) |
| `relay/server.py` | Relay: code-based rooms, WebSocket, storage of bundles and takes |
| `scripts/compare_diar.py` | Dev tool: compare several diarization settings |

## Notes

- Headphones on the players' side, to avoid the background audio leaking into the mic. On Bluetooth, calibrate the mic delay (wireless headsets add 150-300 ms).
- The distribution video is H.264 720p (the original HEVC does not play everywhere); the original files are used for the final assembly.
- ffmpeg encoding goes through the GPU (NVENC) when possible, with an automatic fallback to CPU (`libx264`).
- Language-agnostic: bring subtitles in any language, or auto-generate them with Whisper (multilingual). The screenshots show French scenes only as an example.
- "Between friends" security: a room = an invite code, no accounts. Whoever has the code gets in.
