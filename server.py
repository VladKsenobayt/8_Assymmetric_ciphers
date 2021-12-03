#server
from contextlib import closing
from threading import Thread
import socket, csv
#import assymm
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




def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def gener(i, key_prim, key_publ_m):
    
    while i<3:
        
        i += 1
        #print(i)
        if i == 1:
                key_publ_s = int(conn.recv(1024))
                if check(key_publ_s):
                    msg = str(key_publ_m)
                    conn.send(msg.encode('utf-8'))
                else:
                    print("Error: KeyNotCorrect")
                    global flag
                    flag = False
                    return(False)
        elif i == 2:
                key_part_s = int(conn.recv(1024))
                key_part_m = calc_key(key_publ_s, key_prim, key_publ_m)
                msg = str(key_part_m)
                conn.send(msg.encode('utf-8'))
        elif i == 3:
                #key_full_s = int(conn.recv(1024))
                key_full_m = calc_key(key_part_s, key_prim, key_publ_m)
                with open ('keyserv'+str(addr)+'.txt','w') as f:
                    f.write(str(key_full_m))
    return key_full_m
def calc_key(key_g, key_ab, key_p):
    return key_g ** key_ab % key_p


def poluch():
    global flag
    while flag:
        try:
            #inp=coding(conn.recv(1024).decode('utf-8'),-key_full_m)
            inp=deshifr(conn.recv(1024).decode('utf-8'),key_full_m)
            if inp=='exit':
                print('client out')
                flag = False
            else:
                print('client:', inp)
             #sock.send(data)
        except OSError:
            flag = False
            #continue
   
def check(key_publ_s):
    i = False
    with open ('key_list.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            if line[0] == str(key_publ_s):
                i = True
    return i




flag=True


sock = socket.socket()
#nom=input('input addr: ')
nom = 53480
print('Your port:', nom)
try:
        sock.bind(('', nom))
except OSError:
        nom = find_free_port()
        print('Ошибка. Выбранный вами код сервера уже занят, код сервера будет изменён автоматически. Новый код: ', nom)
        sock.bind(('', nom))
#'''
print('Server activate')
sock.listen(3)
i = 0
conn, addr = sock.accept()
try:
    file = open('keyserv'+str(addr)+'.txt','r')
    key_full_m = file.read()
    file.close()
except:
    key_publ_m = 151
    key_prim = 157
    #conn.send(str(key_publ_m).encode('utf-8'))
    i = 0
    #msg = ''
    key_full_m = str(gener(i, key_prim, key_publ_m))
#print(flag)
if flag:
    print('user addr:', addr)
    port=find_free_port()
    #port=new_port(conn, key_full_m, port)
    msg=shifr(str(port),key_full_m)
    #msg=coding(str(port),key_full_m)
    conn.send(msg.encode('utf-8'))
    
    conn.close()
if flag:
    '''sock = socket.socket()
    sock.bind(('localhost',int(port)))
    sock.listen(1)#'''
    sock=socket.socket()
    sock.bind(('',int(port)))
    sock.listen(3)
    addr2=''
    while True:
        conn, addr2 = sock.accept()
        if addr2 == addr:
            break
        else:
            conn.close()
    stream = Thread(target= poluch)
    stream.start()
    while flag:
        msg=input('input your message: ')
        if msg == 'exit':
            flag=False
        try:
            msg=shifr(msg,key_full_m)
            conn.send(msg.encode('utf-8'))
        except ConnectionResetError:
            flag=False
    
conn.close()
'''
file = open("keyserv.bin", "rb")
    key = file.read()
    file.close()
#'''
