from paramiko import SSHClient, SFTPClient
from scp import SCPClient
import srvConnect
import os
import re
import getopt
import sys


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


def main(argv):
    method = 'get'
    pat = None

    for opt, arg in argv:
        if opt == '-h':
            print "usage: iltmi.py -n server -s /path/to/file -d /path/to/destination/ [-m [get|put]] [-p regex]"
        elif opt == '-n': server = arg
        elif opt == '-s': src = arg
        elif opt == '-d': dst = arg
        elif opt == '-m': method = arg
        elif opt == '-p': pat = arg

    #server = "rnd"
    #src = "/home/copypaste/dir/"
    #dst = "/tmp/testdir/"
    #method = "get"
    #pat1 = '\.txt$'
    if pat: pat = r'' + pat + ''
    move(server, src, dst, method, pat)

if __name__ == "__main__":
    main(sys.argv[1:])
