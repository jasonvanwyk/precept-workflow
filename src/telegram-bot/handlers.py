"""Handler functions for the Precept Bot.

All handlers receive (update, context) and use context.user_data for state:
  - active_project: str | None
  - active_visit_id: int | None
  - active_task_id: int | None
  - page: int (for project pagination)
"""

import logging
import subprocess
import tempfile
from datetime import datetime, timedelta, time as dt_time
from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

import config
import db
import menus

logger = logging.getLogger("precept-bot.handlers")

# Conversation states
(
    MAIN_MENU,
    SELECT_PROJECT,
    VISIT_ACTIVE,
    VISIT_LOCATION,
    TASK_DESCRIPTION,
    SEARCH_QUERY,
    QUICK_NOTE,
    NEW_PROJECT,
) = range(8)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _project(ctx: ContextTypes.DEFAULT_TYPE) -> str | None:
    return ctx.user_data.get("active_project")


def _project_path(ctx: ContextTypes.DEFAULT_TYPE) -> Path | None:
    p = _project(ctx)
    return config.PROJECTS_DIR / p if p else None


def _visit_id(ctx: ContextTypes.DEFAULT_TYPE) -> int | None:
    return ctx.user_data.get("active_visit_id")


def _task_id(ctx: ContextTypes.DEFAULT_TYPE) -> int | None:
    return ctx.user_data.get("active_task_id")


def _reply_keyboard(ctx: ContextTypes.DEFAULT_TYPE):
    """Return the appropriate persistent reply keyboard."""
    if _visit_id(ctx):
        return menus.visit_reply_keyboard()
    return menus.default_reply_keyboard()


def _list_projects() -> list[str]:
    """List project directories."""
    return sorted(
        p.name
        for p in config.PROJECTS_DIR.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )


def _fuzzy_match_project(query: str) -> str | None:
    """Find a project directory matching the query."""
    query_lower = query.lower()
    candidates = _list_projects()
    for name in candidates:
        if name.lower() == query_lower:
            return name
    matches = [n for n in candidates if query_lower in n.lower()]
    if len(matches) == 1:
        return matches[0]
    return None


def _git_commit(cwd: Path, filepath: Path, message: str) -> bool:
    """Stage a file and commit."""
    try:
        subprocess.run(
            ["git", "add", str(filepath)], cwd=cwd, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", message], cwd=cwd, check=True, capture_output=True
        )
        logger.info("Git commit in %s: %s", cwd.name, message)
        return True
    except subprocess.CalledProcessError as exc:
        logger.error("Git error in %s: %s", cwd.name, exc.stderr.decode())
        return False


def _safe_filename(text: str) -> str:
    """Sanitise text for use as a filename."""
    safe = text.lower().replace(" ", "-").replace("/", "-").replace("\\", "-")
    safe = "".join(c for c in safe if c.isalnum() or c in "-_")
    return safe or "untitled"


def _main_menu_text(ctx: ContextTypes.DEFAULT_TYPE) -> str:
    """Build the main menu header text."""
    project = _project(ctx)
    visit_id = _visit_id(ctx)
    task_id = _task_id(ctx)

    lines = ["Precept Bot"]
    if project:
        lines[0] += f" -- Active: {project}"
    else:
        lines[0] += " -- No project selected"

    if visit_id:
        visit = db.get_active_visit(project)
        if visit:
            loc = visit.get("location") or "no location"
            lines.append(f"Site visit in progress ({loc})")
    if task_id:
        task = db.get_active_task(project)
        if task:
            lines.append(f"Task running: {task['description']}")

    return "\n".join(lines)


async def _send_long(update: Update, text: str, **kwargs):
    """Send a message, splitting at the Telegram limit."""
    target = update.callback_query.message if update.callback_query else update.message
    for i in range(0, len(text), config.MAX_MESSAGE_LENGTH):
        await target.reply_text(text[i : i + config.MAX_MESSAGE_LENGTH], **kwargs)


