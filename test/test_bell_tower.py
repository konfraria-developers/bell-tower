import unittest

import os
import datetime

from bell_tower import BellTower



class TestUM(unittest.TestCase):
    credentials_dir = os.path.abspath('test/data/mock_credentials.json')
    data_dir = os.path.abspath('data')

    def setUp(self):
        self.bt = BellTower(self.credentials_dir, self.data_dir)

    def test_01_load_credentials(self):
        self.bt.load_credentials()

        self.assertNotEqual(self.bt.credentials, None)
        self.assertEqual(len(self.bt.credentials), 4)
        self.assertNotEqual(self.bt.api, None)

    def test_02_load_tags(self):
        self.bt.load_tags()
        self.assertNotEqual(self.bt.tags, None)

    def test_03_load_sayings(self):
        self.bt.load_sayings()
        self.assertNotEqual(self.bt.sayings, None)

    def test_04_load_time(self):
        self.bt.load_time()
        self.assertNotEqual(self.bt.time, None)
        self.assertEqual(len(self.bt.time), 48)

    def test_05_simple_tweet(self):
        self.bt.init_bell_tower()

        self.assertNotEqual(self.bt.credentials, None)
        self.assertNotEqual(self.bt.api, None)
        self.assertNotEqual(self.bt.time, None)
        self.assertNotEqual(self.bt.tags, None)

        # good test

        date = datetime.datetime(2016, 5, 22, 19, 0, 0)
        text = self.bt.tweet_mock(date)

        self.assertGreater(len(text), 0)
        self.assertLessEqual(len(text), self.bt.max_tweet_char)

        # bad test

        date = datetime.datetime(2016, 5, 22, 19, 01, 0)

        with self.assertRaises(Exception) as context:
            self.bt.tweet_mock(date)

        self.assertTrue('Minutes must be multiple of 15' in context.exception)

if __name__ == '__main__':
    unittest.main()
