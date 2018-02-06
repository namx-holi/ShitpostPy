# ShitpostPy
Generates sentences and posts them to twitter.

Written in Python2.7 but it also works in Python3.


## Setup

### Dependencies
* cronex
* googletrans
* tweepy

### Configuration
1. Make a duplicate of **settings_template.py** and name it **settings.py.**
2. Find your Twitter consumer key, access token, and their respective secrets and add them to **settings.py** under the user section.
3. Configure the minutes between posts and syncs per day in **settings.py** under the posts section.
4. Head into the Words directory and set up some formatting for sentence structure using the **example.txt**. Make sure the base sentence is named **base.txt**.
5. If you are going to use a premade *Words* directory, you can set the path to it in **settings.py**.
6. Configure any words that you don't want to be seen in the posts in **restricted_words.txt**.


## Running ShitpostPy
Either doubleclick on **bot.py** or launch from command line. Enjoy!