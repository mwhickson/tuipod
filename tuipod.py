#
# tuipod.py
#
# 2024-11-12: Matthew Hickson
#

APPLICATION_NAME = "tuipod"
APPLICATION_VERSION = "2024-11-12.5c24b1e90d6c4ae28faceec6bbcdff7a"


from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, Static


class Episode:

    def __init__(self, title: str, url: str, description: str, duration: int) -> None:
        self.title = title
        self.url = url
        self.description = description
        self.duration = duration


class Podcast:

    def __init__(self, title: str, url: str, description: str) -> None:
        self.title = title
        self.url = url
        self.description = description
        self.episodes = []

    def add_episode(self, episode: Episode) -> None:
        self.episodes.append(episode)

    def remove_episode(self, url: str) -> None:
        for e in self.episodes:
            if e.url == url:
                self.episodes.remove(e)
                break


class Player:

    def __init__(self, episode: Episode, position_seconds: int) -> None:
        self.episode = episode
        self.position_seconds = position_seconds


class Search:

    def __init__(self, number_results: int, sort_order: str) -> None:
        self.number_results = number_results
        self.sort_order = sort_order


class SearchInput(Widget):

    DEFAULT_CSS = """
    SearchInput {
        height: auto;
        layout: horizontal;
        margin: 1 0;
    }

    SearchInput Button {
        border: none !important;
        padding: 0;
    }

    SearchInput #searchLabel {
        border: none;
    }

    SearchInput #searchInput {
        border: none !important;
        height: 1;
        width: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Search", id="searchLabel")
        yield Input(id="searchInput")
        yield Button(id="searchButton", label="search") 


class PodcastList(Widget):

    DEFAULT_CSS = """
    PodcastList {
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="PodcastList")

    def on_mount(self):
        table = self.query_one("#PodcastList")

        columns = ["Podcast Title", "Last Published"]

        for column in columns:
            table.add_column(column, key=column)


class EpisodeList(Widget):

    DEFAULT_CSS = """
    EpisodeList {
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="EpisodeList")

    def on_mount(self):
        table = self.query_one("#EpisodeList")

        columns = ["Episode Title", "Last Published"]

        for column in columns:
            table.add_column(column, key=column)


class PodcastPlayer(Widget):

    DEFAULT_CSS = """
    PodcastPlayer {
        dock: bottom;
        height: auto;
        layout: horizontal;
        margin-top: 1;
    }

    PodcastPlayer Button {
        border: none !important;
        padding: 0;
    }

    PodcastPlayer #playerPositionText {
        text-align: right;
        padding: 0 1;
        width: 8;
    }

    PodcastPlayer #playerTitleText {
        text-align: left;
        width: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Button(id="backButton", label="back")
        yield Button(id="playButton", label="play")
        yield Button(id="forwardButton", label="forward")
        yield Static("0:00", id="playerPositionText")
        yield Static("title", id="playerTitleText")
        yield Button(id="infoButton", label="info")


class PodcastApp(App):

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit_application", "Quit application")
    ]
    TITLE = APPLICATION_NAME
    SUB_TITLE = ("version {0}").format(APPLICATION_VERSION)
    
    def compose(self) -> ComposeResult:
        yield Header(icon="#", show_clock=True, time_format="%I:%M %p")

        yield SearchInput()
        yield PodcastList()
        yield EpisodeList()
        yield PodcastPlayer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_quit_application(self) -> None:
        self.exit()


if __name__ == "__main__":

    app = PodcastApp()
    app.run()

