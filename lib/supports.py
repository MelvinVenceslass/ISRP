import json
x = """


42Q- MES - Conduit Integration Setup!

Author  - Melvin Paul Miki
Version - 1.1.2

#Importing the Module:

    > import mesconduit

#Creating a session:

    > session = mesconduit.conduit("http://sanmmed-conduit.42-q.com:18003/conduit","1002440","R129","565","mp5678dc1a")
    
        Attributes Descriptions

                #  endpoint   => "http://sanmmed-conduit.42-q.com:18003/conduit"
                #  Username   => "1002440"
                #  password   => "R129"
                #  station_id => "565"
                #  client_id  => "mp5678dc1a"
            


Login Valdation:
    > session.mes_login()
        
        ==> True  - Authorised User
        ==> False - Unathorised User    


Stage Pasing the unit

    > session.mes_PassUnit("123456")

        ==> STATUS :: Respective Message from the MES

        Attributes Descriptions

                #  Unit Serial Number   => "123456"
        
Mutli Units Pasing 

    > session.mes_MultiPass(["1234","5678",.,.,.,.,n])

        ==> [STATUS :: Respective Message from the MES,STATUS :: Respective Message from the MES,.,.,.,.,.,n]

        Attributes Descriptions

                #  Unit Serial Numbers   => ["123456","5678"]


Applying MEO the Serial Number

    > session.mes_ApplyMeo("123456","Screw 1 - Passed")

        ==> STATUS :: Respective Message from the MES

        Attributes Descriptions

                #  Unit Serial Number   => "123456"
                #  Added MEO Message    => "Screw = 1" 



Adding non tracked component 


    > session.mes_AddNonTrackedComponent("123456","Strip","345363"):

        ==> STATUS :: Respective Message from the MES

        Attributes Descriptions

                #  Unit Serial Number   => "123456"
                #  Component Key        => "Strip" 
                #  Component Value      => "345363" 
Data Collector
    Execute in Command Prompt
        >python -c "import  mesconduit; mesconduit.start_app()"
    
    Ex:
        $Enter the conduit URL
            >www.conduit.com
        $Enter the operator Username
            >1234567
        $Enter the operator Password
            >1234567
        $Enter the Station Id
            >123
        $Enter the Client Id
            >abcb123
        $Serial Number?
            >12334BC123
        $STATUS :: Respective Message from the MES


"""

template = {
    "version": "1.0",
    "source": {
        "client_id": "mp5678dc1a",
        "employee": "1002440",
        "password": "R129",
        "workstation": {
            "type": "Device",
            "station": "418"
        }
    },
    "refresh_unit": "True",
    "token": "",
    "keep_alive": "False",
    "single_transaction": "False",
    "options": {
        "skip_data": [
            "defects",
            "comments",
            "components",
            "attributes"
        ]
    },
    "transactions": [
        {
            "unit": {
                "unit_id": "DUMMY-12345SC103000077",
                "part_number": "",
                "revision": ""
            },
            "commands": [
                {
                    "command": {
                        "name": "End"
                    }
                }
            ]
        }
    ]
}