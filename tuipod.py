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
from textual.widgets import Footer, Header, Input, Label, Static


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
        layout: horizontal;
        height: auto;
    }

    SearchInput Label {
        padding: 1;
    }

    SearchInput Input {
        width: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Search")
        yield Input()


class PodcastList(Widget):

    DEFAULT_CSS = """
    PodcastList {
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Podcasts...")


class EpisodeList(Widget):

    DEFAULT_CSS = """
    EpisodeList {
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Episodes...")


class PodcastPlayer(Widget):

    DEFAULT_CSS = """
    PodcastPlayer {
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Player")


class PodcastApp(App):

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit_application", "Quit application")
    ]
    TITLE = APPLICATION_NAME
    SUB_TITLE = APPLICATION_VERSION
    
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()

        yield SearchInput()
        yield PodcastList()
        yield EpisodeList()
        yield PodcastPlayer()

        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_quit_application(self) -> None:
        self.exit()


if __name__ == "__main__":

    app = PodcastApp()
    app.run()

