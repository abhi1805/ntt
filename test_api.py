import requests                     #importing python module for sending requests
import sys                          #importing python module to manipulate python's runtime environment

try:
    arg = sys.argv[1]               #passing an argument input to python
    r = requests.get(f'http://localhost:5000/interfaces/{arg}/')    #make a get request for the entered interface name
    print(r.text)

except:
    r = requests.get(f'http://localhost:5000/interfaces')           #make a get request for all interfaces
    print(r.text)
