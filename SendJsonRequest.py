import requests
import json
import urllib

#Define Endpoint
endpoint = "http://127.0.0.1:8000/" #Send to Local

#Source Code
#필요에 따라서 json data 형태로 만들어주면 됨

#Data
info_data = {"number":1,
            "product":"information",
            "sample":"sample_information"
            }

#Send Post Request
req = requests.post(url=endpoint, data=info_data)

#Extract Response
response = req
print(response.content)