import bluetooth
import sys
bd_addr = "20:16:04:26:05:68"

port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print('Connected')
sock.settimeout(10.0)

count = 0;
while(count < 6):
    data_sent = {
        0: 'T',
        1: 'e',
        2: 's',
        3: 't',
        4: '1',
        5: '#',
    }
    sock.send(data_sent[count])
    data = ''
    data = sock.recv(1024).decode()
    print('received: %s'%data)

    count += 1

sock.close
sock.disconnect((bd_addr, port))
