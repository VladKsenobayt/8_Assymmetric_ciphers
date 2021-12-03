import socket#, assymm
from threading import Thread
#'''
from binascii import hexlify, unhexlify
from itertools import cycle
def shifr(shifrovka, key):
    cipher = xor_str(shifrovka, key)
    return (hexlify(cipher.encode())).decode()

def deshifr(shifrovka, key):
    shifrovka = (unhexlify(shifrovka.encode())).decode()
    return xor_str(shifrovka, key)


def xor_str(a, b):
    return ''.join([chr(ord(x)^ord(y)) for x, y in zip(a, cycle(b))])#'''


def gener(i, key_prim, key_publ_m):
    
    while i<3:
        i += 1
        #print(i)
        if i == 1:
                msg = str(key_publ_m)
                sock.send(msg.encode('utf-8'))
                try:
                    key_publ_s = int(sock.recv(1024))
                except ValueError:
                    print("Error: KeyNotCorrect")
                    global flag
                    flag = False
                    return(False)
        elif i == 2:
                key_part_m = calc_key(key_publ_m, key_prim, key_publ_s) 
                msg = str(key_part_m)
                sock.send(msg.encode('utf-8'))
                key_part_s = int(sock.recv(1024))
        elif i == 3:
                key_full_m = calc_key(key_part_s, key_prim, key_publ_s)
                #msg = str(key_full_m)
                #sock.send(msg.encode('utf-8'))
                #key_full_s = int(sock.recv(1024))
                #print(key_full_s)
                with open ('keyscl'+str(pr)+'.txt','w') as f:
                    f.write(str(key_full_m))#key_full_s))
    return key_full_m#key_full_s

def calc_key(key_g, key_ab, key_p):
    return key_g ** key_ab % key_p 

def poluch():
    global flag
    while flag:
        try:
            inp=deshifr(sock.recv(1024).decode('utf-8'),key_full_s)
            if inp=='exit':
                print('server out')
                flag = False
            else:
                print('server:', inp)
             #sock.send(data)
        except OSError:
            flag = False
            #continue
            
flag = True

sock = socket.socket()
pr = 5170
try:
    sock.bind(('', pr))
except OSError:
    print('Addr error')
    flag=False
if flag:
    sock.setblocking(1)
    nomser = 53480
    try:
        sock.connect(('localhost', nomser))
        print('connection with server')
    except ConnectionRefusedError:
        print('Server not online')
        flag=False
if flag:
    try:
        #file_name=input('input :')
        file = open('keyscl'+str(pr)+'.txt','r')
        key_full_s = file.read()
        file.close()
    except:
        key_prim = 199
        key_publ_m = 197#int(sock.recv(1024))#197
        i = 0
        #msg = ''
        key_full_s = str(gener(i, key_prim, key_publ_m))

if flag:     
    port = deshifr(sock.recv(1024).decode('utf-8'),key_full_s)
    #po
    sock.close()
if flag:
    sock = socket.socket()
    sock.bind(('', pr))
    sock.setblocking(1)
    sock.connect(('localhost', int(port)))#1024))
    stream = Thread(target= poluch)
    stream.start()
    #print(flag)
    while flag:
        msg=input('input your message: ')
        if msg == 'exit':
            flag=False
        try:
            msg =shifr(msg,key_full_s)
            sock.send(msg.encode('utf-8'))
        except ConnectionResetError:
            flag=False
sock.close()
