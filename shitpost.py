#!/usr/bin/python

"""
Created on Fri Sep 30 15:15:24 2016

@author: namu

This old project has been repurposed as a twitter bot as
of November 2017.
"""

from getopt import getopt, GetoptError
from os import listdir
from os.path import isfile, join
from random import choice
from sys import argv, exit

# If settings exist, pull the directory setting from there
try:
	from settings import words_directory as _DEFAULT_DIRECTORY
except:
	_DEFAULT_DIRECTORY = "Words"


class Shitposter:
	"""
	Generates sentences using templates
	"""

	_dictionaries = []


	def __init__(self, directory=_DEFAULT_DIRECTORY):
		"""
		Constructor

		@Params
		directory : Directory for the templates
		"""

		self._buildDictionaries(directory)

		# in case we want to rebuild dictionaries,
		# keep the method the same but give the option
		# to call it as a public method
		self.rebuildDictionaries = self._buildDictionaries


	def _buildDictionaries(self, directory):
		"""
		Builds the dictionaries using the templates

		@Params
		directory : Directory for the templates
		"""

		self._dictionaries = []

		# for each file in the directory specified,
		for filename in listdir(directory):
			path = join(directory, filename)
			if not isfile(path):
				continue

			# make a dictionary for it
			word_dictionary = _Dictionary(filename.replace(".txt",""), path)
			self._dictionaries.append(word_dictionary)


	def _generateSentence(self):
		"""
		Generates a sentence using the templates

		@Returns
		A generated sentence
		"""

		# starting off sentence generation with base sentence
		sentence = "%base%"
		still_updating = True

		# until there were no updates in a pass, keep going through
		# each dictionary and replacing %word% with a random word
		while still_updating:
			still_updating = False
			for dictionary in self._dictionaries:
				while "%"+dictionary.getName()+"%" in sentence:
					still_updating = True
					sentence = sentence.replace("%"+dictionary.getName()+"%", dictionary.pick(), 1)

		# this line is for formatting hashtags correctly
		sentence = "||".join([x.replace(" ","").replace("-","") if x[0] == "#" else x for x in sentence.split("||")])

		# this is for removing the bars and any %nul% occurrences
		sentence = sentence.replace("%nul%","").replace("||"," ").replace("|","")

		# strip spaces on either side and return
		return sentence.strip()


	def generate(self, count=1, asParagraph=False):
		"""
		Generates a number of sentences and can display them in certain ways

		@Params
		count       : How many lines of sentences to generate
		asParagraph : If true, each sentence is treated like one of a paragraph

		@Returns
		A number of generated sentences
		"""

		# if displaying just one, write the sentence out
		if count is 1:
			return self._generateSentence()

		sentences = []
		for i in range(count):
			sentences.append(self._generateSentence())

		# else, either number the sentences or write like a paragraph
		if asParagraph:
			return " ".join([sentence+"." for sentence in sentences])

		return "\n".join([str(num+1)+") "+sentence for num, sentence in enumerate(sentences)])


class _Dictionary:
	"""
	A dictionary (not quite the python kind of dict) of
	words to pick from when generating a sentence
	"""

	_name = ""
	_words = []


	def __init__(self, name, path):
		"""
		Constructor
		
		@Params
		name : Name of this dictionary of words
		path : Filepath to the file to read words from
		"""

		with open(path, "r") as f:
			text = f.read()

		# we remove \r incase some files
		# are edited on windows
		dictionary_words = text.replace("\r","").split("\n")

		# in the case that the file was ended with a newline
		if  dictionary_words[-1] == "":
			del dictionary_words[-1]

		self._name = name
		self._words = dictionary_words


	def pick(self):
		"""
		Picks a random word from the list of words

		@Returns
		A random word
		"""

		return choice(self._words)


	def getName(self):
		"""
		Gives the name of this dictionary

		@Returns
		Name of dictionary
		"""

		return self._name;


"""
From here on is for if this is being called on command line.
The original purpose of this project was to be able to generate
shitposts on command line and was a learning experience, but
now it has become a little more.

The functionality of being able to call it from command line
has been retained for extra fun and giggles.
"""

def _usage():
	"""
	Displays the help material for using shitpost
	"""

	print("usage: shitpost [option]...")
	print("make a shitpost all by yourself")
	print("-h, --help        := display help")
	print("-c, --count x     := display x number of posts")
	print("-d, --directory x := use x for directory of words")
	print("-p, --paragraph   := display multiple sentences as a paragraph")
	print("")
	print("example:")
	print("shitpost -h")
	print("shitpost -c 20 -d words")
	print("")
	exit(0)


# if this is being run directly
if __name__ == "__main__":
	
	# defaults
	count_arg = 1
	directory = _DEFAULT_DIRECTORY
	asParagraph = False

	# get the options and arguments
	try:
		options, arguments = getopt(
			argv[1:],
			"hc:d:p",
			["help", "count", "directory", "paragraph"]
		)
	except GetoptError as err:
		print(str(err))
		_usage()

	# set the values to be used in the call
	for opt, arg in options:
		if opt in ["-h", "--help"]:
			_usage()
		elif opt in ["-c", "--count"]:
			count_arg = int(arg)
		elif opt in ["-d", "--directory"]:
			directory = arg
		elif opt in ["-p", "--paragraph"]:
			asParagraph = True
		else:
			assert False, "Unhandled Option"

	shitposter = Shitposter(directory)
	print(shitposter.generate(count_arg, asParagraph=asParagraph))