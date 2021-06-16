import socket
import cv2
import pickle
import numpy as np
import struct 
import zlib
import threading  as t
from time import sleep

def shan(serv_ip='127.0.0.1',serv_port=8486,cam_source=0):
     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sleep(10)
     print('Connect Client part 2')

     client_socket.connect((serv_ip,serv_port))
     connection = client_socket.makefile('wb')
     
     cam = cv2.VideoCapture(cam_source)
     
     img_counter = 0
     
     encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
     
     while True:
         ret, frame = cam.read()
         result, frame = cv2.imencode('.jpg', frame)
     #    data = zlib.compress(pickle.dumps(frame),9)
         data = pickle.dumps(frame,0)
         data = zlib.compress(zlib.compress(data,9),9)
         size = len(data)
     
         print(f"{img_counter}: {size}")
         client_socket.sendall(struct.pack(">L", size) + data)
         img_counter += 1
         if cv2.waitKey() == 8:
             break 

     cam.release()
#t1 = t.Thread(target=shan, args=())
HOST=''
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        #print("Recv: {}".format(len(data)))
        data += conn.recv(9999999999)

#    print("Done Recv: {len(data)}")
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print(f"msg_size: {msg_size}")
    while len(data) < msg_size:
        data += conn.recv(9999999999)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    #frame_data = zlib.decompress(zlib.decompress(frame_data))
  #  frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame=pickle.loads(frame_data)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    if cv2.waitKey(10) == 8:
       close()
       exit(0)

