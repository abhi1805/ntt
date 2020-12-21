from flask import Flask
from flask import jsonify
from flask_cors import CORS
from netmiko import ConnectHandler

#device login details
device={"host":"127.0.0.1",
        "username":"admin",
        "password":"admin",
        "port":10001,
        "device_type":"cisco_ios"}



#Parsing config to later feed to endpoints
def get_parse_config(device):
    interfaces = []
    try:
        conn = ConnectHandler(**device)                              #using netmiko function to connect device over ssh
        config = conn.send_command("show running-config")            #Sending running-config command to the device
        interfaces = []
        output = config.split("!")                                   #Spliting the config output using ! to get chunks of data as list elements
        for conf in output:
            description =''                                          #Stating default values for no configs
            ip_address = ''
            mask = ''
            status = 'up'
            if conf.startswith("\ninterface") == True:
                int_name = conf.split("\n")[1].split()[1]            #Fetch interface name
                for line in conf.split("\n"):
                    if line.startswith(" ip address") == True:
                        ip_address = line.split()[2]                 #Fetch only ip address
                        mask = line.split()[3]                       #Fetch only mask
                    if line.startswith(" description") == True:
                        description = line.split("description")[1].strip().strip('"')           #Fetch description
                    if line.startswith(" shutdown") == True:         #Fetch status of the interface 
                        status = 'down'

                interfaces.append({"int_name":int_name,"ip_address":ip_address,"mask":mask,"description":description,"status":status})   #Making a block of interface data
        return interfaces
    except:
        return interfaces




app = Flask(__name__)                                                #Basic flask website using html as frontend code begin
CORS(app)

@app.route('/interfaces' , methods=['GET'])                          #Creating GET Rest call endpoint api for All Interfaces data
def get_interfaces():                                                #function to pass all interfaces data to the GET call in json format
    interfaces = get_parse_config(device)
    return jsonify(interfaces)




@app.route('/interfaces/<name>/' , methods=['GET'])                  #Creating GET Rest call endpoint api for a single interface datablock
def get_single_interface(name):                                      #function to pass requested interface data to the GET call in json format
    interfaces = get_parse_config(device)
    name = name.replace("-" ,"/")                                    #This is done as I couldn't find a way to pass / from frontend
    intf = ''                                                        #initiating a blank value for interface name
    for interface in interfaces:                                     
        if interface['int_name'] == name:                            #Check if User entered interface matches with the device interfaces
            intf = interface
            break
    if len(intf) == 0:
        intf = {"error":f'interface {name} not found'}               #If user entered interface is not found throw error in json
        return intf
    else:
        return jsonify(intf)




if __name__ == '__main__':
    app.run(debug=True)

