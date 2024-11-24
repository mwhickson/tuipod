import json

from urllib.request import build_opener, install_opener

from pynput import keyboard

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
APPLICATION_VERSION = "2024-11-24.6147baed9d02462989c1d8cc65b87af5-beta"

class PodcastApp(App):
    """
    A podcast player application (tuipod) utilizing textual.
    """

    BINDINGS = [
        Binding("f1", "display_about", "Display about information", priority=True),
        Binding("space", "toggle_play", "Play/Pause"),
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("i", "display_info", "Display information"),
        Binding("s", "subscribe_to_podcast", "Subscribe to Podcast"),
        Binding("u", "unsubscribe_from_podcast", "Unsubscribe from Podcast")
    ]
    TITLE = APPLICATION_NAME
    SUB_TITLE = "version {0}".format(APPLICATION_VERSION)

    def __init__(self):
        """
        initialize the application

        NOTE: sets a User-Agent override for urllib.openurl(), and multimedia key support.
        """
        super().__init__()
        self.searcher = Search("")
        self.subscriptions = SubscriptionList()
        self.podcasts = []
        self.current_podcast = None
        self.current_episode = None

        # REF: https://theorangeone.net/posts/urllib-useragent/#global-opener
        # NOTE: _opener is not available for import, but it's not necessary (presumably within an app context)
        opener = build_opener()
        install_opener(opener)
        opener.addheaders = [("User-Agent", "Mozilla/9.9 (github.com/mwhickson/tuipod) Chrome/999.9.9.9 Gecko/99990101 Firefox/999 Safari/999.9")]

        # hookup for multimedia button (play/pause for now)
        self.keylistener = keyboard.Listener(on_release=self.on_listen_keys)
        self.keylistener.start()

    def compose(self) -> ComposeResult:
        """build the app"""
        yield Header(icon="#", show_clock=True, time_format="%I:%M %p")

        yield SearchInput()
        yield PodcastList()
        yield EpisodeList()
        yield PodcastPlayer()

    async def on_mount(self) -> None:
        """set up application, including listing current subscriptions"""
        self.subscriptions.retrieve()
        if len(self.subscriptions.podcasts) > 0:
            await self._refresh_podcast_list("")

    async def _refresh_podcast_list(self, search_term: str) -> None:
        """refresh the podcast list, subscriptions first then search results"""
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
                table.add_row("SUB", p.title, key=row_key)

        if search_term.strip() != "":
            try:

                self.podcasts = await self.searcher.search(search_term)

                if len(self.podcasts) > 0:
                    for podcast in self.podcasts:
                        row_key = json.dumps((podcast.id, podcast.url))
                        if not row_key in table.rows.keys():
                            podcast.subscribed = False
                            table.add_row("", podcast.title, key=row_key)

                    table.focus()
                else:
                    table.add_row("no results")

            except Exception as err:
                table.add_row("error occurred")
                self.app.push_screen(ErrorInfoScreen(str(err)))

        table.loading = False

    @on(Input.Submitted)
    async def action_submit(self, event: Input.Submitted) -> None:
        """perform the search for the criteria entered in the search widget"""
        search_input: Input = event.input
        search_term = search_input.value
        self.notify("searching for: {0}".format(search_term), timeout=3)
        await self._refresh_podcast_list(search_term)

    def _set_player_button_status(self, mode: str):
        """set the visual status of the play button in the podcast player widget"""
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
        """keep track of the highlighted podcast row for easy reference"""
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
        """keep track of the highlighted episode row for easy reference"""
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
        """select the currently highlighted podcast, and retrieve its episode list"""
        self.notify("getting episodes for: {0}".format(self.current_podcast.title), timeout=3)

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
        """select the currently highlighted episode, and begin playing the episode"""
        try:
            playing_episode = self.current_episode

            player: PodcastPlayer = self.query_one(PodcastPlayer)
            player_title: Static = player.query_one("#playerTitleText")
            player_title.update(self.current_episode.title)

            if playing_episode and playing_episode.is_playing:
                playing_episode.stop_episode()

            self.notify("playing: {0}".format(self.current_episode.title), timeout=3)
            self.current_episode.play_episode()
            self._set_player_button_status("playing")
        except Exception as err:
            self.app.push_screen(ErrorInfoScreen(str(err)))

    @on(DataTable.RowHighlighted)
    def action_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """general row highlighting handler"""
        if event.data_table.id == "PodcastList":
            self._action_podcast_row_highlighted(event)
        elif event.data_table.id == "EpisodeList":
            self._action_episode_row_highlighted(event)

    @on(DataTable.RowSelected)
    def action_row_selected(self, event: DataTable.RowSelected) -> None:
        """general row selection handler"""
        if event.data_table.id == "PodcastList":
            self._action_podcast_row_selected(event)
        elif event.data_table.id == "EpisodeList":
            self._action_episode_row_selected(event)

    def action_toggle_dark(self) -> None:
        """toggle between dark and light themes"""
        self.dark = not self.dark

    def action_toggle_play(self) -> None:
        """toggle between playing or pausing an active episode"""
        if not self.current_episode is None:
            if self.current_episode.is_playing:
                self.current_episode.stop_episode()
                self._set_player_button_status("paused")
                self.notify("paused: {0}".format(self.current_episode.title), timeout=3)
            else:
                self.current_episode.play_episode()
                self._set_player_button_status("playing")
                self.notify("playing: {0}".format(self.current_episode.title), timeout=3)

    def action_display_about(self) -> None:
        """display the about/help screen"""
        self.app.push_screen(AboutInfoScreen())

    def action_display_info(self) -> None:
        """display the episode information screen for the active podcast"""
        if not self.current_episode is None:
            self.app.push_screen(EpisodeInfoScreen(self.current_episode.title, self.current_episode.url, self.current_episode.description))

    def action_quit_application(self) -> None:
        """quit the application"""
        self.exit()

    async def action_subscribe_to_podcast(self) -> None:
        """record the subscription of the active podcast"""
        if not self.current_podcast is None:
            self.subscriptions.add_podcast(self.current_podcast)
            self.subscriptions.persist()
            await self._refresh_podcast_list(self.searcher.search_text)
            self.notify("subscribed to: {0}".format(self.current_podcast.title), timeout=3)

    async def action_unsubscribe_from_podcast(self) -> None:
        """remove (and thus unsubscribe) from the active podcast"""
        if not self.current_podcast is None:
            title = self.current_podcast.title
            self.subscriptions.remove_podcast(self.current_podcast.url)
            self.subscriptions.persist()
            await self._refresh_podcast_list(self.searcher.search_text)
            self.notify("unsubscribed from: {0}".format(title), timeout=3)

    def on_listen_keys(self, key) -> None:
        """listen for the media play/pause keypress to complete"""
        if key == keyboard.Key.media_play_pause:
            self.action_toggle_play()