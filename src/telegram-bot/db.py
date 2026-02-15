"""SQLite database for Precept Bot -- persistent logging and state.

Database at ~/.config/precept/precept.db (auto-created on first startup).
Migrations are numbered SQL blocks applied in order.
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import config

logger = logging.getLogger("precept-bot.db")

# ---------------------------------------------------------------------------
# Migrations
# ---------------------------------------------------------------------------

MIGRATIONS = [
    # Migration 1: initial schema
    """
    CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT NOT NULL,
        caption TEXT,
        filepath TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        visit_id INTEGER,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );

    CREATE TABLE IF NOT EXISTS voice_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT NOT NULL,
        filepath TEXT NOT NULL,
        transcript TEXT,
        visit_id INTEGER,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );

    CREATE TABLE IF NOT EXISTS site_visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT NOT NULL,
        location TEXT,
        latitude REAL,
        longitude REAL,
        started_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        ended_at TEXT,
        notes TEXT,
        summary TEXT
    );

    CREATE TABLE IF NOT EXISTS network_scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT NOT NULL,
        scan_type TEXT NOT NULL,
        filepath TEXT,
        raw_output TEXT,
        visit_id INTEGER,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );

    CREATE TABLE IF NOT EXISTS bot_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        detail TEXT,
        project TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );

    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT NOT NULL,
        description TEXT NOT NULL,
        started_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        ended_at TEXT,
        duration_minutes REAL,
        visit_id INTEGER
    );
    """,
]


# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------


def _get_conn() -> sqlite3.Connection:
    """Open a connection to the database."""
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(config.DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Run any unapplied migrations. Called once at bot startup."""
    conn = _get_conn()
    try:
        # Ensure schema_version table exists for the very first run
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_version "
            "(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)"
        )
        conn.commit()

        applied = {
            row[0]
            for row in conn.execute("SELECT version FROM schema_version").fetchall()
        }

        for i, sql in enumerate(MIGRATIONS, start=1):
            if i not in applied:
                logger.info("Applying migration %d", i)
                conn.executescript(sql)
                conn.execute(
                    "INSERT INTO schema_version (version, applied_at) VALUES (?, ?)",
                    (i, datetime.now().isoformat()),
                )
                conn.commit()
                logger.info("Migration %d applied", i)

        logger.info(
            "Database ready at %s (%d migrations applied)",
            config.DB_PATH,
            len(applied | set(range(1, len(MIGRATIONS) + 1))),
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------


def log_photo(
    project: str,
    filepath: str,
    caption: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    visit_id: int | None = None,
) -> int:
    """Log a photo and return its row id."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO photos (project, filepath, caption, latitude, longitude, visit_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (project, filepath, caption, latitude, longitude, visit_id),
        )
        conn.commit()
        log_event("photo_saved", f"{filepath}", project)
        return cur.lastrowid
    finally:
        conn.close()


def log_voice(
    project: str,
    filepath: str,
    transcript: str | None = None,
    visit_id: int | None = None,
) -> int:
    """Log a voice note and return its row id."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO voice_notes (project, filepath, transcript, visit_id) "
            "VALUES (?, ?, ?, ?)",
            (project, filepath, transcript, visit_id),
        )
        conn.commit()
        log_event("voice_saved", f"{filepath}", project)
        return cur.lastrowid
    finally:
        conn.close()


def log_event(
    event_type: str, detail: str | None = None, project: str | None = None
) -> int:
    """Log a bot event and return its row id."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO bot_events (event_type, detail, project) VALUES (?, ?, ?)",
            (event_type, detail, project),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Site visits
# ---------------------------------------------------------------------------


def start_visit(
    project: str,
    location: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> int:
    """Start a site visit and return the visit id."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO site_visits (project, location, latitude, longitude) "
            "VALUES (?, ?, ?, ?)",
            (project, location, latitude, longitude),
        )
        conn.commit()
        log_event("visit_started", location or "no location", project)
        return cur.lastrowid
    finally:
        conn.close()


def end_visit(visit_id: int, notes: str | None = None) -> dict | None:
    """End a site visit and return a summary dict."""
    conn = _get_conn()
    try:
        visit = conn.execute(
            "SELECT * FROM site_visits WHERE id = ?", (visit_id,)
        ).fetchone()
        if not visit:
            return None

        now = datetime.now().isoformat()

        # Count items captured during this visit
        photo_count = conn.execute(
            "SELECT COUNT(*) FROM photos WHERE visit_id = ?", (visit_id,)
        ).fetchone()[0]
        voice_count = conn.execute(
            "SELECT COUNT(*) FROM voice_notes WHERE visit_id = ?", (visit_id,)
        ).fetchone()[0]
        task_count = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE visit_id = ?", (visit_id,)
        ).fetchone()[0]
        scan_count = conn.execute(
            "SELECT COUNT(*) FROM network_scans WHERE visit_id = ?", (visit_id,)
        ).fetchone()[0]

        # Calculate duration
        started = datetime.fromisoformat(visit["started_at"])
        ended = datetime.fromisoformat(now)
        duration = ended - started
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes = remainder // 60

        summary = (
            f"Visit to {visit['project']}"
            f"{' at ' + visit['location'] if visit['location'] else ''}\n"
            f"Duration: {hours}h {minutes}m\n"
            f"Photos: {photo_count}, Voice notes: {voice_count}, "
            f"Tasks: {task_count}, Scans: {scan_count}"
        )
        if notes:
            summary += f"\nNotes: {notes}"

        conn.execute(
            "UPDATE site_visits SET ended_at = ?, notes = ?, summary = ? WHERE id = ?",
            (now, notes, summary, visit_id),
        )
        conn.commit()
        log_event("visit_ended", summary, visit["project"])

        return {
            "visit_id": visit_id,
            "project": visit["project"],
            "location": visit["location"],
            "started_at": visit["started_at"],
            "ended_at": now,
            "duration": f"{hours}h {minutes}m",
            "photo_count": photo_count,
            "voice_count": voice_count,
            "task_count": task_count,
            "scan_count": scan_count,
            "notes": notes,
            "summary": summary,
        }
    finally:
        conn.close()


