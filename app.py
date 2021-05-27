import sys,json,os,logging,ctypes
sys.path.append(os.getcwd()+"/lib")
from PyQt5 import QtWidgets,uic,QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from lib.mesconduit import conduit
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s |  %(levelname)s |  %(message)s', level=logging.DEBUG)
MB_OK = 0x0
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

class main:
    
    def commonHandle(self, desc="INFO", message="message"):
        try:
            if desc=="ERRR":
                self.window.common_sym.setPixmap(QPixmap('img/cat.png'))
                logging.warning(message)
                self.window.common_resposne.setText(message)
                ctypes.windll.user32.MessageBoxW(0, "Please Enter Username/Password" , "Error", ICON_STOP)
            else:
                self.window.common_sym.setPixmap(QPixmap('img/ok.png'))
                logging.info(message)
                self.window.common_resposne.setText(message)
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, str(e) , "Error", ICON_STOP)


    @property
    def configParser(self):
        self.parts=eval(open("templates/part.json",'r').read())
        readData = eval(open("config/config.json", "r+", encoding="utf-8").read())
        return readData

    @property
    def updateConfigPane(self):
        self.window.config_url.setText(self.configurations['urlink_ad'])
        self.window.config_station_a.setText(self.configurations['assign_st'])
        self.window.config_station_b.setText(self.configurations['packin_st'])
        self.window.config_clvl_container.setText(self.configurations['clevel_cn'])
        self.window.config_clvl_skid.setText(self.configurations['clevel_sk'])
        self.window.config_client.setText(self.configurations['client_id'])
        self.window.config_printer.setText(self.configurations['printer_q'])


    @property
    def prerequesties(self):
        self.connectionHandeler
        self.configurations = self.configParser
        self.updateConfigPane
        
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Ui()
        self.window.show()
        self.prerequesties
        sys.exit(self.app.exec_())
   
    @property
    def connectionHandeler(self):
        self.window.login_login.clicked.connect(self.login)
        self.window.assign_assignButton.clicked.connect(self.assign)


    def serialReformer(self,barcode):
        try:
            barcode = (barcode[18:]).strip()
            bcd = barcode
            barcode = [str(barcode[3:])+str(d) if str(barcode[:3]) in str(e) else None for d in self.parts[0] for e in self.parts[0][d]]
            barcode = [each for each in barcode if each][0]
            self.commonHandle(message=f'Barcode <{bcd}> is reframed to <{barcode}>')
            return barcode
        except Exception as e:
             self.commonHandle(desc="ERRR", message=e)


    def login(self):
        try:
            self.commonHandle(message="Logging in...")
            self.commonHandle(message="Collecting username and password")
            self.username =  self.window.login_username.text()
            self.password =  self.window.login_password.text()

            if not self.username=="" and not self.username =="":

                self.commonHandle(message="Creating sessions...")
                self.session_assign = conduit(self.configurations['urlink_ad'],self.username,self.password,self.configurations['assign_st'],self.configurations['client_id'])
                self.session_packin = conduit(self.configurations['urlink_ad'],self.username,self.password,self.configurations['packin_st'],self.configurations['client_id'])
                
                self.commonHandle(message="Attempting...")
                ssession_packin = self.session_packin.mes_login()
                ssession_assign = self.session_assign.mes_login()
                if session_packin ==True and session_assign ==True:
                    self.window.login_TickBox.setPixmap(QPixmap('img/ok.png'))
                    self.commonHandle(message="Login Success!")
                    
                else:
                    self.window.login_TickBox.setPixmap(QPixmap('img/cat.png'))
                    self.commonHandle(desc="ERRR",message="Login Failed!")
                    
            else:
                self.window.login_TickBox.setPixmap(QPixmap('img/cat.png'))
                self.commonHandle(desc="ERRR", message="Enter the Username/Password")
       
        except Exception as e:
           self.commonHandle(desc="ERRR", message=e)
        
    def assign(self):
        try:
            self.commonHandle(message="Trying to Assign the unit to Shop Order!")
            self.commonHandle(message="Reforming the Serial#....")
            labelText = self.window.assign_unitsn.text()
            unitSerial = self.serialReformer(labelText)
            self.commonHandle(message=f"Reformed Serial# <{unitSerial}>")
            
            self.commonHandle(message="Ensuring Auto END Command")
            autoend = self.window.assign_autoend.isChecked()
            if autoend==True:
                self.commonHandle(message="Auto End is True")
                self.commonHandle(message="Stage Passing the unit")
                stagepass = self.session_assign.mes_PassUnit(unitSerial)
            else:
                self.commonHandle(message="Auto End is False")
                self.commonHandle(message="Skipping the Auto end process!")

            
        except Exception as e:
            self.commonHandle(desc="ERRR", message=e)


    
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        
        uic.loadUi('ui/main.ui', self)

if __name__ == "__main__":
   appObj = main()
