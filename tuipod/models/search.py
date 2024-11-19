import json
import urllib.parse
import urllib.request

from tuipod.models.podcast import Podcast

class Search:
    ENDPOINT = "https://itunes.apple.com/search"

    def __init__(self, search_text: str) -> None:
        self.search_text = search_text
        self.cached_results = []

    def get_cached_search_results(self) -> []:
        return self.cached_results

    def get_search_results(self) -> []:
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
        if self.search_text == search_text:
            return self.get_cached_search_results()
        else:
            self.search_text = search_text
            return self.get_search_results()
