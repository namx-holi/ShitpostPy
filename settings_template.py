# Twitter credentials
user = {
	"CONSUMER_KEY": "",
	"CONSUMER_SECRET": "",

	"ACCESS_TOKEN": "",
	"ACCESS_TOKEN_SECRET": ""
}

posts = {
	# cron expression used to create posts
	#
	# first number is the minute of the hour
	# second number is the hour of the day
	# third number is the day of the month
	# fourth number is the month of the year
	# fifth number is the day of the week
	#
	# a number denotes on that unit of its place
	# a star denotes every unit of its place
	# */x means every x units of its place
	"CRON_EXPRESSION": "0 */2 * * *",

	# messages to use on logging
	"MESSAGES": {
		"starting": "Shitposting is starting from now",
		"triggering": "Creating new sentence",
		"syncing": "Syncing",
		"exiting": "Exiting"
	}
}

# Directory where the words are
words_directory = "Words"

# If the post should actually be posted
posting_to_twitter = False