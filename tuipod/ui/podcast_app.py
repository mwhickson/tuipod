from textual import on
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Input

from tuipod.models.search import Search
from tuipod.ui.episode_list import EpisodeList
from tuipod.ui.podcast_list import PodcastList
from tuipod.ui.podcast_player import PodcastPlayer
from tuipod.ui.search_input import SearchInput

APPLICATION_NAME = "tuipod"
APPLICATION_VERSION = "2024-11-18.5c24b1e90d6c4ae28faceec6bbcdff7a"

class PodcastApp(App):
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit_application", "Quit application")
    ]
    TITLE = APPLICATION_NAME
    SUB_TITLE = "version {0}".format(APPLICATION_VERSION)

    def __init__(self):
        super().__init__()
        self.searcher = Search("")
        self.podcasts = []
        self.current_podcast = None
        self.current_episode = None

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

        search_input: Input = event.input
        search_term = search_input.value

        self.podcasts = await self.searcher.search(search_term)

        table.clear()

        if len(self.podcasts) > 0:
            for podcast in self.podcasts:
                # key should be string
                table.add_row(podcast.title, key=(podcast.id, podcast.url))

            table.focus()
        else:
            table.add_row("no results")

        table.loading = False

    @on(DataTable.RowSelected)
    def action_rowselected(self, event: DataTable.RowSelected) -> None:
        triggering_table = event.data_table

        if triggering_table.id == "PodcastList":
            podcast_id = event.row_key.value[0]
            for p in self.podcasts:
                if p.id == podcast_id:
                    self.current_podcast = p
                    break

            self.current_podcast.get_episode_list()

            episode_list = self.query_one(EpisodeList)
            table = episode_list.query_one(DataTable)
            table.clear()

            for e in self.current_podcast.episodes:
                # key should be string
                table.add_row(e.title, e.duration, e.pubdate, key=(e.id, e.url))

            table.focus()
        elif triggering_table.id == "EpisodeList":
            episode_id = event.row_key.value[0]
            for e in self.current_podcast.episodes:
                if e.id == episode_id:
                    self.current_episode = e
                    break

            player: PodcastPlayer = self.query_one(PodcastPlayer)
            player_title = player.query_one("#playerTitleText")
            player_title.update(self.current_episode.title)

            self.current_episode.play_episode()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_quit_application(self) -> None:
        self.exit()
