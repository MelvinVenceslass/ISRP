from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import (QWidget, QComboBox, QPushButton, QLineEdit, QHBoxLayout, QApplication, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import *
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                         QFontDatabase, QIcon, QLinearGradient, QPalette,
                         QPainter, QPixmap,QRadialGradient, QMovie, QTextCursor)
from PyQt5.QtWidgets import *
import sys,sqlite3,dataapi,livetimeapi,ctypes,mesdataapi,machineapi,inspect,conduitapi,time,os,src,timeit,mes_api, asyncio, threading,socket

MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10



class main():

        
    def consoleDraw(self,desc,info,**kwarg):
        try:
            self.info = info
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            mesage = "{} :: {} :: {} :: {} : {} :: {}".format(self.timeapi.sdate(), self.timeapi.stime(), str(desc), str(calframe[1][3]),str(curframe.f_lineno), str(info))
            print(mesage)
            self.window.machResp.setText("  " +str(self.info))

            
            try:
                self.datacon.logwriter(self.timeapi.sdate(),
                                      self.timeapi.stime(),
                                      str(desc),
                                      str(calframe[1][3]),
                                      str(info))
            except:
                pass
            
            if desc == 'ERRR':
                self.datacon.connection.commit()
                ctypes.windll.user32.MessageBoxW(0, str(info) , "Error", ICON_STOP)
                
            
            if desc == 'SAVE':
                self.datacon.connection.commit()
                ctypes.windll.user32.MessageBoxW(0, str(info) , "Alert", ICON_INFO)
                
                #self.window.machResp.moveCursor(QtGui.QTextCursor.End)
            if desc == 'SFDC':
                self.window.sfdcResp.setText(str(info))
                
            return True
                
        except Exception as exceptInfo :
            if not kwarg['erDisp']==False:
                ctypes.windll.user32.MessageBoxW(0, str(exceptInfo) , "Console Failure", ICON_STOP)
                self.datacon.connection.commit()

    def search(self):
        try:
            self.window.unitfootprint.setRowCount(0)
            descList = ['Date / Time','Shift','Employee#','Serial#','Part#','PO#','PO - Quantity','MES-Message','Container#','Skid#','Remarks']
            unitInfo = self.window.unitSearchkey.text()
            unitData = self.datacon.unitHistory(unitInfo)
            self.consoleDraw('INFO',f'Searching <{unitInfo}>  History...')
            for i in (unitData):
                if not len(i)==0:
                    for j, v in enumerate(i):
                        rowPosition = self.window.unitfootprint.rowCount()
                        self.window.unitfootprint.insertRow(rowPosition)
                        self.window.unitfootprint.setItem(rowPosition , 0, QTableWidgetItem(descList[j]))
                        self.window.unitfootprint.setItem(rowPosition , 1, QTableWidgetItem(str(v)))
                        
                else:
                    rowPosition = self.window.unitfootprint.rowCount()
                    self.window.unitfootprint.insertRow(rowPosition+1)
                    self.window.unitfootprint.setItem(rowPosition , 0, QTableWidgetItem('INFO'))
                    self.window.unitfootprint.setItem(rowPosition , 1, QTableWidgetItem("No Records Found!"))
                    self.consoleDraw('SAVE',str('No Records Found'))
            self.consoleDraw('INFO',str('Searching Complete...'))
            
                    
                    
                
        except Exception as e:
            self.consoleDraw('ERRR',str(e))

            
        
        
    def engLockerUnlock(self,Value):
        try:
            self.window.sfdcGroup.setEnabled(Value)
            self.window.plccGroup.setEnabled(Value)
            self.window.scanGroup.setEnabled(Value)
            self.window.packGroup.setEnabled(Value)
            #self.window.perfGroup.setEnabled(Value)
            self.window.regsGroup.setEnabled(Value)
            self.window.opPane.setTabEnabled(3, Value)
            if Value == False:
                self.window.opPane.setTabEnabled(1,True)
                self.window.opPane.setCurrentIndex(1)
                self.configure_app()
                
                #self.window.enginLogin.disconnect()
                #self.window.enginLogin.clicked.connect(self.engLockerLock)
                #self.window.enginLogin.setText('Lock')
            else:
                self.window.opPane.setTabEnabled(1,False)
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
                
    def engLockerLock(self):
        try:
            self.window.enginLogin.disconnect()
            self.window.enginLogin.clicked.connect(self.engineer_unlock)
            self.window.enginLogin.setText('Login')
            self.engLockerUnlock(False)
            
            self.configure_app()
        except Exception as e:
            self.consoleDraw('ERRR',str(e))

    def sfdcParamUpdate(self):
        try:
            self.consoleDraw('INFO',str('Saving SFDC Parameters '))
            save = self.datacon.writeParams(sfdc_ip = self.window.conduitapi.text(),
                                            sfdc_stn = self.window.pass_stn.text(),
                                            pack_stn = self.window.pack_stn.text(),
                                            mes_api = self.window.mesapi.text(),
                                            clientid = self.window.clientid.text(),
                                            pack_loc = self.window.short_workstation.text()
                                            
                                            )
            
            self.consoleDraw('SAVE',str('SFDC Parameters Save Success!'))
            
        except Exception as e:
            self.consoleDraw('ERRR',str(e))


    
    
    def plccParamUpdate(self):
        try:
            self.consoleDraw('INFO',str('Saving PLC Parameters '))
            save = self.datacon.writeParams(plcc_ip   = self.window.plcc_ip.text(),
                                            plcc_port = self.window.plcc_port.text())
            self.consoleDraw('SAVE',str('PLC Parameters Save Success!'))
            
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            
    def scanParamUpdate(self):
        try:
            self.consoleDraw('INFO',str('Saving Scanner Parameters '))
            save = self.datacon.writeParams(scan_ip   = self.window.scan_ip.text(),
                                            scan_port = self.window.scan_port.text())
            self.consoleDraw('SAVE',str('Scanner Parameters Save Success!'))
            
        except Exception as e:
            self.consoleDraw('ERRR',str(e))

    def packParamUpdate(self):
        try:
            self.consoleDraw('INFO',str('Saving Packing Parameters '))
            save = self.datacon.writeParams(cont_clvl = self.window.cont_clevel.text(),
                                            skid_clvl = self.window.skid_clevel.text(),
                                            )
            self.consoleDraw('SAVE',str('Packing Parameters Save Success!'))
            
        except Exception as e:
            self.consoleDraw('ERRR',str(e))

    def regsParamUpdate(self):
        try:
            self.consoleDraw('INFO',str('Saving Register Parameters '))
            save = self.datacon.writeParams(
                read_scanok = self.window.read_scanok.text(),
                read_alarm = self.window.read_alarm.text(),
                read_mstatus = self.window.read_csts.text(),
                writ_passfail = self.window.write_passfail.text(),
                writ_alarm = self.window.write_alarm.text(),
                writ_reset = self.window.write_reset.text(),
                writ_ping = self.window.write_ping.text(),
                read_rtime = self.window.read_runtime.text(),
                read_dtime = self.window.read_downtime.text())
            
            self.consoleDraw('SAVE',str('PLC Register Parameters Save Success!'))
            
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            


    def h_Productivity(self):
        try:
            #OEE = (Good Count × Ideal Cycle Time) / Planned Production Time

            std_cycleTime = self.datacon.config.target_ctime
            start,end,current = self.timeapi.cTimeFrame()
            qty = self.datacon.getqty(start,current)
            pr = round(((int(qty)*int(std_cycleTime))/(int(current)-int(start)))*100)
            self.window.performance.setText(str(pr))
            self.window.producedQty.setText(str(qty))
        except Exception as e:
            if not "division by zero" in e:
                self.consoleDraw('ERRR',str(e))
            pass
        
            
    def uplCounter(self):
        try:
            upc = int(self.window.upc_cont.text())
            cpl = int(self.window.cpl_cont.text())
            upl = upc*cpl
            self.window.upl_cont.setText(str(upl))
            
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            
        
    def read_anyReg(self):
        try:
            reg = int(self.window.read_addd.text())
            val = self.machine.readRegsiter(reg,1)[0]
            self.window.read_value.setText(str(val))
            self.consoleDraw('INFO',str(val))
            
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            
    def writ_anyReg(self):
        try:
            reg = int(self.window.writ_addd.text())
            val = int(self.window.writ_value.text())
            val = self.machine.writeRegsiter(reg,1,val)
            self.consoleDraw('INFO',str(val))
            
            
        except Exception as e:
            self.consoleDraw('ERRE',str(e))
            
    def configure_app(self):
        try:
            self.consoleDraw('INFO','Configuring Application')
            self.consoleDraw('INFO','Setting Up Application enviroinment ')
            self.consoleDraw('INFO','Updating Table configurations')
            self.datacon = dataapi.transport()
            
            #table cell Handle:
            self.table_worder_name = self.window.liveTable.item(1, 1)
            self.table_worder_targ = self.window.liveTable.item(1, 2)
            self.table_worder_actl = self.window.liveTable.item(1, 3)

            self.table_lot_name = self.window.liveTable.item(2, 1)
            self.table_lot_targ = self.window.liveTable.item(2, 2)
            self.table_lot_actl = self.window.liveTable.item(2, 3)

            self.table_cont_name = self.window.liveTable.item(3, 1)
            self.table_cont_targ = self.window.liveTable.item(3, 2)
            self.table_cont_actl = self.window.liveTable.item(3, 3)

            self.table_unit_name = self.window.liveTable.item(4, 1)
            self.table_unit_targ = self.window.liveTable.item(4, 2)
            self.table_unit_actl = self.window.liveTable.item(4, 3)
            
            self.cellHandle = [self.table_worder_name,self.table_worder_targ,self.table_worder_actl,
                                  self.table_lot_name,self.table_lot_targ,self.table_lot_actl,
                                  self.table_cont_name,self.table_cont_targ,self.table_cont_actl,
                                  self.table_unit_name,self.table_unit_targ,self.table_unit_actl]
            
            
            
            self.consoleDraw('INFO','Updating Progress Bar configurations')
            
            #ProgressBar Handle:
            self.lotProgressBar =  self.window.lotProg
            self.conProgressBar =  self.window.conProg
            self.untProgressBar =  self.window.ulotProg
            self.wodProgressBar =  self.window.woProg
            self.progressBarHandle = [self.lotProgressBar, self.conProgressBar,
                                         self.untProgressBar, self.wodProgressBar]

            self.consoleDraw('INFO','Updating Productivity configurations')
            
            #productivity Handle:
            self.target_hourly = self.window.t_hrly
            self.target_clTime = self.window.t_cycltime
            self.productivityHandle = [self.target_hourly,self.target_clTime]

            self.consoleDraw('INFO','Updating Performance configurations')
            
            #performanceHandle:
            self.availablity = self.window.availability
            self.utilization = self.window.utilization
            self.downtimemin = self.window.downTime
            self.idletimemin = self.window.idleTime
            self.performanceHandler = [self.availablity,self.utilization,self.downtimemin,self.idletimemin]
            
            for each in self.progressBarHandle:
                each.setMaximum(0)
                each.setProperty('value',0)
                
            for each in self.cellHandle:
                each.setText('...')
                
            for each in self.productivityHandle:
                each.setText('...')
            for each in self.performanceHandler:
                each.setText('...')

            
            self.consoleDraw('INFO','Setting up Engineer Mode')
            self.consoleDraw('INFO','refreshing SFDC settings')
            
            #SFDC
            self.window.conduitapi.setText(self.datacon.config.conduit_curl)
            self.window.pass_stn.setText(self.datacon.config.pass_station)
            self.window.pack_stn.setText(self.datacon.config.pack_station)
            self.window.short_workstation.setText(self.datacon.config.pack_locales)
            self.window.mesapi.setText(self.datacon.config.mes_api_curl)
            self.window.clientid.setText(self.datacon.config.mes_clientid)
            
            
            self.consoleDraw('INFO','refreshing PLCC settings')
            
            #PLCC
            self.window.plcc_ip.setText(str(self.datacon.config.plcc_ipaddrs))
            self.window.plcc_port.setText(str(self.datacon.config.plcc_portnum))

            self.consoleDraw('INFO','refreshing Scanner settings')
           
            #scanner
            self.window.scan_ip.setText(str(self.datacon.config.scan_ipaddrs))
            self.window.scan_port.setText(str(self.datacon.config.scan_portnum))

            self.consoleDraw('INFO','refreshing Packing settings')
            
            #packing_config
            self.window.cont_clevel.setText(self.datacon.config.cont_clevels)
            self.window.skid_clevel.setText(self.datacon.config.skid_clevels)

            self.consoleDraw('INFO','refreshing Performance settings')
            
           
            self.window.t_hrly.setText(str(self.datacon.config.target_phour))
            self.window.t_cycltime.setText(str(self.datacon.config.target_ctime))
            
            self.consoleDraw('INFO','refreshing Registers settings')
            
            
           #plcc Read registers
            self.window.read_scanok.setText(str(self.datacon.config.read_scan_ok))
            self.window.read_alarm.setText(str(self.datacon.config.read_malarms))
            self.window.read_csts.setText(str(self.datacon.config.read_mstatus))

            #plcc Write registers
            self.window.write_passfail.setText(str(self.datacon.config.writ_pasfail))
            self.window.write_alarm.setText(str(self.datacon.config.writ_salarms))
            self.window.write_reset.setText(str(self.datacon.config.writ_mresets))
            self.window.write_ping.setText(str(self.datacon.config.writ_pingpon))
            #plcc Informers
           
            self.window.read_runtime.setText(str(self.datacon.config.read_runtime))
            self.window.read_downtime.setText(str(self.datacon.config.read_dwntime))
            
            self.consoleDraw('INFO','Updating Configs')
            self.window.plcipdisp.setText(str(self.datacon.config.plcc_ipaddrs))
            self.window.plcportdisp.setText(str(self.datacon.config.plcc_portnum))
            self.window.scanneripdisp.setText(str(self.datacon.config.scan_ipaddrs))
            self.window.scannerportdisp.setText(str(self.datacon.config.scan_portnum))
            self.window.mesapidisp.setText(str(self.datacon.config.mes_api_curl))
            self.window.clientiddisp.setText(str(self.datacon.config.mes_clientid))
            self.window.conduitapidisp.setText(str(self.datacon.config.conduit_curl))
            self.window.packadisp.setText(str(self.datacon.config.pass_station))
            self.window.packbdisp.setText(str(self.datacon.config.pack_station))

            self.consoleDraw('INFO','Building up MES Communications')
            self.mesapi = mes_api.mes_api(self.datacon.config.mes_api_curl,self.datacon.config.mes_clientid)

            self.consoleDraw('INFO','Building up PLC Communications')
            
            
            self.machine = machineapi.machine([ self.datacon.config.plcc_ipaddrs,
                                                self.datacon.config.plcc_portnum,
                                                self.datacon.config.scan_ipaddrs,
                                                int(self.datacon.config.scan_portnum)],self.window)


           

            self.consoleDraw('INFO','Building up Scanner Communications')
            self.readScanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.readScanner.connect((self.datacon.config.scan_ipaddrs,int(self.datacon.config.scan_portnum)))

            

           


                 
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            self.consoleDraw('INFO','Configurations Failure!')
            self.window.error_lab.show()
            self.window.bootErrorLab.show()
            
        
    
    def writeSimulation(self,reg):
        try:
            test = self.machine.writeRegsiter(int(reg),1,1)
            self.consoleDraw('INFO',str(test))
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            
        
    def readSimulation(self,reg,disp):
        try:
            disp.setText(str(self.machine.readRegsiter(int(reg),1)[0]))
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
        


    def getConQty(self,obj):
        try:
            conList = self.datacon.countConsQty(obj)
            if not conList == []:
                for i in conList:
                    if  i[1] < int(self.upc_cont):
                        conQuantity = i[1]
                        obj.con_info  = i[0]
                        break
                    else:
                        conQuantity = 0
            else:
                conQuantity = 0
            return conQuantity
        
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
     
        
    def getLotQty(self,obj):
        try:
            lotList = self.datacon.countLotsQty(obj)
            if not lotList == []:
                for i in lotList:
                    if  i[1] < int(self.upl_cont):
                        lotQuantity  = i[1]
                        setattr(obj,'lot_info',i[0])
                        break
                    else:
                        lotQuantity = 0         
            else:
                lotQuantity = 0
            return lotQuantity
        
        except Exception as error:
            self.consoleDraw('ERRR',str(error))


    def tableUpdate(self,obj):
        try:
            #self.dptimer.stop()
            self.consoleDraw('INFO',f'Updating Table Info.....')
            if self.concap == "" or self.conqty == "" or self.skdcap == "" or self.skdqty =="" or self.lotcap=="" or self.lotqty=="":
                unitSkid = self.mesapi.unitInfo(obj.skid_info)
                unitCont = self.mesapi.unitInfo(obj.con_info)
                shopdata = self.mesapi.shoporderinfo(obj.shop_serial)
                self.target = shopdata['data']['total_quantity']
                self.actual = int(self.target) - int(shopdata['data']['available_count'])
                self.conqty = unitCont['data']['quantity']
                self.concap = unitCont['data']['container_quantity']
                self.skdqty = unitSkid['data']['quantity']
                self.skdcap = unitSkid['data']['container_quantity']

            self.wodProgressBar.setMaximum(int(self.target))
            self.wodProgressBar.setValue(int(self.actual))
            self.table_worder_actl.setText(str(self.actual))
            self.table_worder_targ.setText(str(self.target))
            
            self.table_cont_name.setText(str(obj.con_info))
            self.table_cont_targ.setText(str(self.concap))
            self.table_cont_actl.setText(str(self.conqty))
            self.conProgressBar.setValue(int(self.conqty))
            self.conProgressBar.setMaximum(int(self.concap))
            
            #unit
            self.table_unit_name.setText(str(obj.unit_serial))
            self.table_unit_targ.setText(str(obj.part_serial))
            self.table_unit_actl.setText(str(obj.employee_Id))
            self.datacon.updateUnit(obj)
            self.datacon.connection.commit()

            self.lotcap = str(int(self.skdcap) * int(self.concap))
            self.lotqty = str((int(self.skdqty) * int(self.concap))+int(self.concap))
            
            self.untProgressBar.setValue(int(self.lotqty))
            self.untProgressBar.setMaximum(int(self.lotcap)) 
            self.table_lot_targ.setText(str(self.lotcap))

            
            self.table_worder_name.setText(str(obj.shop_serial))
            self.table_lot_name.setText(str(obj.skid_info))
            self.table_lot_actl.setText(str(self.skdqty))
            self.table_lot_targ.setText(str(self.skdcap))
            self.lotProgressBar.setValue(int(self.skdqty))
            self.lotProgressBar.setMaximum(int(self.skdcap))
            self.datacon.connection.commit()
            self.consoleDraw('INFO',f'Updating table complete...')
            self.consoleDraw('SFDC',obj.ad2con)
            self.consoleDraw('INFO',f'Placing  <{obj.unit_serial}> on Conveyor_{obj.od_evn}')

            
            #workorderinformations
            #wqty = self.datacon.workorderUpdate(obj)
            #self.datacon.workorderUpdate(obj)
            #
            #self.wodProgressBar.setValue(int(wqty))              
            #lotinformations
            #lqty = self.datacon.lotUpdate(obj)
            #self.datacon.workorderUpdate(obj)
            #
            #continformations
            #cqty = self.datacon.conUpdate(obj)
            #self.datacon.workorderUpdate(obj)
                
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
            

    def moveNG(self,msg,obj):
        try:
            #self.tx.stop()
            self.window.indicator.setPixmap(QPixmap(u':src/alert.png'))
            self.consoleDraw('INFO',msg)
            self.consoleDraw('SFDC',msg)
            self.consoleDraw('INFO',"Moving NG")
            self.machine.writeRegsiter(int(self.datacon.config.writ_pasfail),1,3)
            self.datacon.connection.commit()
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
        
    def palletPrint(self,obj):
        try:
            self.lprint.hide()
            labeltype = self.lprint.labelSelector.currentText()
            obj.label_info = self.parts[1]['country'][labeltype]
            print(obj.label_info)
            self.conduit_pack.printSkid(obj)
            
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
        
        

    def printEvluation(self,obj):
        try:
            self.consoleDraw('INFO',f'Evaluating Container....')
            self.machine.writeRegsiter(int(self.datacon.config.writ_pasfail),1,int(obj.od_evn))
            self.concap = obj.concap
            self.conqty = obj.conqty
            self.window.indicator.setPixmap(QPixmap(u':src/ok.png'))
            if obj.conqty == obj.concap:
                self.window.indicator.setPixmap(QPixmap(u':src/ok.png'))
                open('temp','w').write("")
                self.file=""
                self.consoleDraw('INFO',f'Printing Container <{obj.con_info}>  Label....')
                self.conduit_print.printContainer(obj)
                self.conduit_print.moveout(obj.con_info)
                self.consoleDraw('INFO',f'Adding Container <{obj.con_info}> to Skid <{obj.skid_info}>')
                obj = self.conduit_pack.ad2skid(obj)
                unitSkid = self.mesapi.unitInfo(obj.skid_info)
                unitCont = self.mesapi.unitInfo(obj.con_info)
                self.conqty = unitCont['data']['quantity']
                self.concap = unitCont['data']['container_quantity']
                self.skdqty = unitSkid['data']['quantity']
                self.skdcap = unitSkid['data']['container_quantity']
                if obj.adskid == True:
                    self.window.indicator.setPixmap(QPixmap(u':src/ok.png'))
                    open('temp','w').write("")
                    self.file=""
                    self.consoleDraw('INFO',f'Adding Container <{obj.con_info}> to the Skid  <{obj.skid_info}> Success!...')
                    self.consoleDraw('INFO',obj.opnskd)
                    self.consoleDraw('INFO',obj.ad2skd)
                    self.consoleDraw('INFO',obj.clsskd)
                    #self.consoleDraw('SAVE',f' Container <{obj.con_info}> Full!')
                    self.consoleDraw('INFO',f'Evaluating Skid <{obj.skid_info}>....')
                    if obj.skdqty == obj.skdcap:
                        self.window.indicator.setPixmap(QPixmap(u':src/ok.png'))
                        open('temp','w').write("")
                        self.file=""
                        self.lprint.show()
                        self.consoleDraw('INFO',f'Skid <{obj.skid_info}> Full!')
                        self.consoleDraw('INFO',f'Printing Skid <{obj.skid_info}> Label....')
                        self.consoleDraw('INFO',f'Container <{obj.con_info}> Full!')
                        self.consoleDraw('INFO',f'Printing Container <{obj.con_info}>  Label....')
                        unitSkid = self.mesapi.unitInfo(obj.skid_info)
                        unitCont = self.mesapi.unitInfo(obj.con_info)
                        self.conqty = unitCont['data']['quantity']
                        self.concap = unitCont['data']['container_quantity']
                        self.skdqty = unitSkid['data']['quantity']
                        self.skdcap = unitSkid['data']['container_quantity']
                        self.conduit_print.moveout(obj.con_info)
                        self.tok = timeit.default_timer()
                        self.consoleDraw('INFO',f'Processed in {self.tok-self.tic}')
                        self.consoleDraw('INFO',f'Placing  <{obj.unit_serial}> on Conveyor_{obj.od_evn}')
                        try:
                            self.lprint.printButton.disconnect()
                            self.lprint.printButton.clicked.connect(lambda:self.palletPrint(obj))
                        except:
                            self.lprint.printButton.clicked.connect(lambda:self.palletPrint(obj))
                        self.lprint.show()
                        self.consoleDraw('SAVE',f' Skid <{obj.skid_info}> Full!')
                        self.machine.writeRegsiter(int(self.datacon.config.writ_mresets),1,1)
                        
                        
                        
                    else:
                        try:
                            self.file = eval(open('temp','r').read())
                        except:
                            self.file = ""
                        self.window.indicator.setPixmap(QPixmap(u':src/ok.png'))
                        self.tok = timeit.default_timer()
                        self.consoleDraw('INFO',f'Processed in {self.tok-self.tic}')
                        self.machine.writeRegsiter(int(self.datacon.config.writ_pasfail),1,int(obj.od_evn))
                        self.consoleDraw('SAVE',f' Container <{obj.con_info}> Full!')
                        self.machine.writeRegsiter(int(self.datacon.config.writ_mresets),1,1)
                        
                        
                else:
                    self.machine.writeRegsiter(int(self.datacon.config.writ_salarms),1,1)
                    self.window.indicator.setPixmap(QPixmap(u':src/alert.png'))
                    self.tok = timeit.default_timer()
                    self.consoleDraw('INFO',f'Processed in {self.tok-self.tic}')
                    self.machine.writeRegsiter(int(self.datacon.config.writ_pasfail),1,int(obj.od_evn))
                    try:
                        self.file = eval(open('temp','r').read())
                    except:
                        self.file = ""
            else:
                self.window.indicator.setPixmap(QPixmap(u':src/ok.png'))
                self.tok = timeit.default_timer()
                self.consoleDraw('INFO',f'Processed in {self.tok-self.tic}')
                open('temp','w').write(str([obj.con_info,obj.skid_info]))
                self.machine.writeRegsiter(int(self.datacon.config.writ_pasfail),1,int(obj.od_evn))#writ_mresets
                self.machine.writeRegsiter(int(self.datacon.config.writ_mresets),1,1)#
                try:
                    self.file = eval(open('temp','r').read())
                except:
                    self.file = ""
                

            #self.tx.stop()
            self.tableUpdate(obj)       
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
        
        
    def add_unit_to_Container(self,obj):
        
        try:
            self.consoleDraw('INFO',f'Adding Unit to the Container...')
            self.pop.hide()
            #self.selectedContainer = self.pop.skidList.currentText()
            #obj.con_info = self.pop.skidList.currentText()
            obj = self.conduit_pack.ad2Container(obj)
            self.consoleDraw('SFDC',str(obj.admeos))
            self.consoleDraw('SFDC',str(obj.opncon)) 
            self.consoleDraw('SFDC',str(obj.ad2con))
            self.consoleDraw('SFDC',str(obj.clscon))
            if obj.result == 'PASS':
                self.consoleDraw('INFO',f'Adding Success!')
                self.printEvluation(obj)
                 
            else:
                self.consoleDraw('INFO',f'Adding Failed!')
                self.moveNg("Failed",obj)


        except Exception as error:
            self.consoleDraw('ERRR',str(error))
            

    def units_for_the_container(self,obj):
        try:
            selectedContainer = str(self.pop.contList.currentText())
            setattr(obj,"con_info",selectedContainer)
            self.pop.resize(746, 300)
            [self.pop.cqty.setText(str(str(each['quantity']) + "/" + str(each['container_quantity']))) if each['serial_number']== obj.con_info  else None for each in obj.wait_lists]
            try:
                self.pop.proceed.disconnect()
            except:
                pass
            self.pop.proceed.clicked.connect(lambda:self.add_unit_to_Container(obj))
            self.pop.show()
            
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))


            
    def operatorSelection_Container(self,obj):
        try:
            self.pop.contList.clear()
            self.pop.contList.addItem("")
            self.pop.skidList.setCurrentText(str(obj.skid_info))
            self.pop.resize(746, 220)
            [self.pop.sqty.setText(str(str(each['quantity']) + "/" + str(each['container_quantity']))) if each['serial_number'] == obj.skid_info  else None for each in obj.wait_lists]
            [self.pop.contList.addItem(str(each)) if str(obj.skid_info) in str(each) else None for each in obj.cont_clists]
            try:
                self.pop.contList.disconnect()
                self.pop.contList.currentTextChanged.connect(lambda: self.units_for_the_container(obj))

            except:
                self.pop.contList.currentTextChanged.connect(lambda: self.units_for_the_container(obj))
            self.pop.show()
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
   

    def containers_for_the_skid(self,obj):
        try:
            obj.skid_info = str(self.pop.skidList.currentText())
            self.makeDecision_Cont(obj)
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
        
        
    def operatorSelection_Skid(self,obj):
        
        try:
             self.pop.skidList.clear()
             self.pop.skidList.addItem("")
             self.pop.shop_value.setText(str(obj.shop_serial))
             [self.pop.skidList.addItem(str(each)) for each in obj.skid_clists]
             try:
                self.pop.skidList.disconnect()
                self.pop.skidList.currentTextChanged.connect(lambda: self.containers_for_the_skid(obj))
             except:
                self.pop.skidList.currentTextChanged.connect(lambda: self.containers_for_the_skid(obj))
             
             self.pop.show()
             
             
        except Exception as error:
            self.consoleDraw('ERRR',str(error))


    def create_new_container(self,obj):
        try:
            self.consoleDraw('INFO',f'Creating New Container')
            cr8Container = int((self.mesapi.unitInfo(obj.skid_info))['data']['quantity'])+1
            obj.con_info = f"{obj.skid_info}-{cr8Container:02d}"
            obj = self.conduit_pack.add_container(obj)
            
            if obj.con_stat == True:
                self.consoleDraw('INFO',f' Container Creation Success!')
                self.consoleDraw('SFDC',f' {obj.con_msg} ')
                self.consoleDraw('INFO',f' {obj.con_info}')
                self.add_unit_to_Container(obj)
                
                
                
            else:
                self.consoleDraw('INFO',f' Container Creation Failed!')
                self.consoleDraw('SFDC',f' {obj.con_msg}')
                self.moveNg('Move NG',obj)
                
                
            
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
        
    def makeDecision_Cont(self,obj):
        try:
            obj.cont_clists = [each if str(obj.skid_info) in each else None for each in obj.cont_clists]
            if None in obj.cont_clists: obj.cont_clists.remove(None)
            
            self.consoleDraw('INFO',f'Evaluating Containers Availability...')
            
            if len(obj.cont_clists)==0:
                self.consoleDraw('INFO',f'No Incomplete Container is Available!')
                self.consoleDraw('INFO',f'Creating New Container')
                self.create_new_container(obj)
                

                
            elif len(obj.cont_clists)==1:
                 self.consoleDraw('INFO',f'Only one Incomplete Container is Available!')
                 obj.con_info = [each for each in obj.cont_clists][0]
                 self.consoleDraw('INFO',f'Auto selecting the Container <{obj.con_info}>')
                 self.add_unit_to_Container(obj)
                 
                 
                 
    

            elif len(obj.cont_clists) > 1:
                self.consoleDraw('INFO',f'More Incomplete Container Available!')
                self.consoleDraw('INFO',f'Letting operator to select the Container')
                self.operatorSelection_Container(obj)

        except Exception as error:
            self.consoleDraw('ERRR',str(error))


    
    def create_new_skid(self,obj):
        try:
            self.consoleDraw('INFO',f'Creating New Skid')
            obj = self.conduit_pack.add_skid(obj)
            
            if obj.skid_stat == True:
                self.consoleDraw('INFO',f' Skid Creation Success!')
                self.consoleDraw('SFDC',f'{obj.skid_msg}')
                self.consoleDraw('INFO',f'{obj.skid_info}')
                self.makeDecision_Cont(obj)
                
            else:
                self.consoleDraw('INFO',f' Skid Creation Failed!')
                self.consoleDraw('SFDC',f' {obj.skid_msg}')
                self.moveNg('Move NG',obj)
                
                
            
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
        

        
    def makeDecision_Skid(self,obj):
        #return True
        try:
            self.consoleDraw('INFO',f'Evaluating skids Availability...')
            if len(obj.skid_clists) == 0:
                self.consoleDraw('INFO',f'No Incomplete Skid is Available!')
                self.create_new_skid(obj)

                
            elif len(obj.skid_clists) == 1:
                 self.consoleDraw('INFO',f'Only one Incomplete Skid is Available!')
                 [obj.skid_info for obj.skid_info in obj.skid_clists]
                 [self.pop.skidList.addItem(str(obj.skid_info)) for obj.skid_info in obj.skid_clists]
                 obj.cont_clists = {each if obj.skid_info in each else None for each in obj.cont_clists}
                 self.consoleDraw('INFO',f'Auto selecting the skid <{obj.skid_info}>')
                 self.pop.skidList.setEnabled(False)
                 self.makeDecision_Cont(obj)
                 

            elif len(obj.skid_clists) > 1:
                print(obj.skid_clists)
                self.consoleDraw('INFO',f'More Incomplete Skids Available!')
                self.consoleDraw('INFO',f'Letting operator to select the Skids')
                self.operatorSelection_Skid(obj)
                
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
            

    def searchProduction(self,obj):
        try:
            self.consoleDraw('INFO','Downloading Skid and Container informations')
            obj = self.mesapi.containerList(obj)
            obj = self.mesapi.waitingList(obj)
            
            if obj.wait_status == True and obj.acont_status==True:
                self.consoleDraw('INFO','Downloading Skid and Container Success!')
                self.consoleDraw('INFO',f'Soritng Containers of the PO <{obj.shop_serial}>...')
                obj.so_contlist  = { i for key, i in enumerate(obj.so_contlist)}
                self.consoleDraw('INFO','Sorting Complete')
                
                self.consoleDraw('INFO','Checking for incomplete Skids & Containers...')
                obj.mSkid_lists  = { i[1]['serial_number'] if int(i[1]['unit_type']) == obj.skid_clevel and int(i[1]['quantity'])!= int(i[1]['container_quantity']) else None  for i in enumerate(obj.wait_lists)}
                obj.mCont_lists  = { i[1]['serial_number'] if int(i[1]['unit_type']) == obj.cont_clevel and int(i[1]['quantity'])!= int(i[1]['container_quantity']) else None  for i in enumerate(obj.wait_lists)}
                self.consoleDraw('INFO','Check Complete')
                print(obj.mSkid_lists)
                print(obj.mCont_lists)
                
                
                self.consoleDraw('INFO',f'Sorting Skids ')
                obj.skid_clists  = obj.so_contlist.intersection(obj.mSkid_lists)
                
                self.consoleDraw('INFO',f'Sorting Contianers')
                obj.cont_clists  = obj.so_contlist.intersection(obj.mCont_lists)

                obj.skid_clists  = set(list(obj.skid_clists))
                obj.cont_clists  = set(list(obj.cont_clists))
                
                print(obj.cont_clists)
                print(obj.skid_clists)
                
                self.makeDecision_Skid(obj)
                
                
            else:
                self.consoleDraw('INFO','Downloading Skid and Container informations Failed!')
                self.moveNG(obj.wait_status,obj)
            


            
        except Exception as error:
            self.consoleDraw('ERRR','Downloading Skid and Container informations Failed')
            self.consoleDraw('ERRR',str(error))
            
        

    def localEvaluate(self,obj):
        try:
            self.consoleDraw('INFO','Remembering Container...')
            self.file = eval(open('temp','r').read())
            obj.con_info = self.file[0]
            obj.skid_info = self.file[1]
            self.consoleDraw('INFO','Container & Skid Found!')
            self.add_unit_to_Container(obj)
        except Exception as error:
            self.consoleDraw('ERRR',str(error))

    
    def passunit(self,obj):
        try:
            self.consoleDraw('INFO','Stage Passing....')
            obj = self.conduit_pass.conduit_end(obj)
            if obj.exec_stcode =="OK":
                self.consoleDraw('INFO','Stage Passing success!')
                if self.file == "":
                    self.searchProduction(obj)
                else:
                    self.localEvaluate(obj)
                
            else:
                self.consoleDraw('INFO','Stage Passing Failed! ')
                self.moveNG(obj.exec_status,obj)
                
        except Exception as error:
            self.consoleDraw('ERRR',str(error))

        
    def assign_nextPO(self,obj):
        try:
            self.consoleDraw('INFO','Assigning to Next Shop Order')
            obj = self.conduit_pass.conduit_asnso(obj)
            if obj.exec_stcode =="OK":
                if not "No eligible shop orders found for unit" in obj.exec_status:
                    self.consoleDraw('SFDC',str(obj.exec_status))
                    self.consoleDraw('SFDC',str(obj.shop_stat_1))
                    self.consoleDraw('SFDC',str(obj.shop_stat_2))
                    self.consoleDraw('SFDC',str(obj.shop_stat_3))
                    self.consoleDraw('INFO','Assigment Success!')
                    self.passunit(obj)
                else:
                    self.moveNG(str(obj.exec_status),obj)
            else:
                
                self.moveNG(obj.exec_status,obj)
            #yield True

        except Exception as error:
            self.consoleDraw('ERRR',str(error)) 
        
    
    
    
    def unit2Object(self,**kargs):
        try:
            
            self.consoleDraw('INFO','Creating Unit Object....')
            self.window.sfdcResp.setText(str(kargs['unitInfo']))
            class meter():
                
                unit_serial = kargs['unitInfo']
                time_unixts = self.timeapi.unixnow()
                shift_Alpha = self.timeapi.sshift()
                employee_Id = self.credentials[0]
                pack_locale = self.datacon.config.pack_locales
                cont_clevel = int(self.datacon.config.cont_clevels)
                skid_clevel = int(self.datacon.config.skid_clevels)

            self.consoleDraw('INFO','Object Creation Success!')
            self.assign_nextPO(meter)
            #self.th = threading.Thread(target=self.assign_nextPO(meter),name="procs").start()
            #self.tx = QtCore.QTimer()
            #self.tx.timeout.connect(lambda: self.assign_nextPO(meter))
            #self.tx.start(10)
            
            
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
            
        
    def bconstruct(self,barcode):
        try:
            
            barcode = (barcode[18:]).strip()
            bcd = barcode
            self.consoleDraw('INFO','Reframing Barcode....')
            barcode = [str(barcode[3:])+str(d) if str(barcode[:3]) in str(e) else None for d in self.parts[0] for e in self.parts[0][d]]
            barcode = [each for each in barcode if each][0]
            self.consoleDraw('INFO','Reframing Barcode Success!')
            self.consoleDraw('INFO',f'Barcode <{bcd}> is reframed to <{barcode}>')
            return barcode
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
    def scanRead(self):
        return str(self.readScanner.recv(4096).decode())
    def containerGraph(self):
        try:
            
            self.scanCheck = self.machine.readRegsiter(int(self.datacon.config.read_scan_ok),1)[0]
            self.sfdcpass = self.machine.readRegsiter(int(self.datacon.config.writ_pasfail),1)[0]
            self.readwait = self.machine.readRegsiter(int(self.datacon.config.read_mstatus),1)[0]
            self.machine.writeRegsiter(int(self.datacon.config.writ_pasfail),0,0)
            if self.scanCheck == 1 :
                self.machine.writeRegsiter(int(self.datacon.config.writ_salarms),1,0)
                #self.machine.writeRegsiter(int(self.datacon.config.read_scan_ok),1,0)
                self.tic = timeit.default_timer()
                self.window.indicator.setMovie(self.process)
                self.process.start()
                self.sfdcpass = self.machine.writeRegsiter(int(self.datacon.config.read_scan_ok),0,0)
                self.consoleDraw('INFO','Scan Success! Processing Unit')
                barcode = self.scanRead()
                #barcode = str(self.machine.scanRead())
                print(barcode)
                barcode = self.bconstruct(barcode)
                self.consoleDraw('INFO','Processing '+ str(barcode))
                self.unit2Object(unitInfo=barcode)
               
                    
            elif self.readwait == 2 and self.oldRead!=2:
                self.consoleDraw('INFO','Waiting for Downline Transfer')
                self.oldRead = self.readwait
            elif self.readwait == 0 and self.oldRead!=0:
                self.oldRead = self.readwait
                self.consoleDraw('INFO','Waiting for inline transfer!')
                self.oldscanCheck = self.scanCheck
            elif self.readwait == 1 and self.oldRead!=1:
                self.window.indicator.setMovie(self.process)
                self.process.start()
                self.oldRead = self.readwait
                self.consoleDraw('INFO','Processing Unit...')
                self.oldscanCheck = self.scanCheck
                
                self.window.indicator.setMovie(self.process)
                self.process.start()
            
        except Exception as error:
            self.consoleDraw('ERRR',str(error))
            
        
    def readTest(self):
        
        self.window.scannerData.setText(str(self.scanRead()))


    def simulate(self):
        self.machine.writeRegsiter(100,0,1)
        
    def connections(self):
        try:
            self.window.prodloginButton.clicked.connect(self.login)
            self.window.sfdcConEdit.clicked.connect(self.sfdcParamUpdate)
            self.window.plccConEdit.clicked.connect(self.plccParamUpdate)
            self.window.scanConEdit.clicked.connect(self.scanParamUpdate)
            self.window.packingConEdit.clicked.connect(self.packParamUpdate)
            self.window.regsConEdit.clicked.connect(self.regsParamUpdate)
            self.window.genReadReg.clicked.connect(self.read_anyReg)
            self.window.genWritReg.clicked.connect(self.writ_anyReg)
            
            
            self.window.eng_logout.clicked.connect(lambda: self.engLockerUnlock(False))
            self.window.testpassfail.clicked.connect(lambda: self.writeSimulation(self.datacon.config.writ_pasfail))
            self.window.testalarm.clicked.connect(lambda: self.writeSimulation(self.datacon.config.writ_salarms))
            self.window.testreset.clicked.connect(lambda: self.writeSimulation(self.datacon.config.writ_mresets))


            self.window.readscanok.clicked.connect(lambda: self.readSimulation(self.datacon.config.read_scan_ok,self.window.scanoksts))
            self.window.readalarm.clicked.connect(lambda: self.readSimulation(self.datacon.config.read_malarms,self.window.alarmsts))
            self.window.readmsts.clicked.connect(lambda: self.readSimulation(self.datacon.config.read_mstatus,self.window.msts))
            self.window.readrtime.clicked.connect(lambda: self.readSimulation(self.datacon.config.read_runtime,self.window.rtime))
            self.window.readdtime.clicked.connect(lambda: self.readSimulation(self.datacon.config.read_dwntime,self.window.dtime))
                

            self.window.tetBut.clicked.connect(self.simulate)
            self.window.readScanner.clicked.connect(self.readTest)
            self.window.searchButon.clicked.connect(self.search)
            self.consoleDraw('INFO','Click Connections Success!')
            

        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            self.consoleDraw('INFO','Click Connections Failure!')

            
    def stop(self):
        self.looptimer_b.stop()
        self.window.prodloginButton.disconnect()
        self.window.prodloginButton.setText('Login')
        self.window.prodloginButton.clicked.connect(self.login)
        self.consoleDraw('INFO','Application Stopped!')
        self.window.opPane.setTabEnabled(2, False)
        self.window.login_resp.setText(str('Logout Success! Application Stopped '))

    def autoCycle(self):
        try:
            self.oldRead =99
            self.consoleDraw('INFO','Starting Production!')
            self.looptimer_b = QtCore.QTimer()
            self.looptimer_b.timeout.connect(self.containerGraph)
            self.looptimer_b.start(10)
            self.consoleDraw('INFO','Booting Success!')
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            self.consoleDraw('INFO','Booting Failed!')
        
    def login(self):
        try:
            
            self.credentials = [self.window.username_in.text(),
                                self.window.password_in.text()]
            self.window.username_in.clear()
            self.window.password_in.clear()
            if not self.credentials[0] =='':
                dataValid = True    
                    
            else:
                dataValid = False

            if dataValid == True:
                if self.window.opp_mode.isChecked():
                    self.consoleDraw('INFO','Data Validation Passed!')
                    self.consoleDraw('INFO','Logging IN!')
                    
                    self.conduit_pass = conduitapi.conduit(username  = self.credentials[0],
                                                          password   = self.credentials[1],
                                                          station_id = self.datacon.config.pass_station,
                                                          endpoint   = self.datacon.config.conduit_curl,
                                                          client     = self.datacon.config.mes_clientid)
                    
                    self.conduit_pack = conduitapi.conduit(username  = self.credentials[0],
                                                      password       = self.credentials[1],
                                                      station_id     = self.datacon.config.pack_station,
                                                      endpoint       = self.datacon.config.conduit_curl,
                                                      client         = self.datacon.config.mes_clientid)

                    self.conduit_print =  self.conduit_pack   
                    
                    
                    

                    
                    loginToken_pack = self.conduit_pass.conduit_login(serial='abcd')
                    loginToken_pass = self.conduit_pack.conduit_login(serial='abcd')

                    

                    
                    if not "cannot log in with the provided operator" in str(loginToken_pack['status']['message']) and not "cannot log in with the provided operator" in str(loginToken_pass['status']['message']) :
                        self.window.prodloginButton.disconnect()
                        self.window.prodloginButton.setText('Stop / Logout')
                        self.window.prodloginButton.clicked.connect(self.stop)                    
                        self.consoleDraw('INFO','Login Success!')
                        self.window.login_resp.setText('Login Success!')
                        self.window.opPane.setCurrentIndex(2)
                        self.window.opPane.setTabEnabled(2, True)
                        self.machine.writeRegsiter(int(self.datacon.config.writ_salarms),1,1)
                        self.autoCycle()
                    else:
                        self.consoleDraw('ERRR','Login Failed!')
                elif self.window.eng_mode.isChecked():
                    self.engineer_unlock()
                    self.window.eng_mode.setChecked(False)
                    

            if dataValid == False:
                self.window.login_resp.setText('Login Failed - Please Fill up the blanks')
                self.consoleDraw('INFO','Data Validation Failed!')
                    
            
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            self.consoleDraw('INFO','Login Failure!')
        
    def app_clock(self):
        try:
            self.window.machResp.setText("  " +str(self.info))
            #self.machine.writeRegsiter(int(self.datacon.config.writ_pingpon),0,0)
            self.window.date.setText(str(self.timeapi.sdate()))
            self.window.time.setText(str(self.timeapi.stime()))
            self.window.shift.setText(str(self.timeapi.sshift()))
            self.h_Productivity()
            #self.machine.writeRegsiter(int(self.datacon.config.writ_pingpon),0,1)
           
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            self.consoleDraw('INFO','Clock Failure!')

    def pingpong(self):
        try:
            self.machine.writeRegsiter(int(self.datacon.config.writ_pingpon),0,0)
            
            self.machine.writeRegsiter(int(self.datacon.config.writ_pingpon),0,1)
        except:
            pass


    def app_life(self):
        try:
            self.consoleDraw('INFO','Booting up...')
            self.looptimer = QtCore.QTimer()
            self.looptimer.timeout.connect(self.app_clock)
            self.looptimer.start(50)
            self.pingpong_timer = QtCore.QTimer()
            self.pingpong_timer.timeout.connect(self.pingpong)
            self.pingpong_timer.start(50)
            self.consoleDraw('INFO','Booting Success!')
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            self.consoleDraw('INFO','Booting Failed!')
  
        
    def engineer_unlock(self):
        try:
            self.consoleDraw('INFO','Activating Engineer Mode..')
            eusn = self.credentials[0]
            epwd = self.credentials[1]
            if eusn=='admin' and epwd == '012345':
                self.engLockerUnlock(True)
                self.consoleDraw('INFO','Engineer Mode Activated!')
                self.window.opPane.setTabEnabled(3, True)
                self.window.opPane.setCurrentIndex(3)
                
                
            else:
                ctypes.windll.user32.MessageBoxW(0, 'Invalid Credentials' , "Login Failed", 0)
                self.consoleDraw('INFO','Engineer Login Failed!')
        except Exception as e:
            self.consoleDraw('ERRR',str(e))
            self.consoleDraw('INFO','Engineer Login Failed!')
            
        
    def __init__(self):
        self.file = ""
        self.concap = ""
        self.conqty = ""
        self.skdcap = ""
        self.skdqty =""
        self.lotcap =""
        self.lotqty=""
        self.parts=eval(open("templates\part.json",'r').read())
        self.consoleDraw('INFO','Intializing...',erDisp = False)
        self.app = QtWidgets.QApplication(sys.argv)
        self.splash = QtWidgets.QSplashScreen(QPixmap(u':src/loading.png'))
        self.splash.show()
        self.window = Ui()
        self.pop = pop()
        self.lprint = pop_print()
        [self.lprint.labelSelector.addItem(str(each)) for each in self.parts[1]['country']]
        self.window.indicator.setPixmap(QPixmap(u':src/0Y4T-sm6_auto_x2.jpg'))
        self.window.error_lab.hide()
        self.window.bootErrorLab.hide()
        self.ocount = 0
        self.count = 0 
        self.k = 0
        self.timeapi = livetimeapi.main()
        #self.configure_app()
        self.connections()
        self.app_life()
        self.consoleDraw('INFO','Application Ready!')
        QTimer.singleShot(5000, self.splash.close)
        self.process = QMovie(u':src/ss.gif')        
        self.window.opPane.setStyleSheet("QTabBar::tab:selected { color: white; background-color:green }")
        self.window.opp_mode.setChecked(True)
        #self.window.username_in.setText('1002440')
        #self.window.password_in.setText('0129')
        self.engLockerUnlock(False)
        for i in range(2,4):
            self.window.opPane.setTabEnabled(i, False)
        self.window.opPane.setCurrentIndex(0)
        self.window.show()
        
        sys.exit(self.app.exec_())
        
        
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/RPS.ui', self)
        
class pop(QtWidgets.QMainWindow):
    def __init__(self):
        super(pop, self).__init__()
        uic.loadUi('ui/Rpopui.ui', self)
        
class pop_print(QtWidgets.QMainWindow):
    def __init__(self):
        super(pop_print, self).__init__()
        uic.loadUi('ui/lprint.ui', self)
        
if __name__ == "__main__":
   appObj = main()


      
    
    

