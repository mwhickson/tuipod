import uuid

import miniaudio

# way better on the dependency front than miniaudio... needs to download file before playing though (and blocks by default)
# also, doesn't improve the situation re: pause/play or position tracking...
#import playsound3

class Episode:

    def __init__(self, title: str, url: str, description: str, pubdate: str, duration: int) -> None:
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
        if self.pubdate != other.pubdate:
            return self.pubdate < other.pubdate
        else:
            return self.title < other.title

    def is_playing(self) -> bool:
        return self.is_playing()

    def play_episode(self):
        if not self.device is None:
            self.device.start(self.stream)
        else:
            self.source = miniaudio.IceCastClient(self.url)
            self.stream = miniaudio.stream_any(self.source, self.source.audio_format)
            self.device = miniaudio.PlaybackDevice()
            self.device.start(self.stream)

        self.is_playing = True

    def stop_episode(self):
        self.device.stop()
        self.is_playing = False
