import paramiko
import pickle
from pyday.settings import ALARMS_FILE_NAME, ALARMS_FILE_NAME_REMOTE
from pyday_alarms.pass_info import password, username
from pyday_alarms.models import Alarm
from django.utils import timezone
COMMANDS = ['killall python',
            'python ~/multilineMAX7219/main_script.py ~/alarms.pickle']


# It connects to the raspberry
# copies the new alarms (updated)
# stops main_script.py
# runs it again
class RaspberryConnector:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def run_alarms(self):
        try:
            self.ssh.connect('10.42.0.136', username=self.username,
                             password=self.password, timeout=6)
        except Exception:
            return False
        else:
            self._update_alarms()
            self.ssh.exec_command('killall python')
            stdin, stdout, stderr = self.ssh.exec_command('python ~/multilineMAX7219/main_script.py ~/alarms.pickle')
            return True

    def _update_alarms(self):
        sftp = self.ssh.open_sftp()
        sftp.put(ALARMS_FILE_NAME, ALARMS_FILE_NAME_REMOTE)


def dump_alarms(alarms):
    print(alarms)
    with open(ALARMS_FILE_NAME, 'wb') as handle:
        pickle.dump(alarms, handle, 2)


def _prepare_alarms(alarms):
    return [(alarm.date, alarm.message) for alarm in alarms]


def update_alarms(user):
    delete_unnecessary(user)
    alarms = _prepare_alarms(Alarm.objects.filter(user_id=user.id))
    dump_alarms(alarms)
    return RaspberryConnector(username, password).run_alarms()


def delete_unnecessary(user):
    date = timezone.now()
    alarms = list(filter(lambda x: x.date < date, Alarm.objects.filter(user_id=user.id)))
    for alarm in alarms:
        alarm.delete()
