import json
import urllib.parse
import urllib.request

from tuipod.models.podcast import Podcast

class Search:
    """
    A barebones search hooked up to the iTunes podcast search service.

    TODO: abstract and add additional search providers (e.g. gpodder.net, Spotify, YouTube, etc.)
    """

    ENDPOINT = "https://itunes.apple.com/search"

    def __init__(self, search_text: str) -> None:
        """initialize search with text to find"""
        self.search_text = search_text
        self.cached_results = []

    def get_cached_search_results(self) -> []:
        """pull search results from cache"""
        return self.cached_results

    def get_search_results(self) -> []:
        """reach out to provider (iTunes) and retrieve search results"""
        results = []

        data = {"media": "podcast", "entity": "podcast", "term": self.search_text}

        params = urllib.parse.urlencode(data)

        url = self.ENDPOINT + "?" + params

        with urllib.request.urlopen(url) as response:
            result = response.read()
            result_object = json.loads(result)
            if "results" in result_object:
                for detail in result_object["results"]:
                    if "feedUrl" in detail:
                        podcast_title = detail["collectionName"]
                        podcast_url = detail["feedUrl"]
                        podcast_description = detail["artistName"]

                        results.append(Podcast(podcast_title, podcast_url, podcast_description))

                results.sort()
                self.cached_results = results

        return results

    async def search(self, search_text: str) -> []:
        """based on the search_text supplied, either get fresh results, or pull from cache (if same search is conducted)"""
        if self.search_text == search_text:
            return self.get_cached_search_results()
        else:
            self.search_text = search_text
            return self.get_search_results()
