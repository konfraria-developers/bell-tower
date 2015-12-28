import sys
import json
import datetime
import random

from TwitterAPI import TwitterAPI

class BellTower(object):
    """docstring for BellTower"""
    def __init__(self, credentials_path, data_path):
        # internal data
        self.credentials = self.load_credentials(credentials_path)
        self.tags, self.special_tags, self.time = self.load_data(data_path)

        # TwitterAPI
        self.api = TwitterAPI(
            self.credentials['consumer_key'],
            self.credentials['consumer_secret'],
            self.credentials['access_token_key'],
            self.credentials['access_token_secret']
        )

        # internal attributes
        self.max_tweet_char = 140
        self.num_tags = 3

    def load_data(self, path_file):
        data = open(path_file, 'r').read()
        data_json = json.loads(data)
        return data_json['tags'], data_json['special_tags'], data_json['time']

    def load_credentials(self, path_file):
        data = open(path_file, 'r').read()
        return json.loads(data)

    def tweet(self, date):
        text = ''
        while len(text) <= 0 or len(text) > self.max_tweet_char:
            text = self.process_text(date)

        r = self.api.request('statuses/update', {'status': text})
        print('SUCCESS' if r.status_code == 200 else 'FAILURE')

    def process_text(self, date):

        # take hour value and parse hour to AM system
        hour = date.hour % 12

        # produce string for time dict
        hour_key = '%s:%s' % (hour, date.minute)
        hour_cat = self.time[hour_key]
        hour_num = str(date).split()[1][:5]

        # build tweet - HOUR
        text = '%s - %s ' % (hour_num, hour_cat)

        # get day/month key
        month_day_key = '%s/%s' % (date.day, date.month)

        # build tweet - catch random TAGS
        if month_day_key in self.special_tags:
            tags = random.sample(self.special_tags[month_day_key],
                                 self.num_tags)
        else:
            tags = random.sample(self.tags, self.num_tags)

        # append tags tot tweet
        for t in tags:
            text = text + '#%s ' % t

        return text

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print '[ERROR] You must provide the path to your Twitter credentials and tags.'
        sys.exit()

    # Get current date
    now = datetime.datetime.now()

    # Instantiate bell tower
    # Internally loads a file with the app credentials,
    # and loads a file with a list of tags to tweet.
    bell = BellTower(sys.argv[1], sys.argv[2])

    # Tweet in twitter given the current date
    bell.tweet(now)