# chat_client.py
from hashids import Hashids
import sys, socket, select
import re

def chat_client():
    if(len(sys.argv) < 3) :
        print ('Usage : python chat_client.py hostname username key')
        sys.exit()

    host = sys.argv[1]
    port = int(9009)
    name = sys.argv[2]
    key = sys.argv[3]
#Verschluesseln
    save = Hashids(salt=key)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print ('Verbindung nicht moeglich')
        sys.exit()

    print ('Verbunden. Nachrichten koennen versendet werden')
    sys.stdout.write('[ICH] '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print ('\nServer offline!')
                    sys.exit()
                else :
                    #print data
                    #Cut data to length
                    data_raw = str(data)[2:]
                    data_raw = str(data_raw)[:-1]
                    #print(data_raw)
                    #Decode Data with key
                    data_bin = save.decode(data_raw)
                    #print(data_bin)
                    if data_bin:
                        #print(data_bin)
                        #Turn binary to sting
                        data_bin = '0' + str(data_bin[0])
                        data_bin = re.findall('........',str(data_bin))
                        #print(data_bin)
                        #Decode binary
                        data_decode = str()
                        for char in data_bin:
                            char_bin = int(char, 2)
                            char_ascii = chr(char_bin)
                            data_decode = data_decode + char_ascii
                        sys.stdout.write("\r"); sys.stdout.write(str(data_decode)); sys.stdout.write("\n")
                        sys.stdout.write("[ICH] "); sys.stdout.flush()

            else :
                # user entered a message
                msg_ascii = '[' + name + '] ' + sys.stdin.readline()
                #print('msg_ascii ' + msg_ascii)

                #convert to binary
                msg_bin = bin(0)[2:]
                for char in msg_ascii:
                    #print(char)
                    char = '0' + str(bin(ord(char)))[2:]
                    #Repair Space
                    #print(len(char))
                    if len(char) == int('7'):
                        char = '0' + char

                    #print(char)
                    msg_bin = msg_bin + char

                #print('msg_bin ' + msg_bin)

                #encode binary as int
                msg_encode = save.encode(int(msg_bin))
                #print('msg_encode ' + msg_encode)

                #send Message
                s.send(msg_encode.encode())
                sys.stdout.write('[ICH] '); sys.stdout.flush()

if __name__ == "__main__":

    sys.exit(chat_client())
