# Import socket module
import socket


# local host IP '127.0.0.1'
# host = '25.48.108.244'
host = '127.0.0.1'

# Define the port on which you want to connect
port = 9999

def send_message(s,message):

    # message sent to server
    s.send(message.encode('ascii'))

    # messaga received from server
    data = s.recv(1024)

    return data

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

        if string_reply == 'ACK' :
            break
        elif attempt < 3 :
            attempt += 1
            print('Error: Connection will close.')
            continue
        else:
            break
        
    # close the connection
    s.close()

def Main():
    
    for i in range(4):
        message = 'SERA1 INFO 4' + str(i)
        connect_and_send_message(message)

if __name__ == '__main__':
    Main()