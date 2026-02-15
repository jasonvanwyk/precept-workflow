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

    # Read raw output from file if not provided
    if raw_output is None and Path(filepath).exists():
        try:
            raw_output = Path(filepath).read_text()
        except Exception:
            pass

    db.init_db()
    scan_id = db.log_scan(project, scan_type, filepath, raw_output)
    print(f"Scan registered: id={scan_id}, project={project}, type={scan_type}")


if __name__ == "__main__":
    main()
