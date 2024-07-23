

import requests

def webhook_article(payload):
    header = {'Content-Type':'application/json'}
    url = "https://sandbox.contextdata.ai/api/webpush/c5-000001dao964/key=b1aaf26c13f8cd877783cd7cd3b17f2ccc51a4a458d4580c4c13cc8b37215bb5"
    response = requests.post(url,json=payload,headers=header)
    
    print(response.reason)

