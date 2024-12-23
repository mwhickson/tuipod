from os.path import exists
import xml.etree.ElementTree as ET
import xml.sax.saxutils as saxu

from tuipod.models.podcast import Podcast

class SubscriptionList:
    """
    A simple subscription list saved/loaded from a fixed OPML file (subscriptions.opml).
    """

    SUBSCRIPTION_FILE = "subscriptions.opml"

    def __init__(self) -> None:
        """initialize the subscription list"""
        self.podcasts = []

    def add_podcast(self, p: Podcast) -> None:
        """add a podcast subscription"""
        p.subscribed = True
        self.podcasts.append(p)

    def remove_podcast(self, url: str) -> None:
        """remove a subscribed podcast by URL"""
        for p in self.podcasts:
            if p.url == url:
                p.subscribed = False
                self.podcasts.remove(p)
                break

    def retrieve(self) -> []:
        """load subscriptions from disk (if the subscription file exists)"""
        self.podcasts = []

        if exists(self.SUBSCRIPTION_FILE):
            with open(self.SUBSCRIPTION_FILE, "rt", encoding="utf-8") as subscription_file:
                contents = subscription_file.readlines()
                subscription_file.close()

            doc = ET.fromstringlist(contents)

            for item in doc.iter("outline"):
                title = item.get("text")
                url = item.get("xmlUrl")
                if not title is None and not url is None:
                    p = Podcast(title, url, "")
                    p.subscribed = True
                    self.add_podcast(p)

    def persist(self) -> None:
        """save the current subscription list to disk"""
        with open(self.SUBSCRIPTION_FILE, "wt", encoding="utf-8") as subscription_file:
            lines = []
            lines.append('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n')
            lines.append('<opml version="1.0">\n')
            lines.append('<body>\n')
            lines.append('<outline text="feeds">\n')

            for p in self.podcasts:
                escaped_title = saxu.escape(p.title)
                lines.append('<outline text="{0}" xmlUrl="{1}" type="rss" />\n'.format(escaped_title, p.url))

            lines.append('</outline>\n')
            lines.append('</body>\n')
            lines.append('</opml>\n')

            subscription_file.writelines(lines)
            subscription_file.flush()
            subscription_file.close()
