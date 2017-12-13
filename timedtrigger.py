from datetime import datetime
from math import ceil
import schedule
from threading import Thread
from time import sleep


# Used to make the maths a little more easy to read
_DAY_LENGTH = 86400
_HOUR_LENGTH = 3600


class TimedTrigger:
	"""
	Calls a method (with no arguments) on a timer
	"""

	_delay = 0
	_sync_times = []
	_syncs_per_day = 0
	_method = None
	_messages = {}


	def __init__(self, method, minutes_between_posts, syncs_per_day, custom_messages = {}):
		"""
		Constructor

		Params
		method                : Method to be called when the timer is triggered
		minutes_between_posts : Time between calls of the method in minutes
		syncs_per_day         : How often to resync the timer with the clock
		custom_messages       : Custom log messages for console
		"""

		self._messages = {
			"triggering": "Triggering",
			"starting": "Starting",
			"syncing": "Syncing"
		}

		# if only a few messages were chosen, overwrite those ones
		# rather than leave the others blank
		if custom_messages is not {}:
			for message in custom_messages:
				self._messages[message] = custom_messages[message]

		self._delay = minutes_between_posts * 60
		self._syncs_per_day = syncs_per_day
		self._method = method
		self._generateSyncTimes()


	def start(self):
		"""
		Begins the timer and starts triggering the method
		"""

		self._log(self._messages["starting"])
		for sync_time in self._sync_times:
			schedule.every().day.at(sync_time).do(self._sync)

		# because the schedule doesn't exist for calling the method
		# before the first sync, we just add the first sync time for
		# a call to the method
		schedule.every().day.at(self._sync_times[0]).do(self._job)

		while True:
			schedule.run_pending()
			sleep(1)


	def _log(self, message):
		"""
		Displays a message with the current time as a timestamp

		Params
		message : Message to display in console
		"""

		print("[%s] %s" % (str(datetime.now()), message))


	def _job(self):
		"""
		Creates a thread for the method and calls it.

		Threading is used to call the method. This is done in case
		the method takes significant time to complete
		"""

		thread = Thread(target=self._method)
		self._log(self._messages["triggering"])
		thread.start()


	def _generateSyncTimes(self):
		"""
		Generates sync times to use as exact times to sync the clock rather
		than possibly unreliable "in 20 minutes" schedules.
		"""

		current_second = self._getCurrentSecond()

		# Calculating the time of the next trigger of the method
		next_trigger = (1 + ceil(current_second/self._delay))*self._delay

		sync_delay = _DAY_LENGTH / self._syncs_per_day

		# How the timer is written, if there are more syncs than calls in a day,
		# the calls will never be made. This is a current limitation of the timer.
		if sync_delay < self._delay:
			raise Exception("Delay between syncs is shorter than delay between calls to method")

		# The first sync time will always be the same time of the next trigger call.
		# All other sync times are calculated using this next trigger call as
		# the starting point.
		self._sync_times = [
			self._format_seconds(
				(sync * sync_delay + next_trigger) % _DAY_LENGTH
			) for sync in range(self._syncs_per_day)]


	def _sync(self):
		"""
		Syncs the timer.

		Essentially rewrites the schedule. This is probably not the best way
		to sync the timers but this was the best way that I could come up with.
		"""

		schedule.clear()
		self._log(self._messages["syncing"])
		for sync_time in self._sync_times:
			schedule.every().day.at(sync_time).do(self._sync)
		schedule.every(self._delay).seconds.do(self._job)


	def _getCurrentSecond(self):
		"""
		Gets current time of the day as seconds from midnight

		Returns
		Number of seconds from the start of the day
		"""

		current_datetime = datetime.now()
		current_second = (
			current_datetime.second +
			current_datetime.minute * 60 +
			current_datetime.hour * 3600
		)
		return current_second


	@staticmethod
	def _format_seconds(input_seconds, show_hours=True, show_minutes=True, show_seconds=False):
		"""
		Formats time into hh:mm:ss, or the same but without hh or mm or ss.

		Params
		input_seconds : Time of the day in seconds
		show_hours    : Show hours in hh:mm:ss?
		show_minutes  : Show minutes in hh:mm:ss?
		show_seconds  : Show seconds in hh:mm:ss?

		Returns
		Time formatted in hh:mm:ss
		"""

		hours = input_seconds // (60*60)
		input_seconds %= (60*60)
		minutes = input_seconds // 60
		seconds = input_seconds % 60

		formatting_string = ":".join(["%02i"]*(show_hours + show_minutes + show_seconds))
		formatting_tuple = []
		if show_hours: formatting_tuple.append(hours)
		if show_minutes: formatting_tuple.append(minutes)
		if show_seconds: formatting_tuple.append(seconds)
		formatting_tuple = tuple(formatting_tuple)

		return formatting_string % formatting_tuple


if __name__ == "__main__":
	
	count = 0

	custom_messages = {
		"starting": "Example timed trigger is starting",
		"triggering": "Example method is being called now",
		"syncing": "The timer method is syncing now"
	}

	def exampleMethod():
		"""
		Just increases count by 1 and prints what it is.
		"""
		global count
		count = count + 1
		print("A method has been called. Count is currently: "+str(count))
		
	a = TimedTrigger(exampleMethod, 1, 720, custom_messages = custom_messages)
	a.start()