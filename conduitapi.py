import json,os
from collections import namedtuple
from json import JSONEncoder
import requests




class conduit():

    def customObjectConvert(self,dictionary):
        return namedtuple('x', dictionary.keys())(*dictionary.values())


    def __init__(self,**attribs):
        try:
            self.json_template = json.loads(open('templates/template.json','r').read())
            self.endpoint = attribs['endpoint']
            self.json_template['source']['client_id']=attribs['client']
            self.json_template['source']['workstation']['station']=attribs['station_id']
            self.json_template['source']['employee']= attribs['username']
            self.json_template['source']['password']= attribs['password']
        except Exception as e:
            print(e)

    def conduit_asnso(self,obj):
        
        self.json_template['transactions'] = []
        self.json_template['transactions'].append({"unit": {"unit_id":obj.unit_serial,"part_number": "","revision": ""},"commands": [{"command":{"name": "AssignToNextShopOrder"}}]})
        posting = requests.post(self.endpoint, json=self.json_template)
        
        if posting.status_code == 200:
            reply = posting.json()
            obj.exec_stcode = reply['status']['code']
            obj.exec_status = reply['status']['message']
            if obj.exec_stcode == "OK":
                try:
                    obj.unit_serial = reply['transaction_responses'][0]['scanned_unit']['unit']['unit_id']
                    obj.part_serial = reply['transaction_responses'][0]['scanned_unit']['unit']['part_number']
                    obj.shop_serial = reply['transaction_responses'][0]['scanned_unit']['unit_info']['shop_order_number']
                    obj.shop_stat_1 = reply['transaction_responses'][0]['command_responses'][0]['results'][0]['message']
                    obj.shop_stat_2 = reply['transaction_responses'][0]['command_responses'][0]['results'][1]['message']
                    obj.shop_stat_3 = reply['transaction_responses'][0]['command_responses'][0]['results'][2]['message']
                except:
                    
                    obj.exec_status = reply['transaction_responses'][0]['command_responses'][0]['results'][0]['message']
                    obj.exec_stcode = "ERROR"
                    
            
            return obj
        
        else:
            raise Exception('Conduit Communication Error')
       
        
        
        

    def conduit_login(self,**args):
            self.json_template['transactions'] = []
            self.json_template['transactions'].append({"unit": {"unit_id":args['serial'] ,"part_number": "","revision": ""},"commands": [{"command":{"name": "End"}}]})
            posting = requests.post(self.endpoint, json=self.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                return reply
            else:
                raise Exception('Conduit Communication Error')



            
    def conduit_end(self,obj):
            self.json_template['transactions'] = []
            self.json_template['transactions'].append({"unit": {"unit_id":obj.unit_serial ,"part_number": "","revision": ""},"commands": [{"command":{"name": "End"}}]})
            posting = requests.post(self.endpoint, json=self.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                obj.exec_stcode = reply['status']['code']
                obj.exec_status = reply['status']['message']
                return obj
                
            else:
                raise Exception('Conduit Communication Error')

            
    def conduit_Move(self,**args):
        self.json_template['transactions'] = []
        self.json_template['transactions'].append({"unit": {"unit_id":args['serial'] ,"part_number": "","revision": ""},"commands": [{"command":{"name": "Move","workstation":"SOAN"}}]})
        posting = requests.post(self.endpoint, json=self.json_template)
        if posting.status_code == 200:
            reply = posting.json()
            return reply
        else:
            raise Exception('Conduit Communication Error')

    def conduit_part(self,sn,part):
        #ROCHEBACKENDPN
        self.json_template['transactions'] = []
        self.json_template['transactions'].append({"unit":{"unit_id":sn,"part_number": "","revision": ""},
                                                   "commands": [{"command": {"name": "ChangePartNumber","new_part_number":part}},{"command":{"name":"End"}}]})
        posting = requests.post(self.endpoint, json=self.json_template)
        if posting.status_code == 200:
            reply = posting.json()
            return reply
        else:
            raise Exception('Conduit Communication Error')

    
    def addAttribute(self,target,keys):
        transaction = self.json_template['transactions'] = []
        transaction.append({"unit":{"unit_id":target,"part_number":"", "revision":""},"commands": [{"command": {"name": "AddAttribute","attr_name":"po_info","attr_data":keys}}]})
        posting = requests.post(self.endpoint, json=self.json_template)
        
                
            
        
        
    def add_skid(self,obj):
            transaction = self.json_template['transactions'] = []
            unit = {"unit":{"unit_id":obj.unit_serial,"part_number": "","revision": ""},"commands":[]}
            conadd = {"command":{"name":"CreateContainer","c_level":obj.skid_clevel,"container_part_number":obj.part_serial,"container_serial_number":""}}
            transaction.append(unit)
            transaction[0]['commands'].append(conadd)
            posting = requests.post(self.endpoint, json=self.json_template)
            
            if posting.status_code == 200:
                reply = posting.json()
                #print(json.dumps(reply))
                if reply['status']['code']=='OK':
                    skid_stat = reply['transaction_responses'][0]['command_responses'][0]['status']['code']
                    if skid_stat =="OK":
                        obj.skid_info = str(reply['transaction_responses'][0]['command_responses'][0]['results'][0]['data']['serial_number'])
                        obj.skid_msg  = reply['transaction_responses'][0]['command_responses'][0]['status']['message']
                        self.addAttribute(obj.skid_info, obj.shop_serial)
                        obj.skid_stat = True

                        
                    else:
                        obj.skid_stat = False
                        open(str(obj.unit_serial),'w').write(str(self.json_template) + "\n\n" + str(reply))
                        raise Exception('Container Creation Error')
                        
                    return obj
                    
                else:
                    open(str(obj.unit_serial),'w').write(str(self.json_template) + "\n\n" + str(reply))
                    raise Exception('Container Creation Error')
            else:
                raise Exception('Conduit Communication Error')



    def add_container(self,obj): #unit_id | partnum |con_id
            transaction = self.json_template['transactions'] = []
            unit = {"unit":{"unit_id":obj.unit_serial,"part_number": "","revision": ""},"commands":[]}
            conadd = {"command":{"name":"CreateContainer","c_level":f"{obj.cont_clevel}","container_part_number":obj.part_serial,"container_serial_number":f"{obj.con_info}"}}
            transaction.append(unit)
            transaction[0]['commands'].append(conadd)
            posting = requests.post(self.endpoint, json=self.json_template)

            
            if posting.status_code == 200:
                reply = posting.json()
                print(reply)
                if reply['status']['code']=='OK':
                   
                    con_stat = reply['transaction_responses'][0]['command_responses'][0]['status']['code']
                    if con_stat =="OK":
                        obj.con_info = str(reply['transaction_responses'][0]['command_responses'][0]['results'][0]['data']['serial_number'])
                        obj.con_msg  = reply['transaction_responses'][0]['command_responses'][0]['status']['message']
                        self.addAttribute(obj.con_info, obj.shop_serial)
                        obj.con_stat = True
                    else:
                        obj.con_stat = False
                        open(str(obj.unit_serial),'w').write(str(self.json_template) + "\n\n" + str(reply))
                        raise Exception('Container Creation Error')
                        
                    return obj
                    
                else:
                    open(str(obj.unit_serial),'w').write(str(self.json_template) + "\n\n" + str(reply))
                    raise Exception('Container Creation Error')
            else:
                raise Exception('Conduit Communication Error')


            
        
    def ad2Container(self,obj): #lot_id | con_id | unit_id |
            transaction = self.json_template['transactions'] = []


            unit = {"unit":{"unit_id":obj.unit_serial},"commands":[]}
            transaction.append(unit)
            
            opencon = {"command":{"name":"AddNontrackedComponent", "component_id":obj.skid_info, "ref_designator":"skid"}}
            transaction[0]['commands'].append(opencon)
            
            #openingContianer
            unit = {"commands":[]}
            transaction.append(unit)
            
            opencon = {"command":{"name":"OpenContainer","container_serial_number":f"{obj.con_info}"}}
            transaction[1]['commands'].append(opencon)

    
            #Adding2Contianer
            unit = {"unit":{"unit_id":obj.con_info},"commands":[]}
            transaction.append(unit)
            
            conaddunits = {"command":{"name":"AddUnitToContainer","unit_serial_number":obj.unit_serial}}
            transaction[2]['commands'].append(conaddunits)

            #ClosingContianer
            unit = {"commands":[]}
            transaction.append(unit)
            
            closecon = {"command":{"name":"CloseContainer","container_serial_number":obj.con_info }}
            transaction[3]['commands'].append(closecon)
            
            posting = requests.post(self.endpoint, json=self.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                #print(json.dumps(reply))
                #['status']]
                admeos = reply['transaction_responses'][1]['status']['code']    
                opncon = reply['transaction_responses'][1]['status']['code']
                ad2con = reply['transaction_responses'][2]['status']['code']
                conqty = reply['transaction_responses'][2]['scanned_unit']['unit_info']['quantity']
                concap = reply['transaction_responses'][2]['scanned_unit']['unit_info']['container_quantity']
                clscon = reply['transaction_responses'][3]['status']['code']

                obj.admeos = reply['transaction_responses'][0]['command_responses'][0]['status']['message']
                obj.opncon = reply['transaction_responses'][1]['command_responses'][0]['status']['message']
                obj.ad2con = reply['transaction_responses'][2]['command_responses'][0]['status']['message']
                obj.clscon = reply['transaction_responses'][3]['command_responses'][0]['status']['message']
                  
            
                if admeos=="OK" and opncon =='OK' and ad2con =='OK' and clscon =='OK':
                    obj.result = 'PASS'
                    con = int(obj.con_info[-1:])
                    obj.conqty = conqty
                    obj.concap = concap
                    if (con % 2) == 0:
                        obj.od_evn = 2
                    else:
                        obj.od_evn = 1
                        
                else:
                    obj.result = 'FAIL'
                    obj.od_evn = 3
            
            else:
                obj.result = 'FAIL'
                raise Exception('Conduit Communication Error')

            return obj


    def ad2skid(self,obj): #lot_id | con_id | unit_id |
            transaction = self.json_template['transactions'] = []

            #openingContianer
            unit = {"unit":{"unit_id":obj.con_info},"commands":[]}
            transaction.append(unit)
            
            opencon = {"command":{"name":"OpenContainer","container_serial_number":obj.skid_info}}
            transaction[0]['commands'].append(opencon)

    
            #Adding2Contianer
            unit = {"unit":{"unit_id":obj.skid_info},"commands":[]}
            transaction.append(unit)
            
            conaddunits = {"command":{"name":"AddUnitToContainer","unit_serial_number":obj.con_info}}
            transaction[1]['commands'].append(conaddunits)

            #ClosingContianer
            unit = {"unit":{"unit_id":obj.skid_info},"commands":[]}
            transaction.append(unit)
            
            closecon = {"command":{"name":"CloseContainer","container_serial_number":obj.skid_info }}
            transaction[2]['commands'].append(closecon)
            
            #print(json.dumps(self.json_template))
            posting = requests.post(self.endpoint, json=self.json_template)
            
            if posting.status_code == 200:
                reply = posting.json()#['status']
                #print(json.dumps(reply))
                opnskd = reply['transaction_responses'][0]['status']['code']
                ad2skd = reply['transaction_responses'][1]['status']['code']
                skdqty = reply['transaction_responses'][1]['scanned_unit']['unit_info']['quantity']
                skdcap = reply['transaction_responses'][1]['scanned_unit']['unit_info']['container_quantity']
                clsskd = reply['transaction_responses'][2]['status']['code']

                obj.opnskd = reply['transaction_responses'][0]['command_responses'][0]['status']['message']
                obj.ad2skd = reply['transaction_responses'][1]['command_responses'][0]['status']['message']
                obj.clsskd = reply['transaction_responses'][2]['command_responses'][0]['status']['message']
                
                if opnskd =='OK' and ad2skd =='OK' and clsskd =='OK':
                    obj.adskid = True
                    obj.skdqty = skdqty
                    obj.skdcap = skdcap

                else:
                    obj.adskid = False
                    obj.od_evn = 3
            
            else:
                raise Exception('Conduit Communication Error')

            return obj  

    def close_con(self,obj):
        transaction = self.json_template['transactions'] = []
        command = {"Commands":[{"Command":{"name":"OpenContainer","Container_serial_number":obj.con_info}}],"Unit":{"unit_id":obj.con_info}}
        transaction.append(command)
        posting = requests.post(self.endpoint, json=self.json_template)

    def printContainer(self,obj):
        transaction = self.json_template['transactions'] = []
        labelPrint  = eval(open('templates/print.json','r').read())
        labelPrint[0]['unit']['unit_id'] = obj.con_info
        labelPrint[1]['unit']['unit_id'] = obj.con_info
        transaction.append(labelPrint[0])
        transaction.append(labelPrint[1])
        print(self.json_template)
        posting = requests.post(self.endpoint, json=self.json_template)
        if posting.status_code == 200:
            reply = posting.json()
            if reply['status']['code']=='OK':
                obj.clabel = 'PASS'
            else:
                obj.clabel = 'FAIL'
        else:
            obj.clabel == 'FAIL'
        return obj

        
    def printSkid(self,obj):
        transaction = self.json_template['transactions']=[]
        labelPrint  = json.loads(open('templates/print.json','r').read())
        labelPrint[0]['unit']['unit_id'] = obj.con_info
        labelPrint[1]['unit']['unit_id'] = obj.con_info
        labelPrint[0]['commands'][0]['command']['label_name'] = obj.label_info
        transaction.append(labelPrint[0])
        transaction.append(labelPrint[1])
        print(self.json_template)
        posting = requests.post(self.endpoint, json=self.json_template)
        #print(posting)
        if posting.status_code == 200:
            reply = posting.json()
            print(reply)
            if reply['status']['code']=='OK':
                obj.slabel = 'PASS'
            else:
                obj.slabel = 'FAIL'
        else:
            obj.clabel == 'FAIL'
        return obj
            
    def moveout(self,data):
        transaction = self.json_template['transactions'] = []
        command = {"Commands":[{"Command":{"name":"OpenContainer","Container_serial_number":data}}],"Unit":{"unit_id":data}}
        transaction.append(command)
        posting = requests.post(self.endpoint, json=self.json_template)
        transaction = self.json_template['transactions'] = []
        command = {"Commands":[{"Command":{"name":"CloseContainer","Container_serial_number":data}}],"Unit":{"unit_id":data}}
        transaction.append(command)
        posting = requests.post(self.endpoint, json=self.json_template)
        
        
        
        





