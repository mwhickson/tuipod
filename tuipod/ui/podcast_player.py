from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button, Static

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
        padding: 0 1;
        width: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        #yield Button(id="backButton", label="back")
        yield Button(id="playButton", label="play")
        #yield Button(id="forwardButton", label="forward")
        # yield Static("0:00", id="playerPositionText")
        yield Static("", id="playerTitleText")
        # yield Button(id="infoButton", label="info")
