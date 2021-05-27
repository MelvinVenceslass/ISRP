import socket,ctypes

class dataCollector():

    def transact(self,message):
        try:
            SFDC_Connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SFDC_Connect.connect((self.ip,int(self.port)))
            SFDC_Connect.send((str(self.stn)+'T'+message).encode())
            response = (SFDC_Connect.recv(4096).decode())
            return response
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, str(e), "SFDC Error", 0)

    def __init__(self,ip,port,stn):
        self.ip,self.port,self.stn = [ip,port,stn]
        

