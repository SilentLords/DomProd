import requests as r
b = '''{"id":"1","jsonrpc":"2.0","method":"item.GetItemPhoneV1","params":{"meta":{"platform":"web","language":"ru"},"id":2683745406,"itemType":"Listing"}}'''
a = r.post(url='https://api.domofond.ru/rpc', data=b.encode('utf-8'))
print(a.text)
