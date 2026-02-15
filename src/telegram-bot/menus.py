"""Keyboard builders for the Precept Bot menu system.

Builds InlineKeyboardMarkup and ReplyKeyboardMarkup for tap-friendly UX.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

import config

# ---------------------------------------------------------------------------
# Callback data prefixes
# ---------------------------------------------------------------------------

# Prefixes for callback_data parsing
PROJECT_CB = "proj:"
PAGE_CB = "page:"
MENU_CB = "menu:"
VISIT_CB = "visit:"
TASK_CB = "task:"

# Menu actions
MENU_SWITCH_PROJECT = f"{MENU_CB}switch_project"
MENU_STATUS = f"{MENU_CB}status"
MENU_START_VISIT = f"{MENU_CB}start_visit"
MENU_QUICK_NOTE = f"{MENU_CB}quick_note"
MENU_START_TASK = f"{MENU_CB}start_task"
MENU_SEARCH = f"{MENU_CB}search"
MENU_RECENT = f"{MENU_CB}recent"
MENU_MAIN = f"{MENU_CB}main"
MENU_NEW_PROJECT = f"{MENU_CB}new_project"

# Visit actions
VISIT_CONFIRM = f"{VISIT_CB}confirm"
VISIT_SWITCH_FIRST = f"{VISIT_CB}switch_first"
VISIT_SKIP_LOCATION = f"{VISIT_CB}skip_location"
VISIT_END = f"{VISIT_CB}end"
VISIT_END_CONFIRM = f"{VISIT_CB}end_confirm"

# Task actions
TASK_FINISH = f"{TASK_CB}finish"

PROJECTS_PER_PAGE = 6


# ---------------------------------------------------------------------------
# Inline keyboards
# ---------------------------------------------------------------------------


def main_menu_keyboard(active_project: str | None = None) -> InlineKeyboardMarkup:
    """Build the main menu inline keyboard."""
    buttons = [
        [
            InlineKeyboardButton("Switch project", callback_data=MENU_SWITCH_PROJECT),
            InlineKeyboardButton("Status", callback_data=MENU_STATUS),
        ],
        [
            InlineKeyboardButton("Start site visit", callback_data=MENU_START_VISIT),
            InlineKeyboardButton("Quick note", callback_data=MENU_QUICK_NOTE),
        ],
        [
            InlineKeyboardButton("Start task", callback_data=MENU_START_TASK),
            InlineKeyboardButton("Search transcripts", callback_data=MENU_SEARCH),
        ],
        [
            InlineKeyboardButton("Recent activity", callback_data=MENU_RECENT),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def project_list_keyboard(
    projects: list[str],
    page: int = 0,
    active_project: str | None = None,
) -> InlineKeyboardMarkup:
    """Build a paginated project selection keyboard.

    Most-recently-used (active) project is shown first.
    """
    # Put active project first if it exists
    if active_project and active_project in projects:
        projects = [active_project] + [p for p in projects if p != active_project]

    total_pages = max(1, (len(projects) + PROJECTS_PER_PAGE - 1) // PROJECTS_PER_PAGE)
    page = max(0, min(page, total_pages - 1))

    start = page * PROJECTS_PER_PAGE
    page_items = projects[start : start + PROJECTS_PER_PAGE]

    # Two columns of project buttons
    rows = []
    for i in range(0, len(page_items), 2):
        row = []
        for p in page_items[i : i + 2]:
            label = f">> {p}" if p == active_project else p
            row.append(InlineKeyboardButton(label, callback_data=f"{PROJECT_CB}{p}"))
        rows.append(row)

    # Pagination row
    if total_pages > 1:
        nav = []
        if page > 0:
            nav.append(InlineKeyboardButton("<< Prev", callback_data=f"{PAGE_CB}{page - 1}"))
        nav.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"))
        if page < total_pages - 1:
            nav.append(InlineKeyboardButton("Next >>", callback_data=f"{PAGE_CB}{page + 1}"))
        rows.append(nav)

    # New project + back to menu
    rows.append([
        InlineKeyboardButton("+ New project", callback_data=MENU_NEW_PROJECT),
        InlineKeyboardButton("<< Back", callback_data=MENU_MAIN),
    ])

    return InlineKeyboardMarkup(rows)


def visit_confirm_keyboard(project: str) -> InlineKeyboardMarkup:
    """Confirm starting a visit for the active project."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"Yes, visit {project}", callback_data=VISIT_CONFIRM
                ),
            ],
            [
                InlineKeyboardButton(
                    "Switch project first", callback_data=VISIT_SWITCH_FIRST
                ),
            ],
        ]
    )


def visit_location_keyboard() -> InlineKeyboardMarkup:
    """Options for setting visit location."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Skip location", callback_data=VISIT_SKIP_LOCATION),
            ],
        ]
    )


def end_visit_keyboard() -> InlineKeyboardMarkup:
    """Confirm ending the current visit."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("End visit now", callback_data=VISIT_END_CONFIRM),
            ],
            [
                InlineKeyboardButton("<< Back", callback_data=MENU_MAIN),
            ],
        ]
    )


def finish_task_keyboard(task_id: int) -> InlineKeyboardMarkup:
    """Button to finish the active task."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Finish task", callback_data=TASK_FINISH),
            ],
        ]
    )


# ---------------------------------------------------------------------------
# Reply keyboards (persistent bottom buttons)
# ---------------------------------------------------------------------------


def default_reply_keyboard() -> ReplyKeyboardMarkup:
    """Default persistent keyboard shown when no visit is active."""
    return ReplyKeyboardMarkup(
        [["Menu", "Status"], ["Projects", "Quick note"]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def visit_reply_keyboard() -> ReplyKeyboardMarkup:
    """Persistent keyboard shown during an active site visit."""
    return ReplyKeyboardMarkup(
        [["Quick note", "End visit"], ["Start task", "Status"]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
