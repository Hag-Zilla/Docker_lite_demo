#############################################################################################################################
#                                                  test_authentification                                                    #
#############################################################################################################################

# ================================================          Header           ================================================

"""
Title : test_authentification.py
Init craft date : 27/10/2022
Handcraft with love and sweat by : Damien Mascheix @Hagzilla
Notes :
    Authentification test script for train_Docker_lite_demo
"""
# ================================================    Modules import     =====================================================

import os
import requests
import json
from datetime import datetime
today = datetime.now()

# ================================================          Functions / Class          ================================================

# définition de l'adresse de l'API
api_address = '172.17.0.2'
# port de l'API
api_port = 8000
# node definition
api_node = "/permissions"

test_name = "Authentication test"

def auth_request (api_address,api_port,api_node,test_name,username,password,exp_status_code,output,date):
    """_summary_
    
    auth_request : Function that manage the authorization request. It will give a full log if the "LOG" environment variable is set to 1.

    Args:
        api_address (string): The API adress to request
        api_port (integer): The API port to request
        api_node (string): The endpoint to request
        test_name (string): The test name
        username (string): username to test
        password (string): password to test
        exp_status_code (integer): expected status code
        output (string): formated string with the following parameters : {date} {node} {user} {pwd} {exp_status_code} {status_code} {test_status}
        date (string): date of the day
    """
    try:
        r = requests.get(url='http://{address}:{port}{node}'.format(address=api_address, port=api_port, node = api_node),
                    params= {'username': username,
                            'password': password}
                    )
        
        # statut de la requête
        status_code = r.status_code

        if status_code == exp_status_code:
            test_status = 'SUCCESS'
        else: 
            test_status = 'FAILURE'
    
         
    except:
        test_status = 'FAILURE'
        status_code == 503

    # Formating output
    output = output.format(test_name = test_name,
                           date = date,
                           node = api_node,
                           user = username,
                           pwd= password,
                           exp_status_code=exp_status_code,
                           status_code=status_code,
                           test_status=test_status
                            )
            
    # ===================== Ticket print or interactive mode prints
    if os.environ.get('LOG') == None:
        print("WARNING : LOG environment variable is not configured. Please confugure it (0 or 1)")
    elif os.environ.get('LOG') == '0':
        print(output)
    elif os.environ.get('LOG') == '1':
        with open('./logs/api_test.log', 'a') as file:
            file.write(output)
    else:
        print("WARNING : LOG environment variable is not well configured. Please confugure it (0 or 1)")

# ================================================          Warfield          ================================================

# ===================== Configuration

# définition de l'adresse de l'API
api_address = '172.17.0.2'
# port de l'API
api_port = 8000
# node definition
api_node = "/permissions"

test_name = "Authentication test"

# Message formating
output = '''
============================
    {test_name}
============================

Date :
{date}

request done at {node}
| username={user}
| password={pwd}

expected result = {exp_status_code}
actual restult = {status_code}

==>  {test_status}

'''

# Opening JSON file with credentials to test
with open('test_credentials.json') as json_file:
    test_credentials = json.load(json_file)
  
# ===================== Requests

# Loop to go through all the test credentials        
for name in test_credentials:
    auth_request (api_address = api_address,
                  api_port = api_port,
                  api_node = api_node,
                  test_name = test_name,
                  username = name,
                  password = test_credentials[name]["pwd"],
                  exp_status_code = test_credentials[name]["expected_code"],
                  output = output,
                  date = today
                  )
     
# ===========================================================================================================================
# =                                                Debug WORLD !!!!!                                                        =
# ===========================================================================================================================

if __name__ == '__main__':
    # print(output)
    # print(test_credentials)
    pass