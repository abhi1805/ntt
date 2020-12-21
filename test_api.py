import requests
import sys

try:
    arg = sys.argv[1]
    r = requests.get(f'http://localhost:5000/interfaces/{arg}/')
    print(r.text)

except:
    r = requests.get(f'http://localhost:5000/interfaces')
    print(r.text)