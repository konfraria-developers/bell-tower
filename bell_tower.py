import os
import sys
import json
import datetime
import random

from TwitterAPI import TwitterAPI

class BellTower(object):

	# internal data
	credentials_path = None
	data_path = None
	credentials = None
	api = None
	tags = None
	sayings = None
	time = None

	# internal attributes
	num_tags = 1
	num_sayings = 1
	periodicity = 15
	max_tweet_char = 140

	"""docstring for BellTower"""
	def __init__(self, credentials_path, data_path):
		self.credentials_path = credentials_path
		self.data_path = data_path

	def init_bell_tower(self):
		self.load_credentials()
		self.load_tags()
		self.load_sayings()
		self.load_time()

	def load_data(self, path_file):
		data = open(path_file, 'r').read()
		return json.loads(data)

	# For testing purpose

	def load_credentials(self):
		self.credentials = self.load_data(self.credentials_path)

		# TwitterAPI
		self.api = TwitterAPI(
			self.credentials['consumer_key'],
			self.credentials['consumer_secret'],
			self.credentials['access_token_key'],
			self.credentials['access_token_secret']
		)

	def load_tags(self):
		self.tags = self.load_data(os.path.join(self.data_path, 'tags.json'))

	def load_sayings(self):
		self.sayings = self.load_data(os.path.join(self.data_path, 'sayings.json'))

	def load_time(self):
		self.time = self.load_data(os.path.join(self.data_path, 'time.json'))

	def tweet_mock(self, date):
		return self.process_date(date)

	# Twitter API implementation

	def process_date(self, date):
		if date.minute % self.periodicity != 0:
			raise Exception('Minutes must be multiple of 15')

		text = ''
		while len(text) <= 0 or len(text) > self.max_tweet_char:
			text = self.process_text(date)
		return text

	def send_tweet(self, text):
		r = self.api.request('statuses/update', {'status': text})
		print('SUCCESS' if r.status_code == 200 else 'FAILURE')

	def tweet(self, date):
		text = process_date(date)
		send_tweet(text)

	def process_text(self, date):
		# build tweet message - hour
		text = self.get_hour(date)
		# build tweet message - saying
		text += '\n%s' % self.get_random_token(self.sayings, date)
		# build tweet message - tag
		text += ' #%s' % self.get_random_token(self.tags, date)
		return text

	def get_hour(self, date):
		# take hour value and parse hour to AM system
		hour = date.hour % 12
		# produce string for time dict
		hour_key = '%s:%s' % (hour, date.minute)
		hour_cat = self.time[hour_key]
		hour_num = str(date).split()[1][:5]
		# hour message
		text = '%s - %s' % (hour_num, hour_cat)
		return text

	def get_random_token(self, tokens, date):
		# get day/month key
		key_day = '%s/%s' % (date.day, date.month)

		if key_day in tokens['day_month']:
			keys_list = ['day_month'] * 50 +          \
						['other'] * 10 +              \
						['month'] * 10 +              \
						['day_week'] * 10 +           \
						['hours_interval'] * 10 +     \
						['season'] * 10
		else:
			keys_list = ['other'] * 20 +              \
						['month'] * 20 +              \
						['day_week'] * 20 +           \
						['hours_interval'] * 20 +     \
						['season'] * 20

		# choose weighted random keys
		key = str(random.choice(keys_list))

		if key == 'day_month':
			key_ = key_day

		elif key == 'month':
			key_ = str(date.month)

		elif key == 'season':
			# seasons definitions
			spring_start = datetime.datetime(date.year, 3, 21)
			spring_end = datetime.datetime(date.year, 6, 21)
			summer_start = datetime.datetime(date.year, 6, 21)
			summer_end = datetime.datetime(date.year, 9, 23)
			autumn_start = datetime.datetime(date.year, 9, 23)
			autumn_end = datetime.datetime(date.year, 12, 21)
			# check current season
			if date > spring_start and date < spring_end:
				key_ = 'spring'
			elif date > summer_start and date < summer_end:
				key_ = 'summer'
			elif date > autumn_start and date < autumn_end:
				key_ = 'autumn'
			else:
				key_ = 'winter'

		elif key == 'day_week':
			key_ = str(date.weekday() + 1)

		elif key == 'hours_interval':
			if date.hour < 6:
				key_ = '0-5'
			elif date.hour < 13:
				key_ = '6-12'
		elif date.hour < 16:
			key_ = '13-15'
		elif date.hour < 21:
			key_ = '16-20'
		else:
			key_ = '21-24'

		# get a random tokens
		if key == 'other':
			tag = random.sample(tokens[key], 1)
		else:
			tag = random.sample(tokens[key][key_], 1)

		return tag[0]

if __name__ == '__main__':

	if len(sys.argv) < 3:
		print '[ERROR] You must provide the path to your Twitter credentials and tags.'
		sys.exit()

	# Get current date
	now = datetime.datetime.now()

	# Instantiate bell tower
	# Internally loads a file with the app credentials,
	# and loads a file with a list of tags to tweet.
	bt = BellTower(sys.argv[1], sys.argv[2])

	# Init data
	bt.init_bell_tower()

	# Tweet in twitter given the current date
	bt.tweet(now)
