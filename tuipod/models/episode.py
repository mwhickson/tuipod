import uuid

import miniaudio

# way better on the dependency front than miniaudio... needs to download file before playing though (and blocks by default)
# also, doesn't improve the situation re: pause/play or position tracking...
#import playsound3

class Episode:
    """
    A minimal representation of a podcast episode.

    It also handles playback of the episode (at the moment).

    FIX: extract play functionality from model.
    """

    def __init__(self, title: str, url: str, description: str, pubdate: str, duration: int) -> None:
        """initialize episode with title, url, description, pubdate and duration"""
        self.id = uuid.uuid4().hex
        self.title = title
        self.url = url
        self.description = description
        self.pubdate = pubdate
        self.duration = duration
        self.current_position = 0
        self.source = None
        self.stream = None
        self.device = None
        self.is_playing = False

    def __lt__(self, other):
        """'less than' support to allow episode sorting"""
        if self.pubdate != other.pubdate:
            return self.pubdate < other.pubdate
        else:
            return self.title < other.title

    def is_playing(self) -> bool:
        """track whether episode is playing or not"""
        return self.is_playing()

    def play_episode(self):
        """
        play the episode audio directly from its internet source

        TODO: extract this, and add ability to track playback (and ideally switch from internet play to cached play from disk, once file is downloaded)
        """
        if not self.device is None:
            self.device.start(self.stream)
        else:
            self.source = miniaudio.IceCastClient(self.url)
            self.stream = miniaudio.stream_any(self.source, self.source.audio_format)
            self.device = miniaudio.PlaybackDevice()
            self.device.start(self.stream)

        self.is_playing = True

    def stop_episode(self):
        """
        stop episode from playing

        NOTE: more like pausing, since we don't close/destroy the associated playback device.
        """
        self.device.stop()
        self.is_playing = False
