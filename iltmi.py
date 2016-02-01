from paramiko import SSHClient, SFTPClient
from scp import SCPClient
import srvConnect
import os
import re
import getopt
import sys

def move(server, src, dst, direction, debug, pat=None):
    ssh = srvConnect.srv_connect(server)
    sftp = ssh.open_sftp()

    def single_file(src=src, dst=dst):
        if os.path.isdir(dst) and direction == 'put':
            exit()
        if os.path.isdir(dst):
            dst = dst + '/' + src.split('/')[-1]
            print dst
        if direction == 'put':
            sftp.put(src, dst)
        elif direction == 'get':
            sftp.get(src, dst)

    def multi_file():
        files = sftp.listdir(src)
        for filename in files:
            if debug: print "Mathing file " + filename + " in " + src
            matched = re.search(pat, filename)
            if matched:
                if debug: print "Matched file: " + matched
                src_file = os.path.join(src, filename)
                dst_file = dst + '/' + os.path.basename(filename)
                single_file(src_file, dst_file)

    if debug:
        print "Server: " + server + " Source: " + src + " Destination " + dst + " Direction " + direction + " Pattern " + pat
    if pat: multi_file()
    else: single_file()

    ssh.close()


def main(argv):
    method = 'get'
    pat = None
    debug = False

    try:
        opts, args = getopt.getopt(argv, "n:s:d:m:p:v:")
    except getopt.GetoptError:
        print 'usage: iltmi.py -n server -s /path/to/file -d /path/to/destination/ [-m [get|put]] [-p regex]'
        sys.exit(2)

    print opts

    for opt, arg in opts:
        if debug: print opt, arg
        if opt == '-h':
            print "usage: iltmi.py -n server -s /path/to/file -d /path/to/destination/ [-m [get|put]] [-p regex]"
            # sys.exit(0)
        elif opt == '-n': server = arg
        elif opt == '-s': src = arg
        elif opt == '-d': dst = arg
        elif opt == '-m': method = arg
        elif opt == '-p': pat = arg
        elif opt == '-v': debug = True

    # server = "rnd"
    # src = "/home/copypaste/dir/"
    # dst = "/tmp/testdir/"
    # method = "get"
    # pat1 = '\.txt$'
    if pat: pat = r'' + re.escape(pat) + ''
    if server and src and dst and method:
        move(server, src, dst, method, debug, pat)

if __name__ == "__main__":
    main(sys.argv[1:])
