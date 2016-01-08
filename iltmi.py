from paramiko import SSHClient, SFTPClient
from scp import SCPClient
import srvConnect
import os
import re


def move(server, src, dst, direction, pat=None):
    ssh = srvConnect.srv_connect(server)
    sftp = ssh.open_sftp()

    def single_file(src=src, dst=dst):
        if direction == 'put':
            sftp.put(src, dst)
        elif direction == 'get':
            sftp.get(src, dst)

    def multi_file():
        files = sftp.listdir(src)
        for filename in files:
            matched = re.search(pat, filename)
            if matched:
                src_file = os.path.join(src, filename)
                dst_file = dst + '/' + os.path.basename(filename)
                single_file(src_file, dst_file)

    if pat: multi_file()
    else: single_file()

    ssh.close()


def main():
    server = "rnd"
    src = "/home/copypaste/dir/"
    dst = "/tmp/testdir/"
    direction = "get"
    pat1 = '\.txt$'
    pat = r'' + pat1 + ''
    move(server, src, dst, direction, pat)

if __name__ == "__main__":
    main()
