from multiprocessing import Process 
import os 
import socket 
from _thread import * 
import threading 
import time 
from threading import Thread 
import logging
import random

def consumer(conn):
    print("consumer accepted connection" + str(conn) + "\n")
    msg_queue = []
    sleepVal = 1/random.randint(1,6)
    clock = 0

    while True:
        time.sleep(sleepVal)

        if len(msg_queue) > 0:
            msg = msg_queue.pop(0)
            clock += 1
            print("Message received: " + time.time() + ", " + len(msg_queue) + ", " + clock)
        else:
            n = random.randint(1,10)
            if n == 1:
                # send to one of the other machines a message that is the local logical clock time
                clock += 1
                print("Message sent: " + time.time() + ", " + clock)
            elif n == 2:
                # send to the other machine a message that is the local logical clock time
                clock += 1
                print("Message sent: " + time.time() + ", " + clock)
            elif n == 3:
                # send to both of the other virtual machines a message that is the logical clock time
                clock += 1
                print("Message sent: " + time.time() + ", " + clock)
            else:
                clock += 1
                print("Message sent: " + time.time() + ", " + clock)





        data = conn.recv(1024)
        print("msg received\n")
        dataVal = data.decode('ascii')
        print("msg received:", dataVal)
        msg_queue.append(dataVal)

        clock += 1



def producer(portVal):
    host = "127.0.0.1"
    port = int(portVal)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sleepVal = 0.500
    # sema acquire
    try:
        s.connect((host,port))
        print("Client-side connection success to port val:" + str(portVal) + "\n")

        while True:
            codeVal = str(code)
            time.sleep(sleepVal)
            s.send(codeVal.encode('ascii'))
            print("msg sent", codeVal)

    except socket.error as e: print ("Error connecting producer: %s" % e)



def init_machine(config):
    HOST = str(config[0])
    PORT = int(config[1])
    print("starting server| port val:", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,))

def machine(config):
    config.append(os.getpid())
    global code
    # print(config)
    init_thread = Thread(target=init_machine, args=(config,))
    init_thread.start()
    
    # add delay to initialize the server-side logic on all processes 
    time.sleep(5)
    
    # extensible to multiple producers 
    prod_thread = Thread(target=producer, args=(config[2],))
    prod_thread.start()
    
    while True: 
        code = random.randint(1,3)



localHost = "127.0.0.1"
 
if __name__ == '__main__':
    port1 = 2056
    port2 = 3056
    port3 = 4056

    config1 = [localHost, port1, port2]
    p1 = Process(target=machine, args=(config1,))
    config2 = [localHost, port2, port3]
    p2 = Process(target=machine, args=(config2,))
    config3 = [localHost, port3, port1]
    p3 = Process(target=machine, args=(config3,))

    logging.basicConfig(filename='machine' + port1 + '.log', encoding='utf-8', level=logging.DEBUG)
    logging.basicConfig(filename='machine' + port2 + '.log', encoding='utf-8', level=logging.DEBUG)
    logging.basicConfig(filename='machine' + port3 + '.log', encoding='utf-8', level=logging.DEBUG)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()