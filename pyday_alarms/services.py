import paramiko
import pickle
from pyday.settings import ALARMS_FILE_NAME, ALARMS_FILE_NAME_REMOTE
from pyday_alarms.pass_info import password, username
from pyday_alarms.models import Alarm
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
        self.ssh.connect('10.42.0.136', username=self.username,
                         password=self.password)
        self._update_alarms()
        stdin, stdout, stderr = self.ssh.exec_command(COMMANDS[1])
        print(stdout)

    def _update_alarms(self):
        sftp = self.ssh.open_sftp()
        sftp.put(ALARMS_FILE_NAME, ALARMS_FILE_NAME_REMOTE)


def dump_alarms(alarms):
    with open(ALARMS_FILE_NAME, 'wb') as handle:
        pickle.dump(alarms, handle, 2)


def _prepare_alarms(alarms):
    return [(alarm.date, alarm.message) for alarm in alarms]


def update_alarms(user):
    alarms = _prepare_alarms(Alarm.objects.filter(user_id=user.id))
    print(alarms)
    dump_alarms(alarms)
    # raspberry-то на съответния user - IP адрес,
    RaspberryConnector(username, password).run_alarms()
