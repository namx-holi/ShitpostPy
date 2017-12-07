from datetime import datetime
from helpers import *
import schedule
import threading
import time

# Times of the day to resync the timer
reset_time_1 = "16:20"
reset_time_2 = "4:20"

# Delay between posts in minutes
post_delay = 20

def log(message):
    """
    Displays a message with timestamp in console
    """
    print "[%s] %s" % (str(datetime.now()), message)

def do_post():
    """
    Generates a tweet and posts it
    """
    log("Posting tweet.")
    tweet = createTweet()
    postTweet(tweet)

def job():
    """
    Creates and starts a thread that creates the post.
    Threading is used as sometimes generating a post can take
    a little while and that sets the timer even more out
    of sync
    """
    thread = threading.Thread(target=do_post)
    thread.start()

def syncTimer():
    schedule.clear()
    schedule.every(post_delay).minutes.do(job)
    schedule.every().day.at(reset_time_1).do(syncTimer)
    schedule.every().day.at(reset_time_2).do(syncTimer)
    log("Synced timer.")
    job()

def main():
    log("Started schedule.")
    schedule.every().day.at(reset_time_1).do(syncTimer)
    schedule.every().day.at(reset_time_2).do(syncTimer)
    while True:
        schedule.run_pending()
        time.sleep(1)


main()
