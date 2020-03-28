import sys
import socket
for i in range(1,65535):
    s   =   socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:    s.connect((sys.argv[1],i))
    except: pass
print('DONE')
        
