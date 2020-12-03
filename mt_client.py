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
        
         #Example reply :ACK,TEMP 16
        replies = string_reply.split(",") 
        print("Connection: " + replies[0])
        if replies[0] == 'ACK' :

            target_temp  =replies[1].split(" ")[1]   #OK or target temp
            if  target_temp == "OK":
                print("No need to heat")
            else:
                print("Heat until " + target_temp+" C is reached")
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

def Main():
    
    for i in range(1,2):
        message = 'SERA{} TEMP 16'.format(i)
        connect_and_send_message(message)

if __name__ == '__main__':
    Main()