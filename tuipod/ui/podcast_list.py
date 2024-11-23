from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable

class PodcastList(Widget):

    DEFAULT_CSS = """
    PodcastList {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="PodcastList", cursor_type="row", zebra_stripes=True)

    def on_mount(self):
        table: DataTable = self.query_one("#PodcastList")
        table.add_column("Status")
        table.add_column("Podcast Title")
        #table.add_column("Last Published")
