from googletrans import Translator
from random import choice
import re
from tweepy import API, OAuthHandler


class Tweeter:
	"""
	Handler for posting tweets
	"""

	_api = None
	_DEBUG = False


	def __init__(self, user):
		"""
		Constructor

		@Params
		user : User credentials imported from settings
		"""

		auth = OAuthHandler(user["CONSUMER_KEY"], user["CONSUMER_SECRET"])
		auth.set_access_token(user["ACCESS_TOKEN"], user["ACCESS_TOKEN_SECRET"])
		api = API(auth)
		self._api = api


	def tweet(self, message):
		"""
		Posts a message to twitter

		@Params
		message : Message to tweet
		"""

		if self._DEBUG:
			print("Updating status with : \n\n"+message+"\n\n")
		try:
			self._api.update_status(message)
		except Exception as err:
			print(err)


class SentenceMalformer:
	"""
	Mangles a sentence by translating it to and from languages
	"""

	_translator = None
	_passes = 0
	_languages = []
	_DEBUG = False
	_skipping_regexes = []
	

	def __init__(self, langs = ["ja"], passes = 20, skipping_regexes = []):
		"""
		Constructor

		@Params
		langs            : List of languages to pick from when translating
		passes           : Number of translations to go through before returning the sentence
		skipping_regexes : If the generated sentence fits any of these formats, it won't get mangled
		"""

		self._translator = Translator()
		self._languages = langs + ["en"]
		self._passes = passes

		for regex in skipping_regexes:
			self._skipping_regexes.append(re.compile(regex))


	def malform(self, string):
		"""
		Malforms a string by translating it several times
		
		@Params
		string : Sentence to malform
		
		@Returns
		Malformed sentence
		"""

		# if the sentence matches any of the skipping regexes, just return it
		for regex in self._skipping_regexes:
			if regex.match(string):
				return string

		last_lang = "en"
		for i in range(self._passes - 1):
			if self._DEBUG:
				try:
					print(last_lang + " : " + string)
				except:
					print(last_lang + " : " + "Could not display")

			# choose a random language that wasn't the last language and translate it
			lang = choice([lang for lang in self._languages if lang is not last_lang])
			string = self._translator.translate(string, dest=lang).text
			last_lang = lang

		# make sure the last pass is to english
		string = self._translator.translate(string, dest="en").text

		string = self._fixHashtags(string)
		return string


	def _fixHashtags(self, string):
		"""
		Fixes up hashtags after being malformed

		If a sentence is in the format:
			"The quick brown # fox jumps over # lazy #dog"

		This will make the sentence into:
			"The quick brown #FoxJumpsOver #Lazy #Dog"

		@Params
		string : String to fix up hashtags of

		@Returns
		Sentence with fixed up hashtags
		"""

		if string.count("#") < 1:
			return string
		temp = string.split("#")
		hashtags = ["#"+hashtag.title().replace(" ","") for hashtag in temp[1:] if hashtag.strip() is not u""]
		return temp[0] + " ".join(hashtags)


if __name__ == "__main__":
	malformer = SentenceMalformer(["ja", "yi", "sw"], 20)
	malformer._DEBUG = True
	sentence = malformer.malform("It's over Anakin, I have the high ground")
	print(sentence)