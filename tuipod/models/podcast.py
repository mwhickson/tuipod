import urllib.request
import uuid
import xml.etree.ElementTree as ET

from tuipod.models.episode import Episode

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
        with urllib.request.urlopen(self.url) as response:
            result = response.read()

        episodes = ET.fromstring(result)
        for e in episodes.iter("item"):
            title = e.find("title").text
            description = e.find("description").text
            enclosure = e.find("enclosure")
            url = enclosure.attrib["url"]
            pubdate = e.find("pubDate").text
            duration = 0 #e.find("itunes:duration").text

            self.episodes.append(Episode(title, url, description, pubdate, duration))

        return self.episodes
