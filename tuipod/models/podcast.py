from bs4 import BeautifulSoup
import urllib.request
import uuid
import xml.etree.ElementTree as ET

from tuipod.models.episode import Episode

class Podcast:
    """
    A minimal representation of a podcast.

    It also handles retrieval of episodes from the podcast feed (at the moment).

    FIX: extract episode retrieval into a more appropriate spot.
    """

    def __init__(self, title: str, url: str, description: str) -> None:
        """initialize a podcast with title, url, and description"""
        self.id = uuid.uuid4().hex
        self.title = title
        self.url = url
        self.description = description
        self.episodes = []
        self.subscribed = False

    def __lt__(self, other):
        """'less than' support to allow podcast sorting"""
        return self.title < other.title

    def add_episode(self, episode: Episode) -> None:
        """add an episode to the podcast"""
        self.episodes.append(episode)

    def remove_episode(self, url: str) -> None:
        """remove an episode from the podcast based on the episode URL"""
        for e in self.episodes:
            if e.url == url:
                self.episodes.remove(e)
                break

    def get_episode_list(self) -> []:
        """
        Get an episode list from the podcast feed.

        Works around missing data in a tested, but haphazard, manner.

        TODO: put this someplace more appropriate.
        """
        with urllib.request.urlopen(self.url) as response:
            result = response.read()

        episodes = ET.fromstring(result)
        for e in episodes.iter("item"):
            title = e.find("title").text

            enclosure = e.find("enclosure")
            if not enclosure is None:
                url = enclosure.attrib["url"]

                raw_description = e.find("description").text
                if not raw_description is None:
                    soup = BeautifulSoup(raw_description, "html.parser") # I'd change "soup", but I like it...
                    clean_description = soup.get_text()
                    description = clean_description
                else:
                    description = ""

                pubdate = e.find("pubDate").text

                duration = 0
                possible_duration = e.find("itunes:duration")
                if not possible_duration is None:
                    duration = possible_duration.text

                if not url is None:
                    self.episodes.append(Episode(title, url, description, pubdate, duration))

        return self.episodes