def get_active_visit(project: str) -> dict | None:
    """Return the active (unended) visit for a project, or None."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM site_visits WHERE project = ? AND ended_at IS NULL "
            "ORDER BY started_at DESC LIMIT 1",
            (project,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Tasks (time tracking)
# ---------------------------------------------------------------------------


def start_task(
    project: str, description: str, visit_id: int | None = None
) -> int:
    """Start a timed task and return its id."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO tasks (project, description, visit_id) VALUES (?, ?, ?)",
            (project, description, visit_id),
        )
        conn.commit()
        log_event("task_started", description, project)
        return cur.lastrowid
    finally:
        conn.close()


def end_task(task_id: int) -> dict | None:
    """End a task and return its details including duration."""
    conn = _get_conn()
    try:
        task = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if not task:
            return None

        now = datetime.now().isoformat()
        started = datetime.fromisoformat(task["started_at"])
        ended = datetime.fromisoformat(now)
        duration = ended - started
        duration_minutes = duration.total_seconds() / 60

        conn.execute(
            "UPDATE tasks SET ended_at = ?, duration_minutes = ? WHERE id = ?",
            (now, duration_minutes, task_id),
        )
        conn.commit()
        log_event("task_ended", f"{task['description']} ({duration_minutes:.0f}m)", task["project"])

        return {
            "task_id": task_id,
            "project": task["project"],
            "description": task["description"],
            "started_at": task["started_at"],
            "ended_at": now,
            "duration_minutes": duration_minutes,
        }
    finally:
        conn.close()


def get_active_task(project: str) -> dict | None:
    """Return the active (unfinished) task for a project, or None."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM tasks WHERE project = ? AND ended_at IS NULL "
            "ORDER BY started_at DESC LIMIT 1",
            (project,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Network scans
# ---------------------------------------------------------------------------


def log_scan(
    project: str,
    scan_type: str,
    filepath: str | None = None,
    raw_output: str | None = None,
    visit_id: int | None = None,
) -> int:
    """Log a network scan and return its row id."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO network_scans (project, scan_type, filepath, raw_output, visit_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (project, scan_type, filepath, raw_output, visit_id),
        )
        conn.commit()
        log_event("scan_logged", f"{scan_type}: {filepath or 'inline'}", project)
        return cur.lastrowid
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------


def search_transcripts(query: str, limit: int = 10) -> list[dict]:
    """Search voice note transcripts for a keyword."""
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT id, project, filepath, transcript, created_at FROM voice_notes "
            "WHERE transcript LIKE ? ORDER BY created_at DESC LIMIT ?",
            (f"%{query}%", limit),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def recent_activity(limit: int = 20) -> list[dict]:
    """Return recent bot events."""
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM bot_events ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def visit_history(project: str | None = None, limit: int = 10) -> list[dict]:
    """Return visit history, optionally filtered by project."""
    conn = _get_conn()
    try:
        if project:
            rows = conn.execute(
                "SELECT * FROM site_visits WHERE project = ? "
                "ORDER BY started_at DESC LIMIT ?",
                (project, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM site_visits ORDER BY started_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def project_stats(project: str) -> dict:
    """Return aggregate stats for a project."""
    conn = _get_conn()
    try:
        photos = conn.execute(
            "SELECT COUNT(*) FROM photos WHERE project = ?", (project,)
        ).fetchone()[0]
        voices = conn.execute(
            "SELECT COUNT(*) FROM voice_notes WHERE project = ?", (project,)
        ).fetchone()[0]
        visits = conn.execute(
            "SELECT COUNT(*) FROM site_visits WHERE project = ?", (project,)
        ).fetchone()[0]
        scans = conn.execute(
            "SELECT COUNT(*) FROM network_scans WHERE project = ?", (project,)
        ).fetchone()[0]
        total_task_mins = conn.execute(
            "SELECT COALESCE(SUM(duration_minutes), 0) FROM tasks "
            "WHERE project = ? AND ended_at IS NOT NULL",
            (project,),
        ).fetchone()[0]
        return {
            "photos": photos,
            "voice_notes": voices,
            "visits": visits,
            "scans": scans,
            "total_task_hours": round(total_task_mins / 60, 1),
        }
    finally:
        conn.close()
