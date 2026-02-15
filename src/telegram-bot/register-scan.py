#!/usr/bin/env python3
"""Register a network scan in the Precept SQLite database.

Called by precept-scan.sh on the laptop via SSH:
    python3 register-scan.py <project> <scan_type> <filepath> [raw_output]

Can also read raw output from stdin if not provided as argument.
"""

import sys
from pathlib import Path

# Add the telegram-bot directory to path so we can import db and config
sys.path.insert(0, str(Path(__file__).parent))

import config
import db


def main():
    if len(sys.argv) < 4:
        print("Usage: register-scan.py <project> <scan_type> <filepath> [raw_output]", file=sys.stderr)
        sys.exit(1)

    project = sys.argv[1]
    scan_type = sys.argv[2]
    filepath = sys.argv[3]
    raw_output = sys.argv[4] if len(sys.argv) > 4 else None

    # Validate project name
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+$', project):
        print(f"Invalid project name: {project}", file=sys.stderr)
        sys.exit(1)

    # Validate filepath stays within project directory
    project_dir = config.PROJECTS_DIR / project
    file_path = (project_dir / filepath).resolve()
    if not str(file_path).startswith(str(project_dir.resolve())):
        print("Path escape detected", file=sys.stderr)
        sys.exit(1)

    # Read raw output from file if not provided
    if raw_output is None and file_path.exists():
        try:
            raw_output = file_path.read_text()
        except Exception:
            pass

    db.init_db()
    scan_id = db.log_scan(project, scan_type, str(file_path), raw_output)
    print(f"Scan registered: id={scan_id}, project={project}, type={scan_type}")


if __name__ == "__main__":
    main()
