from flask import Flask
from flask import jsonify
from flask_cors import CORS
from netmiko import ConnectHandler

device={"username":"admin",
        "password":"admin",
        "port":10001,
        "device_type":"cisco_ios"}

#filename = "running.txt"

#with open(filename,'r') as fh:
#    config = fh.read()

def get_parse_config(device):
    interfaces = []
    try:
        conn = ConnectHandler(**device)
        config = conn.send_command("show running-config")
        interfaces = []
        output = config.split("!")
        for conf in output:
            description =''
            ip_address = ''
            mask = ''
            status = 'up'
            if conf.startswith("\ninterface") == True:
                int_name = conf.split("\n")[1].split()[1]
                for line in conf.split("\n"):
                    if line.startswith(" ip address") == True:
                        ip_address = line.split()[2]
                        mask = line.split()[3]
                    if line.startswith(" description") == True:
                        description = line.split("description")[1].strip().strip("'")
                    if line.startswith(" shutdown") == True:
                        status = 'down'

                interfaces.append({"int_name":int_name,"ip_address":ip_address,"mask":mask,"description":description,"status":status})
        return interfaces
    except:
        return interfaces 




app = Flask(__name__)
CORS(app)

@app.route('/connect/<device_ip>/' , methods=['GET'])
def connect_device(device_ip):
    device['ip'] = device_ip
    print ('device connected :' + device_ip)
    return device

@app.route('/interfaces' , methods=['GET'])
def get_interfaces():
    interfaces = get_parse_config(device)
    return jsonify(interfaces)


@app.route('/interfaces/<name>/' , methods=['GET'])
def get_single_interface(name):
    interfaces = get_parse_config(device)
    name = name.replace("-" ,"/")
    intf = ''
    for interface in interfaces:
        if interface['int_name'] == name:
            intf = interface
            break
    if len(intf) == 0:
        intf = {"error":f'interface {name} not found'}
        return intf
    else:
        return jsonify(intf)




if __name__ == '__main__':
    app.run(debug=True)

