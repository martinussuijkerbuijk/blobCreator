import socket
import pickle
import time
import random


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
number = 1

dictNeutral = {'name': 'neutral', 'size': random.uniform(0, 2), 'depth': random.randint(1, 4), 'turbulence': random.uniform(0,30), 'file_nr': number}
dictHappy = {'name': 'happy', 'repeat_x': random.randint(1, 3), 'repeat_y': random.randint(1, 3), 'brightness': random.uniform(0.1,1.4), 'file_nr': number}
dictAnger = {'name': 'angry', 'brightness': random.uniform(1, 1.5), 'contrast': random.uniform(1, 2.5), 'file_nr': number}
dictSurprise = {'name': 'surprise', 'brightness': random.uniform(0.4, 1), 'contrast': random.uniform(1, 2), 'file_nr': number}
dictSad = {'name': 'sad', 'brightness': random.uniform(0.3, 1.5), 'contrast': random.uniform(1, 3.5), 'file_nr': number}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    i = 0

    s.connect((HOST, PORT))
    try:
        while True:
            if i == 5:
                msg = pickle.dumps(dictNeutral)
                s.sendall((msg))
                number += 1
            if i == 10:
                msg = pickle.dumps(dictHappy)
                s.sendall((msg))
                number += 1
            if i == 15:
                msg = pickle.dumps(dictAnger)
                s.sendall((msg))
                number += 1
            if i == 20:
                msg = pickle.dumps(dictSurprise)
                s.sendall((msg))
                number += 1
            if i == 25:
                msg = pickle.dumps(dictSad)
                s.sendall((msg))
                number += 1
            else:
                i += 1
                print(i)
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    data = s.recv(1024)
print(repr(data))