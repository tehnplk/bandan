import socket
import time
import datetime

depart='39'
point=2
server='192.168.1.151'
port=1002
print('------------------------------')
print('    Welcome to Smart Queue')
print('******************************')
while True:
    n=raw_input('Scan Barcode HN : ')
    if(n=='exit'):
        print("Bye bye")
        break
    else:
        try:
            s=socket.socket()
            s.connect((server,port))
            hn=n;
            n= "3|" + depart + "|" + n + "|"+ str(point)
            s.send(n.encode())
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Calling  ----------> HN : ",hn ,' Time : ',dt)
            s.close()
        except Exception as e:
            print("Error : ",e)
        else:
            pass
        finally:
            pass
