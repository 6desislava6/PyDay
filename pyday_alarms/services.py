import paramiko
import pickle
from pyday.settings import ALARMS_FILE_NAME
from pass_info import password, username

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

    def connect(self, file):
        self.ssh.connect('10.42.0.136', username=self.username,
                         password=self.password)

        sftp = self.ssh.open_sftp()
        sftp.put('/home/me/file.ext', '/remote/home/file.ext')
        stdin, stdout, stderr = self.ssh.exec_command(self.COMMAND.format(message))


def dump_alarms(file_name, alarms):
    with open(file_name, 'wb') as handle:
        pickle.dump(alarms, handle)


def _prepare_alarms(alarms):
    return [(alarm.date, alarm.message) for alarm in alarms]


def update_alarms(user):
    alarms = _prepare_alarms(Alarms.objects.filter(pk=user.id))
    dump_alarms(ALARMS_FILE_NAME)
    # raspberry-то на съответния user
    connector = RaspberryConnector(username, password)

