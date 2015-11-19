"""
This is a simple LED demo that demonstrates integration with
Samsung smarthings
"""
import sys
import socket
import select
import json
 
def chat_client():
    host = '52.25.165.62'
    port = 80
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    while 1:
        data = s.recv(4096)
        json_data = json.loads(data)        
        
        if json_data['display_name'] == 'LED #1':
            if json_data['value'] == 'on':
                print 'LED #1 is on'
            else:
                print 'LED #1 is off'
        
        if json_data['display_name'] == 'LED #2':
            if json_data['value'] == 'on':
                print 'LED #2 is on'
            else:
                print 'LED #2 is off'
 
if __name__ == "__main__":
    sys.exit(chat_client())
