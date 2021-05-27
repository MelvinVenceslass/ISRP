import os,datetime,time,sys,sqlite3,ctypes,socket,time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

class machine():
    
    def readRegsiter(self,address,value):
        holdRegisters = self.plccon.read_holding_registers(address,value)
        self.holdRegisters = holdRegisters.registers
        return self.holdRegisters
    
    def writeRegsiter(self,address,value,cmd):
        self.writeRegisters = self.plccon.write_register(address,cmd,unit=value)
        return self.writeRegisters
    
    def scanRead(self):
        self.readScanner.send(str('2').encode())
        response = self.readScanner.recv(4096).decode()
        return response
        
    def __init__(self,data,obj):
        try:
            
            self.pip,self.pport,self.sip,self.sport = data
            self.plccon = ModbusClient(self.pip,port=int(self.pport), timeout=3)
            #self.readScanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.readScanner.connect((self.sip,int(self.sport)))
            
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, str(e), "PLC COM Error", 0)
            obj.error_lab.show()
            obj.bootErrorLab.show()
            self.window.opPane.setEnabled(False)
           
def readS(host,port):
    try:
        readScanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        readScanner.connect((host,port))
        return readScanner
    except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, str(e), "Scanner COM Error", 0)
        
    
