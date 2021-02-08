import serial as Serial
import threading
from time import sleep

from threading import Thread 
class th_barcode_callback(Thread):
    main=object
    def __init__(self,Main, firstName):
        Thread.__init__(self)
        self.firstName = firstName
        global main
        main=Main
    def run(self):
        global main
        print("Hello " + self.firstName + " from " + self.name)
        try:           
            #ser_barcode=Serial.Serial("COM4")
            
            try:
                ser = Serial.Serial("/dev/ttyACM0", baudrate=19200, timeout=1.0)
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
                                main.ui.txterror.setText(str(msg))
                                #main.get_patient_data("")
                                ser.flushOutput
            except KeyboardInterrupt:
                ser_barcode.close()
                if not ser.isOpen():
                    print("Error : Barcode Scan not connect")
            except NameError:
                #ser_barcode.close()
                if not ser.isOpen():
                    print("Error : " + NameError.args)
            finally:         
                ser_barcode.close()
                #if not ser.isOpen():                     
                #   self.ui.txterror.setText("Error : Barcode Scan not connect")
        except:
            main.ui.txterror.setText("Error : Barcode Scan not connect")