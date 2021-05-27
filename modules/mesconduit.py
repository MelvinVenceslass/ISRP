import json,os,sys,requests,logging

from collections import namedtuple
from json import JSONEncoder
import supports


__version__ = "1.1.2"
__author__ = "Melvin Paul Miki"
__credits__ = "Mickie Studioz"

logging.basicConfig(filename='conduit.log', filemode='a', format='%(asctime)s |  %(levelname)s |  %(message)s', level=logging.INFO)

class conduit():
    def __init__(mes,endpoint,username,password,device_id,client_id):
        try:
            logging.info("Initializing Instance...")
            mes.json_template = supports.template
            mes.endpoint = endpoint
            mes.json_template['source']['client_id']=client_id
            mes.json_template['source']['workstation']['station']=device_id
            mes.json_template['source']['employee']= username
            mes.json_template['source']['password']= password
            logging.info("Instance Ready!")
            
        except Exception as e:
            logging.error("Instance Creation error!")
            logging.error(e)
            
################### Login Verification ##############################################
    
    def mes_login(mes):
        try:
            mes.json_template['transactions'] = []
            mes.json_template['transactions'].append({"unit": {"unit_id":"ABCD1234" ,"part_number": "","revision": ""},"commands": [{"command":{"name": "End"}}]})
            posting = requests.post(mes.endpoint, json=mes.json_template)
            if posting.status_code == 200:
                reply = posting.json()
                if "cannot log in" in reply["transaction_responses"][0]["scanned_unit"]["status"]["message"]:
                    logging.info("Login Failed!")
                    return False
                else:
                    logging.info("Login Success!")
                    return True
            else:
                return False
                logging.error("Conduit Communication Error")

        except Exception as e:
            logging.error(e)
            return False


################### Data Parser ##############################################

    def parser(mes,obj):
        try:
            mesreply = []
            for i in range(len(obj["transaction_responses"])):
                a = obj["transaction_responses"][i]["scanned_unit"]["status"]["code"]
                b = obj["transaction_responses"][i]["scanned_unit"]["status"]["message"]
                logging.info(f"{a} |  {b}")
                mesreply.append(f"{a} :: {b}")

            if len(mesreply)>1:
                return mesreply
            else:
                return mesreply[0]

        except Exception as e:
            return False
            logging.error(e)

################### Sending to MES ##############################################

    def speak(mes,obj):
        try:
            posting = requests.post(mes.endpoint, json=obj)
            if posting.status_code == 200:
                reply = posting.json()
                return mes.parser(reply)

            else:
                return False
                logging.error("Conduit Communication Error")
        except Exception as e:
            return False
            logging.error(e)

################### Passing Single Unit #########################################

    def mes_PassUnit(mes,unitSerial):
        try:
            mes.json_template['transactions'] = []
            mes.json_template['transactions'].append({"unit": {"unit_id":unitSerial ,"part_number": "","revision": ""},"commands": [{"command":{"name": "End"}}]})
            return mes.speak(mes.json_template)

        except Exception as e:
            logging.error(e)

################### Admeo ##############################################

    def mes_ApplyMeo(mes,unitSerial,admeocode):
        try:
            transaction =  mes.json_template['transactions'] = []

            unit = {"unit":{"unit_id":unitSerial},"commands":[]}
            transaction.append(unit)

            admeo = {"command":{"name": "ApplyMeo","meo_number":admeocode}}
            transaction[0]['commands'].append(admeo)
            
            return mes.speak(mes.json_template)

        except Exception as e:
            logging.error(e)

################### Adding Non Tracked Component #######################

    def mes_AddNonTrackedComponent(mes,unitSerial,component,value):
        try:
            transaction =  mes.json_template['transactions'] = []

            unit = {"unit":{"unit_id":unitSerial},"commands":[]}
            transaction.append(unit)

            admeo = {"command":{"name": "AddNontrackedComponent","ref_designator":component,"component_id":value}}
            transaction[0]['commands'].append(admeo)

            return mes.speak(mes.json_template)

        except Exception as e:
            logging.error(e)

################### Multi Passing unit ##############################################

    def mes_MultiPass(mes,unitSerial):
        try:
            mes.json_template['transactions'] = []
            for i in range(len(unitSerial)):
                mes.json_template['transactions'].append({"unit": {"unit_id":unitSerial[i] ,"part_number": "","revision": ""},
                "commands": [{"command":{"name": "End"}}]})
            
            return mes.speak(mes.json_template)
            
        except Exception as e:
            return e
            logging.error(e)


def help():
    print(supports.x)

def start_app():
    url = input("Enter the conduit URL\n")
    username = input("Enter the operator Username\n")
    password = input("Enter the operator Password\n")
    station_id = input("Enter the Station Id\n")
    client_id  = input("Enter the Client Id \n")
    session = conduit(url,username,password,station_id,client_id)
    login = session.mes_login()
    if login == True:
        while 1:
            serial = input("Serial Number? \n")
            print(session.mes_PassUnit(serial))
    else:
        print("Login Error Restart the Applications")


session = conduit("http://sanmmed-conduit.42-q.com:18003/conduit","1002440","R129","565","mp5678dc1a")
print(session.mes_login())
print(session.mes_PassUnit("1"))
print(session.mes_MultiPass(["1","2"]))
print(session.mes_ApplyMeo("1","2"))
print(session.mes_AddNonTrackedComponent("1","a","b"))