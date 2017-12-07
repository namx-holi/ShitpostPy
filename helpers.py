from googletrans import Translator
from secrets import *
from shitpost import *
import re
import tweepy

# create defaults
translator = Translator()
max_passes = 20
lets_get_x_trending_pattern = re.compile("lets get #.* trending")
# rarely but not never does translating certian things many times just
# creates bad words. DO NOT WANT
bad_words = ["rape", "shooting"]

def _malform(text, translator=translator, lang='ja', max_passes=20):
    """munts a sentence with google translate"""
    for i in range(max_passes):
        #print("Translating")
        previous = text
        temp = translator.translate(text, dest=lang)
        text = translator.translate(temp.text, dest='en').text
        if previous == text:
            break
    return text


def createTweet(translator=translator, max_passes=max_passes):
    """creates a post and mangles it with google translate"""
    initial_text = getShitpost()

    if lets_get_x_trending_pattern.match(initial_text):
        tweet = initial_text[0].upper() + initial_text[1:]
    else:
        while True:
            split_text = initial_text.split(" ")
            text=[]
            hashtags=[]
            for word in split_text:
                if word:
                    if word[0] is not "#":
                        text.append(word)
                    else:
                        hashtags.append(word)
            text = " ".join(text)
            hashtags = " ".join(hashtags)
            text = _malform(text, max_passes=max_passes)
            tweet = " ".join([text, hashtags]).strip()
            for word in bad_words:
                if word in tweet.split(" "):
                    initial_text = getShitpost()
                    continue
            break
    
    return tweet


def postTweet(tweet):
    """posts a tweet"""
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
    api = tweepy.API(auth)
    api.update_status(tweet)

def _debug(x=20):
    while 1:print(createTweet(max_passes=x))
