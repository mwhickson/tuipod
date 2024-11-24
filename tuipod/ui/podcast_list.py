from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable

class PodcastList(Widget):
    """
    A simple podcast list widget using a datatable for columnar display.
    """

    DEFAULT_CSS = """
    PodcastList {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        """build the widget"""
        yield DataTable(id="PodcastList", cursor_type="row", zebra_stripes=True)

    def on_mount(self):
        """set up the columns on mount"""
        table: DataTable = self.query_one("#PodcastList")
        table.add_column("Status")
        table.add_column("Podcast Title")
        #table.add_column("Last Published")
