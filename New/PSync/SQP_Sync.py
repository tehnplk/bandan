from PyQt5.QtWidgets import  QWidget,QApplication, QMainWindow
from PyQt5 import QtGui,QtCore
import requests 
import bps
import serial as Serial
import sys
from time import sleep
import threading
import json
import time
import base64
import pygame.mixer
import requests


with open("/home/pi/Desktop/New/Config/setting.json") as json_data_file:
    datas = json.load(json_data_file)
ComBarcode=datas["ComBarcode"]
API=datas["API"]
ComPB=datas["ComBP"]
ISTEMP=datas["TMP"]
#print(datas[2:6])

vn=""
hn=""
fvn=""
class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = bps.Ui_bp_sync()
        self.ui.setupUi(self)        
        self.ui.hn.setText("HN:1111111")       
        #self.showFullScreen()

    def keyPressEvent(self, event):
        keypress(self,event)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    myapp = MyApp()
    myapp.show()
    myapp.ui.pname.setText("ชื่อ :-")
    myapp.ui.lname.setText("สกุล :-")
    myapp.ui.hn.setText("HN :-")

    if ComPB["IS_BDW"]==1:
        myapp.ui.pname_5.setText("kg")
        myapp.ui.pname_3.setText("Higth")     
        myapp.ui.label_2.setText("โรงพยาบาลอำนาจเจริญ")
        myapp.ui.pname_4.setText("kg")
        myapp.ui.pname_7.setText("BMI")
        myapp.ui.pname_2.setText("Weight")
        myapp.ui.pname_6.setText("")
    else:        
        myapp.ui.pname_5.setText("mmHg")
        myapp.ui.pname_3.setText("DAI")
        myapp.ui.label_2.setText("โรงพยาบาลอำนาจเจริญ")
        myapp.ui.pname_4.setText("mmHg")
        myapp.ui.pname_7.setText("PULSE")
        myapp.ui.pname_2.setText("SYS")
        myapp.ui.pname_6.setText("/min")

    pm =QtGui.QPixmap()
    pm.load("/home/pi/Desktop/New/image/no_image.png")   
    pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
    myapp.ui.pimage.setPixmap(pm)
    #myapp.keyPressEvent(keypres())
    def keypress(self,event):
        global vn,fvn
        #if event.key() == Qt.Key_Enter:
        if(event.key()==16777220):
            print("EnterKey :" +vn)
            #ค้นหาข้อมูล
            get_patient_data(fvn)
            vn=fvn
            fvn=""
        elif(event.key()<=255):
            #vn=event.key()           
            #vn=chr(event.key())
            fvn +=chr(event.key())
            print(chr(event.key()))

    from pygame import mixer
    mixer.init(frequency=45500)
    def playsound(file_path=None):
        try:        
            mixer.music.load(file_path)
            mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(100)          
            
        except ValueError as e:
            print('error '+e)
    
    def get_patient_data(data):
        if data=="EXIT" or data=="exit":
            from subprocess import call
            call("sudo poweroff", shell=True)
        else:
            global vn,hn
            url = API["URL"] +"?data_type=get_patient&hn="+ data
            r = requests.get(url)
            files = r.json()
            if len(files)>0:
                if files["fname"]!=None:
                    myapp.ui.pname.setText("ชื่อ :" + files["fname"])
                    myapp.ui.lname.setText("สกุล :"+ files["lname"])
                    myapp.ui.hn.setText("HN :" + files["hn"])
                    #vn=files["vn"]
                    hn=files["hn"]
                    if files["image"]!=None:
                        imgdata = files["image"]
                        pm =QtGui.QPixmap()
                        pm.loadFromData(base64.b64decode(imgdata))   
                        pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
                        myapp.ui.pimage.setPixmap(pm)
                        myapp.ui.txt_sys.setProperty("value",0)
                        myapp.ui.txt_dai.setProperty("value",0)
                        myapp.ui.txt_pulse.setProperty("value",0)
                        filename = '/home/pi/Desktop/New/Sound/start.wav'
                        #filename = 'myfile.wav'
                        playsound(filename)
                    else:
                        pm =QtGui.QPixmap()
                        pm.load("/home/pi/Desktop/New/image/no_image.png")   
                        pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
                        myapp.ui.pimage.setPixmap(pm)
                else:
                    vn=""
                    hn=""
                    myapp.ui.pname.setText("ชื่อ :-")
                    myapp.ui.lname.setText("สกุล :-")
                    myapp.ui.hn.setText("HN :-")
                    myapp.ui.txt_sys.setProperty("value",0)
                    myapp.ui.txt_dai.setProperty("value",0)
                    myapp.ui.txt_pulse.setProperty("value",0)
                    pm =QtGui.QPixmap()
                    pm.load("/home/pi/Desktop/New/image/no_image.png")   
                    pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
                    myapp.ui.pimage.setPixmap(pm)
                    filename = '/home/pi/Desktop/New/Sound/no_register.wav'
                    #playsound(filename)
            else:
                vn=""
                hn=""
                myapp.ui.pname.setText("ชื่อ :-")
                myapp.ui.lname.setText("สกุล :-")
                myapp.ui.hn.setText("HN :-")
                myapp.ui.txt_sys.setProperty("value",0)
                myapp.ui.txt_dai.setProperty("value",0)
                myapp.ui.txt_pulse.setProperty("value",0)
                pm =QtGui.QPixmap()
                pm.load("/home/pi/Desktop/New/image/no_image.png")   
                pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
                myapp.ui.pimage.setPixmap(pm)
                filename = '/home/pi/Desktop/New/Sound/no_register.wav'
                playsound(filename)


    def triker_time_out():        
        filename = '/home/pi/Desktop/New/Sound/time_out.wav'
        playsound(filename)
        vn="";
        myapp.ui.pname.setText("ชื่อ :-")
        myapp.ui.lname.setText("สกุล :-")
        myapp.ui.hn.setText("HN :-")

        
        pm =QtGui.QPixmap()
        pm.load("/home/pi/Desktop/New/image/no_image.png")   
        pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
        myapp.ui.pimage.setPixmap(pm)

    def triker1():   
        #get_patient_data("000095702")
      
        thrbp=threading.Thread(target=th_bp_callback("BP"))
        thrbp.daemon =True
        thrbp.start()     
       

    def triker2():
        thr=threading.Thread(target=th_barcode_callback("barcode"))
        thr.daemon =True
        thr.start()


    timer1 = threading.Timer(5.0, triker1)    
    timer1.start()
  
    timer2 = threading.Timer(5.0, triker2)    
    timer2.start()
  
    #thr=threading.Thread(target=th_bp.th_barcode_callback, daemon=True)  
    #thr=th_barcode.th_barcode_callback("barcode")
    #thr.start()
    #thr.start()
    #timer.cancel()
    
    def th_barcode_callback(self):   
        global vn
        print("Hello " + self)
        
    def clear(self):
        vn=""
        hn=""
        myapp.ui.pname.setText("ชื่อ :-")
        myapp.ui.lname.setText("สกุล :-")
        myapp.ui.hn.setText("HN :-")
        myapp.ui.txt_sys.setProperty("value",0)
        myapp.ui.txt_dai.setProperty("value",0)
        myapp.ui.txt_pulse.setProperty("value",0)
        pm =QtGui.QPixmap()
        pm.load("/home/pi/Desktop/New/image/no_image.png")   
        pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
        myapp.ui.pimage.setPixmap(pm)

    def th_bp_callback(self):
        print("Hello " + self)
        global vn,hn
         
        ser = Serial.Serial(ComPB["PortName"],ComPB["BaudRate"] , timeout=1.0)
                              
        if ser.isOpen():
            if ComPB["IS_BDW"]==1:
                playsound("/home/pi/Desktop/New/Sound/ready.wav")
            else:
                playsound("/home/pi/Desktop/New/Sound/ready_bp.wav")

            if ser.isOpen():
                #print("Serial com is opened")

                while True:
                    #print("Polling...")
                    sleep(0.5)
                    w=""
                    h=""
                    bmi=""
                    pulse=0
                    dbp=0
                    sbp=0
                    if ser.inWaiting() > 0:

                        msg = ser.read(ser.inWaiting())
                        ser.flushInput()
                        data=msg.decode("utf-8")
                        print(">> " ,data)                            
                        if ComPB["IS_BDW"]==1:
                            #ชั่งน้ำหนัก                                   
                            print(data)
                            data=data.replace(chr(30),"").replace("\r","")
                            ResultBP=data.split(" ")
                            print(ResultBP[0])
                            print(ResultBP[1])
                            w=float(ResultBP[0].replace("W:","").strip())
                            h=float(ResultBP[1].replace("H:","").strip())
                            bmi=float(w)/(float(h)/100 * float(h)/100)
                            myapp.ui.txt_sys.setProperty("value",w)
                            myapp.ui.txt_dai.setProperty("value",h)
                            myapp.ui.txt_pulse.setProperty("value",bmi) 

                        else:
                            if ComPB["BP_Brand"]=="TERUMO":
                                #00TM26552005110848RBME00S107M 85D 59P 88I16L 92
                                ResultBP = data.split(chr(30))                                    
                                if len(ResultBP)>5:
                                    myapp.ui.txt_sys.setProperty("value",ResultBP[5].replace("S",""))
                                    myapp.ui.txt_dai.setProperty("value",ResultBP[7].replace("D",""))
                                    myapp.ui.txt_pulse.setProperty("value",ResultBP[8].replace("P",""))                                  
                            elif ComPB["BP_Brand"]=="OMRON":
                                ResultBP = data.split(",")
                                if len(ResultBP)>5:                                           
                                    myapp.ui.txt_sys.setProperty("value",ResultBP[4])
                                    myapp.ui.txt_dai.setProperty("value",ResultBP[6])
                                    myapp.ui.txt_pulse.setProperty("value",ResultBP[7])                           
                            elif ComPB["BP_Brand"]=="AND":
                                ResultBP = data.split(chr(13))
                                if len(ResultBP)>5:                                           
                                    myapp.ui.txt_sys.setProperty("value",ResultBP[5])
                                    myapp.ui.txt_dai.setProperty("value",ResultBP[7])
                                    myapp.ui.txt_pulse.setProperty("value",ResultBP[8])     
                            elif ComPB["BP_Brand"]=="ACCUNIQ":
                                ResultBP = data.split(",")
                                if len(ResultBP)>5:     
                                    sbp=int(ResultBP[4])
                                    dbp=int(ResultBP[6])
                                    pulse=int(ResultBP[7])
                                    myapp.ui.txt_sys.setProperty("value",ResultBP[4])
                                    myapp.ui.txt_dai.setProperty("value",ResultBP[6])
                                    myapp.ui.txt_pulse.setProperty("value",ResultBP[7])
                            elif COMPB["BP_Brand"]=="INBODY":
                                ResultBP = data.split(",")
                                if len(ResultBP)>5:     
                                    sbp=int(ResultBP[4])
                                    dbp=int(ResultBP[6])
                                    pulse=int(ResultBP[7])
                                    myapp.ui.txt_sys.setProperty("value",ResultBP[4])
                                    myapp.ui.txt_dai.setProperty("value",ResultBP[6])
                                    myapp.ui.txt_pulse.setProperty("value",ResultBP[7])

                        if vn=="":
                            filename = '/home/pi/Desktop/New/Sound/no_register.wav'
                            playsound(filename)
                        else:
                            #ส่งข้อมูลบันทึก HIS
                            #play("SAVE")
                            if ComPB["IS_BDW"]==1:
                                filename = '/home/pi/Desktop/New/Sound/done_wh.wav'
                                playsound(filename)
                                #myapp.ui.txt_sys.setProperty("value",w)
                                #myapp.ui.txt_dai.setProperty("value",h)
                                #myapp.ui.txt_pulse.setProperty("value",bmi)
                                url=""
                                if ISTEMP["TMP"]==1:
                                    url = API["URL"]+"?tmp=1&data_type=set_wh&vn="+vn +"&w="+str(w)+"&h="+str(h)+"&bmi="+str(bmi)
                                else:
                                    url = str(API["URL"])+"?data_type=set_wh&vn="+str(vn)+"&w="+str(w)+"&h="+str(h)+"&bmi="+str(bmi)
                                #myobj = {'somekey': 'somevalue'}
                                print(url)
                                x = requests.post(url, data = None)
                            else:
                                filename = '/home/pi/Desktop/New/Sound/done.wav'
                                playsound(filename)
                                if ISTEMP["TMP"]==1:
                                    url = API["URL"]+"?data_type=set_bp&vn="+str(vn)+"&sbp="+sbp+"&dbp="+dbp+"&pulse="+pulse
                                else:
                                    url = API["URL"]+"?tmp=1&data_type=set_bp&vn="+str(vn) +"&sbp="+sbp+"&dbp="+dbp+"&pulse="+pulse
                                myobj = {'somekey': 'somevalue'}
                                x = requests.post(url, data = None)
                                print(x)

                            #m_NotificationTimer.moveToThread(this)
                            time.sleep(5)
                            clear("")
                            playsound('/home/pi/Desktop/New/Sound/next.wav')
                            playsound(filename)
                                    
                        clear("")
                        ser.flushOutput

    sys.exit(app.exec_())  

