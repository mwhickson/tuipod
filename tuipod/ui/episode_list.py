from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable

class EpisodeList(Widget):

    DEFAULT_CSS = """
    EpisodeList {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="EpisodeList", cursor_type="row", zebra_stripes=True)

    def on_mount(self):
        table: DataTable = self.query_one("#EpisodeList")
        table.add_column("Episode Title")
        table.add_column("Duration")
        table.add_column("Published")
