import cv2
import socket
import struct
import pickle
import zlib
import threading
def shan():
     
     HOST=''
     PORT=8486
     
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
             data += conn.recv(4096)
     
#    print("Done Recv: {len(data)}")
         packed_msg_size = data[:payload_size]
         data = data[payload_size:]
         msg_size = struct.unpack(">L", packed_msg_size)[0]
         print(f"msg_size: {msg_size}")
         while len(data) < msg_size:
             data += conn.recv(4096)
         frame_data = data[:msg_size]
         data = data[msg_size:]
         frame_data = zlib.decompress(zlib.decompress(frame_data))
         frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
         frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
         cv2.imshow('ImageWindow client',frame)
         if cv2.waitKey(10) == 8:
            close()
            exit(0)
#t1 = threading.Thread(target=shan)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8485))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture('rtsp://192.168.137.37:9999/h264_pcm.sdp')
cam.set(3, 320);
cam.set(4, 240);
img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame)
#    data = zlib.compress(pickle.dumps(frame),9)
    data = pickle.dumps(frame)
   # data = zlib.compress(zlib.compress(data,9),9)
    size = len(data)

    print(f"{img_counter}: {size}")
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
    if cv2.waitKey() == 8:
       break 

cam.release()