#
# test_tuipod.py
#
# TODO: https://textual.textualize.io/guide/testing/
#
# 2024-11-12: Matthew Hickson
#

import unittest

from tuipod.models.podcast import Podcast
from tuipod.models.episode import Episode
#TODO:  Player, Search, PodcastApp


TEST_PODCAST_NAME = "A Podcast"
TEST_EPISODE_NAME = "An Episode"
TEST_PODCAST_FEED_URL = "https://localhost/podcast"
TEST_EPISODE_FEED_URL = "https://localhost/podcast/episode1.mp3"
TEST_PODCAST_DESCRIPTION = "A test podcast."
TEST_EPISODE_DESCRIPTION = "A test podcast episode."
TEST_EPISODE_PUBDATE = "2024-01-01 12:00:00"
TEST_EPISODE_DURATION_MINUTES = 5

class TestSmokeTest(unittest.TestCase):

    def test_sanity_check(self):
        self.assertEqual(1, 1)


class TestModelTests(unittest.TestCase):

    def test_create_podcast(self):
        p = Podcast(TEST_PODCAST_NAME, TEST_PODCAST_FEED_URL, TEST_PODCAST_DESCRIPTION)
        
        self.assertIsNotNone(p)
        self.assertEqual(p.title, TEST_PODCAST_NAME)
        self.assertEqual(p.url, TEST_PODCAST_FEED_URL)
        self.assertEqual(p.description, TEST_PODCAST_DESCRIPTION)
        self.assertIsNotNone(p.episodes)
        self.assertEqual(p.episodes, [])


    def test_create_episode(self):
        e = Episode(TEST_EPISODE_NAME, TEST_EPISODE_FEED_URL, TEST_EPISODE_DESCRIPTION, TEST_EPISODE_PUBDATE, TEST_EPISODE_DURATION_MINUTES)
        
        self.assertIsNotNone(e)
        self.assertEqual(e.title, TEST_EPISODE_NAME)
        self.assertEqual(e.url, TEST_EPISODE_FEED_URL)
        self.assertEqual(e.description, TEST_EPISODE_DESCRIPTION)
        self.assertEqual(e.pubdate, TEST_EPISODE_PUBDATE)
        self.assertEqual(e.duration, TEST_EPISODE_DURATION_MINUTES)


    def test_add_episode_to_podcast(self):
        p = Podcast(TEST_PODCAST_NAME, TEST_PODCAST_FEED_URL, TEST_PODCAST_DESCRIPTION)
        e = Episode(TEST_EPISODE_NAME, TEST_EPISODE_FEED_URL, TEST_EPISODE_DESCRIPTION, TEST_EPISODE_PUBDATE, TEST_EPISODE_DURATION_MINUTES)
        
        p.add_episode(e)

        self.assertIsNotNone(p.episodes)
        self.assertEqual(len(p.episodes), 1)

        self.assertIsNotNone(e)
        self.assertEqual(p.episodes[0].title, TEST_EPISODE_NAME)
        self.assertEqual(p.episodes[0].url, TEST_EPISODE_FEED_URL)
        self.assertEqual(p.episodes[0].description, TEST_EPISODE_DESCRIPTION)
        self.assertEqual(p.episodes[0].pubdate, TEST_EPISODE_PUBDATE)
        self.assertEqual(p.episodes[0].duration, TEST_EPISODE_DURATION_MINUTES)


    def test_remove_episode_to_podcast(self):
        p = Podcast(TEST_PODCAST_NAME, TEST_PODCAST_FEED_URL, TEST_PODCAST_DESCRIPTION)
        e = Episode(TEST_EPISODE_NAME, TEST_EPISODE_FEED_URL, TEST_EPISODE_DESCRIPTION, TEST_EPISODE_PUBDATE, TEST_EPISODE_DURATION_MINUTES)
                
        p.add_episode(e)

        self.assertIsNotNone(p.episodes)
        self.assertEqual(len(p.episodes), 1)

        p.remove_episode(TEST_EPISODE_FEED_URL)

        self.assertIsNotNone(p.episodes)
        self.assertEqual(p.episodes, [])


if __name__ == "__main__":
    unittest.main()
