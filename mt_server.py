#import firebase libraries
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials

# import socket programming library
import socket

# import thread module
from _thread import *
import threading

import os,sys


working_directory = os.path.dirname(sys.argv[0])
os.chdir(working_directory)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=working_directory+"\green-house_admin.json"

# initialize sdk
cred = credentials.Certificate("green-house_admin.json")
firebase_admin.initialize_app(cred)

# initialize firestore instance
db = firestore.Client()

def read_and_set_firebase(sera_id,current_temp):
    message = "TEMP "

    #Check if there is a heating request
    sera_dict = db.collection(u'GreenHouses').document(u'sera{}'.format(sera_id)).get().to_dict()

    #set sera's new temp
    sera_dict['current_temp'] = current_temp
    db.collection(u'GreenHouses').document(u'sera{}'.format(sera_id)).set(sera_dict)

    if sera_dict['current_temp'] != sera_dict['target_temp']:
        message += str(sera_dict['target_temp'])
    else:
        message +="OK"

    return message

def proccess_request(data):
    #processing request will take place in this function
    #Example command: Sera1 TEMP 14
    commandNum = 3
    commands = data.split(" ")
    
    if len(commands) == commandNum :

        sera_id= commands[0][-1]
        current_temp = commands[2]

        message = read_and_set_firebase(sera_id,current_temp)
        #put_to_firebase(sera_id,current_temp)

        return 'ACK,'+message
    else:
        return 'ERROR,Command size must be {}'.format(commandNum)

# thread fuction
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('No other data, connection will close')

            # lock released on exit
            print_lock.release()
            break

        string_data = str(data.decode('ascii'))

        print('Recieved message: '+string_data )
        reply = proccess_request(string_data)

        print(reply)

        # send reply to client
        c.send(reply.encode('ascii'))

    # connection closed
    c.close()

print_lock = threading.Lock()

def Main():
   # host = '25.48.108.244'
    host = ''
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        conn, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (conn,))
    s.close()


if __name__ == '__main__':
    Main()