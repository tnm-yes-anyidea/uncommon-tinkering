# /// script
# dependencies = [
#   "textual",
# ]
# ///

import subprocess
import sys

from desc_manager import core, interface


def handle_auto():
    files, msg = core.get_latest_commit()
    if files:
        data = core.load_desc()
        for f in files:
            data[f] = [msg]
        core.save_desc(data)
        subprocess.run(
            ["git", "commit", "-m", "docs: auto-sync via push stream"],
            capture_output=True,
        )
        sys.exit(5)
    sys.exit(0)


if __name__ == "__main__":
    if "--auto" in sys.argv:
        handle_auto()
    else:
        app = interface.GdbStyleTui()
        app.run()
        sys.exit(5 if getattr(app, "should_restart", False) else 0)
