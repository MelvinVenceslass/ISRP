import sqlite3,time

class transport():
    
    def writeParams(self,**params):
        try:
            for key,value in params.items():
                self.cursor.execute("UPDATE configuration SET {}='{}' WHERE 1".format(key,value))
                self.connection.commit()
                self.config = self.cursor.execute('select * from configuration').fetchall()
        except Exception as e:
            print(e)
            
    def readParams(self,*params):
        for value in params:
            rows = self.cursor.execute("SELECT {} FROM configuration WHERE 1".format(value)).fetchall()
            yield rows
    
    def customQueryW(self,query):
        rows = self.cursor.execute(query)
        self.connection.commit()
        return rows
    
    def customQueryR(self,query):
        rows = self.cursor.execute(query).fetchall()
        return rows

    def countLotsQty(self,obj):
         query = """SELECT lot_names, count(lot_names) from unitfootprint WHERE unit_wkod='{}' and unit_part='{}' and lot_names IS NOT NULL  GROUP BY lot_names """.format(obj.shop_serial,obj.part_serial)
         return self.customQueryR(query)

    def countConsQty(self,obj):
         query = """SELECT con_names, count(con_names) from unitfootprint WHERE unit_wkod='{}' and unit_part='{}' and lot_names='{}' and  con_names IS NOT NULL GROUP BY con_names """.format(obj.shop_serial,
                                                                                                                                                                obj.part_serial,
                                                                                                                                                                obj.skid_info)
         return self.customQueryR(query)
        
    def updateUnit(self,obj):
         query = """INSERT INTO unitfootprint (lot_names,con_names,unit_name,unit_part,unit_wkod,times_now,shift_now,empy_name)
                        VALUES('{}','{}','{}','{}','{}','{}','{}','{}') """.format(obj.skid_info,
                                                                        obj.con_info,
                                                                        obj.unit_serial,
                                                                        obj.part_serial,
                                                                        obj.shop_serial,
                                                                        obj.time_unixts,
                                                                        obj.shift_Alpha,
                                                                        obj.employee_Id)
         return self.customQueryW(query)
        
        
    def saveUnit(self,obj):
        query = """INSERT INTO unitfootprint (times_now,shift_now,empy_name,unit_name,unit_part,unit_wkod,sfdc_resp)
                   VALUES('{}','{}','{}','{}','{}','{}','{}') """.format(obj.time_unixts,obj.shift_Alpha , obj.employee_Id,
                                                                         obj.unit_serial, obj.part_serial, obj.shop_serial, obj.sfdc_rs)
        saveUnit = self.customQueryW(query)
        
    def updatefootPrints(self,**params):
        try:
            for key,value in params.items():
                self.cursor.execute("UPDATE unitFootPrint SET {}='{}' WHERE 1".format(key,value))
                self.connection.commit()
                self.config = self.cursor.execute('select * from configuration').fetchall()
        except Exception as e:
            print(e)  
    
    def __init__(self):
        self.connection = sqlite3.connect("roche.msl")
        self.cursor = self.connection.cursor()
        tables = self.cursor.execute("""SELECT name FROM sqlite_master  WHERE type ='table';""").fetchall()
        if not('configuration',) in tables:
            self.cursor.execute("""CREATE TABLE configuration (sfdc_ip TEXT,   sfdc_stn TEXT,  pack_stn TEXT,  mes_api TEXT,   clientid TEXT,
                                                               pack_loc TEXT,  plcc_ip TEXT,   plcc_port TEXT, scan_ip TEXT,   scan_port TEXT,
                                                               cont_clvl TEXT, skid_clvl TEXT, targ_hour TEXT, targ_cylt TEXT, read_scanok TEXT,
                                                               read_alarm TEXT,read_mstatus TEXT, writ_passfail TEXT, writ_alarm TEXT, writ_reset TEXT,
                                                               writ_ping TEXT, read_rtime TEXT, read_dtime TEXT )""")
            self.connection.commit()
            self.cursor.execute("""INSERT INTO configuration VALUES('http://corpconduit3.sanmina.com:18003/conduit','114', '331',
                                                               'https://production.42-q.com/mes-api/','p5599dc1','9K11',
                                                               '172.25.213.51', '502', '148.164.104.99', '9006',
                                                               '100', '110','360', '60','100', '101', '102','103','104','105','106','108','109')""")
            self.connection.commit()

        if not('unitFootPrint',) in tables:
            
            self.cursor.execute("""CREATE VIRTUAL TABLE unitFootPrint using fts5(  times_now , shift_now , empy_name ,
                                                                    unit_name , unit_part , unit_wkod ,
                                                                    wkod_targ , sfdc_resp , con_names ,
                                                                    lot_names , add_resps )""")
            self.connection.commit()
            
        if not('systemfoots',) in tables:
            self.cursor.execute("""CREATE VIRTUAL TABLE systemfoots using fts5( date , time , desc , function , message )""")
            
           
            self.connection.commit()

            
        self.params = (self.cursor.execute('select * from configuration').fetchall())[0]
        
        class config():
            conduit_curl, pass_station, pack_station, mes_api_curl, mes_clientid  = self.params[0:5]
            pack_locales, plcc_ipaddrs, plcc_portnum, scan_ipaddrs, scan_portnum  = self.params[5:10]
            cont_clevels, skid_clevels, target_phour, target_ctime, read_scan_ok  = self.params[10:15]
            read_malarms, read_mstatus, writ_pasfail, writ_salarms, writ_mresets  = self.params[15:20]
            writ_pingpon, read_runtime, read_dwntime                               = self.params[20:23]

        self.config = config()
             
            
            
            
            
        

        
        
        
    def unitExistance(self,obj):
        query =""" SELECT CASE WHEN EXISTS (SELECT *FROM unitFootPrint WHERE unit_name = "{}" )THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END""".format(obj)
        return self.customQueryR(query)[0][0]
    


    def workorderUpdate(self,obj):
        query =""" SELECT count(unit_wkod) from unitFootPrint where unit_wkod ='{}' and unit_wkod IS NOT NULL GROUP BY unit_wkod """.format(obj.shop_serial)
        return self.customQueryR(query)[0][0]
    
    def lotUpdate(self,obj):
        query =""" SELECT count(lot_names) from unitFootPrint where lot_names ='{}' and unit_wkod='{}' and  lot_names IS NOT NULL GROUP BY lot_names """.format(obj.skid_info,obj.shop_serial)
        return self.customQueryR(query)[0][0]
       
    def conUpdate(self,obj):
        query =""" SELECT count(con_names) from unitFootPrint where con_names ='{}' and unit_wkod='{}' and lot_names = '{}' and  con_names IS NOT NULL GROUP BY con_names """.format(obj.con_info,obj.shop_serial,obj.skid_info,)
        return self.customQueryR(query)[0][0]
    
    def unitHistory(self,sn):
        query =""" SELECT  DATETIME(times_now, 'unixepoch', 'localtime')  , shift_now , empy_name ,
                    unit_name , unit_part , unit_wkod , wkod_targ , sfdc_resp , con_names , lot_names , add_resps
                    from unitFootPrint where unit_name ='{}'  """.format(sn)
        
        query =""" SELECT  DATETIME(times_now, 'unixepoch', 'localtime')  , shift_now , empy_name ,
                    unit_name , unit_part , unit_wkod , wkod_targ , sfdc_resp , con_names , lot_names , add_resps
                    from unitFootPrint where  unitFootPrint MATCH '"{}"'  """.format(sn)



        return self.customQueryR(query)

    def logwriter(self,time,shift,desc,line,info):
        self.cursor.execute(""" INSERT INTO systemfoots VALUES ('{}','{}','{}','{}','{}')""".format(time,shift,desc,line,info))

    def getqty(self,stime,etime):
        query =""" SELECT COUNT(*)from unitFootPrint WHERE times_now BETWEEN '{}' and '{}' """.format(stime,etime)
        return self.customQueryR(query)[0][0]
        
