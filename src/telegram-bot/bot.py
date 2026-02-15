#!/usr/bin/env python3
"""Precept Telegram Bot -- photo filing, voice transcription, menu UX, site visits.

Runs on the dev server (10.0.10.21) as a systemd user service.
Single-user bot: silently ignores messages from unauthorized users.
"""

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import config
import db
import handlers
import menus

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("precept-bot")


# ---------------------------------------------------------------------------
# Auth filter -- rejects unauthorized users at the filter level
# ---------------------------------------------------------------------------


class AuthFilter(filters.MessageFilter):
    """Only allow messages from the configured user."""

    def filter(self, message):
        if message.from_user is None:
            return False
        return message.from_user.id == config.ALLOWED_USER_ID


AUTH = AuthFilter()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    config.validate()

    # Initialise SQLite database
    db.init_db()

    logger.info(
        "Starting Precept Bot (user whitelist: %s, projects: %s, db: %s)",
        config.ALLOWED_USER_ID,
        config.PROJECTS_DIR,
        config.DB_PATH,
    )

    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # The ConversationHandler manages all state transitions
    conv = ConversationHandler(
        entry_points=[
            CommandHandler(["start", "help", "menu"], handlers.cmd_start, AUTH),
        ],
        states={
            handlers.MAIN_MENU: [
                # Inline button callbacks
                CallbackQueryHandler(handlers.menu_callback, pattern=f"^{menus.MENU_CB}"),
                CallbackQueryHandler(handlers.visit_callback, pattern=f"^{menus.VISIT_CB}"),
                CallbackQueryHandler(handlers.task_callback, pattern=f"^{menus.TASK_CB}"),
                CallbackQueryHandler(handlers.project_callback, pattern=f"^({menus.PROJECT_CB}|{menus.PAGE_CB})"),
                CallbackQueryHandler(lambda u, c: handlers.MAIN_MENU, pattern="^noop$"),
                # Slash commands (legacy fallbacks)
                CommandHandler("project", handlers.cmd_project, AUTH),
                CommandHandler("projects", handlers.cmd_projects, AUTH),
                CommandHandler("status", handlers.cmd_status, AUTH),
                CommandHandler("visit", handlers.cmd_visit, AUTH),
                CommandHandler("endvisit", handlers.cmd_endvisit, AUTH),
                CommandHandler("task", handlers.cmd_task, AUTH),
                CommandHandler("endtask", handlers.cmd_endtask, AUTH),
                CommandHandler("search", handlers.cmd_search, AUTH),
                CommandHandler("recent", handlers.cmd_recent, AUTH),
                CommandHandler("visits", handlers.cmd_visits, AUTH),
                CommandHandler("cancel", handlers.cancel, AUTH),
                # Media handlers
                MessageHandler(AUTH & filters.PHOTO, handlers.handle_photo),
                MessageHandler(AUTH & filters.VOICE, handlers.handle_voice),
                MessageHandler(AUTH & filters.Document.ALL, handlers.handle_document),
                # Reply keyboard text
                MessageHandler(AUTH & filters.TEXT & ~filters.COMMAND, handlers.reply_keyboard_handler),
            ],
            handlers.SELECT_PROJECT: [
                CallbackQueryHandler(handlers.project_callback, pattern=f"^({menus.PROJECT_CB}|{menus.PAGE_CB}|{menus.MENU_CB})"),
                CallbackQueryHandler(lambda u, c: handlers.MAIN_MENU, pattern="^noop$"),
                CommandHandler("cancel", handlers.cancel, AUTH),
                # Allow typing a project name too
                MessageHandler(AUTH & filters.TEXT & ~filters.COMMAND, handlers.project_name_text),
            ],
            handlers.VISIT_LOCATION: [
                CallbackQueryHandler(handlers.visit_callback, pattern=f"^{menus.VISIT_CB}"),
                CallbackQueryHandler(handlers.project_callback, pattern=f"^({menus.PROJECT_CB}|{menus.PAGE_CB}|{menus.MENU_CB})"),
                MessageHandler(AUTH & filters.LOCATION, handlers.visit_location_gps),
                MessageHandler(AUTH & filters.TEXT & ~filters.COMMAND, handlers.visit_location_text),
                CommandHandler("cancel", handlers.cancel, AUTH),
            ],
            handlers.VISIT_ACTIVE: [
                CallbackQueryHandler(handlers.visit_callback, pattern=f"^{menus.VISIT_CB}"),
                CallbackQueryHandler(handlers.menu_callback, pattern=f"^{menus.MENU_CB}"),
                CommandHandler("cancel", handlers.cancel, AUTH),
                MessageHandler(AUTH & filters.TEXT & ~filters.COMMAND, handlers.reply_keyboard_handler),
            ],
            handlers.TASK_DESCRIPTION: [
                MessageHandler(AUTH & filters.TEXT & ~filters.COMMAND, handlers.task_description_text),
                CommandHandler("cancel", handlers.cancel, AUTH),
            ],
            handlers.SEARCH_QUERY: [
                MessageHandler(AUTH & filters.TEXT & ~filters.COMMAND, handlers.search_query_text),
                CommandHandler("cancel", handlers.cancel, AUTH),
            ],
            handlers.QUICK_NOTE: [
                MessageHandler(AUTH & filters.TEXT & ~filters.COMMAND, handlers.quick_note_text),
                CommandHandler("cancel", handlers.cancel, AUTH),
            ],
        },
        fallbacks=[
            CommandHandler(["start", "help", "menu"], handlers.cmd_start, AUTH),
            CommandHandler("cancel", handlers.cancel, AUTH),
            # Always handle media even outside conversation states
            MessageHandler(AUTH & filters.PHOTO, handlers.handle_photo),
            MessageHandler(AUTH & filters.VOICE, handlers.handle_voice),
            MessageHandler(AUTH & filters.Document.ALL, handlers.handle_document),
        ],
        per_user=True,
        per_chat=True,
    )

    app.add_handler(conv)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
