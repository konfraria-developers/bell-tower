import sys
import datetime

from bell_tower import BellTower

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
