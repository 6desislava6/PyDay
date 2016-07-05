import cPickle
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
from message_display import display_messages


# The alarms are tuples: date, message
# It loads all alarms from a pickle file
def load_alarms(file):
    with open(file, 'rb') as handle:
        return cPickle.loads(handle)


# It adds all alarms from the pickle file as jobs
def add_alarms_as_jobs(sched, alarms):
    for alarm in alarms:
        sched.add_job(display_messages,
                      'date', run_date=alarm[0], args=[alarm[1]])

alarms = load_alarms(sys.argv[1])
sched = BlockingScheduler()
add_alarms_as_jobs(sched, alarms)
sched.start()


