import socket
import sys
import pygame
import requests
import base64
import os
import pygame.mixer, pygame.time 
import atexit

API='http://192.168.1.8/p_queue/'
HOST = '192.168.1.12'   # Symbolic name, meaning all available interfaces
PORT = 5001 # Arbitrary non-privileged port

def exit_handler():
    s.close()
    
atexit.register(exit_handler)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
    
print('Socket bind complete')

#Start listening on socket
s.listen()
print ('Socket now listening')


def speed_change(fpath, speed=1.0):
    sound=AudioSegment.from_mp3(fpath)
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

#now keep talking with the client
from pygame import mixer

mixer.init(frequency=45500)
def Play(file_path=None,dodel=0):
    try:        
        #song = AudioSegment.from_mp3(file_path)
        #play(speed_change(file_path,1.0))
        
        
        mixer.music.load(file_path)
        mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(100)
        
        if(dodel==1):
            os.remove(file_path)
    except ValueError as e:
        print('error'+e)

while 1:
    #wait to accept a connection - blocking call
    try:
        conn, addr = s.accept()
        print ('Connected with ' + addr[0] + ':' + str(addr[1]))
        data = conn.recv(1024).decode()
        print("From Client :" , data)
        #conn.send(bytes("done",'UTF-8'))
        conn.close()
        if data!='':
            Play('./sound/first.mp3',0)
            Play('./sound/Begin.mp3',0)
            datas=data.replace(chr(4),'').split('|')
            hn=datas[2]
            depart=datas[1]
            point=datas[3]
            
            url = API +"?data_type=patient_sound&hn="+hn+"&depart="+depart
            r = requests.get(url)
            print(url)
            
            files = r.json()
            if len(files)>0:            
                f = open('./sound/'+hn+'.mp3', 'wb')
                sound=files["patient_name_sound"]            
                f.write(base64.b64decode(sound))
                f.close()
                Play('./sound/'+hn+'.mp3',1) 
                
                if files["patient_name_sound_eng"]!=None:
                    f = open('./sound/'+hn+'_eng.mp3', 'wb')
                    sound=files["patient_name_sound_eng"]            
                    f.write(base64.b64decode(sound))
                    f.close()
                    Play('./sound/'+hn+'_eng.mp3',1) 
                    
                
                f1 = open('./sound/'+depart+'.mp3', 'wb')
                sound=files["depart_sound"]            
                f1.write(base64.b64decode(sound))
                f1.close()
                Play('./sound/'+depart+'.mp3',1) 
                
            if point!="0":
                Play('./sound/Sound'+point+'.mp3')
                
            Play('./sound/last.mp3',0)
    except ValueError as e:
        print('error ' + e)
        
s.close()


