import uuid

import miniaudio

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

    def __lt__(self, other):
        return self.title < other.title

    def play_episode(self):
        if not self.device is None:
            self.device.start(self.stream)
        else:
            self.source = miniaudio.IceCastClient(self.url)
            self.stream = miniaudio.stream_any(self.source, self.source.audio_format)
            self.device = miniaudio.PlaybackDevice()
            self.device.start(self.stream)

    def pause_episode(self):
        pass
