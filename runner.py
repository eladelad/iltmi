from iltmi import move
import json

conf_file = "move_list.json"

conf_file_h = open(conf_file, 'r')
conf = conf_file_h.read()
moves_dict = json.loads(conf)
moves_dict = moves_dict['moves']

for move_inst in moves_dict:
    method = 'get'
    pat = None
    debug = False
    if 'debug' in move_inst: debug = move_inst['debug']
    if 'pat' in move_inst: pat = move_inst['pat']
    if 'method' in move_inst: method = move_inst['method']
    if 'server' in move_inst and 'src' in move_inst and 'dst' in move_inst:
        if debug: print move_inst['server'], move_inst['src'], move_inst['dst'], method, debug, pat
        move(move_inst['server'], move_inst['src'], move_inst['dst'], method, debug, pat)
