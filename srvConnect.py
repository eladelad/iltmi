import json
from paramiko import SSHClient


def srv_connect(server, conf_file='srv_conf'):
    conf_file_h = open(conf_file, 'r')
    conf = conf_file_h.read()
    servers = json.loads(conf)
    if servers[server]:
        server = servers[server]
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(server['host'], username=server['username'], password=server['password'])
        return ssh
    else:
        return None
