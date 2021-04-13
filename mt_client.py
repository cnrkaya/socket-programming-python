# Import socket module
import socket
import serial 

DATA_LENGTH = 128
MESSAGE_DISCONNECT = 'DISCONNECT'
MESSAGE_FORMAT = 'utf-8'

COM = 'COM2'
BAUD = 9600
client_name = 'SERA3'

# local host IP '127.0.0.1'
host = '127.0.0.1'

# Define the port on which you want to connect
port = 9999

serial_communication = serial.Serial(COM, BAUD, parity=serial.PARITY_NONE, stopbits=1)

def send_message(s,message):

    # message sent to server
    s.send(message.encode('ascii'))

    # messaga received from server
    data = s.recv(1024)

    return data

def send_data_to_microprocessor(serial_communication, message):
    serial_communication.write(message.encode())
    print('Message sent to microprocessor : ' + str(message))
    return

def connect_and_send_message(message):

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host,port))



    attempt = 0
    while True:

        reply = send_message(s,message)

        string_reply = str(reply.decode('ascii'))

        # print the received message
        print('Received from the server :',string_reply)
        
        #Example reply :ACK,TEMP 16
        replies = string_reply.split(",") 
        print("Connection: " + replies[0])
        if replies[0] == 'ACK' :

            target_temp  =replies[1].split(" ")[1]   #OK or target temp
            if  target_temp == "OK":
                print("No need to heat")
            else:
                print("Heat until " + target_temp+" C is reached")
                send_data_to_microprocessor(serial_communication,target_temp)
            break
        elif attempt < 2 :
            attempt += 1
            print('Error{}'.format(attempt))
            continue
        else:
            print('3 Attempt failed,the connection will close')
            break
        
    # close the connection
    s.close()

def get_greenhouse_temp():
    message = serial_communication.readline()
    print(message)
    message = message[:2]
    if message != '':
        return str(message.decode(MESSAGE_FORMAT))
    return 0

def Main():
    temp = get_greenhouse_temp()
    print('Read temperature : ' + str(temp))
    message = client_name + ' TEMP ' + temp
    connect_and_send_message(message)

import time
val = 0
start_time = time.time()
if __name__ == '__main__':
    start_time = time.time()
    seconds = 10


    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > seconds:
            val += seconds
            print("Finished iterating in: " + str(val))
            start_time = time.time()
            message = client_name + ' TEMP ' + str(get_greenhouse_temp())
            connect_and_send_message(message)

    #Main()