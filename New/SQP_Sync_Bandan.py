#from goto import goto, label
import goto
from PyQt5.QtWidgets import  QWidget,QApplication, QMainWindow
from PyQt5 import QtGui,QtCore
import requests 
import bps
#_1024_800
import serial as Serial
import sys
from time import sleep
import threading
import json
import time
import base64
import pygame.mixer
import requests
import os
from goto import with_goto


path=os.path.dirname(os.path.realpath(__file__)) + "/"

#./
#timer_out= threading.Timer
done=0
vn=""
hn=""
oldhn=""
fvn=""
#print('triker_time_out'.decode("utf-8"))
with open(path+"/Config/setting.json") as json_data_file:
    datas = json.load(json_data_file)
ComBarcode=datas["ComBarcode"]
API=datas["API"]
ComPB=datas["ComBP"]
ISTEMP=datas["TMP"]
WAIT_Result=datas["WAIT_RESULT"]
LIMIT_BP=datas["LIMIT_BP"]
SHOW_Result=datas["SHOW_RESULT"]
#print(datas[2:6])

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            #i = self.in_waiting
            data = self.s.read()
            #print('data='+data)
            i = data.find(b"\r")
            if i==-1:
                i=data.find(b"\r")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = bps.Ui_bp_sync()
        self.ui.setupUi(self)        
        self.ui.hn.setText("HN:1111111")       
        self.showFullScreen()
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
        myapp.ui.pname_5.setText("cm")
        myapp.ui.pname_3.setText("Higth")     
        myapp.ui.label_2.setText("ระบบบันทึกน้ำหนักส่วนสูงอัตโนมัติ")
        #myapp.ui.label_2.setText(_translate("bp_sync", "ระบบบันทึกข้อมูล ความดันโลหิต อัตโนมัติ"))
        myapp.ui.pname_4.setText("kg")
        myapp.ui.pname_7.setText("BMI")
        myapp.ui.pname_2.setText("Weight")
        myapp.ui.pname_6.setText("")
    else:        
        myapp.ui.pname_5.setText("mmHg")
        myapp.ui.pname_3.setText("DAI")
        #myapp.ui.label_2.setText("โรงพยาบาลอำนาจเจริญ")
        myapp.ui.pname_4.setText("mmHg")
        myapp.ui.pname_7.setText("PULSE")
        myapp.ui.pname_2.setText("SYS")
        myapp.ui.pname_6.setText("/min")

    pm =QtGui.QPixmap()
    pm.load(path+"/image/no_image.png")   
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
            #while pygame.mixer.music.get_busy():
             #   pygame.time.Clock().tick(100)          
            
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
            print(r)
            if r.status_code==200:                
                files = r.json()
                if len(files)>0:
                    if files["fname"]!=None:
                        if files["vn"]!=None:        
                            #ttime_out= threading.Timer(WAIT_Result["TIME"],triker_time_out)                   
                            #ttime_out.start()
                            filename = path+"/Sound/start.wav"
                            myapp.ui.pname.setText("ชื่อ :" + files["fname"])
                            myapp.ui.lname.setText("สกุล :"+ files["lname"])
                            myapp.ui.hn.setText("HN :" + files["hn"])
                            #vn=files["vn"]
                            hn=files["hn"]
                            #timer_out = threading.Timer(15.0,triker_time_out)    
                            #timer_out.start()
                            if files["image"]!=None:
                                imgdata = files["image"]
                                pm =QtGui.QPixmap()
                                pm.loadFromData(base64.b64decode(imgdata))                                   
                                pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)                                
                                myapp.ui.pimage.setPixmap(pm)
                                #filename = 'myfile.wav'
                            else:
                                pm =QtGui.QPixmap()
                                pm.load(path+"/Image/no_image.png")   
                                pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
                                myapp.ui.pimage.setPixmap(pm)

                            myapp.ui.txt_sys.setProperty("value",0)
                            myapp.ui.txt_dai.setProperty("value",0)
                            myapp.ui.txt_pulse.setProperty("value",0)
                            playsound(filename)
                        else:
                            filename = path+"/Sound/no_register.wav"
                            playsound(filename)
                            clear("")
                    else:
                        vn=""
                        hn=""
                        clear("")
                        filename = path+"/Sound/no_register.wav"
                        playsound(filename)
                else:
                    vn=""
                    hn=""
                    clear("")
                    filename = path+"Sound/no_register.wav"
                    playsound(filename)

    def triker_time_out():
        global oldhn
        global vn,hn,done
        if(hn!=oldhn):            
            if(done==0):            
                filename = path+"Sound/time_out.wav"
                playsound(filename)
                vn="";
                #thr.daemon =True
                myapp.ui.pname.setText("ชื่อ :-")
                myapp.ui.lname.setText("สกุล :-")
                myapp.ui.hn.setText("HN :-")
                    
                pm =QtGui.QPixmap()
                pm.load(path+"Image/no_image.png")   
                pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
                myapp.ui.pimage.setPixmap(pm)
                clear("")
        oldhn=hn

    #def triker1():   
        #get_patient_data("000095702")
  
       

    #def triker2():
    #thr=threading.Thread(target=th_barcode_callback("barcode"))
    #thr.daemon =True
    #thr.start()
    def bp():
        thrbp=threading.Thread(target=th_bp_callback("BP"))
        thrbp.daemon =True
        thrbp.start()  

    timer1 = threading.Timer(5.0, bp)    
    timer1.start()
  
    #timer2 = threading.Timer(5.0, triker2)    
    #timer2.start()
  
    #thr=threading.Thread(target=th_bp.th_barcode_callback, daemon=True)  
    #thr=th_barcode.th_barcode_callback("barcode")
    #thr.start()
    #thr.start()
    #timer.cancel()
    
    def th_barcode_callback(self):   
        global vn
        print("Hello " + self)
        
    def clear(self):
        global vn,hn,done
        vn=""
        hn=""
        done=1
        myapp.ui.pname.setText("ชื่อ : -")
        myapp.ui.lname.setText("สกุล : -")
        myapp.ui.hn.setText("HN : -")
        myapp.ui.txt_sys.setProperty("value",0)
        myapp.ui.txt_dai.setProperty("value",0)
        myapp.ui.txt_pulse.setProperty("value",0)
        pm =QtGui.QPixmap()
        pm.load(path+"Image/no_image.png")   
        pm= pm.scaled(150, 171, QtCore.Qt.KeepAspectRatio)
        myapp.ui.pimage.setPixmap(pm)

    @with_goto
    def th_bp_callback(self):
        print("Hello " + self)
        global vn,hn,done
        try:
            
            ser = Serial.Serial(port=ComPB["PortName"],baudrate=ComPB["BaudRate"],timeout=2.0)
            label .openport
            ser.open
            print("Open") 
            ser.flushInput()
            #rl = ReadLine(ser)
            
            i=0
            w=""
            h=""
            bmi=""
            pulse=0
            dbp=0
            sbp=0
            data=""           

            while True:                
                try:                                 
                    size = ser.inWaiting()
                    if size:                 
                        msg = ser.read(size)                            
                        data=str(msg,"latin")
                        print(data)
                        done=1
                        if data!="":
                            if ComPB["IS_BDW"]==1:
                                    #ชั่งน้ำหนัก                                   
                                    print(data)
                                    #data=data.replace(chr(30),"").replace("\r","")
                                    ResultBP=data.split(" ")
                                    print(ResultBP[0])
                                    print(ResultBP[1])
                                    w=round(float(ResultBP[0].replace("W:","").replace(":","").strip()),0)
                                    h=round(float(ResultBP[1].replace("H:","").replace(":","").strip()),0)
                                    bmi=round(float(w)/(float(h)/100 * float(h)/100),2)
                                    #bmi=bmi[0,4]
                                    print("BMI:"+str(bmi))
                                    myapp.ui.txt_sys.setProperty("value",w)
                                    myapp.ui.txt_dai.setProperty("value",h)
                                    myapp.ui.txt_pulse.setProperty("value",bmi) 
                                    #bmi=round(fbmi,2)
                            else:
                                if ComPB["BP_Brand"]=="TERUMO":
                                    #00TM26552005110848RBME00S107M 85D 59P 88I16L 92
                                    ResultBP = data.split(chr(30))                                    
                                    if len(ResultBP)>5:
                                        sbp=int(ResultBP[5].replace("S",""))
                                        dbp=int(ResultBP[7].replace("D",""))
                                        pulse=int(ResultBP[8].replace("P",""))
                                        myapp.ui.txt_sys.setProperty("value",sbp)
                                        myapp.ui.txt_dai.setProperty("value",dbp)
                                        myapp.ui.txt_pulse.setProperty("value",pulse)                          
                                elif ComPB["BP_Brand"]=="OMRON":
                                    ResultBP = data.split(",")
                                    if len(ResultBP)>5:
                                        sbp=int(ResultBP[4])
                                        dbp=int(ResultBP[6])
                                        pulse=int(ResultBP[7])
                                        myapp.ui.txt_sys.setProperty("value",sbp)
                                        myapp.ui.txt_dai.setProperty("value",dbp)
                                        myapp.ui.txt_pulse.setProperty("value",pulse)                           
                                elif ComPB["BP_Brand"]=="AND":
                                    ResultBP = data.split(chr(13))
                                    if len(ResultBP)>5:
                                        sbp=int(ResultBP[5])
                                        dbp=int(ResultBP[7])
                                        pulse=int(ResultBP[8])

                                        myapp.ui.txt_sys.setProperty("value",sbp)
                                        myapp.ui.txt_dai.setProperty("value",dbp)
                                        myapp.ui.txt_pulse.setProperty("value",pulse)     
                                elif ComPB["BP_Brand"]=="ACCUNIQ":
                                    ResultBP = data.split(",")
                                    if len(ResultBP)>5:     
                                        sbp=int(ResultBP[4])
                                        dbp=int(ResultBP[6])
                                        pulse=int(ResultBP[7])
                                        myapp.ui.txt_sys.setProperty("value",sbp)
                                        myapp.ui.txt_dai.setProperty("value",dbp)
                                        myapp.ui.txt_pulse.setProperty("value",pulse)
                                elif COMPB["BP_Brand"]=="INBODY":
                                    data = data.replace("S","|")
                                    data = data.replace("M","|")
                                    data = data.replace("D","|")
                                    data = data.replace("P","|")
                                    ResultBP = data.split("|")
                                   
                                    sbp=int(ResultBP[1])
                                    dbp=int(ResultBP[2])
                                    pulse=int(ResultBP[4])

                                    myapp.ui.txt_sys.setProperty("value",sbp)
                                    myapp.ui.txt_dai.setProperty("value",dbp)
                                    myapp.ui.txt_pulse.setProperty("value",pulse)

                            over=0
                            if ComPB["IS_BDW"]==0 and (sbp>LIMIT_BP["SBP"] or dbp > LIMIT_BP["DBP"]):                                    
                                over=1
                            if vn=="":
                                #filename = './Sound/no_register.wav'
                                #playsound(filename)
                                if over==1:
                                    filename=path+ "/Sound/over.wav"
                                else:
                                    if ComPB["IS_BDW"]==0:
                                        filename = path+"/Sound/done_no_visit.wav"
                                    else:
                                        filename = path+"/Sound/done_wh.wav"
                                playsound(filename)
                                print("No Visit")       
                                time.sleep(SHOW_Result["TIME"])
                                filename = path+"/Sound/next.wav"
                                playsound(filename)
                            else:
                                #ส่งข้อมูลบันทึก HIS
                                #play("SAVE")
                                if ComPB["IS_BDW"]==1:
                                    filename = path+"Sound/done_wh.wav"
                                    playsound(filename)
                                    url=""
                                    if ISTEMP["TMP"]==1:
                                        url = API["URL"]+"?tmp=1&data_type=set_wh&vn="+vn +"&w="+str(w)+"&h="+str(h)+"&bmi="+str(bmi)
                                    else:
                                        url = str(API["URL"])+"?data_type=set_wh&vn="+str(vn)+"&w="+str(w)+"&h="+str(h)+"&bmi="+str(bmi)
                                    #myobj = {'somekey': 'somevalue'}
                                    print(url)
                                    x = requests.post(url, data = None)
                                else:
                                    if over==1:
                                        filename=path+ "/Sound/over.wav"
                                    else:
                                        filename = path+"/Sound/done.wav"
                                    playsound(filename)                    
                                    
                                    url = API["URL"]+"?tmp=0&data_type=set_bp&vn="+str(vn) +"&sbp="+str(dbp)+"&dbp="+str(sbp)+"&pulse="+str(pulse)
                                    #myobj = {'somekey': 'somevalue'}
                                    x = requests.post(url, data = None)
                                    print(x)
                                    print(url)                                

                                time.sleep(SHOW_Result["TIME"])
                                filename = path+"/Sound/next.wav"
                                playsound(filename)
                            clear("")
                            data=""
                            ser.close
                            #del ser
                            break     
                        else:
                            sleep(1)   
                    else:
                        sleep(1)
                except:
                    print("error")
                    if ComPB["IS_BDW"]==0:
                        filename=path+"/Sound/error_bp.wav"
                    else:
                        filename=path+"/Sound/error_bw.wav"

                    playsound(filename)
                    clear("")
                    data=""
                    ser.close
                    #del ser
                    break
            goto .openport
        except ValueError as e:
            print('error '+e)

    sys.exit(app.exec_())  