# ---------------------------------------------------------------------------
# /start and main menu
# ---------------------------------------------------------------------------


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /start, /help, /menu, "menu", or "0"."""
    text = _main_menu_text(context)
    await update.message.reply_text(
        text,
        reply_markup=menus.main_menu_keyboard(_project(context)),
    )
    # Also set the persistent reply keyboard
    await update.message.reply_text(
        "Tap a button above or use the keyboard below.",
        reply_markup=_reply_keyboard(context),
    )
    return MAIN_MENU


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Route main menu inline button presses."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == menus.MENU_MAIN:
        text = _main_menu_text(context)
        await query.edit_message_text(
            text, reply_markup=menus.main_menu_keyboard(_project(context))
        )
        return MAIN_MENU

    if data == menus.MENU_SWITCH_PROJECT:
        return await _show_project_list(update, context, page=0)

    if data == menus.MENU_STATUS:
        await _show_status(update, context)
        return MAIN_MENU

    if data == menus.MENU_START_VISIT:
        return await _start_visit_flow(update, context)

    if data == menus.MENU_QUICK_NOTE:
        await query.edit_message_text("Type your quick note:")
        return QUICK_NOTE

    if data == menus.MENU_START_TASK:
        return await _start_task_flow(update, context)

    if data == menus.MENU_SEARCH:
        await query.edit_message_text("Enter search term:")
        return SEARCH_QUERY

    if data == menus.MENU_RECENT:
        await _show_recent_activity(update, context)
        return MAIN_MENU

    if data == "noop":
        return MAIN_MENU

    return MAIN_MENU


# ---------------------------------------------------------------------------
# Project selection
# ---------------------------------------------------------------------------


async def _show_project_list(
    update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0
) -> int:
    """Show paginated project list."""
    query = update.callback_query
    projects = _list_projects()

    if not projects:
        await query.edit_message_text("No projects found.")
        return MAIN_MENU

    context.user_data["page"] = page
    keyboard = menus.project_list_keyboard(projects, page, _project(context))
    await query.edit_message_text(
        "Select a project:", reply_markup=keyboard
    )
    return SELECT_PROJECT


async def project_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle project selection and pagination."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith(menus.PAGE_CB):
        page = int(data[len(menus.PAGE_CB) :])
        return await _show_project_list(update, context, page)

    if data.startswith(menus.PROJECT_CB):
        project_name = data[len(menus.PROJECT_CB) :]
        context.user_data["active_project"] = project_name
        db.log_event("project_switched", project_name)
        await query.edit_message_text(f"Active project: {project_name}")
        await query.message.reply_text(
            _main_menu_text(context),
            reply_markup=menus.main_menu_keyboard(project_name),
        )
        return MAIN_MENU

    if data == menus.MENU_MAIN:
        return await _back_to_menu(update, context)

    return SELECT_PROJECT


async def project_name_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle typed project name in SELECT_PROJECT state."""
    query_text = update.message.text.strip()
    match = _fuzzy_match_project(query_text)

    if match is None:
        await update.message.reply_text(
            f"No unique match for '{query_text}'. Tap a button or try again.",
            reply_markup=_reply_keyboard(context),
        )
        return SELECT_PROJECT

    context.user_data["active_project"] = match
    db.log_event("project_switched", match)
    await update.message.reply_text(
        f"Active project: {match}",
        reply_markup=_reply_keyboard(context),
    )
    await update.message.reply_text(
        _main_menu_text(context),
        reply_markup=menus.main_menu_keyboard(match),
    )
    return MAIN_MENU


async def _back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to the main menu from a callback."""
    query = update.callback_query
    text = _main_menu_text(context)
    await query.edit_message_text(
        text, reply_markup=menus.main_menu_keyboard(_project(context))
    )
    return MAIN_MENU


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------


async def _show_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show project status + DB stats."""
    query = update.callback_query
    project = _project(context)

    if not project:
        await query.edit_message_text(
            "No active project. Select one first.",
            reply_markup=menus.main_menu_keyboard(),
        )
        return

    lines = [f"Status for {project}:"]

    # STATUS.md content
    pp = config.PROJECTS_DIR / project
    status_file = pp / "STATUS.md"
    if status_file.exists():
        content = status_file.read_text().strip()
        if content:
            # Truncate if very long
            if len(content) > 2000:
                content = content[:2000] + "\n... (truncated)"
            lines.append(f"\n{content}")
    else:
        lines.append("No STATUS.md found.")

    # DB stats
    stats = db.project_stats(project)
    lines.append(
        f"\nDB: {stats['photos']} photos, {stats['voice_notes']} voice notes, "
        f"{stats['quick_notes']} notes, {stats['visits']} visits, "
        f"{stats['scans']} scans, {stats['total_task_hours']}h tracked"
    )

    # Active task info
    active_task = db.get_active_task(project)
    if active_task:
        lines.append(f"\nActive task: {active_task['description']} (since {active_task['started_at'][:16]})")

    text = "\n".join(lines)
    # Can't edit_message_text if it's too long, so use reply
    if len(text) > config.MAX_MESSAGE_LENGTH:
        await query.edit_message_text("Status loading...")
        await _send_long(update, text)
    else:
        await query.edit_message_text(text, reply_markup=menus.main_menu_keyboard(project))


# ---------------------------------------------------------------------------
# Site visit flow
# ---------------------------------------------------------------------------


