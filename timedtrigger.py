from datetime import datetime
from cronex import CronExpression
from threading import Thread
from time import gmtime, sleep, time


class TimedTrigger:
	"""
	Calls a method (with no arguments) on a timer
	"""

	_job = None
	_method = None
	_messages = {}


	def __init__(self, method, cron_expression, custom_messages = {}):
		"""
		Constructor

		@Params
		method                : Method to be called when the timer is triggered
		minutes_between_posts : Time between calls of the method in minutes
		custom_messages       : Custom log messages for console
		"""

		self._messages = {
			"triggering": "Triggering",
			"starting": "Starting",
			"syncing": "Syncing",
			"exiting": "Exiting"
		}

		# if only a few messages were chosen, overwrite those ones
		# rather than leave the others blank
		if custom_messages is not {}:
			for message in custom_messages:
				self._messages[message] = custom_messages[message]

		self._job = CronExpression(cron_expression + " Run timed method")
		self._method = method


	def start(self):
		"""
		Begins the timer and starts triggering the method
		"""

		self._log(self._messages["starting"])

		while True:
			try:
				# if we are not triggering, wait a minute so
				# we dont cause the CPU to commit seppuku
				#
				# for the first pass we wait until the start
				# of a new minute anyway
				self._wait_until_next_minute()

				# check if we are in a minute to trigger on
				if self._job.check_trigger(gmtime(time())[:5]):

					# run the method
					self._run_method()

			# if there is a keyboard interrupt during this,
			# stop the loop please
			except KeyboardInterrupt:
				break

		self._log(self._messages["exiting"])


	def _log(self, message):
		"""
		Displays a message with the current time as a timestamp

		@Params
		message : Message to display in console
		"""

		print("\r[%s] %s" % (str(datetime.now()), message))


	def _run_method(self):
		"""
		Creates a thread for the method and calls it.

		Threading is used to call the method. This is done in case
		the method takes significant time to complete
		"""

		thread = Thread(target=self._method)
		self._log(self._messages["triggering"])
		thread.start()


	def _wait_until_next_minute(self):
		"""
		Waits until the start of a minute.
		"""

		time_to_wait = 60-gmtime(time())[5]
		sleep(time_to_wait)


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
		print("Method is starting")
		sleep(10)
		print("Count is currently: "+str(count))
		
	a = TimedTrigger(exampleMethod, "* * * * *", custom_messages = custom_messages)
	a.start()