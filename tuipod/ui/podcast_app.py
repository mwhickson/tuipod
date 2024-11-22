import json

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, DataTable, Header, Input, RichLog, Static

from tuipod.models.search import Search
from tuipod.ui.episode_info import EpisodeInfoScreen
from tuipod.ui.episode_list import EpisodeList
from tuipod.ui.podcast_list import PodcastList
from tuipod.ui.podcast_player import PodcastPlayer
from tuipod.ui.search_input import SearchInput

APPLICATION_NAME = "tuipod"
APPLICATION_VERSION = "2024-11-18.5c24b1e90d6c4ae28faceec6bbcdff7a"

class PodcastApp(App):
    BINDINGS = [
        ("space", "toggle_play", "Play/Pause"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("i", "display_info", "Display information"),
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
                row_key = json.dumps((podcast.id, podcast.url))
                table.add_row(podcast.title, key=row_key)

            table.focus()
        else:
            table.add_row("no results")

        table.loading = False

    @on(DataTable.RowSelected)
    def action_row_selected(self, event: DataTable.RowSelected) -> None:
        triggering_table = event.data_table
        row_keys = json.loads(event.row_key.value)

        if triggering_table.id == "PodcastList":
            podcast_id = row_keys[0]
            for p in self.podcasts:
                if p.id == podcast_id:
                    self.current_podcast = p
                    break

            self.current_podcast.get_episode_list()

            episode_list = self.query_one(EpisodeList)
            table = episode_list.query_one(DataTable)
            table.clear()

            for e in self.current_podcast.episodes:
                row_key = json.dumps((e.id, e.url))
                table.add_row(e.title, e.duration, e.pubdate, key=row_key)

            table.focus()
        elif triggering_table.id == "EpisodeList":
            playing_episode = self.current_episode

            episode_id = row_keys[0]
            for e in self.current_podcast.episodes:
                if e.id == episode_id:
                    self.current_episode = e
                    break

            player: PodcastPlayer = self.query_one(PodcastPlayer)
            player_title: Static = player.query_one("#playerTitleText")
            player_title.update(self.current_episode.title)

            if playing_episode and playing_episode.is_playing:
                playing_episode.stop_episode()

            self.current_episode.play_episode()

            play_button: Button = player.query_one("#playButton")
            play_button.label = "pause"
            play_button.styles.background = "green"
            play_button.styles.color = "white"

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_toggle_play(self) -> None:
        player: PodcastPlayer = self.query_one(PodcastPlayer)
        play_button: Button = player.query_one("#playButton")

        if not self.current_episode is None:
            if self.current_episode.is_playing:
                self.current_episode.stop_episode()
                play_button.label = "play"
                play_button.styles.background = "red"
                play_button.styles.color = "white"
            else:
                self.current_episode.play_episode()
                play_button.label = "pause"
                play_button.styles.background = "green"
                play_button.styles.color = "white"

    def action_display_info(self) -> None:
        if not self.current_episode is None:
            self.app.push_screen(EpisodeInfoScreen(self.current_episode.title, self.current_episode.url, self.current_episode.description))

    def action_quit_application(self) -> None:
        self.exit()