async def _start_visit_flow(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Begin the site visit start process."""
    query = update.callback_query
    project = _project(context)

    # Check for already-active visit
    if _visit_id(context):
        await query.edit_message_text(
            f"Visit already in progress. End it first.",
            reply_markup=menus.end_visit_keyboard(),
        )
        return MAIN_MENU

    if project:
        await query.edit_message_text(
            f"Start visit for {project}?",
            reply_markup=menus.visit_confirm_keyboard(project),
        )
        return VISIT_LOCATION
    else:
        # No project set -- go to project selector
        return await _show_project_list(update, context, page=0)


async def visit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle visit-related callbacks."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == menus.VISIT_CONFIRM:
        await query.edit_message_text(
            "Set visit location:\n"
            "- Type a location name\n"
            "- Share your GPS location\n"
            "- Or tap Skip"
        )
        await query.message.reply_text(
            "Waiting for location...",
            reply_markup=menus.visit_location_keyboard(),
        )
        return VISIT_LOCATION

    if data == menus.VISIT_SWITCH_FIRST:
        return await _show_project_list(update, context, page=0)

    if data == menus.VISIT_SKIP_LOCATION:
        return await _create_visit(update, context, location=None)

    if data == menus.VISIT_END:
        await query.edit_message_text(
            "End current visit?",
            reply_markup=menus.end_visit_keyboard(),
        )
        return VISIT_ACTIVE

    if data == menus.VISIT_END_CONFIRM:
        return await _end_visit_handler(update, context)

    if data == menus.MENU_MAIN:
        return await _back_to_menu(update, context)

    return VISIT_ACTIVE


async def visit_location_text(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle typed location name during visit setup."""
    location = update.message.text.strip()
    return await _create_visit(update, context, location=location)


async def visit_location_gps(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle shared GPS location during visit setup."""
    loc = update.message.location
    context.user_data["visit_lat"] = loc.latitude
    context.user_data["visit_lon"] = loc.longitude
    return await _create_visit(
        update,
        context,
        location=f"{loc.latitude:.6f}, {loc.longitude:.6f}",
        latitude=loc.latitude,
        longitude=loc.longitude,
    )


async def _create_visit(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    location: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> int:
    """Create the visit in DB and switch to visit mode."""
    project = _project(context)
    pp = _project_path(context)

    # Ad-hoc project creation
    if pp and not pp.exists():
        pp.mkdir(parents=True)
        subprocess.run(["git", "init"], cwd=pp, capture_output=True)
        logger.info("Created ad-hoc project: %s", pp)

    visit_id = db.start_visit(project, location, latitude, longitude)
    context.user_data["active_visit_id"] = visit_id

    loc_text = f" at {location}" if location else ""
    target = update.callback_query.message if update.callback_query else update.message
    await target.reply_text(
        f"Site visit started for {project}{loc_text}\n"
        f"Visit ID: {visit_id}\n\n"
        "Photos and voice notes will be tagged to this visit.\n"
        "Use the keyboard below during your visit.",
        reply_markup=menus.visit_reply_keyboard(),
    )
    return MAIN_MENU


async def _end_visit_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """End the active visit and generate summary."""
    visit_id = _visit_id(context)
    if not visit_id:
        target = update.callback_query.message if update.callback_query else update.message
        await target.reply_text("No active visit to end.")
        return MAIN_MENU

    summary_data = db.end_visit(visit_id)
    context.user_data["active_visit_id"] = None

    if summary_data:
        # Save summary as markdown in project
        pp = _project_path(context)
        if pp and pp.exists():
            docs_dir = pp / "docs" / "site-visits"
            docs_dir.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime(config.DATE_FORMAT)
            summary_file = docs_dir / f"{date_str}-visit-{visit_id}.md"
            md_content = (
                f"# Site Visit -- {summary_data['project']}\n\n"
                f"**Date:** {summary_data['started_at'][:10]}\n"
                f"**Location:** {summary_data['location'] or 'Not set'}\n"
                f"**Duration:** {summary_data['duration']}\n\n"
                f"## Summary\n\n"
                f"- Photos: {summary_data['photo_count']}\n"
                f"- Voice notes: {summary_data['voice_count']}\n"
                f"- Quick notes: {summary_data['note_count']}\n"
                f"- Tasks: {summary_data['task_count']}\n"
                f"- Network scans: {summary_data['scan_count']}\n"
            )
            if summary_data["notes"]:
                md_content += f"\n## Notes\n\n{summary_data['notes']}\n"
            summary_file.write_text(md_content)
            _git_commit(pp, summary_file, f"Add site visit summary: {summary_file.name}")

        target = update.callback_query.message if update.callback_query else update.message
        await target.reply_text(
            f"Visit ended.\n\n{summary_data['summary']}",
            reply_markup=menus.default_reply_keyboard(),
        )
    else:
        target = update.callback_query.message if update.callback_query else update.message
        await target.reply_text(
            "Visit ended.", reply_markup=menus.default_reply_keyboard()
        )

    return MAIN_MENU


# ---------------------------------------------------------------------------
# Task timer
# ---------------------------------------------------------------------------


async def _start_task_flow(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Begin starting a task."""
    query = update.callback_query
    project = _project(context)

    if not project:
        await query.edit_message_text(
            "Set a project first.",
            reply_markup=menus.main_menu_keyboard(),
        )
        return MAIN_MENU

    # Check for already-active task
    active = _task_id(context)
    if active:
        task = db.get_active_task(project)
        if task:
            await query.edit_message_text(
                f"Task already running: {task['description']}\n"
                f"Started: {task['started_at']}",
                reply_markup=menus.finish_task_keyboard(active),
            )
            return MAIN_MENU

    await query.edit_message_text("Describe the task:")
    return TASK_DESCRIPTION


async def task_description_text(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle typed task description."""
    description = update.message.text.strip()
    project = _project(context)
    visit_id = _visit_id(context)

    task_id = db.start_task(project, description, visit_id)
    context.user_data["active_task_id"] = task_id

    await update.message.reply_text(
        f"Task started: {description}\nTask ID: {task_id}",
        reply_markup=menus.finish_task_keyboard(task_id),
    )
    return MAIN_MENU


async def task_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle task-related callbacks."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == menus.TASK_FINISH:
        task_id = _task_id(context)
        if not task_id:
            await query.edit_message_text("No active task to finish.")
            return MAIN_MENU

        result = db.end_task(task_id)
        context.user_data["active_task_id"] = None

        if result:
            await query.edit_message_text(
                f"Task finished: {result['description']}\n"
                f"Duration: {result['duration_minutes']:.0f} minutes"
            )
        else:
            await query.edit_message_text("Task finished.")

        await query.message.reply_text(
            _main_menu_text(context),
            reply_markup=menus.main_menu_keyboard(_project(context)),
        )
        return MAIN_MENU

    return MAIN_MENU


# ---------------------------------------------------------------------------
# Quick note
# ---------------------------------------------------------------------------


async def quick_note_text(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Save a quick text note to the project."""
    project = _project(context)
    if not project:
        await update.message.reply_text(
            "No active project.", reply_markup=_reply_keyboard(context)
        )
        return MAIN_MENU

    note = update.message.text.strip()
    pp = _project_path(context)

    # Save to correspondence
    corr_dir = pp / "correspondence"
    corr_dir.mkdir(exist_ok=True)
    date_str = datetime.now().strftime(config.DATE_FORMAT)
    time_str = datetime.now().strftime("%H:%M")

    note_file = corr_dir / f"{date_str}_quick-note.md"
    # Append if file exists for today
    if note_file.exists():
        existing = note_file.read_text()
        note_file.write_text(f"{existing}\n**{time_str}:** {note}\n")
    else:
        note_file.write_text(f"# Quick Notes -- {date_str}\n\n**{time_str}:** {note}\n")

    _git_commit(pp, note_file, f"Add quick note: {date_str}")

    # Log to DB
    visit_id = _visit_id(context)
    db.log_quick_note(project, note, visit_id)

    await update.message.reply_text(
        f"Note saved to {project}/correspondence/{note_file.name}",
        reply_markup=_reply_keyboard(context),
    )
    return MAIN_MENU


async def note_save_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle 'save as note' confirmation from outside-visit text."""
    query = update.callback_query
    await query.answer()

    if query.data != "save_as_note":
        await query.edit_message_text("Cancelled.")
        return MAIN_MENU

    note_text = context.user_data.pop("pending_note", "")
    if not note_text:
        await query.edit_message_text("Nothing to save.")
        return MAIN_MENU

    project = _project(context)
    if not project:
        await query.edit_message_text("No active project.")
        return MAIN_MENU

    pp = _project_path(context)

    # Save to correspondence file
    corr_dir = pp / "correspondence"
    corr_dir.mkdir(exist_ok=True)
    date_str = datetime.now().strftime(config.DATE_FORMAT)
    time_str = datetime.now().strftime("%H:%M")

    note_file = corr_dir / f"{date_str}_quick-note.md"
    if note_file.exists():
        existing = note_file.read_text()
        note_file.write_text(f"{existing}\n**{time_str}:** {note_text}\n")
    else:
        note_file.write_text(
            f"# Quick Notes -- {date_str}\n\n**{time_str}:** {note_text}\n"
        )

    _git_commit(pp, note_file, f"Add quick note: {date_str}")
    db.log_quick_note(project, note_text)

    await query.edit_message_text(
        f"Note saved to {project}/correspondence/{note_file.name}"
    )
    await query.message.reply_text(
        _main_menu_text(context),
        reply_markup=menus.main_menu_keyboard(project),
    )
    return MAIN_MENU


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


async def search_query_text(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Search voice transcripts and quick notes for a keyword."""
    query_text = update.message.text.strip()
    results = db.search_transcripts(query_text)

    if not results:
        await update.message.reply_text(
            f"No results matching '{query_text}'.",
            reply_markup=_reply_keyboard(context),
        )
        return MAIN_MENU

    lines = [f"Found {len(results)} result(s) for '{query_text}':\n"]
    for r in results:
        text_content = r.get("text") or ""
        source_tag = r.get("source", "voice")
        idx = text_content.lower().find(query_text.lower())
        start = max(0, idx - 40)
        end = min(len(text_content), idx + len(query_text) + 40)
        snippet = text_content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(text_content):
            snippet = snippet + "..."

        lines.append(
            f"[{r['project']}] {r['created_at'][:10]} ({source_tag})\n"
            f"  {snippet}\n"
        )

    await _send_long(update, "\n".join(lines), reply_markup=_reply_keyboard(context))
    return MAIN_MENU


# ---------------------------------------------------------------------------
# Recent activity
# ---------------------------------------------------------------------------


async def _show_recent_activity(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Show recent bot events."""
    query = update.callback_query
    events = db.recent_activity(15)

    if not events:
        await query.edit_message_text(
            "No recent activity.",
            reply_markup=menus.main_menu_keyboard(_project(context)),
        )
        return

    lines = ["Recent activity:\n"]
    for e in events:
        project_tag = f" [{e['project']}]" if e["project"] else ""
        lines.append(f"{e['created_at'][:16]} {e['event_type']}{project_tag}")
        if e["detail"]:
            lines.append(f"  {e['detail'][:80]}")

    await query.edit_message_text(
        "\n".join(lines),
        reply_markup=menus.main_menu_keyboard(_project(context)),
    )


# ---------------------------------------------------------------------------
# Photo handler (updated with DB logging)
# ---------------------------------------------------------------------------


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save photo to {project}/pics/ and log in DB."""
    pp = _project_path(context)
    if pp is None:
        await update.message.reply_text(
            "Set a project first.",
            reply_markup=_reply_keyboard(context),
        )
        return MAIN_MENU

    project = _project(context)
    caption = update.message.caption or "photo"
    safe_caption = _safe_filename(caption)
    date_str = datetime.now().strftime(config.DATE_FORMAT)
    filename = f"{date_str}-{safe_caption}.jpg"

    pics_dir = pp / "pics"
    pics_dir.mkdir(exist_ok=True)
    dest = pics_dir / filename

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    await file.download_to_drive(str(dest))
    logger.info("Photo saved: %s", dest)

    committed = _git_commit(pp, dest, f"Add photo: {filename}")

    # DB logging
    visit_id = _visit_id(context)
    db.log_photo(project, str(dest), caption, visit_id=visit_id)

    status = "saved + committed" if committed else "saved (git commit failed)"
    await update.message.reply_text(
        f"Photo {status}: pics/{filename}",
        reply_markup=_reply_keyboard(context),
    )
    return MAIN_MENU


# ---------------------------------------------------------------------------
# Voice handler (updated with DB logging)
# ---------------------------------------------------------------------------


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Transcribe voice note and log in DB."""
    from openai import OpenAI

    pp = _project_path(context)
    if pp is None:
        await update.message.reply_text(
            "Set a project first.",
            reply_markup=_reply_keyboard(context),
        )
        return MAIN_MENU

    project = _project(context)
    await update.message.reply_text("Transcribing...")

    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        tmp_path = Path(tmp.name)
        await file.download_to_drive(str(tmp_path))

    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file
            )
        text = transcript.text
    except Exception as exc:
        logger.error("Whisper transcription failed: %s", exc)
        await update.message.reply_text(f"Transcription failed: {exc}")
        return MAIN_MENU
    finally:
        tmp_path.unlink(missing_ok=True)

    # Save transcript
    date_str = datetime.now().strftime(config.DATE_FORMAT)
    corr_dir = pp / "correspondence"
    corr_dir.mkdir(exist_ok=True)

    base = f"{date_str}_voice-note"
    md_path = corr_dir / f"{base}.md"
    counter = 2
    while md_path.exists():
        md_path = corr_dir / f"{base}-{counter}.md"
        counter += 1

    content = f"# Voice Note -- {date_str}\n\n{text}\n"
    md_path.write_text(content)
    logger.info("Voice transcript saved: %s", md_path)

    committed = _git_commit(pp, md_path, f"Add voice transcript: {md_path.name}")

    # DB logging
    visit_id = _visit_id(context)
    db.log_voice(project, str(md_path), text, visit_id)

    status = "transcribed + committed" if committed else "transcribed (git commit failed)"
    await update.message.reply_text(
        f"{status}: correspondence/{md_path.name}",
        reply_markup=_reply_keyboard(context),
    )
    await _send_long(update, text)
    return MAIN_MENU


# ---------------------------------------------------------------------------
# Document handler (files sent via Telegram)
# ---------------------------------------------------------------------------


MAX_FILE_SIZE_MB = 100
BLOCKED_EXTENSIONS = {".exe", ".bat", ".cmd", ".ps1", ".sh"}


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save any document sent via Telegram to the project and log in DB."""
    pp = _project_path(context)
    if pp is None:
        await update.message.reply_text(
            "Set a project first.",
            reply_markup=_reply_keyboard(context),
        )
        return MAIN_MENU

    project = _project(context)
    doc = update.message.document

    # File size check
    if doc.file_size and doc.file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        db.log_event("file_rejected", f"Too large: {doc.file_size} bytes", project)
        await update.message.reply_text(
            f"File too large (max {MAX_FILE_SIZE_MB}MB).",
            reply_markup=_reply_keyboard(context),
        )
        return MAIN_MENU

    original_name = doc.file_name or "document"

    # Dangerous extension check
    ext = Path(original_name).suffix.lower()
    if ext in BLOCKED_EXTENSIONS:
        db.log_event("file_rejected", f"Blocked extension: {ext}", project)
        await update.message.reply_text(
            f"File type {ext} not allowed.",
            reply_markup=_reply_keyboard(context),
        )
        return MAIN_MENU

    date_str = datetime.now().strftime(config.DATE_FORMAT)

    # Determine destination based on file type
    ext = Path(original_name).suffix.lower()
    if ext in (".png", ".jpg", ".jpeg", ".heic", ".heif", ".gif", ".bmp"):
        subdir = "pics"
    elif ext in (".csv", ".txt", ".log", ".json", ".xml", ".pcap"):
        subdir = "docs/network"
    else:
        subdir = "docs"

    dest_dir = pp / subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    safe_name = _safe_filename(Path(original_name).stem)
    dest = dest_dir / f"{date_str}-{safe_name}{ext}"

    file = await context.bot.get_file(doc.file_id)
    await file.download_to_drive(str(dest))
    logger.info("Document saved: %s", dest)

    committed = _git_commit(pp, dest, f"Add document: {dest.name}")

    # Log as a scan if it's a network-type file
    visit_id = _visit_id(context)
    if subdir == "docs/network":
        db.log_scan(project, "file", str(dest), visit_id=visit_id)
    else:
        db.log_event("document_saved", str(dest), project)

    status = "saved + committed" if committed else "saved (git commit failed)"
    await update.message.reply_text(
        f"Document {status}: {subdir}/{dest.name}",
        reply_markup=_reply_keyboard(context),
    )
    return MAIN_MENU


# ---------------------------------------------------------------------------
# Reply keyboard text handler (routes persistent keyboard taps)
# ---------------------------------------------------------------------------


async def reply_keyboard_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle persistent reply keyboard button presses."""
    text = update.message.text.strip().lower()

    if text in ("menu", "0", "/start"):
        return await cmd_start(update, context)

    if text == "status":
        return await _status_text_handler(update, context)

    if text == "projects":
        return await _projects_text_handler(update, context)

    if text == "quick note":
        await update.message.reply_text("Type your quick note:")
        return QUICK_NOTE

    if text == "end visit":
        return await _end_visit_text(update, context)

    if text == "start task":
        return await _start_task_text(update, context)

    # Fallback: treat as quick note if in visit
    if _visit_id(context):
        return await quick_note_text(update, context)

    # Outside visit: offer to save as quick note if project is set
    project = _project(context)
    if project:
        context.user_data["pending_note"] = update.message.text.strip()
        await update.message.reply_text(
            f'Save as quick note to {project}?',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Yes, save", callback_data="save_as_note")],
                [InlineKeyboardButton("No, cancel", callback_data="noop")],
            ]),
        )
        return MAIN_MENU

    # No project set
    await update.message.reply_text(
        "Set a project first to save notes.",
        reply_markup=menus.main_menu_keyboard(),
    )
    return MAIN_MENU


async def _status_text_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle 'Status' from reply keyboard."""
    project = _project(context)
    if not project:
        await update.message.reply_text(
            "No active project.", reply_markup=_reply_keyboard(context)
        )
        return MAIN_MENU

    pp = config.PROJECTS_DIR / project
    lines = [f"Status for {project}:"]

    status_file = pp / "STATUS.md"
    if status_file.exists():
        content = status_file.read_text().strip()
        if content:
            if len(content) > 2000:
                content = content[:2000] + "\n... (truncated)"
            lines.append(f"\n{content}")
    else:
        lines.append("No STATUS.md found.")

    stats = db.project_stats(project)
    lines.append(
        f"\nDB: {stats['photos']} photos, {stats['voice_notes']} voice notes, "
        f"{stats['quick_notes']} notes, {stats['visits']} visits, "
        f"{stats['scans']} scans, {stats['total_task_hours']}h tracked"
    )

    # Active task info
    active_task = db.get_active_task(project)
    if active_task:
        lines.append(f"\nActive task: {active_task['description']} (since {active_task['started_at'][:16]})")

    await _send_long(update, "\n".join(lines), reply_markup=_reply_keyboard(context))
    return MAIN_MENU


async def _projects_text_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle 'Projects' from reply keyboard -- show as inline buttons."""
    projects = _list_projects()
    if not projects:
        await update.message.reply_text("No projects found.")
        return MAIN_MENU

    keyboard = menus.project_list_keyboard(projects, 0, _project(context))
    await update.message.reply_text("Select a project:", reply_markup=keyboard)
    return SELECT_PROJECT


async def _end_visit_text(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle 'End visit' from reply keyboard."""
    visit_id = _visit_id(context)
    if not visit_id:
        await update.message.reply_text(
            "No active visit.", reply_markup=_reply_keyboard(context)
        )
        return MAIN_MENU

    summary_data = db.end_visit(visit_id)
    context.user_data["active_visit_id"] = None

    if summary_data:
        pp = _project_path(context)
        if pp and pp.exists():
            docs_dir = pp / "docs" / "site-visits"
            docs_dir.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime(config.DATE_FORMAT)
            summary_file = docs_dir / f"{date_str}-visit-{visit_id}.md"
            md_content = (
                f"# Site Visit -- {summary_data['project']}\n\n"
                f"**Date:** {summary_data['started_at'][:10]}\n"
                f"**Location:** {summary_data['location'] or 'Not set'}\n"
                f"**Duration:** {summary_data['duration']}\n\n"
                f"## Summary\n\n"
                f"- Photos: {summary_data['photo_count']}\n"
                f"- Voice notes: {summary_data['voice_count']}\n"
                f"- Quick notes: {summary_data['note_count']}\n"
                f"- Tasks: {summary_data['task_count']}\n"
                f"- Network scans: {summary_data['scan_count']}\n"
            )
            if summary_data["notes"]:
                md_content += f"\n## Notes\n\n{summary_data['notes']}\n"
            summary_file.write_text(md_content)
            _git_commit(pp, summary_file, f"Add site visit summary: {summary_file.name}")

        await update.message.reply_text(
            f"Visit ended.\n\n{summary_data['summary']}",
            reply_markup=menus.default_reply_keyboard(),
        )
    else:
        await update.message.reply_text(
            "Visit ended.", reply_markup=menus.default_reply_keyboard()
        )

    return MAIN_MENU


async def _start_task_text(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle 'Start task' from reply keyboard."""
    project = _project(context)
    if not project:
        await update.message.reply_text(
            "Set a project first.", reply_markup=_reply_keyboard(context)
        )
        return MAIN_MENU

    active = _task_id(context)
    if active:
        task = db.get_active_task(project)
        if task:
            await update.message.reply_text(
                f"Task already running: {task['description']}\n"
                f"Started: {task['started_at']}",
                reply_markup=menus.finish_task_keyboard(active),
            )
            return MAIN_MENU

    await update.message.reply_text("Describe the task:")
    return TASK_DESCRIPTION


# ---------------------------------------------------------------------------
# Legacy slash commands (still work as fallbacks)
# ---------------------------------------------------------------------------


async def cmd_project(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /project <name> -- set active project with fuzzy matching."""
    if not context.args:
        if _project(context):
            await update.message.reply_text(
                f"Active project: {_project(context)}",
                reply_markup=_reply_keyboard(context),
            )
        else:
            await update.message.reply_text(
                "No active project. Usage: /project <name>",
                reply_markup=_reply_keyboard(context),
            )
        return MAIN_MENU

    query = " ".join(context.args)
    match = _fuzzy_match_project(query)

    if match is None:
        await update.message.reply_text(
            f"No unique match for '{query}'. Try /projects or tap Projects.",
            reply_markup=_reply_keyboard(context),
        )
        return MAIN_MENU

    context.user_data["active_project"] = match
    db.log_event("project_switched", match)
    await update.message.reply_text(
        f"Active project: {match}",
        reply_markup=_reply_keyboard(context),
    )
    return MAIN_MENU


async def cmd_projects(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /projects -- list projects as inline buttons."""
    return await _projects_text_handler(update, context)


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /status."""
    return await _status_text_handler(update, context)


async def cmd_visit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /visit -- start or check visit status."""
    visit_id = _visit_id(context)
    if visit_id:
        visit = db.get_active_visit(_project(context))
        if visit:
            loc = visit.get("location") or "no location"
            await update.message.reply_text(
                f"Visit in progress: {visit['project']} ({loc})\n"
                f"Started: {visit['started_at']}",
                reply_markup=menus.end_visit_keyboard(),
            )
            return MAIN_MENU

    project = _project(context)
    if not project:
        await update.message.reply_text("Set a project first.")
        return MAIN_MENU

    await update.message.reply_text(
        f"Start visit for {project}?",
        reply_markup=menus.visit_confirm_keyboard(project),
    )
    return VISIT_LOCATION


async def cmd_endvisit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /endvisit."""
    return await _end_visit_text(update, context)


async def cmd_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /task -- start or check task status."""
    return await _start_task_text(update, context)


async def cmd_endtask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /endtask."""
    task_id = _task_id(context)
    if not task_id:
        await update.message.reply_text(
            "No active task.", reply_markup=_reply_keyboard(context)
        )
        return MAIN_MENU

    result = db.end_task(task_id)
    context.user_data["active_task_id"] = None

    if result:
        await update.message.reply_text(
            f"Task finished: {result['description']}\n"
            f"Duration: {result['duration_minutes']:.0f} minutes",
            reply_markup=_reply_keyboard(context),
        )
    else:
        await update.message.reply_text(
            "Task finished.", reply_markup=_reply_keyboard(context)
        )
    return MAIN_MENU


async def cmd_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /search <query>."""
    if not context.args:
        await update.message.reply_text("Usage: /search <keyword>")
        return MAIN_MENU

    query_text = " ".join(context.args)
    # Reuse the search logic
    update.message.text = query_text
    return await search_query_text(update, context)


async def cmd_recent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /recent -- show recent activity."""
    events = db.recent_activity(15)
    if not events:
        await update.message.reply_text(
            "No recent activity.", reply_markup=_reply_keyboard(context)
        )
        return MAIN_MENU

    lines = ["Recent activity:\n"]
    for e in events:
        project_tag = f" [{e['project']}]" if e["project"] else ""
        lines.append(f"{e['created_at'][:16]} {e['event_type']}{project_tag}")
        if e["detail"]:
            lines.append(f"  {e['detail'][:80]}")

    await _send_long(update, "\n".join(lines), reply_markup=_reply_keyboard(context))
    return MAIN_MENU


async def cmd_visits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /visits -- show visit history."""
    project = _project(context)
    visits = db.visit_history(project, limit=10)

    if not visits:
        await update.message.reply_text(
            "No visit history.", reply_markup=_reply_keyboard(context)
        )
        return MAIN_MENU

    lines = ["Visit history:\n"]
    for v in visits:
        status = "active" if not v["ended_at"] else "completed"
        loc = v["location"] or "no location"
        lines.append(f"#{v['id']} [{v['project']}] {v['started_at'][:16]} ({loc}) -- {status}")
        if v["summary"]:
            lines.append(f"  {v['summary'][:80]}")

    await _send_long(update, "\n".join(lines), reply_markup=_reply_keyboard(context))
    return MAIN_MENU


# ---------------------------------------------------------------------------
# Daily reminders
# ---------------------------------------------------------------------------


async def morning_briefing(context: ContextTypes.DEFAULT_TYPE):
    """7:30 AM SAST daily briefing."""
    if not context.bot_data.get("reminders_enabled", True):
        return

    # Use stored project or skip
    project = context.bot_data.get("reminder_project")
    if not project:
        return

    stats = db.project_stats(project)
    active_task = db.get_active_task(project)
    active_visit = db.get_active_visit(project)

    # Recent activity from last 24 hours
    events = db.recent_activity(limit=20)
    yesterday = (datetime.now() - timedelta(hours=24)).isoformat()
    recent = [e for e in events if e["created_at"] >= yesterday]

    lines = [f"Good morning. Daily briefing for {project}:\n"]
    lines.append(
        f"Photos: {stats['photos']}, Voice notes: {stats['voice_notes']}, "
        f"Notes: {stats['quick_notes']}, Visits: {stats['visits']}, "
        f"Scans: {stats['scans']}, Time tracked: {stats['total_task_hours']}h"
    )

    if active_task:
        lines.append(f"\nActive task: {active_task['description']} (started {active_task['started_at'][:16]})")
    if active_visit:
        loc = active_visit.get("location") or "no location"
        lines.append(f"\nVisit in progress: {loc} (started {active_visit['started_at'][:16]})")

    if recent:
        lines.append(f"\nLast 24h: {len(recent)} events")
    else:
        lines.append("\nNo activity in the last 24 hours.")

    await context.bot.send_message(
        chat_id=config.ALLOWED_USER_ID,
        text="\n".join(lines),
    )


async def afternoon_wrapup(context: ContextTypes.DEFAULT_TYPE):
    """4:30 PM SAST afternoon wrap-up."""
    if not context.bot_data.get("reminders_enabled", True):
        return

    project = context.bot_data.get("reminder_project")
    if not project:
        return

    stats = db.project_stats(project)
    active_task = db.get_active_task(project)

    # Today's activity
    events = db.recent_activity(limit=30)
    today = datetime.now().strftime("%Y-%m-%d")
    todays = [e for e in events if e["created_at"].startswith(today)]

    lines = [f"Afternoon wrap-up for {project}:\n"]

    if todays:
        lines.append(f"Today: {len(todays)} events")
        for e in todays[:10]:
            tag = f" [{e['project']}]" if e["project"] and e["project"] != project else ""
            lines.append(f"  {e['created_at'][11:16]} {e['event_type']}{tag}")
    else:
        lines.append("No activity today.")

    if active_task:
        lines.append(f"\nReminder: task still running -- {active_task['description']}")

    # Visit summaries from today
    visits = db.visit_history(project, limit=5)
    todays_visits = [v for v in visits if v["started_at"].startswith(today)]
    if todays_visits:
        lines.append(f"\nVisits today: {len(todays_visits)}")
        for v in todays_visits:
            loc = v["location"] or "no location"
            status = "active" if not v["ended_at"] else "completed"
            lines.append(f"  {loc} -- {status}")

    await context.bot.send_message(
        chat_id=config.ALLOWED_USER_ID,
        text="\n".join(lines),
    )


async def cmd_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /reminders -- toggle daily reminders on/off."""
    current = context.bot_data.get("reminders_enabled", True)

    # Toggle
    context.bot_data["reminders_enabled"] = not current
    new_state = "on" if not current else "off"

    # Store current project for reminders
    project = _project(context)
    if project and not current:
        context.bot_data["reminder_project"] = project

    await update.message.reply_text(
        f"Daily reminders: {new_state}"
        + (f" (project: {project})" if project and not current else ""),
        reply_markup=_reply_keyboard(context),
    )
    return MAIN_MENU


# ---------------------------------------------------------------------------
# Fallback / cancel
# ---------------------------------------------------------------------------


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /cancel -- return to main menu."""
    await update.message.reply_text(
        "Cancelled.", reply_markup=_reply_keyboard(context)
    )
    return MAIN_MENU
