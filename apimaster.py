import os,datetime,time,sys,sqlite3,ctypes,socket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QComboBox, QPushButton, QLineEdit, QHBoxLayout, QApplication, QMessageBox)
from PyQt5.QtCore import Qt
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

    
def printout(desc,info):
    nows = time.strftime("%T | %d-%b-%Y",time.localtime(time.time()))
    console = ("{} :: {} : {}".format(nows,desc,info))
    cellValue = "('{}','{}','{}')".format(nows,desc,info)
    print(console)

#Database modules
class constants():
    
    def updateto(self,tbname,data, where):
        #print("UPDATE {} SET {} WHERE {}".format(tbname,data,where))
        self.cursor.execute("UPDATE {} SET {} WHERE {}".format(tbname,data,where))
        self.connection.commit()
         
    
    def writeto(self,tbname,data):
        self.cursor.execute("INSERT INTO {} VALUES {}".format(tbname,data))
        self.connection.commit()
        
    def readfrom(self,tbname,what,where):
        rows = self.cursor.execute("SELECT {} FROM {} where {}".format(what,tbname,where)).fetchall()
        return rows
    
    def writeParams(self,**params):
        try:
            for key,value in params.items():
                self.cursor.execute("UPDATE configuration SET {}='{}' WHERE 1".format(key,value))
                self.connection.commit()
        except Exception as e:
            print(e)
    def readParams(self,*params):
        for value in params:
            rows = self.cursor.execute("SELECT {} FROM configuration WHERE 1".format(value))
            yield rows
            
    def __init__(self):
        self.connection = sqlite3.connect("autobatch.db")
        self.cursor = self.connection.cursor()
        tables = self.cursor.execute("""SELECT name FROM sqlite_master  WHERE type ='table';""").fetchall()
        
        if ('configuration',) in tables:
            printout("INFO","Table Exists - Configuration")
            
        else:
            self.cursor.execute("""CREATE TABLE configuration (sfdcip TEXT, sfdcport TEXT, sfdcstn TEXT,
                                    plcip TEXT, plcport TEXT, scannerip TEXT, scannerport TEXT, scannercom TEXT, scannerbaud TEXT)""")

        if ('hourlycount',) in tables:
             printout("INFO","Table Exists - hourlycount")
        else:
            self.cursor.execute("CREATE TABLE hourlycount (timez INTEGER, serials TEXT)")

        if ('systemLog',) in tables:
             printout("INFO","Table Exists - Systemlog")
        else:
            self.cursor.execute("CREATE TABLE systemLog (time TEXT, desc TEXT, message INTEGER)")

        if ('processlog',) in tables:
             printout("INFO","Table Exists - Processlog")
        else:
            self.cursor.execute("CREATE TABLE processlog (time INTEGER, batchno TEXT, serialNo TEXT, status TEXT)")
            
        if ('registermap',) in tables:
             printout("INFO","Table Exists - registerTab")
        else:
            self.cursor.execute("CREATE TABLE registermap (desc TEXT, reg INTEGER)")
        
        printout("INFO","Database Initialization Success!")


class sfdc():
    def transact(self,message):
        try:
            SFDC_Connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SFDC_Connect.connect((self.ip,int(self.port)))
            SFDC_Connect.send((str(self.stn)+'T'+message).encode())
            response = (SFDC_Connect.recv(4096).decode())
            return response
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, str(e), "SFDC Error", 0)
    
    def __init__(self):
        data = constants().readfrom('configuration','sfdcip,sfdcport,sfdcstn','1')
        try:
            self.ip,self.port,self.stn = data[0]
        except:
            self.ip,self.port,self.stn = ['','','']
            
class machinecom():
    
    def plcWritecoil(self):
        try:
            writeCoils = self.plc.write_coil(30, True, unit=1)
            self.writeCoils = writeCoils.registers

        except Exception as e:
            self.writeCoils  = e

        return self.writeCoils

            
    def plcReadinput(self):
        try:
            inputRegisters = self.plc.read_input_registers(address,value)
            self.inputRegisters = inputRegisters.registers

        except Exception as e:
            self.inputRegisters  = e

        return self.inputRegisters

    def plcReadholding(self,address,value):
        try:
            holdRegisters = self.plccon.read_holding_registers(address,value)
            self.holdRegisters = holdRegisters.registers
        except Exception as e:
            self.holdRegisters  = e
        return self.holdRegisters
    
    def plcWriteReg(self,address,value,cmd):
        try:
            self.writeRegisters = self.plccon.write_register(address,cmd,unit=value)
        except Exception as e:
            self.writeRegisters  = str(e)+'Melvin'
        return self.writeRegisters
    
    def scanRead(self):
        
        response = (self.readScanner.recv(4096).decode())
        #readScanner.close()
        return str(response)
    
    def __init__(self):
        try:
            data = constants().readfrom('configuration','plcip,plcport,scannerip,scannerport,scannercom,scannerbaud','1')
            self.pip,self.pport,self.sip,self.sport,self.scom,self.smod = data[0]
            self.plccon = ModbusClient(self.pip,port=int(self.pport), timeout=3)
            self.readScanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.readScanner.connect((self.sip,int(self.sport)))
            printout('INFO',"Machine Communication Success!")
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, str(e), "PLC & Scanner COM Error", 0)
            printout('ERRR',e)
            #raise Exception(str(e))
            
    

class dtshift():
    def stime(self):
        ctime = time.strftime("%T",time.localtime(time.time()))
        return ctime
    
    def sdate(self):
        cdate = time.strftime("%d-%b-%Y",time.localtime(time.time()))
        return cdate
    
    def shour(self):
        chour = time.strftime("%H",time.localtime(time.time()))
        return chour

    def sshift(self):
        now = self.shour()
        if now in self.shift_A:
            cshift = "A"
            return cshift
        elif now in self.shift_B:
            cshift = "B"
            return cshift
        elif now in self.shift_C:
            cshift = "C"
            return cshift
        
    def timeframe(self,unixtimes,out):
        ctime = datetime.datetime.fromtimestamp(int(round(unixtimes)))
        stime = ctime.replace(minute=0, second=0).timestamp()
        etime = stime + 3600
        ptime = stime - 3600

        if out =='s':
            return stime
        elif out == 'e':
            return etime
        
            
       
    
    def __init__(self):
        self.shift_C = ['23','00','01','02','03','04','05','06']
        self.shift_A = ['07','08','09','10','11','12','13','14']
        self.shift_B = ['15','16','17','18','19','20','21','22']
        




