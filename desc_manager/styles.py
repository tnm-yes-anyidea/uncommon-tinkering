import os

# Solarized Colors
BASE03 = "#002b36"
BASE02 = "#073642"
BASE0 = "#839496"
GREEN = "#859900"
BLUE = "#268bd2"
YELLOW = "#b58900"
CYAN = "#2aa198"
MAGENTA = "#d33682"

IS_VSCODE = os.environ.get("TERM_PROGRAM") == "vscode"

if IS_VSCODE:
    # Blend smoothly with VS Code's internal window layout
    CSS = f"""
    Screen {{ background: transparent; color: {BASE0}; }}
    #top_pane {{ height: 55%; border: hkey {BLUE}; }}
    #bottom_pane {{ height: 45%; border: hkey {CYAN}; background: {BASE02}; padding: 1; }}
    ListView {{ background: transparent; }}
    ListItem.--highlight {{ background: {BASE02}; color: {CYAN}; text-style: bold; }}
    Input {{ background: {BASE03}; border: tall {CYAN}; color: {BASE0}; }}
    .pane_label {{ background: {BLUE}; color: {BASE03}; width: auto; padding: 0 1; text-style: bold; }}
    """
else:
    # Max color vibrancy for Neovim / Raw Linux Terminals (GDB Dash Look)
    CSS = f"""
    Screen {{ background: {BASE03}; color: {BASE0}; }}
    #top_pane {{ height: 55%; border: heavy {BLUE}; }}
    #bottom_pane {{ height: 45%; border: heavy {YELLOW}; background: {BASE02}; padding: 1; }}
    ListView {{ background: {BASE03}; }}
    ListItem.--highlight {{ background: {BASE02}; color: {GREEN}; text-style: bold; }}
    Input {{ background: {BASE03}; border: tall {MAGENTA}; color: #ffffff; }}
    .pane_label {{ background: {YELLOW}; color: {BASE03}; width: auto; padding: 0 1; text-style: bold; }}
    """
