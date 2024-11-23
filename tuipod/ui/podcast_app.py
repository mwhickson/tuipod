import json
import uuid

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, DataTable, Header, Input, Static

from tuipod.models.search import Search
from tuipod.models.subscription_list import SubscriptionList
from tuipod.ui.about_info import AboutInfoScreen
from tuipod.ui.episode_info import EpisodeInfoScreen
from tuipod.ui.episode_list import EpisodeList
from tuipod.ui.error_info import ErrorInfoScreen
from tuipod.ui.podcast_list import PodcastList
from tuipod.ui.podcast_player import PodcastPlayer
from tuipod.ui.search_input import SearchInput

# DEBUG:
# import logging
# logging.basicConfig(filename="debug.log", filemode="w", level="NOTSET")

APPLICATION_NAME = "tuipod"
APPLICATION_VERSION = "2024-11-22.5c24b1e90d6c4ae28faceec6bbcdff7a"

class PodcastApp(App):
    BINDINGS = [
        Binding("f1", "display_about", "Display about information", priority=True),

        # don't let search swallow input (but don't prioritize standard text entry characters to hamper search)
        Binding("ctrl+q", "quit_application", "Quit application", priority=True),

        # may dupe, but lets us avoid the need to CTRL chord keys for some functions (these will be 'undocumented' to avoid confusion re: the conditions necessary for these to work)
        Binding("space", "toggle_play", "Play/Pause"),
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("i", "display_info", "Display information"),
        Binding("q", "quit_application", "Quit application"),
        Binding("s", "subscribe_to_podcast", "Subscribe to Podcast"),
        Binding("u", "unsubscribe_from_podcast", "Unsubscribe from Podcast")
    ]
    TITLE = APPLICATION_NAME
    SUB_TITLE = "version {0}".format(APPLICATION_VERSION)

    def __init__(self):
        super().__init__()
        self.searcher = Search("")
        self.subscriptions = SubscriptionList()
        self.podcasts = []
        self.current_podcast = None
        self.current_episode = None

    def compose(self) -> ComposeResult:
        yield Header(icon="#", show_clock=True, time_format="%I:%M %p")

        yield SearchInput()
        yield PodcastList()
        yield EpisodeList()
        yield PodcastPlayer()

    async def on_mount(self) -> None:
        self.subscriptions.retrieve()
        if len(self.subscriptions.podcasts) > 0:
            await self._refresh_podcast_list("")

    async def _refresh_podcast_list(self, search_term: str) -> None:
        podcast_list = self.query_one(PodcastList)
        episode_list = self.query_one(EpisodeList)

        table = podcast_list.query_one(DataTable)
        table.loading = True

        episodes_table = episode_list.query_one(DataTable)

        table.clear()
        episodes_table.clear()

        if len(self.subscriptions.podcasts) > 0:
            self.podcasts = self.subscriptions.podcasts
            for p in self.subscriptions.podcasts:
                row_key = json.dumps((p.id, p.url))
                table.add_row(p.title, key=row_key)

        if search_term.strip() != "":
            try:

                self.podcasts = await self.searcher.search(search_term)

                if len(self.podcasts) > 0:
                    for podcast in self.podcasts:
                        row_key = json.dumps((podcast.id, podcast.url))
                        if not row_key in table.rows.keys():
                            table.add_row(podcast.title, key=row_key)

                    table.focus()
                else:
                    table.add_row("no results")

            except Exception as err:
                table.add_row("error occurred")
                self.app.push_screen(ErrorInfoScreen(str(err)))

        table.loading = False

    @on(Input.Submitted)
    async def action_submit(self, event: Input.Submitted) -> None:
        search_input: Input = event.input
        search_term = search_input.value
        await self._refresh_podcast_list(search_term)

    def _set_player_button_status(self, mode: str):
        player: PodcastPlayer = self.query_one(PodcastPlayer)
        play_button: Button = player.query_one("#playButton")

        if mode == "playing":
            play_button.label = "playing"
            play_button.styles.background = "green"
            play_button.styles.color = "white"
        elif mode == "paused":
            play_button.label = "paused"
            play_button.styles.background = "red"
            play_button.styles.color = "white"
        else:
            play_button.label = "..."
            play_button.styles.background = "blue"
            play_button.styles.color = "white"

    def _action_podcast_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        k = event.row_key
        if not k is None:
            v = k.value
            if not v is None:
                row_keys = json.loads(v)
                podcast_id = row_keys[0]
                for p in self.podcasts:
                    if p.id == podcast_id:
                        self.current_podcast = p
                        break

    def _action_episode_row_highlighted(self, event: DataTable.RowSelected) -> None:
        k = event.row_key
        if not k is None:
            v = k.value
            if not v is None:
                row_keys = json.loads(v)
                episode_id = row_keys[0]
                for e in self.current_podcast.episodes:
                    if e.id == episode_id:
                        self.current_episode = e
                        break

    def _action_podcast_row_selected(self, event: DataTable.RowSelected) -> None:
        episode_list = self.query_one(EpisodeList)
        table = episode_list.query_one(DataTable)
        table.loading = True
        table.clear()

        try:
            self.current_podcast.get_episode_list()

            for e in self.current_podcast.episodes:
                row_key = json.dumps((e.id, e.url))
                table.add_row(e.title, e.duration, e.pubdate, key=row_key)

            table.focus()
        except Exception as err:
            self.app.push_screen(ErrorInfoScreen(str(err)))

        table.loading = False

    def _action_episode_row_selected(self, event: DataTable.RowSelected) -> None:
        try:
            playing_episode = self.current_episode

            player: PodcastPlayer = self.query_one(PodcastPlayer)
            player_title: Static = player.query_one("#playerTitleText")
            player_title.update(self.current_episode.title)

            if playing_episode and playing_episode.is_playing:
                playing_episode.stop_episode()

            self.current_episode.play_episode()
            self._set_player_button_status("playing")
        except Exception as err:
            self.app.push_screen(ErrorInfoScreen(str(err)))

    @on(DataTable.RowHighlighted)
    def action_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.data_table.id == "PodcastList":
            self._action_podcast_row_highlighted(event)
        elif event.data_table.id == "EpisodeList":
            self._action_episode_row_highlighted(event)

    @on(DataTable.RowSelected)
    def action_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "PodcastList":
            self._action_podcast_row_selected(event)
        elif event.data_table.id == "EpisodeList":
            self._action_episode_row_selected(event)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_toggle_play(self) -> None:
        if not self.current_episode is None:
            if self.current_episode.is_playing:
                self.current_episode.stop_episode()
                self._set_player_button_status("paused")
            else:
                self.current_episode.play_episode()
                self._set_player_button_status("playing")

    def action_display_about(self) -> None:
        self.app.push_screen(AboutInfoScreen())

    def action_display_info(self) -> None:
        if not self.current_episode is None:
            self.app.push_screen(EpisodeInfoScreen(self.current_episode.title, self.current_episode.url, self.current_episode.description))

    def action_quit_application(self) -> None:
        self.exit()

    async def action_subscribe_to_podcast(self) -> None:
        if not self.current_podcast is None:
            self.subscriptions.add_podcast(self.current_podcast)
            self.subscriptions.persist()
            await self._refresh_podcast_list(self.searcher.search_text)

    async def action_unsubscribe_from_podcast(self) -> None:
        if not self.current_podcast is None:
            self.subscriptions.remove_podcast(self.current_podcast.url)
            self.subscriptions.persist()
            await self._refresh_podcast_list(self.searcher.search_text)
