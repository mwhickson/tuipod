#
# tuipod.py
#
# 2024-11-12: Matthew Hickson
#

APPLICATION_NAME = "tuipod"
APPLICATION_VERSION = "2024-11-12.5c24b1e90d6c4ae28faceec6bbcdff7a"


import json
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, Static
import urllib.request
import urllib.parse
import uuid


class Episode:

    def __init__(self, title: str, url: str, description: str, duration: int) -> None:
        self.id = uuid.uuid4().hex
        self.title = title
        self.url = url
        self.description = description
        self.duration = duration

    def __lt__(self, other):
        return self.title < other.title


class Podcast:

    def __init__(self, title: str, url: str, description: str) -> None:
        self.id = uuid.uuid4().hex
        self.title = title
        self.url = url
        self.description = description
        self.episodes = []

    def __lt__(self, other):
        return self.title < other.title

    def add_episode(self, episode: Episode) -> None:
        self.episodes.append(episode)

    def remove_episode(self, url: str) -> None:
        for e in self.episodes:
            if e.url == url:
                self.episodes.remove(e)
                break

    def get_episode_list(self) -> []:
        return []


class Player:

    def __init__(self, episode: Episode, position_seconds: int) -> None:
        self.episode = episode
        self.position_seconds = position_seconds


class Search:

    ENDPOINT = "https://itunes.apple.com/search"

    def __init__(self, search_text: str) -> None:
        self.search_text = search_text
        self.cached_results = []

    def get_cached_search_results(self) -> []:
        return self.cached_results

    def get_search_results(self) -> []:
        results = []

        data = {}
        data["media"] = "podcast"
        data["entity"] = "podcast"
        data["term"] = self.search_text

        params = urllib.parse.urlencode(data)

        url = self.ENDPOINT + "?" + params

        with urllib.request.urlopen(url) as response:
            result = response.read()
            result_object = json.loads(result)
            if "results" in result_object:
                for detail in result_object["results"]:
                    if "feedUrl" in detail:
                        podcast_title = detail["collectionName"]
                        podcast_url = detail["feedUrl"]
                        podcast_description = detail["artistName"]

                        results.append(Podcast(podcast_title, podcast_url, podcast_description))

                results.sort()            
                self.cached_results = results

        return results
        
    async def search(self, search_text: str) -> []:
        if (self.search_text == search_text):
            return self.get_cached_search_results()
        else:
            self.search_text = search_text
            return self.get_search_results()


class SearchInput(Widget):

    DEFAULT_CSS = """
    SearchInput {
        height: auto;
        layout: horizontal;
        margin: 1 0;
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


class PodcastList(Widget):

    DEFAULT_CSS = """
    PodcastList {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="PodcastList", cursor_type="row", zebra_stripes=True)

    def on_mount(self):
        table = self.query_one("#PodcastList")
        table.add_column("Podcast Title")
        #table.add_column("Last Published")


class EpisodeList(Widget):

    DEFAULT_CSS = """
    EpisodeList {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield DataTable(id="EpisodeList")

    def on_mount(self):
        table = self.query_one("#EpisodeList")
        table.add_column("Episode Title")
        table.add_column("Duration")
        table.add_column("Published")


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
    
    def __init__(self):
        super().__init__()
        self.searcher = Search("")    
        self.podcasts = []
        self.current_podcast = None

    def compose(self) -> ComposeResult:
        yield Header(icon="#", show_clock=True, time_format="%I:%M %p")

        yield SearchInput()
        yield PodcastList()
        yield EpisodeList()
        yield PodcastPlayer()

    @on(Input.Submitted) 
    async def action_submit(self, event: Input.Submitted) -> None:
        podcast_list = self.query_one(PodcastList)
        table = podcast_list.query_one(DataTable)
        table.loading = True
        
        searchInput = self.query_one("#searchInput")
        searchTerm = searchInput.value

        self.podcasts = await self.searcher.search(searchTerm)

        table.clear()

        if (len(self.podcasts) > 0):
            for podcast in self.podcasts:
                table.add_row(podcast.title, key=(podcast.id, podcast.url))
        else:
            table.add_row("no results");

        table.loading = False

    @on(DataTable.RowSelected)
    def action_rowselected(self, event: DataTable.RowSelected) -> None:
        triggering_table = event.data_table

        if triggering_table.id == "PodcastList":
            podcast_id = event.row_key.value[0]
            #podcast_url = event.row_key.value[1]
            for p in self.podcasts:
                if p.id == podcast_id:
                    self.current_podcast = p
                    break

            episode_list = self.query_one(EpisodeList)
            table = episode_list.query_one(DataTable)
            table.clear()
            table.add_row((self.current_podcast.title, self.current_podcast.url))
        elif triggering_table.id == "EpisodeList":
            pass

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_quit_application(self) -> None:
        self.exit()


if __name__ == "__main__":

    app = PodcastApp()
    app.run()

