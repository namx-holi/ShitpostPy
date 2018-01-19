#!/usr/bin/python

"""
PLEASE PUT MY SON TO GOOD USE

@parent : Namx-Holi
@born   : November 1st, 2017
"""


from helpers import SentenceMalformer, Tweeter
from shitpost import Shitposter
from timedtrigger import TimedTrigger

from settings import user as USER
from settings import posts as POSTS
from settings import posting_to_twitter as DO_POST


class Bot:
	"""
	Bot that posts generated sentences on a timer
	"""

	_shitposter = None
	_malformer = None
	_tweeter = None
	_timer = None
	_bad_words = []
	_DEBUG = False


	def __init__(self, user, cron_expression, custom_messages=None):
		"""
		Constructor

		@Params
		user            : User credentials imported from settings
		cron_expression : Expression to use for posting times
		custom_messages : Messages to use when logging
		"""

		self._shitposter = Shitposter()
		self._malformer = SentenceMalformer(["ja", "yi", "sw"], 20)
		self._tweeter = Tweeter(user)

		if not DO_POST:
			self._tweeter._POSTING = False

		if custom_messages is None:
			custom_messages = {
				"starting": "Shitposting is starting from now",
				"triggering": "Creating new sentence",
				"syncing": "Syncing"
			}

		self._timer = TimedTrigger(
			self._postTweet,
			cron_expression,
			custom_messages=custom_messages)

		self._loadRestrictedWords()


	def start(self):
		"""
		Kicks off the scheduled timer
		"""

		self._timer.start()


	def _postTweet(self):
		"""
		Generates a sentence and posts it to Twitter
		"""

		while True:
			# generate one sentence and check if it has a bad word
			sentence = self._shitposter.generate(1)
			if self._containsBadWord(sentence):
				continue

			# mangle it and check if the translated version has a bad word
			new_sentence = self._malformer.malform(sentence)
			if self._containsBadWord(new_sentence):
				continue

			# if everything is okay, exit the loop
			break
		
		if self._DEBUG:
			post = "Original:"+sentence+"\n"+"New and Improved:"+new_sentence
		else:
			post = new_sentence

		self._tweeter.tweet(post)


	def _containsBadWord(self, sentence, exact=True):
		"""
		Checks if a sentence contains a bad word. If exact is false,
		this will check for if a restricted word is contained within a word.
		Otherwise this just checks if there is an exact match.

		@Params
		sentence : The sentence to check for restricted words
		exact    : If looking for an exact match

		@Returns
		True if a restricted word is contained in the sentence
		"""
		
		for word in self._bad_words:
			if exact:
				if word in sentence.split(" "):
					return True
			else:
				if word in sentence:
					return True
		return False


	def _loadRestrictedWords(self, path = "restricted_words.txt"):
		"""
		Loads words to not use when posting

		@Params
		path : Path to the file containing restricted words
		"""
		
		with open(path, "r") as f:
			text = f.read()
		self._bad_words = [bad_word for bad_word in text.split("\n") if bad_word is not ""]


if __name__ == "__main__":
	bot = Bot(USER, POSTS["CRON_EXPRESSION"], POSTS["MESSAGES"])
	bot.start()