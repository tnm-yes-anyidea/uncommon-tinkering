# /// script
# dependencies = [
#   "textual",
# ]
# ///
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Input, Label, ListItem, ListView

from desc_manager import core, styles


class FileItem(ListItem):
    def __init__(self, filename, has_desc):
        super().__init__()
        self.filename = filename
        self.has_desc = has_desc

    def compose(self) -> ComposeResult:
        yield Label(f"{'💚' if self.has_desc else '⚙️ '} {self.filename}")


class GdbStyleTui(App):
    CSS = styles.CSS
    BINDINGS = [
        ("q", "quit", "Exit & Push"),
        ("ctrl+s", "save_all", "Force Commit Docs"),
    ]

    def __init__(self):
        super().__init__()
        self.descriptions = core.load_desc()
        self.git_files = core.get_git_files()
        self.should_restart = False

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="top_pane"):
            yield Label(" 🖥️  SOURCE: REPOSITORY LOG ", classes="pane_label")
            yield Input(placeholder="Type pattern to filter files...", id="search_box")
            yield ListView(id="file_list")

        with Vertical(id="bottom_pane"):
            yield Label(" 🎛️  CONSOLE: DESCRIPTION METADATA ", classes="pane_label")
            yield Label(
                "Navigate the top pane. Enter a file to modify details.",
                id="status_lbl",
            )
            yield Input(
                placeholder="Ex: First item line\\, with literal comma, next array line item",
                id="desc_input",
            )

        yield Footer()

    def on_mount(self):
        self.update_list()
        self.query_one("#search_box").focus()

    def update_list(self, filter_text=""):
        lst = self.query_one("#file_list")
        lst.clear()
        for f in self.git_files:
            if filter_text.lower() in f.lower():
                lst.append(FileItem(f, f in self.descriptions))

    def on_input_changed(self, event: Input.Changed):
        if event.input.id == "search_box":
            self.update_list(event.value)

    def on_list_view_selected(self, event: ListView.Selected):
        self.active_file = event.item.filename
        self.query_one("#status_lbl").update(f"Target file: {self.active_file}")

        # Load existing data, format literal commas as \, so it displays properly for editing
        current_lines = self.descriptions.get(self.active_file, [])
        self.query_one("#desc_input").value = core.format_for_input_box(current_lines)

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "desc_input" and hasattr(self, "active_file"):
            raw_val = event.value
            # Parse via lookbehind engine rules
            parsed_lines = core.parse_custom_input(raw_val)

            if parsed_lines:
                self.descriptions[self.active_file] = parsed_lines
            else:
                self.descriptions.pop(self.active_file, None)

            core.save_desc(self.descriptions)
            self.notify(f"Updated metadata for {self.active_file}")
            self.update_list(self.query_one("#search_box").value)
            self.query_one("#search_box").focus()

    def action_save_all(self):
        core.export_markdown()
        import subprocess

        subprocess.run(
            ["git", "commit", "-m", "docs: update metadata indexes"],
            capture_output=True,
        )
        self.should_restart = True
        self.notify("Changes saved and committed successfully!")
