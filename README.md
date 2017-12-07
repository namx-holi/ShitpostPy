# ShitpostPy
Written in Python
Requires googletrans, schedule, tweepy

Generates sentences and posts them to twitter

## Setup
Make sure you have the requirements installed mentioned at the top of this README.
Make a duplicate of secrets_template.py and name it secrets.py. Find your Twitter consumer key, access token, and their respective secrets and add them to secrets.py.
Head into the Words directory and set up some formatting for sentence structure using the example.txt. Make sure the base sentence is named base.txt.
Open up bot.py and set the sync times and delay between posts right at the top
Run bot.py and it should start creating sentences and posting them to Twitter.