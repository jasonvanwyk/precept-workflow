#!/usr/bin/env python3
"""Precept Telegram Bot -- photo filing, voice transcription, status queries.

Runs on the dev server (10.0.10.21) as a systemd user service.
Single-user bot: silently ignores messages from unauthorized users.
"""

import functools
import logging
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import config

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("precept-bot")

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

active_project: str | None = None  # name (not full path)


# ---------------------------------------------------------------------------
# Auth decorator
# ---------------------------------------------------------------------------


def authorized(func):
    """Silently ignore messages from users not in the whitelist."""

    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != config.ALLOWED_USER_ID:
            logger.warning(
                "Unauthorized access attempt from user %s (%s)",
                update.effective_user.id,
                update.effective_user.username,
            )
            return
        return await func(update, context)

    return wrapper


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def project_path() -> Path | None:
    """Return the full path of the active project, or None."""
    if active_project is None:
        return None
    return config.PROJECTS_DIR / active_project


def git_commit(cwd: Path, filepath: Path, message: str) -> bool:
    """Stage a file and commit. Returns True on success."""
    try:
        subprocess.run(
            ["git", "add", str(filepath)],
            cwd=cwd,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=cwd,
            check=True,
            capture_output=True,
        )
        logger.info("Git commit in %s: %s", cwd.name, message)
        return True
    except subprocess.CalledProcessError as exc:
        logger.error("Git error in %s: %s", cwd.name, exc.stderr.decode())
        return False


def fuzzy_match_project(query: str) -> str | None:
    """Find a project directory matching the query (case-insensitive substring)."""
    query_lower = query.lower()
    candidates = sorted(
        p.name
        for p in config.PROJECTS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )
    # Exact match first
    for name in candidates:
        if name.lower() == query_lower:
            return name
    # Substring match
    matches = [n for n in candidates if query_lower in n.lower()]
    if len(matches) == 1:
        return matches[0]
    return None


async def send_long_message(update: Update, text: str):
    """Send a message, splitting at the Telegram limit if needed."""
    for i in range(0, len(text), config.MAX_MESSAGE_LENGTH):
        await update.message.reply_text(text[i : i + config.MAX_MESSAGE_LENGTH])


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


@authorized
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start and /help."""
    text = (
        "Precept Bot ready.\n\n"
        "/projects -- list available projects\n"
        "/project <name> -- set active project\n"
        "/status -- show active project STATUS.md\n\n"
        "Send a photo with caption to file it.\n"
        "Send a voice note to transcribe it."
    )
    await update.message.reply_text(text)


@authorized
async def cmd_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /projects -- list ~/Projects/ directories."""
    dirs = sorted(
        p.name
        for p in config.PROJECTS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )
    if not dirs:
        await update.message.reply_text("No projects found.")
        return

    marker = lambda d: " <<" if d == active_project else ""
    lines = [f"  {d}{marker(d)}" for d in dirs]
    await update.message.reply_text("Projects:\n" + "\n".join(lines))


@authorized
async def cmd_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /project <name> -- set active project with fuzzy matching."""
    global active_project

    if not context.args:
        if active_project:
            await update.message.reply_text(f"Active project: {active_project}")
        else:
            await update.message.reply_text("No active project. Usage: /project <name>")
        return

    query = " ".join(context.args)
    match = fuzzy_match_project(query)

    if match is None:
        await update.message.reply_text(
            f"No unique match for '{query}'. Try /projects to see available projects."
        )
        return

    active_project = match
    await update.message.reply_text(f"Active project: {active_project}")


@authorized
async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status -- show active project's STATUS.md."""
    pp = project_path()
    if pp is None:
        await update.message.reply_text("No active project. Use /project <name> first.")
        return

    status_file = pp / "STATUS.md"
    if not status_file.exists():
        await update.message.reply_text(f"No STATUS.md in {active_project}.")
        return

    content = status_file.read_text()
    if not content.strip():
        await update.message.reply_text(f"STATUS.md in {active_project} is empty.")
        return

    await send_long_message(update, content)


# ---------------------------------------------------------------------------
# Message handlers
# ---------------------------------------------------------------------------


@authorized
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save photo to {project}/pics/YYYY-MM-DD-{caption}.jpg and git commit."""
    pp = project_path()
    if pp is None:
        await update.message.reply_text("Set a project first: /project <name>")
        return

    caption = update.message.caption or "photo"
    # Sanitise caption for use as filename
    safe_caption = (
        caption.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace("\\", "-")
    )
    # Remove characters that aren't alphanumeric, hyphens, or underscores
    safe_caption = "".join(
        c for c in safe_caption if c.isalnum() or c in "-_"
    )
    if not safe_caption:
        safe_caption = "photo"

    date_str = datetime.now().strftime(config.DATE_FORMAT)
    filename = f"{date_str}-{safe_caption}.jpg"

    pics_dir = pp / "pics"
    pics_dir.mkdir(exist_ok=True)
    dest = pics_dir / filename

    # Download the highest-resolution photo
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    await file.download_to_drive(str(dest))

    logger.info("Photo saved: %s", dest)

    # Git commit
    committed = git_commit(
        cwd=pp,
        filepath=dest,
        message=f"Add photo: {filename}",
    )

    status = "saved + committed" if committed else "saved (git commit failed)"
    await update.message.reply_text(f"Photo {status}: pics/{filename}")


@authorized
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Transcribe voice note via Whisper, save to {project}/correspondence/."""
    pp = project_path()
    if pp is None:
        await update.message.reply_text("Set a project first: /project <name>")
        return

    await update.message.reply_text("Transcribing...")

    # Download voice file to temp location
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        tmp_path = Path(tmp.name)
        await file.download_to_drive(str(tmp_path))

    try:
        # Transcribe with Whisper
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
        text = transcript.text
    except Exception as exc:
        logger.error("Whisper transcription failed: %s", exc)
        await update.message.reply_text(f"Transcription failed: {exc}")
        return
    finally:
        tmp_path.unlink(missing_ok=True)

    # Save transcript
    date_str = datetime.now().strftime(config.DATE_FORMAT)
    corr_dir = pp / "correspondence"
    corr_dir.mkdir(exist_ok=True)

    # Find next available filename if one already exists for today
    base = f"{date_str}_voice-note"
    md_path = corr_dir / f"{base}.md"
    counter = 2
    while md_path.exists():
        md_path = corr_dir / f"{base}-{counter}.md"
        counter += 1

    content = f"# Voice Note -- {date_str}\n\n{text}\n"
    md_path.write_text(content)

    logger.info("Voice transcript saved: %s", md_path)

    # Git commit
    committed = git_commit(
        cwd=pp,
        filepath=md_path,
        message=f"Add voice transcript: {md_path.name}",
    )

    status = "transcribed + committed" if committed else "transcribed (git commit failed)"
    await update.message.reply_text(f"{status}: correspondence/{md_path.name}")

    # Send the transcript text back
    await send_long_message(update, text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    config.validate()

    logger.info(
        "Starting Precept Bot (user whitelist: %s, projects: %s)",
        config.ALLOWED_USER_ID,
        config.PROJECTS_DIR,
    )

    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler(["start", "help"], cmd_start))
    app.add_handler(CommandHandler("projects", cmd_projects))
    app.add_handler(CommandHandler("project", cmd_project))
    app.add_handler(CommandHandler("status", cmd_status))

    # Messages
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
