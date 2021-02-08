import serial as Serial
import threading
from time import sleep

from threading import Thread 
class th_bp_callback(Thread):
    main=object
    def __init__(self,Main, firstName):
        Thread.__init__(self)
        self.firstName = firstName
        global main
        main=Main
    def run(self):
        print("Hello " + self.firstName + " from " + self.name)
        try:
            #ser=Serial.Serial("COM3")
            try:
                ser = Serial.Serial("COM3", baudrate=19200, timeout=1.0)
                if ser.isOpen():                   
                    if ser.isOpen():
                        #print("Serial com is opened")

                        while True:
                            #print("Polling...")
                            sleep(0.5)
                            if ser.inWaiting() > 0:
                                msg = ser.read(ser.inWaiting())
                                ser.flushInput()
                                print(">> " ,msg)
                                #msg = "\<\< ", msg
                                #ser.write(msg+"\r\n")
                                self.ui.txterror.setText(str(msg))
                                ser.flushOutput
            except KeyboardInterrupt:
                ser.close()
                if not ser.isOpen():
                    print("Error : ติดต่ออุปกรณ์ไม่ได้")
            except:
                main.ui.txterror.setText("Error : ติดต่ออุปกรณ์ไม่ได้")
            finally:         
                ser.close()
                if not ser.isOpen():                     
                    main.ui.txterror.setText("Error : ติดต่ออุปกรณ์ไม่ได้")
        except:
            main.ui.txterror.setText("Error : ไม่มีอุปกรณ์ต่ออยุ่")

